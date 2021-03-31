using Godot;

public class PassTurnButton : TextureButton
{
    [Signal] public delegate void PassTurnButtonPressed();

    public override void _Pressed()
        => EmitSignal(nameof(PassTurnButtonPressed));
}
