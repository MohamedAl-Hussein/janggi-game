using Godot;
using janggi.Game.Piece;
using System;
using System.Collections.Generic;
using System.Linq;

public class Board : Node2D
{
    private readonly int _tileOffset = 18;
    private readonly int _pieceOffset = 32;
    private readonly int _scale = 100;
    public Tile Source;
    public Tile Destination;
    private readonly PieceData[] _pieceData = new PieceData[]
    {
        new PieceData(0, "red", "chariot", (x : 0, y : 0)),
        new PieceData(1, "red", "elephant", (x : 1, y : 0)),
        new PieceData(2, "red", "horse", (x : 2, y : 0)),
        new PieceData(3, "red", "guard", (x : 3, y : 0)),
        new PieceData(4, "red", "guard", (x : 5, y : 0)),
        new PieceData(5, "red", "elephant", (x : 6, y : 0)),
        new PieceData(6, "red", "horse", (x : 7, y : 0)),
        new PieceData(7, "red", "chariot", (x : 8, y : 0)),
        new PieceData(8, "red", "general", (x : 4, y : 1)),
        new PieceData(9, "red", "cannon", (x : 1, y : 2)),
        new PieceData(10, "red", "cannon", (x : 7, y : 2)),
        new PieceData(11, "red", "soldier", (x : 0, y : 3)),
        new PieceData(12, "red", "soldier", (x : 2, y : 3)),
        new PieceData(13, "red", "soldier", (x : 4, y : 3)),
        new PieceData(14, "red", "soldier", (x : 6, y : 3)),
        new PieceData(15, "red", "soldier", (x : 8, y : 3)),
        new PieceData(16, "blue", "chariot", (x : 0, y : 9)),
        new PieceData(17, "blue", "elephant", (x : 1, y : 9)),
        new PieceData(18, "blue", "horse", (x : 2, y : 9)),
        new PieceData(19, "blue", "guard", (x : 3, y : 9)),
        new PieceData(20, "blue", "guard", (x : 5, y : 9)),
        new PieceData(21, "blue", "elephant", (x : 6, y : 9)),
        new PieceData(22, "blue", "horse", (x : 7, y : 9)),
        new PieceData(23, "blue", "chariot", (x : 8, y : 9)),
        new PieceData(24, "blue", "general", (x : 4, y : 8)),
        new PieceData(25, "blue", "cannon", (x : 1, y : 7)),
        new PieceData(26, "blue", "cannon", (x : 7, y : 7)),
        new PieceData(27, "blue", "soldier", (x : 0, y : 6)),
        new PieceData(28, "blue", "soldier", (x : 2, y : 6)),
        new PieceData(29, "blue", "soldier", (x : 4, y : 6)),
        new PieceData(30, "blue", "soldier", (x : 6, y : 6)),
        new PieceData(31, "blue", "soldier", (x : 8, y : 6))
    };
    private Dictionary<Tuple<int, int>, Node> _tileMap = new Dictionary<Tuple<int, int>, Node>();

    public override void _Ready()
    {
        SetupTiles();
        SetupPieces();
    }

    // Create new tiles and place them on every intersection on the board.
    public void SetupTiles()
    {
        var tile = GD.Load<PackedScene>("res://Game/Tile/Tile.tscn");
        for (int x = 0; x < 9; x++)
        {
            for (int y = 0; y < 10; y++)
            {
                Tile newTile = (Tile)tile.Instance();
                newTile.Coordinates = new Tuple<int, int>(x, y);
                newTile.Position = new Vector2(x * this._scale + this._tileOffset, y * this._scale + this._tileOffset);
                newTile.Connect("TileSelected", this, "OnTileSelected");
                AddChild(newTile);

                _tileMap.Add(new Tuple<int, int>(x, y), newTile);
            }
        }
    }
    public void SetupPieces()
    {
        var piece = GD.Load<PackedScene>("res://Game/Piece/Piece.tscn");

        int offset = this._tileOffset + this._pieceOffset;
        foreach (PieceData data in _pieceData)
        {
            Piece newPiece = (Piece)piece.Instance();
            Texture texture = (Texture)ResourceLoader.Load($"res://Assets/Pieces/HanjaBlue/{data.Color}_{data.Category}.png");
            newPiece.GetNode<Sprite>("Sprite").Texture = texture;
            newPiece.Position = new Vector2(data.Position.x * this._scale + offset, data.Position.y * this._scale + offset);
            newPiece.Destinations.Add(new Tuple<int, int>(data.Position.x + 1, data.Position.y));
            AddChild(newPiece);

            Tuple<int, int> key = new Tuple<int, int>(data.Position.x, data.Position.y);

            Tile tile = (Tile)_tileMap[key];
            tile.Occupant = (Piece)newPiece;
        }
    }

    public void OnTileSelected(Tile tile)
    {
        GD.Print($"TILE selected at position: {tile.Position}");
        GD.Print($"OCCUPANT is: {tile.Occupant?.GetType()}");

        // No piece at source and tile selected contains piece.
        if (this.Source is null && !(tile.Occupant is null))
        {
            this.Source = tile;
            tile.HighlightTile();
            foreach (Tuple<int, int> destination in tile.Occupant.Destinations)
            {
                if (!_tileMap.ContainsKey(destination))
                {
                    return;
                }
                Tile destTile = (Tile)_tileMap[destination];

                destTile.HighlightTile();
                GD.Print($"DESTINATION: {destination}.");
            }
            return;
        }

        // Piece at source so tile selected is destination.
        if (!(this.Source is null))
        {
            this.Destination = tile;

            GD.Print($"MOVE from {this.Source.Occupant.Position} to {this.Destination.Position}");
            MovePiece();

            // Clear all tile destination highlights.
            this.Source.UnHighlightTile();

            foreach (Tile t in _tileMap.Values)
            {
                t.UnHighlightTile();
            }

            // Clear source and destination.
            this.Source = null;
            this.Destination = null;
        }
    }

    public void MovePiece()
    {
        if (this.Source.Occupant == this.Destination.Occupant)
        {
            return;
        }

        // Check if destination can be reached by piece.
        bool isDestinationReachable = this.Source.Occupant.Destinations
            .Where(dest => dest.Item1 == this.Destination.Coordinates.Item1 && dest.Item2 == this.Destination.Coordinates.Item2)
            .Any();

        if (!isDestinationReachable)
        {
            return;
        }

        // Move to destination.
        Piece target = this.Destination.Occupant;

        if (!(target is null))
        {
            target.QueueFree();
        }

        this.Destination.Occupant = this.Source.Occupant;
        this.Source.Occupant = null;

        Vector2 destination = this.Destination.Position;
        destination.x += this._pieceOffset;
        destination.y += this._pieceOffset;

        this.Destination.Occupant.Position = destination;
    }

    public override void _Process(float delta)
    {
    }
}
