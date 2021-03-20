using Godot;
using System;

public class Piece : Area2D 
{
    public Tile OccupyingTile;

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
