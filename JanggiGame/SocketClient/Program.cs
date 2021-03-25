using Common;
using System;
using System.Collections.Generic;
using System.Net;
using System.Threading.Tasks;

namespace Client
{
    class Program
    {
        static Message _message;
        static async Task Main(string[] args)
        {
            Console.WriteLine("Press Enter to Connect");
            Console.ReadLine();

            var endpoint = new IPEndPoint(IPAddress.Loopback, 9001);

            var channel = new ClientChannel<JsonMessageProtocol, Message>();

            channel.OnMessage(OnMessage);

            await channel.ConnectAsync(endpoint).ConfigureAwait(false);

            var myMessage = new Message 
            {
                Action = MessageAction.NEW_GAME,
                Data = null 
            };

            Console.WriteLine("Sending");
            Print(myMessage);

            await channel.SendAsync(myMessage).ConfigureAwait(false);

            //var responseMsg = channel.ReceiveAsync<Message>();

            Console.ReadLine();

            await channel.ConnectAsync(endpoint).ConfigureAwait(false);
            var myMessage2 = new Message
            {
                Action = MessageAction.SETUP_COMPLETED,
                Data = new InitialSetup
                {
                    BlueLeftTransposed = false,
                    BlueRightTransposed = true,
                    RedLeftTransposed = true,
                    RedRightTransposed = false
                } 
            };
            Console.WriteLine("Sending");
            Print(myMessage2);

            await channel.SendAsync(myMessage2).ConfigureAwait(false);

            Console.ReadLine();

            await channel.ConnectAsync(endpoint).ConfigureAwait(false);
            var myMessage3 = new Message 
            {
                Action = MessageAction.GET_PIECE_DESTINATIONS,
                Data = new PieceDestinations
                {
                    Source = new List<int> { 0, 0 },
                    Destinations = new List<List<int>>() 
                } 
            };
            Console.WriteLine("Sending");
            Print(myMessage3);
            await channel.SendAsync(myMessage3).ConfigureAwait(false);

            Console.ReadLine();

            await channel.ConnectAsync(endpoint).ConfigureAwait(false);
            var myMessage4 = new Message
            {
                Action = MessageAction.GET_GAME_STATUS,
                Data = new GameStatus 
                {
                    GameState = null,
                    PlayerTurn = null,
                    IsChecked = false 
                } 
            };
            Console.WriteLine("Sending");
            Print(myMessage4);
            await channel.SendAsync(myMessage4).ConfigureAwait(false);

            Console.ReadLine();
        }

        static Task OnMessage(Message message)
        {
            _message = message;
            Console.WriteLine("Received");
            Print(message);
            return Task.CompletedTask;
        }

        static void Print(Message m) => Console.WriteLine($"MyMessage.Action = {m.Action}, MyMessage.Data = {m.Data}");
        }
}