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

        Connect("MoveCompleted", this, "OnMoveCompleted");
        Connect("SetupCompleted", this, "OnSetupCompleted");
        Connect("GameExited", this, "OnGameExited");

        // Connect to game interface buttons.
        Node passBtn = GetNode<TextureButton>("BottomActionBar/QuickActions/PassTurnButton");
        passBtn.Connect("PassTurnButtonPressed", this, "OnPassTurnButtonPressed");

        Node rotateViewBtn = GetNode<TextureButton>("BottomActionBar/QuickActions/RotateViewButton");
        rotateViewBtn.Connect("RotateViewButtonPressed", this, "OnRotateViewButtonPressed");

        Node forfeitBtn = GetNode<TextureButton>("BottomActionBar/QuickActions/ForfeitButton");
        forfeitBtn.Connect("ForfeitButtonPressed", this, "OnForfeitButtonPressed");
    }

    /// <summary>
    /// Method <c>OnPassTurnButtonPressed</c> is called after the pass turn button is pressed.
    /// Makes a request to server to pass the turn for the current player. Only valid if the player's
    /// general is not in check.
    /// </summary>
    public void OnPassTurnButtonPressed()
    {
        // Can't pass turn if General in check.
        if (_client.IsChecked)
            return;

        // Grab a piece that belongs to player and make a move request to/from same position.
        Piece src = new Piece();
        bool found = false;
        List<Tile> tiles = _board.TileMap.Values.ToList();

        foreach (Tile tile in tiles)
        {
            if (tile.Occupant != null)
            {
                Piece piece = tile.Occupant;
                if (piece.Color == _client.PlayerTurn)
                {
                    src = piece;
                    found = true;
                    break;
                }
            }
        }

        if (found)
            OnMoveCompleted(src.Coordinates, src.Coordinates);
    }

    public void OnRotateViewButtonPressed()
        => GD.Print("Rotate View Button Pressed!");

    public void OnForfeitButtonPressed()
        => GD.Print("Forfeit Button Pressed!");

    /// <summary>
    /// Method <c>NewGame</c> configures the game board and sets the pieces at their starting positions.
    /// </summary>
    private void NewGame()
    {
        SetupBoard();
        _client.NewRequest(MessageAction.NEW_GAME);
        _board.SetupPieces(_client.PieceDTOs);
    }

    /// <summary>
    /// Method <c>SetupBoard</c> adds a new game board to the Game instance.
    /// </summary>
    private void SetupBoard()
    {
        var board = GD.Load<PackedScene>(BOARD_SCENE);
        Board boardNode = (Board)board.Instance();

        AddChild(boardNode);
        _board = boardNode;
    }

    /// <summary>
    /// Method <c>OnTileSelected</c> is called when a given tile is selected by the player. 
    /// Stores the selected tile and performs a move action if the source and destinations are valid.
    /// </summary>
    /// <param name="tile">The selected tile.</param>
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

    /// <summary>
    /// Method <c>OnMoveCompleted</c> is called after a valid destination is selected for a given piece.
    /// Calls the game engine so that it can update its position map.
    /// </summary>
    /// <param name="source">The source coordinate.</param>
    /// <param name="destination">The destination coordinate.</param>
    public void OnMoveCompleted(Coordinate source, Coordinate destination)
    {
        _client.NewRequest(MessageAction.MOVE_COMPLETED, source, destination);

        string msg;
        if (source.x_coord != destination.x_coord || source.y_coord != destination.y_coord)
            msg = $"{_client.PlayerTurn}: ({source.x_coord}, {source.y_coord}) --> ({destination.x_coord}, {destination.y_coord})\n";
        else
            msg = $"{_client.PlayerTurn}: Passed turn\n";

        _client.NewRequest(MessageAction.GET_GAME_STATUS);

        if (_client.IsChecked)
        {
            msg += "CHECK!\n";
        }

        if (_client.GameState != GameState.UNFINISHED)
        {
            msg += $"{_client.GameState}!";
        }

        Label msgDisplay = GetNode<Label>("TopActionBar/QuickActions/CenterDisplay/ScrollingLog/Messages");
        ScrollContainer container = GetNode<ScrollContainer>("TopActionBar/QuickActions/CenterDisplay/ScrollingLog");
        ScrollBar scrollBar = container.GetVScrollbar();

        container.ScrollVertical = (int)(scrollBar.MaxValue + 1);
        msgDisplay.Text += msg;

        _turn = _client.PlayerTurn;
    }

    /// <summary>
    /// Method <c>OnSetupCompleted</c> is called after the player's finalize their starting positions.
    /// </summary>
    public void OnSetupCompleted() { }

    /// <summary>
    /// Method <c>OnGameExited</c> is called if the current game session is exited by the player.
    /// </summary>
    public void OnGameExited() { }

    /// <summary>
    /// Method <c>HighlightSourceDestinations</c> highlights the tiles that a given piece can travel to.
    /// </summary>
    /// <param name="tile">The source tile.</param>
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

    /// <summary>
    /// Method <c>UnHighlightTiles</c> resets the tile highlight for all pieces, but keeps any red highlights
    /// for generals in check.
    /// </summary>
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

    /// <summary>
    /// Method <c>MovePiece</c> moves a piece from the source coordinate to the destination coordinate.
    /// </summary>
    /// <param name="source">The source coordinate.</param>
    /// <param name="destination">The destination coordinate.</param>
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
