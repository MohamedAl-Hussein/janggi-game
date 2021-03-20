using Godot;
using janggi.Game.Piece;
using System;

public class Board : Node2D
{
    private readonly int _tileOffset = 18;
    private readonly int _pieceOffset = 32;
    private readonly int _scale = 100;
    public Area2D Source;
    public Area2D Destination;
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
                Area2D newTile = (Area2D)tile.Instance();
                newTile.Position = new Vector2(x * this._scale + this._tileOffset, y * this._scale + this._tileOffset);
                newTile.Connect("TileSelected", this, "OnItemSelected");
                AddChild(newTile);
            }
        }
    }
    public void SetupPieces()
    {
        var piece = GD.Load<PackedScene>("res://Game/Piece/Piece.tscn");

        int offset = this._tileOffset + this._pieceOffset;
        foreach (PieceData data in _pieceData)
        {
            Area2D newPiece = (Area2D)piece.Instance();
            Texture texture = (Texture)ResourceLoader.Load($"res://Assets/Pieces/HanjaBlue/{data.Color}_{data.Category}.png");
            newPiece.GetNode<Sprite>("Sprite").Texture = texture;
            newPiece.Position = new Vector2(data.Position.x * this._scale + offset, data.Position.y * this._scale + offset);
            newPiece.Connect("PieceSelected", this, "OnItemSelected");
            AddChild(newPiece);
        }
    }

    public void OnItemSelected(Area2D item)
    {
        string t = ""; 

        switch (item)
        {
            case Piece piece:

                t = "PIECE";
                if (this.Source is null)
                {
                    this.Source = piece;
                }
                else
                {
                    this.Destination = piece;
                }
                break;
            case Tile tile:
                t = "TILE";
                if (!(this.Source is null))
                {
                    this.Destination = tile;
                }
                break;
        } 

        //GD.Print($"{t} selected at position: {item.Position}.");
        GD.Print($"SOURCE: {this.Source?.GetType()}. DESTINATION: {this.Destination?.GetType()}.");
    }

    public void MovePiece()
    {
        Vector2 destination = this.Destination.Position;

        if (this.Destination.GetType() == typeof(Piece))
        {
            destination.x -= this._pieceOffset;
            destination.y -= this._pieceOffset;
            this.Destination.QueueFree();
        }

        destination.x += this._pieceOffset;
        destination.y += this._pieceOffset;

        this.Source.Position = destination;
    }

    public override void _Process(float delta)
    {
        if (!(this.Source is null) && !(this.Destination is null))
        {
            if (this.Source != this.Destination)
            {
                MovePiece();
                this.Source = null;
                this.Destination = null;
            }
        }
    }
}
