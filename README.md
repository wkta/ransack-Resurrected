# Ravenous Caves: the game

<p align="center">
  <a href="https://discord.gg/SHdJhcWvQD">join us on Discord<br>
    <img alt="join us on Discord" src="https://img.shields.io/discord/876813074894561300.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2">
  </a>
</p>

## About

The project consists in a remake of old indie games (roguelike genre).
Our inspiration comes from a software
initially built with by pygame and authored by *Dan Allen*,
and also from a game name
"The enchanted cave" by *Dustin Auxier*.

Now we are using the `pyved-engine` + Python3.
The new project maintainer is [moonb3ndr](https://github.com/wkta).


## How to test the game?

**Important**: Our game depends on the `pyved_engine`:
a work-in-progress [game engine](https://github.com/gaudiatech/pyved-engine)

It also depends on libraries that are listen in the `requirements.txt` file.

To install all these dependencies it is recommended to proceed as follows:
1. download both ravenous caves, and *the custom game engine* on your computer.
The best option is to use git:
```shell
git clone https://github.com/wkta/ravenous-caves.git
git clone https://github.com/gaudiatech/pyved-engine.git
```
2. using the command line, navigate to the folder that contains ravenous caves.
3. setup a new virtual environment by typing `python -m venv venv`
4. activate the virtual environment, for example on windows: `venv\Scripts\activate.bat`
5. install all basic requirements by typing `pip install -r requirements.txt`
6. using the command line, navigate to the folder that contains the game engine.
7. install the engine within the current (still active) virtual environment. You can do that
by typing `pip install -e .` See pip documentation and "editable mode" installation if you wish to learn more.

## Copyright notice

The artwork and visual assets, which includes the contents of the assets/IMG/ folder, are covered by the CC Attribution 4.0 license in the root file CC.

Please note that this project include TrueType fonts under the internal/FONTS/ folder which are NOT covered by the CC License. These are:

Spinal Tap (http://www.rockbandfonts.com/), 
Devinne Swash, by Dieter Steffmann.
http://www.fontspace.com/dieter-steffmann/devinne-swash
Chancery Gothic and Courier.

Todo: either obtain permission to use these files or remove them from the current (derivative) repo.
