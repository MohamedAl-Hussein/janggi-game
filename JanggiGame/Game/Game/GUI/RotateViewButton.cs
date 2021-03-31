using Godot;

public class RotateViewButton : TextureButton
{
    [Signal] public delegate void RotateViewButtonPressed();

    public override void _Pressed()
        => EmitSignal(nameof(RotateViewButtonPressed));
}
