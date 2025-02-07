# Chess with AI
Single player chess game (user v. computer AI) with move prioritizing AI. 

This project was the final project for my Principles of Programming course.
We were provided with a prompt to create a 1-player chess game with a functional opponent AI, the ability to read and write to the file, and interact as a player to be play
a chess game incorporating only bishops (of any amount per side) and a King. 

Because the course work was completed under a GitHub classroom, version control history is not available - but I have copied over the code. 

## About AI
My AI first simulates all possible moves, appending them to a list, and then assigns and prioritizes moves by in accordance with best strategy to win: 
{'checkmate': 4, 'check': 3, 'capture': 2, 'valid': 1} 
