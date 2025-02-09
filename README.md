# Chess with AI
A single player chess game where the user (who plays as white) verses the computer AI (playing as black). 

## About Project
This project was the final project for my Principles of Programming course.
We were provided with a prompt to create a chess game with the following conditions: 
- Single player capabilities where the user always plays as white and the computer always plays as black. 
- From a pre-existing file, the program must read the piece locations and be able to create a board from them.
- Pieces include the king and an unlimited amount of placeable bishops for each side. 
- Pieces can be placed anywhere on the board to start, and are not confined to their usual chess starting positions. 

Because the course work was completed under a GitHub classroom, version control history is not available - but the code itself it viewable in this repository. 

## About AI
While the assignment allowed for the submission of a random AI, I decided to create a more complex AI which prioritizes moves to the AI's benefit.

First the AI simulates all possible legal moves for its side and stores them in a list. 
Then, it identifies the value of different moves {'checkmate': 4, 'check': 3, 'capture': 2, 'valid': 1}. 
Finally, it prioritizes its next move based on that of the highest value. 
