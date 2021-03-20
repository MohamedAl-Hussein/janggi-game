using Godot;
using System;
using System.Collections.Generic;
using janggi.Game.Piece;

public class Piece : Area2D 
{
    public Tile OccupyingTile;
    public List<Tuple<int, int>> Destinations = new List<Tuple<int, int>>();
    public PieceColor Color;

    [Signal]
    public delegate void PieceSelected(Piece piece);

    public override void _Ready()
    {
    }

    public override void _InputEvent(Godot.Object viewport, InputEvent @event, int shapeIdx)
    {
        if (@event is InputEvent mouse)
        {
            if (mouse.IsPressed())
            {
                this.EmitSignal("PieceSelected", this);
            }
        }
    }
}
