using Godot;
using System;

public class Tile : Area2D
{
    public Piece Occupant;

    [Signal]
    public delegate void TileSelected(Tile tile);

    public override void _Ready()
    {
    }

    public override void _InputEvent(Godot.Object viewport, InputEvent @event, int shapeIdx)
    {
        if (@event is InputEventMouse mouse)
        {
            if (mouse.IsPressed())
            {
                this.EmitSignal("TileSelected", this);
            }
        }
    }
}
