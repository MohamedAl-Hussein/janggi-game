using System.Collections.Generic;

using Common;

namespace SocketClient.Messages
{
    public class MessageData { }

    public class PieceData : MessageData
    {
        public List<PieceDTO> Pieces { get; set; }
    }

    public class InitialSetup : MessageData 
    { 
        public bool BlueLeftTransposed { get; set; }
        public bool BlueRightTransposed { get; set; }
        public bool RedLeftTransposed { get; set; }
        public bool RedRightTransposed { get; set; }
    }

    public class GameStatus : MessageData 
    { 
        public string GameState { get; set; }
        public string PlayerTurn { get; set; }
        public bool IsChecked { get; set; }
    }

    public class PieceDestinations : MessageData 
    { 
        public List<int> Source { get; set; }
        public List<List<int>> Destinations { get; set; }
    }

    public class MoveRequest : MessageData 
    { 
        public List<int> Source { get; set; }
        public List<int> Destination { get; set; }
    }
}
