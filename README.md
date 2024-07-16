# puzzleeditor2020
A web application for editing JSON puzzle files for the MAGiE game

## [/puzzles](puzzles) is the main application.
The basic data model is pretty simple.
- A Menu is a list of Categories.
- A Category is a list of Levels.
- And a Level is a list of Puzzles.

You can look at [puzzles/models.py](puzzles/models.py), there's a bit of kruft in there.

## Clients
The service was made to drive a game developed in Unity that is no longer available in the app stores.

I have a partially built [Python command-line version](https://github.com/n8mob/MAGiEpy/) of the game.

And I recently started a React application, but I haven't published that code yet.
