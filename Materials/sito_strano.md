
[Link](http://web.archive.org/web/20041012023358/http://ssel.vub.ac.be/Members/LucGoossens/quarto/quartotext.htm)

Quarto

 

you can play the game here

 

The game.

 

Quarto is played an a 4 by 4 board. There are 16 pieces. Pieces are either black or white, small or tall, round or square, and solid or hollow.

The goal of the game is to have four pieces on a row (horizontally, vertically or diagonally) such that they all have one of the four properties in common, e.g. four tall pieces.

An additional twist that has a major impact on the game’s complexity, is that players do not in turn pick a piece and put it on the board. Instead, the piece that one player must place on the board is chosen by its opponent.

The game thus starts with one of the players choosing a piece and giving it to his opponent. The opponent puts it on the board and then chooses a piece to be put next.

 

Strategy.

 

Because both players do not have their own pieces (as in chess, checkers, qubic, etc.) timing is everything. If the board is full of opportunities to make a quarto for you, it is so as well for your opponent in the next round. Conversely, if there is no way your opponent can make a quarto in his round, there is little chance that you will be able to do so in the next.

 
Search space

 

For the first move (i.e. picking the initial piece) there are 16 possibilities. In the next move this piece can be put on 16 places and one of the remaining 15 pieces can be chosen. An upper limit for the total search space is thus

16. (16.15).(15.14). … . (2.1).1 = (16!)2 = 4.4e26

The actual number is smaller because it is possible to win before the board is full. The number of these early wins is however so small when compared with the number of draw games that the upper limit is a very good estimate.

This is an enormous number. Supposing that checking a board configuration can be done in a single machine cycle. A full naïve search would on a 500 MHz computer require … 280 billion years!!

 

Fortunately there is an algorithm named minimax search that can reduce this number drastically. Without getting into details the idea is that if one of your search branches would be found to be a win for you, there is obviously no need to examine any alternatives (it doesn’t matter if there is an even faster win in another branch). A bit more subtle is the case where your best branch so far is a draw. In that case you can stop searching the alternatives as soon as it is clear that they will not be better than draw, i.e. as soon as one of their subbranches evaluates to draw or lose.

 

In practice it takes approximately 30 million board evaluations to make a decision in case of 5 pieces on the board (instead of 11.(10!)2 = 1.4e14) and this number is more or less multiplied by a factor ten for each extra level of search depth. A search for a board with two pieces placed (a 2 + 1 configuration) e.g. requires on average 30 billion board evaluations.

 

In the summer of ‘98 deciding a 2 + 1 board on an avarage PC required several hours of computing. Given that, after taking symmetries into account, there are only 4 different 1 + 1 board configurations, it was soon discovered that all of them have a 2 + 1 continuation that evaluates to draw. This implies that a player that has to place the first piece can not win against an opponent that plays perfectly.

Next, we looked if it was possible to win with the right 2 + 1 configuration. Due to symmetries there are only 336 different such configurations (see symmetries). For each of them we searched and found a 3 + 1 extension that evaluates to draw. This implies that a player that has to place the second piece can not win against an opponent that plays perfectly.

Consequently, if both players play perfectly they will always be able to force a draw. Quarto is thus in the end a very fancy version of … tic-tac-toe.

 

Next, it would be interesting to know what the deepest win is. With a little bit of testing we found a 4 + 1 win. If there are no 3 + 1 wins, it is useless to look for one if you are faced with a 3 + 1 configuration. In that case it is enough to look for a draw move (which will take on average 10 times less time). Additionally, it doesn’t matter what you do if you are faced with a 2 + 1 configuration.

 

In the summer of ‘99 we evaluated each of the 336.14.13 = 61 152 configurations to see if some of them were winning positions. None of them were. In the process we did find a great number of winning 4 + 1 configurations. (About one out of thousand checked 4 + 1 boards was winning.) This implies that in case your opponent does not play perfectly it is an advantage to play the fifth piece, i.e. let your opponent pick the starting piece.

 

Finally this means that, given the current speed of an average PC, it is even possible for a Java implementation of the game, to play perfectly within a reasonable amount of time. A 550 MHz PC running the Java version of the search algorithm can evaluate about 5 million boards per second. A 4 + 1 search (300 million boards) is thus a matter of minutes.

 

Given that evaluating a single 3 + 1 configuration on average requires 3 billion board evaluations, we checked in total ca. 200e12 boards. On a single PC running the Java version this would have required about 500 days. Using about 50 PC’s of varying speed and an optimised C version it took less than one month.

 
Symmetries

 

Naively there are 16 board configurations with zero pieces on the board, corresponding with the sixteen possible pieces your opponent could have chosen for you to put. In reality all of them are identical. The easiest way of seeing this is, is by mapping the pieces to bit strings of length four. The pieces are then

0000, 0001, 0010, 0011, …, 1111

The first bit represents the color, the second the size, the third roundness, the fourth solidness. Black is zero, white is one, tall is zero, small is one, and so on.

Given an arbitrary piece xxxx we can always reduce it to 0000 by toggling the appropriate bits. Toggling bits preserves quarto’s.

 

What about the number of places where we can put this piece. With a proper rotation or mirroring most of the board positions can be reduced to one of the four in the upper left corner (positions 0, 1 ,4 and 5). Position 4 can be mapped to 1 by mirroring over the diagonal. Additionally, position 5 can be mapped to 0 by a more complex operation mapping the center of the square to the corners and vice versa (see figure 1).

 

 

 

 

Figure 1

 

 

From the figure it is clear that this mapping as well preserves the rows, columns and diagonals of the square. So in the end there are only two different positions for the first placement: 0 and 1.

 

How many different choices are there for the second piece. Toggling any bits would change our 0000 piece again so this is no option anymore. We can however still change the order of the bits. For 0000 this will for sure make no difference. Taking this into account there are thus four different choices. A piece with one 1, one with two 1’s, one with three 1’s, and finally one with four 1’s. For each of these categories it doesn’t really matter which one we pick, e.g. : 0001, 0011, 0111 and 1111.

 

Suppose we had put our first piece on position 0, how many different choices are there for the second position. It seems there is only one board transformation that will not move position 0 and that preserves rows, columns and diagonals: mirroring over the down diagonal. This implies that there are 9 possibilities: 1, 2, 3, 5, 6, 7, 10, 11 and 15.

In case we had put our first piece on position 1, it seems that there is no such board transformation. This leaves us the full 15 remaining positions.

 

What about the third piece? All depends upon our choice of the first two.

For 0000 and 0001 the remaining pieces are

0010

0011

0100 = 0010 by switching bit 2 and 3

0101 = 0011 by switching bit 2 and 3

0110

0111

1000 = 0010 by switching bit 1 and 3

1001 = 0011 by switching bit 1 and 3

1010 = 0110 by switching bit 1 and 2

1011 = 0111 by switching bit 1 and 2

1100 = 0110 by switching bit 1 and 3

1101 = 0111 by switching bit 1 and 3

1110

1111

thus 6 pieces (again corresponding with 1, 2 or 3 ones in the remaining first 3 bits)

 

For 0000 and 0011 the remaining pieces are (we can switch 1 and 2 and/or 3 and 4)

0001 leads to 0000 0011 0001 = 0000 0001 0011

0010 = 0001 by switching bit 3 and 4

0100

0101

0110 = 0101 by 3 and 4

0111

1000 = 0100 by 1 and 2

1001 = 0101 by 1 and 2

1010 = 1001 by 3 and 4

1011 = 0111 by 1 and 2

1100

1101

1110 = 1101 by 3 and 4

1111

thus 6 pieces

 

For 0000 and 0111 the remaining pieces are (we can switch bits 2, 3 and 4)

0001 leads to 0000 0111 0001 = 0000 0001 0111

0010 = 0001

0011 leads to 0000 0111 0011 = 0000 0011 0111

0100 = 0001

0101 = 0011

0110 = 0011

1000

1001

1010 = 1001

1011

1100 = 1001

1101 = 1011

1110 = 1011

1111

thus 4 pieces

 

For 0000 and 1111 the remaining pieces are (we can switch any bits)

0001 leads to 0000 1111 0001 = 0000 0001 1111

0011 leads to 0000 1111 0011 = 0000 0011 1111

0111 leads to 0000 1111 0111 = 0000 0111 1111

thus 0 pieces

 

For 2 + 1 configurations this means

(9.6) + (9.6) + (9.4) + (9.0) + (15.6) + (15.6) + (15.4) + (15.0) = 336 configurations

instead of 16. (16.15). (15.14) = 806 400

 

And consequently for 3 +1 configurations

336.14.13 = 61 152 configurations

 

 

 
