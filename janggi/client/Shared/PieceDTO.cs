using System.Collections.Generic;

namespace Shared
{
    public class PieceDTO
    {
        public List<int> Position { get; set; }
        public PieceColor Color { get; set; }
        public PieceCategory Category { get; set; }
    }

    public enum PieceColor
    {
        BLUE,
        RED
    }

    public enum PieceCategory
    {
        GENERAL,
        GUARD, 
        HORSE, 
        ELEPHANT,
        CHARIOT,
        CANNON,
        SOLDIER
    }

}
