import dataclasses


@dataclasses.dataclass
class MessageDTO:
    pass


class GameStateMessageDTO(MessageDTO):
    player_turn: str
    game_state: str


class DestinationMessageDTO(MessageDTO):
    coordinate: (int, int)


class StartLayoutMessageDTO(MessageDTO):
    l_blue_swap: bool
    r_blue_swap: bool
    l_red_swap: bool
    r_red_swap: bool


class MoveRequestDTO(MessageDTO):
    source: (int, int)
    destination: (int, int)
