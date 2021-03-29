# About The Project

**Project is still under development. Most recent updates can be found under the `dev` branch.**

Two-player game for playing a game of Janggi. 

This project consists of four primary components:

1. Game
2. Engine
3. SocketClient
4. SocketServer

### Game

User interface is designed using Godot's game engine.

### Engine

Game engine is responsible for path-generation algorithms, obstacle-detection strategies, and overall rules for playing the game. 

### SocketClient

Responsible for dispatching messages from Game UI to Engine and passing responses back to Game UI. 

### SocketServer

Responsible for consuming message from Game UI and calling relevant methods within the Engine. Sends back response message containing requested data (if any). 

![Gameplay Demo](https://github.com/MohamedAl-Hussein/janggi-game/blob/main/media/gameplay_demo_01.gif)

### Built With

* Python 3.8
* C# 7.3, 9.0
* Godot
* .NET Framework 4.7.2
* .NET 5.0

The Game and SocketClient components are written in C#, using a combination of .NET Framework 4.7.2 (latest supported framework by Godot) and .Net 5.0.

The Engine and SocketServer components are written in Python.

# Getting Started

# License

Distributed under the MIT License. See `LICENSE` for more information.

# Contact

Mohamed Al-Hussein - [LinkedIn](https://www.linkedin.com/in/mohamedal-hussein/) - mohamed.n.al.hussein@gmail.com

Project Link: https://github.com/MohamedAl-Hussein/janggi-game

# Acknowledgements

* [C# Socket Programming Series](https://www.youtube.com/playlist?list=PLHLYG7mk_iQnUkCK3SvZVWghJ1Qts9WKn) by Richard Weeks.
* [Godot Mono Series](https://www.youtube.com/playlist?list=PLMgDVIa0Pg8XMe1GVc5eg0Rwi-cXqIR6q) by Abdullah Aghazadah.
* [Game Assets](https://www.pychess.org/variant/janggi) from PyChess.
* [ReadMe Template](https://github.com/othneildrew/Best-README-Template) by Othneil Drew.
