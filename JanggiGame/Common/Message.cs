using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using System.Collections.Generic;

namespace Common
{
    public class Message
    {
        public MessageAction Action { get; set; }

        public MessageData Data { get; set; }
    }

    [JsonConverter(typeof(StringEnumConverter))]
    public enum MessageAction
    {
        NEW_GAME,
        GAME_STARTED,
        SETUP_COMPLETED,
        SETUP_CONFIRMED,
        GET_GAME_STATUS,
        GAME_STATUS,
        GET_PIECE_DESTINATIONS,
        PIECE_DESTINATIONS,
        MOVE_COMPLETED,
        MOVE_CONFIRMED,
        END_GAME,
        GAME_OVER,
        DEFAULT 
    }
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
        public Tuple<int, int> Source { get; set; }
        public Tuple<int, int> Destination { get; set; }
    }
}
