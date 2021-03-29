using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Runtime.InteropServices;
using System.Threading.Tasks;

using Common;
using SocketClient.Channels;
using SocketClient.Messages;
using SocketClient.Protocols;

namespace SocketClient
{
    /// <summary> 
    /// Class <c>Client</c> is responsible for dispatching messages to server and storing response to be returned to
    /// caller.
    /// </summary>
    public class Client
    {
        private const int PORT = 9001;

        private readonly IPEndPoint _endpoint;
        private readonly ClientChannel<JsonMessageProtocol, Message> _channel;

        public List<PieceDTO> PieceDTOs;
        public List<Coordinate> PieceDestinations;
        public GameState GameState;
        public PieceColor PlayerTurn;
        public bool IsChecked;

        /// <summary>
        /// Constructor <c>Client</c> creates a new instance of <c>Client</c> class.
        /// Configures the endpoint to reach the server and creates and configures new <c>Channel</c> instance to handle 
        /// messages between client and server. 
        /// </summary>
        public Client()
        { 
            _endpoint = new IPEndPoint(IPAddress.Loopback, PORT);
            _channel = new ClientChannel<JsonMessageProtocol, Message>();
            _channel.OnMessage(OnMessage);
        }

        /// <summary>
        /// Method <c>NewRequest</c> dispatches a request to the server and waits for a response.
        /// </summary>
        /// <param name="action">Type of message to dispatch.</param>
        /// <param name="source">Optional source coordinate.</param>
        /// <param name="destination">Optional destination coordinate.</param>
        public void NewRequest(MessageAction action, [Optional] Coordinate source, [Optional] Coordinate destination)
        {
            switch (action)
            {
                case MessageAction.NEW_GAME:
                    HandleRequest(RequestNewGame).Wait(500);
                    break;
                case MessageAction.MOVE_COMPLETED:
                    HandleRequest(() => RequestConfirmMove(source, destination)).Wait(250);
                    break;
                case MessageAction.GET_GAME_STATUS:
                    HandleRequest(RequestGameStatus).Wait(250);
                    break;
                case MessageAction.GET_PIECE_DESTINATIONS:
                    HandleRequest(() => RequestPieceDestinations(source)).Wait(100);
                    break;
                case MessageAction.SETUP_COMPLETED:
                    break;
            }
        }

        /// <summary>
        /// Method <c>HandleRequest</c> acts as a wrapper for requests by allowing them to be waitable.
        /// </summary>
        /// <param name="handler">The request to wrap alongside its parameters.</param>
        /// <returns>Waitable task.</returns>
        private async Task HandleRequest(Action handler)
        {
            Task task = new Task(handler);
            task.Start();
            await task;
        }


        /// <summary>
        /// Method <c>RequestNewGame</c> sends a request to server to start a new instance of a game.
        /// </summary>
        private async void RequestNewGame()
        {
            var message = new Message() 
            {
                Action = MessageAction.NEW_GAME,
                Data = null
            };

            await SendMessage(message).ConfigureAwait(false);
        }

        /// <summary>
        /// Method <c>RequestConfirmSetup</c> sends a request to server to tranpose the horse and elephant
        /// when specified.
        /// </summary>
        /// <param name="left_blue">Whether or not to transpose Blue's left horse and elephant.</param>
        /// <param name="right_blue">Whether or not to transpose Blue's right horse and elephant.</param>
        /// <param name="left_red">Whether or not to transpose Red's left horse and elephant.</param>
        /// <param name="right_red">Whether or not to transpose Red's right horse and elephant.</param>
        private async void RequestConfirmSetup(bool left_blue, bool right_blue, bool left_red, bool right_red)
        {
            Message message = new Message() 
            {
                Action = MessageAction.SETUP_COMPLETED,
                Data = new InitialSetup
                {
                    BlueLeftTransposed = left_blue,
                    BlueRightTransposed = right_blue,
                    RedLeftTransposed = left_red,
                    RedRightTransposed = right_red
                }
            };

            await SendMessage(message).ConfigureAwait(false);
        }

