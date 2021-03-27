using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;

using Common;
using SocketClient.Channels;
using SocketClient.Messages;
using SocketClient.Protocols;

namespace SocketClient
{
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

        public Client()
        { 
            _endpoint = new IPEndPoint(IPAddress.Loopback, PORT);
            _channel = new ClientChannel<JsonMessageProtocol, Message>();
            _channel.OnMessage(OnMessage);
        }

        public async void HandleNewGameRequest()
        {
            var message = new Message() 
            {
                Action = MessageAction.NEW_GAME,
                Data = null
            };

            await SendMessage(message).ConfigureAwait(false);
        }

        public async void HandleSetupRequest(bool left_blue, bool right_blue, bool left_red, bool right_red)
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

        public async void HandleGameStatusRequest()
        {
            Message message = new Message()
            {
                Action = MessageAction.GET_GAME_STATUS,
                Data = null
            };

            await SendMessage(message).ConfigureAwait(false);
        }

        public async void HandlePieceDestinationsRequest(Coordinate position)
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

        public async void HandleMoveRequest(Coordinate source, Coordinate destination)
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

        public async void HandleEndGameRequest()
        {
            Message message = new Message()
            {
                Action = MessageAction.END_GAME,
                Data = null
            };

            await SendMessage(message);
        }

        public async Task Connect()
            => await _channel.ConnectAsync(_endpoint).ConfigureAwait(false);

        public async Task SendMessage(Message message)
        {
            await Connect().ConfigureAwait(false);
            await _channel.SendAsync(message).ConfigureAwait(false);
        }

        public Task OnMessage(Message message)
        {
            ExtractDTO(message);
            return Task.CompletedTask;
        }

        private void ExtractDTO(Message message)
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
