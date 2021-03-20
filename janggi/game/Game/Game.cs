using Godot;
using janggi.Game.Piece;
using System;

public class Game : Node2D
{
    private Board _board;
    public override void _Ready()
    {
        NewGame();
    }

    public void NewGame()
    {
        SetupBoard();
    }

    public void SetupBoard()
    {
        var board = GD.Load<PackedScene>("res://Game/Board/Board.tscn");
        Board boardNode = (Board)board.Instance();
        AddChild(boardNode);
        boardNode.Connect("MoveCompleted", this, "OnMoveCompleted");

        _board = boardNode;
    }

    public void OnMoveCompleted()
    {
        // Change turn to next color.
        if (_board.Turn == PieceColor.BLUE)
        {
            _board.Turn = PieceColor.RED;
        }
        else
        {
            _board.Turn = PieceColor.BLUE;
        }
    }


    // Create instance of board
    // Add tiles to board
    // Add pieces to board

    // Handle movement on board
    // Handle game state and turns
    // Make calls to engine to validate moves and get legal paths
}
