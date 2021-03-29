using System.Collections.Generic;

namespace Common
{
    public class PieceDTO
    {
        public List<int> Position { get; set; }
        public PieceColor Color { get; set; }
        public PieceCategory Category { get; set; }
    }
}
