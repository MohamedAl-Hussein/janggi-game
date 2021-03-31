using Godot;

public class ForfeitButton : TextureButton
{
    [Signal] public delegate void ForfeitButtonPressed();

    public override void _Pressed()
        => EmitSignal(nameof(ForfeitButtonPressed));
}
