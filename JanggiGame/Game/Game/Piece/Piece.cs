using Godot;
using System;
using System.Collections.Generic;

using Common;

public class Piece : Area2D 
{
    public PieceColor Color;
    public PieceCategory Category;
    public Coordinate Coordinates;

    public List<Coordinate> Destinations = new List<Coordinate>();

    public void FromDTO(PieceDTO dto)
    {
        if (Enum.TryParse(dto.Color.ToString(), out PieceColor color))
            Color = color;

        if (Enum.TryParse(dto.Category.ToString(), out PieceCategory category))
            Category = category;

        Coordinates = new Coordinate() { x_coord = (int)dto.Position[0], y_coord = (int)dto.Position[1] };
    }
}
