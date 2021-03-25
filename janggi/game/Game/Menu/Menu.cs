using Godot;
using System;

public class Menu : Panel
{
    public override void _Ready()
    {
        GetNode("PlayButton").Connect("pressed", this, nameof(_OnPlayButtonPressed));
        GetNode("LeaderboardButton").Connect("pressed", this, nameof(_OnLeaderboardButtonPressed));
        GetNode("SettingsButton").Connect("pressed", this, nameof(_OnSettingsButtonPressed));
        GetNode("ExitButton").Connect("pressed", this, nameof(_OnExitButtonPressed));
    }

    public void _OnPlayButtonPressed()
    {
        GetNode<Label>("Label").Text = "NEW GAME!";
    }

    public void _OnLeaderboardButtonPressed()
    {
        GetNode<Label>("Label").Text = "Leaderboard";
    }

    public void _OnSettingsButtonPressed()
    {
        GetNode<Label>("Label").Text = "Settings";
    }

    public void _OnExitButtonPressed()
    {
        GetNode<Label>("Label").Text = "Exit";
    }

    public override void _Process(float delta)
    {
    }
}
