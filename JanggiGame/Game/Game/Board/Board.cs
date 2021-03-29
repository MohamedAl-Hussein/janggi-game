using Common;
using Godot;
using System.Collections.Generic;

public class Board : Node2D
{
    private const string TILE_SCENE = "res://Game/Tile/Tile.tscn";
    private const string PIECE_SCENE = "res://Game/Piece/Piece.tscn";
    private const string PIECE_ASSET_PATH = "res://Assets/Pieces/"; 
    private const int GRID_COLS = 9;
    private const int GRID_ROWS = 10;
    private const int TILE_OFFSET = 18;
    private const int PIECE_OFFSET = 32;
    private const int POSITION_OFFSET = TILE_OFFSET + PIECE_OFFSET;
    private const int SCALE = 100;


    public Dictionary<Coordinate, Tile> TileMap = new Dictionary<Coordinate, Tile>();

    public override void _Ready()
        => SetupTiles();

    // Create new tiles and place them on every intersection on the board.
    public void SetupTiles()
    {
        var tile = GD.Load<PackedScene>(TILE_SCENE);
        for (int x = 0; x < GRID_COLS; x++)
        {
            for (int y = 0; y < GRID_ROWS; y++)
            {
                Tile newTile = (Tile)tile.Instance();
                newTile.Coordinates = new Coordinate { x_coord = x, y_coord = y };
                newTile.Position = new Vector2(x * SCALE + TILE_OFFSET, y * SCALE + TILE_OFFSET);
                newTile.Connect("TileSelected", GetParent(), "OnTileSelected");
                AddChild(newTile);

                TileMap.Add(newTile.Coordinates, newTile);
            }
        }
    }
    public void SetupPieces(List<PieceDTO> pieceDTOs)
    {
        var piece = GD.Load<PackedScene>(PIECE_SCENE);

        foreach(PieceDTO dto in pieceDTOs)
        {
            // Create Piece
            Piece newPiece = (Piece)piece.Instance();
            newPiece.FromDTO(dto);
            Texture texture = (Texture)ResourceLoader.Load(PieceAssetPath(newPiece));
            newPiece.GetNode<Sprite>("Sprite").Texture = texture;
            newPiece.Position = ToPosition(newPiece.Coordinates);

            // Add to Board
            AddChild(newPiece);

            // Add to tile map
            Coordinate key = new Coordinate 
            { 
                x_coord = newPiece.Coordinates.x_coord, 
                y_coord = GRID_ROWS - 1 - newPiece.Coordinates.y_coord 
            };
            Tile tile = TileMap[key];
            tile.Occupant = newPiece;
        }
    }
    private string PieceAssetPath(Piece piece)
        => $"{PIECE_ASSET_PATH}HanjaBlue/{piece.Color.ToString().ToLower()}_{piece.Category.ToString().ToLower()}.png";

    #region Converters

    public Coordinate FromPosition(Vector2 position)
    {
        float x = (position.x - POSITION_OFFSET) / SCALE;
        float y = -((position.y - POSITION_OFFSET) / SCALE - GRID_ROWS + 1);

        return new Coordinate { x_coord = (int)x, y_coord = (int)y };
    }

    public Vector2 ToPosition(Coordinate location)
    {
        int x = location.x_coord * SCALE + POSITION_OFFSET;
        int y = (-location.y_coord + GRID_ROWS - 1) * SCALE + POSITION_OFFSET;

        return new Vector2(x, y);
    }

    public Vector2 NewDestination(Vector2 oldDestination)
    {
        int newDestX = (int)(oldDestination.x + PIECE_OFFSET);
        int newDestY = (int)(oldDestination.y + PIECE_OFFSET);

        return new Vector2(newDestX, newDestY);
    }

    public Coordinate ConvertYCoord(Coordinate position)
        => new Coordinate { x_coord = position.x_coord, y_coord = GRID_COLS - position.y_coord };

    public Coordinate FromTilePosition(Vector2 position)
    {
        int x = (int)(position.x - TILE_OFFSET) / SCALE;
        int y = (int)(position.y - TILE_OFFSET) / SCALE;

        return new Coordinate { x_coord = x, y_coord = y };
    }

    #endregion
}
