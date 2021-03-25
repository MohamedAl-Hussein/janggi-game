namespace janggi.Game.Piece
{
    public struct PieceData
    {
        public PieceData(int id, string color, string category, (int x, int y) position)
        {
            ID = id;
            Color = color;
            Category = category;
            Position = position;
        }

        public int ID { get; set; }
        public string Color { get; set; }
        public string Category { get; set; }
        public (int x, int y) Position { get; set; }
    }
}
