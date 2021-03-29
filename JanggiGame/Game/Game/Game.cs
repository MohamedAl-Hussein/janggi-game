using Godot;
using System.Collections.Generic;
using System.Linq;

using Common;
using SocketClient;
using SocketClient.Messages;

public class Game : Node2D
{
    private const string BOARD_SCENE = "res://Game/Board/Board.tscn";

    private Board _board;
    private Client _client;
    private PieceColor _turn;
    private Tile _source;
    private Tile _destination;

    [Signal] public delegate void SetupCompleted();
    [Signal] public delegate void GameExited();
    [Signal] public delegate void MoveCompleted(List<int> source, List<int> destination);

    public override void _Ready()
    {
        _client = new Client();
        NewGame();
    }

    private void NewGame()
    {
        SetupBoard();
        _client.NewRequest(MessageAction.NEW_GAME);
        _board.SetupPieces(_client.PieceDTOs);
    }

    private void SetupBoard()
    {
        var board = GD.Load<PackedScene>(BOARD_SCENE);
        Board boardNode = (Board)board.Instance();

        AddChild(boardNode);
        Connect("MoveCompleted", this, "OnMoveCompleted");
        Connect("SetupCompleted", this, "OnSetupCompleted");
        Connect("GameExited", this, "OnGameExited");

        _board = boardNode;
    }

    public void OnTileSelected(Tile tile)
    {
        // No piece at source and tile selected contains piece.
        if (_source is null)
        {
            // Highlight selected tile and its valid destinations
            if (tile.Occupant != null && tile.Occupant.Color == _turn)
            {
                _source = tile;
                HighlightSourceDestinations(tile);
            }
        }

        // Piece at source so tile selected is destination.
        else
        {
            _destination = tile;
            MovePiece(_source, _destination);
            UnHighlightTiles();

            // Clear source and destination.
            _source = null;
            _destination = null;
        }
    }

    public void OnMoveCompleted(Coordinate source, Coordinate destination)
    {
        _client.NewRequest(MessageAction.MOVE_COMPLETED, source, destination);
        _client.NewRequest(MessageAction.GET_GAME_STATUS);
        _turn = _client.PlayerTurn;
    }

    public void OnSetupCompleted() { }

    public void OnGameExited() { }

    private void HighlightSourceDestinations(Tile tile)
    {
        // Get valid destinations for selected tile
        Coordinate pos = _board.ConvertYCoord(tile.Occupant.Coordinates);
        _client.NewRequest(MessageAction.GET_PIECE_DESTINATIONS, pos);
        tile.Occupant.Destinations = _client.PieceDestinations
            .Select(dest => _board.ConvertYCoord(dest))
            .ToList();

        // Highlight the tiles
        tile.HighlightTile();
        foreach (Coordinate destination in tile.Occupant.Destinations)
        {
            if (!_board.TileMap.ContainsKey(destination))
                return;

            Tile destTile = _board.TileMap[destination];

            destTile.HighlightTile();
        }
    }

    private void UnHighlightTiles()
    {
        // Clear all tile destination highlights.
        _source.UnHighlightTile();

        foreach (Tile t in _board.TileMap.Values)
        {
            t.UnHighlightTile();

            // Highlight general if they are in check
            if (_client.IsChecked && t.Occupant != null)
            {
                Piece p = t.Occupant;

                if (p.Color == _turn && p.Category == PieceCategory.GENERAL)
                {
                    t.HighlightTile(true);
                }
            }
        }
    }

    private void MovePiece(Tile source, Tile destination)
    {
        // Can't move to-from same position.
        if (source.Occupant == destination.Occupant)
            return;

        // Check if destination can be reached by piece.
        bool isDestinationReachable = source.Occupant.Destinations
            .Where(dest => dest.x_coord == destination.Coordinates.x_coord && dest.y_coord == destination.Coordinates.y_coord)
            .Any();

        // Can't move to unreachable destination.
        if (!isDestinationReachable)
            return;

        // Remove target piece.
        Piece target = destination.Occupant;
        if (!(target is null))
            target.QueueFree();

        // Update destination and source tiles.
        destination.Occupant = source.Occupant;
        source.Occupant = null;

        // Move piece to new position.
        Vector2 newDestination = _board.NewDestination(destination.Position);
        destination.Occupant.Position = newDestination;

        // Update piece location.
        destination.Occupant.Coordinates = _board.FromPosition(destination.Occupant.Position);

        // Send request to server to complete move.
        Coordinate src = _board.ConvertYCoord(_board.FromTilePosition(source.Position));
        Coordinate dst = _board.ConvertYCoord(_board.FromTilePosition(destination.Position));

        OnMoveCompleted(src, dst);
    }
}
