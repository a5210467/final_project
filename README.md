
# Final_project

After Download the all file.

File connect4_final.py is the running file.

use python3 connect4_final to run the file.

First you need to set the table size. The stardand size is 6*7 which means 6 rows and 7 columns. After that you have 4 option to play the game. you can see the message print from the terminal.

The additional rule is here. For each player there has 15% chance to drop the dice and go to next round.

The game ends when there is a 4-in-a-row or column or diaginal or it is a stalemate.

I am using the MCTS for implement the AI. I still not implement the easy AI.

Update 03/12/2022 I am already finish the easy AI. 

https://github.com/KeithGalli/Connect4-Python is a reference for me to implement the rule and logic.
https://github.com/floriangardin/connect4-mcts/blob/master/main.py is also a reference for me to implement the AI

MCTS chapter in class is also a reference for me. I implment the Node based on that.

After you run the program. first the AI will search for 800 times for initial and then based on your move to learn more.

For playing the game AI will automatically drop the dice. For you. you need enter the corresponding column for drop the dice to continue playing. You can only enter numbers between the column size otherwise it will throw a exception.


Update:
For NN network. I use the code example in the class to train the NN network.

https://colab.research.google.com/drive/1QF8IJHlZ597esIU-vmW7u9KARhyXIjOY?authuser=1#scrollTo=iD67tKPuMaTr is the link for me to implement the NN network.

For NN network. Use the NN_Connect4.ipynb note book file. execute the code from the begining to end. until you find a function called play_it. that's the function you can play with AI. I use Minimax tree struction but with limit depth to limit the time.

For function test_hundred_times you can see the result for 100 simulation games that AI against simple AI.