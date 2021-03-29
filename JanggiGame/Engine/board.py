from __future__ import annotations

from typing import Dict, Iterator, List, Optional, Tuple, TYPE_CHECKING

from piece import PieceCategory
from utils import Point2D
from utils import Rectangle

if TYPE_CHECKING:
    from piece import JanggiPiece, PieceColor


class JanggiBoard:
    """
    Represents a Janggi game board, where a coordinate map holds the position of each Piece, and updates can be made
    to the map to reflect moves. Also holds the coordinates of the palaces and game board for a given game.
    """

    def __init__(self,
                 coord_map: Dict[Tuple[int, int], JanggiPiece],
                 blue_palace: Rectangle,
                 red_palace: Rectangle,
                 boundaries: Rectangle) -> None:
        """
        Initialize JanggiBoard with a coord_map, blue_palace and red_palace coordinates, and board boundaries.

        :param coord_map: Holds the coordinates of each Piece.
        :param blue_palace: Represents the blue palace.
        :param red_palace: Represents the red palace.
        :param boundaries: Represents the board boundaries.
        """

        self.__coord_map: Dict[Tuple[int, int], JanggiPiece] = coord_map
        self.__blue_palace: Rectangle = blue_palace
        self.__red_palace: Rectangle = red_palace
        self.__boundaries: Rectangle = boundaries

    @property
    def coord_map(self) -> Dict[Tuple[int, int], JanggiPiece]:
        return self.__coord_map

    @property
    def blue_palace(self) -> Rectangle:
        return self.__blue_palace

    @property
    def red_palace(self) -> Rectangle:
        return self.__red_palace

    @property
    def boundaries(self) -> Rectangle:
        return self.__boundaries

    def move(self, source: Point2D, destination: Point2D) -> None:
        """
        Move a piece from source coordinate to destination coordinate.

        Updates the piece's position after the move has been completed.

        :param source: Source coordinate.
        :param destination: Destination coordinate.
        """

        self.update_coord_map(source, destination)
        self.update_piece_position(destination)

    def swap(self, position_a: Point2D, position_b: Point2D):
        """
        Swaps two pieces at position a and b.

        Used during initialization as players can transpose their horse and elephants before game start.
        """

        piece_a: JanggiPiece = self.coord_map.get(position_a.to_tuple())
        piece_b: JanggiPiece = self.coord_map.get(position_b.to_tuple())
        self.coord_map[position_b.to_tuple()] = piece_a
        self.coord_map[position_a.to_tuple()] = piece_b

    def update_coord_map(self, source: Point2D, destination: Point2D) -> None:
        """
        Updates the coordinate map to reflect a piece moving from a source to a destination coordinate.

        Overwrites/adds new key-value pair with the destination as the key and Piece as the value.
        Then deletes the source-key from map.

        :param source: Source coordinate.
        :param destination: Destination coordinate.
        """

        self.coord_map[destination.to_tuple()] = self.coord_map.pop(source.to_tuple())

    def update_piece_position(self, position: Point2D) -> None:
        """
        Updates the piece's position to reflect the new coordinate they occupy.

        :param position: New coordinate.
        """

        self.coord_map[position.to_tuple()].position = position

    def is_inside_palace(self, piece: JanggiPiece):
        """
        Determines if a piece is within the boundaries of either the red palace or blue palace.

        :param piece: Piece object to investigate.
        :return: True if the piece is in the palace, False otherwise.
        """

        return piece.position in self.blue_palace or piece.position in self.red_palace

    def search(self, color: PieceColor, category_filter: PieceCategory = None) -> List[Optional[JanggiPiece]]:
        """
        Given a color and (optionally a category filter), searches coordinate map and returns all matches.

        :param color: Piece color attribute.
        :param category_filter: Piece category attribute to filter on.
        :return: A list of Piece objects or an empty list if no matches found.
        """

        matches: List[Optional[JanggiPiece]] = list()

        for piece in self.coord_map.values():
            if piece.color == color:

                # Filtering on category is disabled; so add any pieces that have the same color attribute.
                if category_filter is None:
                    matches.append(piece)
                    continue

                # Filtering on category is enabled; so only add pieces that have the same color and category attributes.
                if piece.category == category_filter:
                    matches.append(piece)

        return matches

    def find_path(self, source: Point2D, destination: Point2D) -> Optional[List[Point2D]]:
        """
        Given a source and destination, find the first path that can take the piece residing at source to the
        destination.

        :param source: Source coordinate.
        :param destination: Destination coordinate.
        :return: List of coordinates going from source to destination, or an empty list if no path exists.
        """

        piece: JanggiPiece = self.coord_map[source.to_tuple()]
        in_palace: bool = self.is_inside_palace(piece)

        path_generator: Iterator[List[Point2D]] = piece.generate_path(source=source, in_palace=in_palace)
        path: List[Point2D] = next(path_generator)

        # Iteratively generate each path the piece can travel on until a match is found or no more paths exist.
        while path[-1] != destination:
            try:
                path = next(path_generator)
            except StopIteration:
                return list()

        return path

    def find_obstacles(self, path: List[Point2D]) -> bool:
        """
        Given a path, determine if any obstacles exist that will block piece travelling from start to end of path.

        :param path: Array of ordered coordinates representing a path from point a to b.
        :return: True if the path is free of obstacles, False otherwise.
        """

        piece: JanggiPiece = self.coord_map[path[0].to_tuple()]
        in_palace: bool = self.is_inside_palace(piece)
        path_objects: List[Optional[JanggiPiece]] = list()

        # Examine each point along the path for any pieces.
        for coord in path:

            # Only consider coordinates within the board boundaries.
            if coord not in self.boundaries:
                return True

            obj = self.coord_map.get(coord.to_tuple())
            path_objects.append(obj)

        # Examine the objects on the path to determine if they can be traversed.
        # Note that the palace walls are considered as virtual obstacles.
        return piece.is_obstacle_in_path(in_palace, path_objects, path, self.blue_palace, self.red_palace)

    def generate_paths(self, *pieces: JanggiPiece) -> List[List[Point2D]]:
        """
        Generate traversable paths for one or more pieces.

        Each path is inspected for obstacles and only returned if it can be traversed by the starting piece.

        :param pieces: One or more pieces.
        :return: List of paths.
        """

        paths = list()

        # Generate paths for all provided pieces.
        for piece in list(pieces):
            in_palace = self.is_inside_palace(piece)

            # Generate all paths for single piece.
            piece_paths = list(piece.generate_path(source=piece.position, in_palace=in_palace))

            # Keep the paths that can be traversed.
            for path in piece_paths:
                if not self.find_obstacles(path):
                    paths.append(path)

        return paths

