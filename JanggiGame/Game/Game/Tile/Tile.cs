using Godot;

using Common;

public class Tile : Area2D
{
    public Piece Occupant;
    public Coordinate Coordinates;

    [Signal]
    public delegate void TileSelected(Tile tile);

    public override void _InputEvent(Object viewport, InputEvent @event, int shapeIdx)
    {
        if (@event is InputEventMouse mouse)
        {
            if (mouse.IsPressed())
                this.EmitSignal("TileSelected", this);
        }
    }

    public void HighlightTile(bool isChecked = false)
    {
        if (!isChecked)
            GetNode<Sprite>("Highlighter").Visible = true;
        else
            GetNode<Sprite>("IsCheckedHighlighter").Visible = true;
    }

    public void UnHighlightTile()
    {
        GetNode<Sprite>("Highlighter").Visible = false;
        GetNode<Sprite>("IsCheckedHighlighter").Visible = false;
    }
}
