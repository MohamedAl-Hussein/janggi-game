using System.IO;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;

using SocketClient.Messages;

namespace SocketClient.Protocols
{
    public class JsonMessageProtocol : Protocol<Message>
    {
        static readonly JsonSerializer _serializer;
        static readonly JsonSerializerSettings _settings;

        static JsonMessageProtocol()
        {
            _settings = new JsonSerializerSettings
            {
                Formatting = Formatting.Indented,
                DateTimeZoneHandling = DateTimeZoneHandling.Utc,
                ContractResolver = new DefaultContractResolver { },
                Converters = new JsonConverter[] { new MessageConverter() } 
            };
            _settings.PreserveReferencesHandling = PreserveReferencesHandling.None;
            _serializer = JsonSerializer.Create(_settings);
        }

        protected override Message Decode(byte[] message)
            => JsonConvert.DeserializeObject<Message>(Encoding.UTF8.GetString(message), _settings);

        protected override byte[] EncodeBody<T>(T message)
        {
            var sb = new StringBuilder();
            var sw = new StringWriter(sb);
            _serializer.Serialize(sw, message);
            return Encoding.UTF8.GetBytes(sb.ToString());
        }
    }
}