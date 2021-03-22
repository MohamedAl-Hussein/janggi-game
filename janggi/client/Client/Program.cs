using System;
using System.Net;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using Shared;

namespace Client
{

    public class MyMessage
    {
        public string StringProperty { get; set; }
        public int IntProperty { get; set; }
    }



    class Program
    {
        static async Task Main(string[] args)
        {

            Console.WriteLine("Press Enter to Connect");
            Console.ReadLine();

            var endpoint = new IPEndPoint(IPAddress.Loopback, 9001);

            var channel = new ClientChannel<JsonMessageProtocol,JObject>();

            channel.OnMessage(OnMessage);

            await channel.ConnectAsync(endpoint).ConfigureAwait(false);

            var myMessage = new MyMessage
            {
                IntProperty = 404,
                StringProperty = "Hello World"
            };

            Console.WriteLine("Sending");
            Print(myMessage);

            await channel.SendAsync(myMessage).ConfigureAwait(false);

            Console.ReadLine();

            await channel.ConnectAsync(endpoint).ConfigureAwait(false);
            Console.WriteLine("Sending");
            Print(myMessage);
            await channel.SendAsync(myMessage).ConfigureAwait(false);

            Console.ReadLine();
        }

        static Task OnMessage(JObject jObject)
        {
            Console.WriteLine("Received JObject Message");
            Print(Convert(jObject));
            return Task.CompletedTask;
        }

        static MyMessage Convert(JObject jObject)
            => jObject.ToObject(typeof(MyMessage)) as MyMessage;

        static void Print(MyMessage m) => Console.WriteLine($"MyMessage.IntProperty = {m.IntProperty}, MyMessage.StringProperty = {m.StringProperty}");
    }
}