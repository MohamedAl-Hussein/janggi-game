using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;

using Common;

namespace SocketClient.Messages
{
    public class MessageConverter : JsonConverter
    {
        public override bool CanConvert(Type objectType)
        {
            return (objectType == typeof(Message));
        }

        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer)
        {
            JObject jObject = JObject.Load(reader);
            MessageData data = new MessageData();
            _ = Enum.TryParse(jObject["Action"].ToString(), out MessageAction action);

            switch (action)
            {
                case MessageAction.GAME_STARTED:
                    PieceData pieceData = new PieceData();
                    List<PieceDTO> pieces = new List<PieceDTO>();
                    foreach (JObject piece in jObject["Data"]["Pieces"])
                    {
                        List<int> position = piece["Position"].ToObject(typeof(List<int>)) as List<int>;
                        _ = Enum.TryParse(piece["Category"].ToString(), out PieceCategory category);
                        _ = Enum.TryParse(piece["Color"].ToString(), out PieceColor color);

                        PieceDTO pieceDTO = new PieceDTO()
                        {
                            Position = position,
                            Category = category,
                            Color = color
                        };

                        pieces.Add(pieceDTO);
                    }

                    pieceData.Pieces = pieces;
                    data = pieceData;
                    break;
                case MessageAction.GAME_STATUS:
                    data = jObject["Data"].ToObject(typeof(GameStatus)) as GameStatus;
                    break;
                case MessageAction.PIECE_DESTINATIONS:
                    data = jObject["Data"].ToObject(typeof(PieceDestinations)) as PieceDestinations;
                    break;
            }

            return new Message
            {
                Action = action,
                Data = data
            };
        }

        public override bool CanWrite
        {
            get { return false; }
        }

        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
        {
            throw new NotImplementedException();
        }
    }
}
