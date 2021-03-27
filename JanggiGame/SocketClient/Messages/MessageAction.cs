using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace SocketClient.Messages
{
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
}