        /// <summary>
        /// Method <c>RequestGameStatus</c> sends a request to server for current game's status.
        /// </summary>
        private async void RequestGameStatus()
        {
            Message message = new Message()
            {
                Action = MessageAction.GET_GAME_STATUS,
                Data = null
            };

            await SendMessage(message).ConfigureAwait(false);
        }

        /// <summary>
        /// Method <c>RequestPieceDestinations</c> sends a request to server for all possible destinations a given
        /// piece can travel to given its source coordinate.
        /// </summary>
        /// <param name="position">The source coordinate of the piece.</param>
        private async void RequestPieceDestinations(Coordinate position)
        {
            Message message = new Message()
            {
                Action = MessageAction.GET_PIECE_DESTINATIONS,
                Data = new PieceDestinations
                {
                    Source = new List<int> { position.x_coord, 9 - position.y_coord },
                    Destinations = null
                }
            };

            await SendMessage(message).ConfigureAwait(false);
        }

        /// <summary>
        /// Method <c>RequestConfirmMove</c> sends a request to server to finalize a move made by a piece from a 
        /// source coordinate to a destination coordinate.
        /// </summary>
        /// <param name="source">The source coordinate of the piece.</param>
        /// <param name="destination">The destination coordinate of the piece.</param>
        private async void RequestConfirmMove(Coordinate source, Coordinate destination)
        {
            Message message = new Message()
            {
                Action = MessageAction.MOVE_COMPLETED,
                Data = new MoveRequest
                {
                    Source = new List<int> { source.x_coord, source.y_coord },
                    Destination = new List<int> { destination.x_coord, destination.y_coord } 
                }
            };

            await SendMessage(message);
        }

        /// <summary>
        /// Method <c>RequestEndGame</c> sends a request to server to end the current game.
        /// </summary>
        private async void RequestEndGame()
        {
            Message message = new Message()
            {
                Action = MessageAction.END_GAME,
                Data = null
            };

            await SendMessage(message);
        }

        /// <summary>
        /// Method <c>Connect</c> starts a new connection with the server.
        /// </summary>
        /// <returns></returns>
        private async Task Connect()
            => await _channel.ConnectAsync(_endpoint).ConfigureAwait(false);

        /// <summary>
        /// Method <c>SendMessage</c> dispatches a <c>Message</c> object to the server.
        /// </summary>
        /// <param name="message">The message to dispatch.</param>
        /// <returns></returns>
        private async Task SendMessage(Message message)
        {
            await Connect().ConfigureAwait(false);
            await _channel.SendAsync(message).ConfigureAwait(false);
        }

        /// <summary>
        /// Method <c>OnMessage</c> is called upon a response from the server. 
        /// </summary>
        /// <param name="message">The returned message.</param>
        /// <returns></returns>
        public Task OnMessage(Message message)
        {
            ExtractMessageData(message);
            return Task.CompletedTask;
        }

        /// <summary>
        /// Method <c>ExtractMessageData</c> extracts the <c>MessageData</c> object of a given <c>Message</c> into a 
        /// class property. 
        /// </summary>
        /// <param name="message">The message to extract.</param>
        private void ExtractMessageData(Message message)
        {
            switch (message.Data)
            {
                case PieceData pieceData:
                    PieceDTOs = pieceData.Pieces;
                    break;
                case PieceDestinations pieceDestinations:
                    PieceDestinations = pieceDestinations.Destinations
                        .Select(dest => new Coordinate { x_coord = dest[0], y_coord = dest[1] })
                        .ToList();
                    break;
                case GameStatus status:
                    if (Enum.TryParse(status.GameState, out GameState state))
                        GameState = state;
                    if (Enum.TryParse(status.PlayerTurn, out PieceColor turn))
                        PlayerTurn = turn;
                    IsChecked = status.IsChecked;
                    break;
            }
        }
    }
}
