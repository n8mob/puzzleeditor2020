# puzzleeditor2020
A web application for editing JSON puzzle files for the MAGiE game

## [/puzzles](puzzles) is the main application.
The basic data model is pretty simple.
- A Menu is a list of Categories.
- A Category is a list of Levels.
- And a Level is a list of Puzzles.

You can look at [puzzles/models.py](puzzles/models.py), there's a bit of kruft in there.

## Menu UI
1. Which menu to use is kind of baked into the game.

   In the [Python version of the game](https://github.com/n8mob/MAGiEpy/blob/main/__main__.py), the full URL to the menu is provided as a command-line argument to the game.

2. After that, the user is presented with a list of categories.  They select one.
3. Then they are shown a list of levels.  They select one.

After that, the game just presents each puzzle in the level. One after then other.


## Clients
The service was made to drive a game developed in Unity that is no longer available in the app stores.

I have a partially built [Python command-line version](https://github.com/n8mob/MAGiEpy/) of the game.

And I recently started a React application, but I haven't published that code yet.
