import itertools
import matplotlib.pyplot as plt
import numpy as np
import random

HIGHT = 6
WIDTH = 7
WINNING_NUMBER = 4

def move_still_possible(S):
    return not (S[S==0].size == 0)

# Return all column indices of columns
# in which there exists a free entry.
def column_with_empty_entries(S):
    return np.where(np.any(S==0, axis=0))[0]

def move_at_random(S, p):
    randomColumnIdx = random.choice(column_with_empty_entries(S))

    # Find the lowest entry (in terms of the board) of the random column,
    # s.t. this entry is still free.
    rowIdx = np.argmax(np.where(S. T[randomColumnIdx]==0))

    # Insert the player's token into the board.
    S[rowIdx,randomColumnIdx] = p
    return (S, rowIdx, randomColumnIdx)

# Returns true iff. the last move by player 'p' at ('lastMoveRow','lastMoveCol') was a winning move.
def move_was_winning_move(S, p, lastMoveRow, lastMoveCol):
    # Each of the following cases counts the number of contiguous disks
    # player 'p' has set, starting from position ('lastMoveRow', 'lastMoveCol').
    # If there are at least WINNING_NUMBER many contiguous disks, player p has won.

    # Vertical check
    diskCounter = 1
    for i in range(1, WINNING_NUMBER):
        if lastMoveRow+i < HIGHT and S[lastMoveRow+i,lastMoveCol] == p:
            diskCounter += 1
        else:
            break

    for i in range(1, WINNING_NUMBER):
        if lastMoveRow-i >= 0 and S[lastMoveRow-i,lastMoveCol] == p:
            diskCounter += 1
        else:
            break

    if diskCounter >= WINNING_NUMBER:
        return True
    ###########################################

    # Horizontal check
    diskCounter = 1
    for i in range(1, WINNING_NUMBER):
        if lastMoveCol+i < WIDTH and S[lastMoveRow,lastMoveCol+i] == p:
            diskCounter += 1
        else:
            break

    for i in range(1, WINNING_NUMBER):
        if lastMoveCol-i >= 0 and S[lastMoveRow,lastMoveCol-i] == p:
            diskCounter += 1
        else:
            break

    if diskCounter >= WINNING_NUMBER:
        return True
    ###########################################

    # Diagonal check (bottom left to top right)
    diskCounter = 1
    for i in range(1, WINNING_NUMBER):
        if lastMoveRow+i < HIGHT and lastMoveCol-i >= 0 and S[lastMoveRow+i,lastMoveCol-i] == p:
            diskCounter += 1
        else:
            break

    for i in range(1, WINNING_NUMBER):
        if lastMoveRow-i >= 0 and lastMoveCol+i < WIDTH and S[lastMoveRow-i,lastMoveCol+i] == p:
            diskCounter += 1
        else:
            break

    if diskCounter >= WINNING_NUMBER:
        return True
    ###########################################

    # Diagonal check (top left to bottom right)
    diskCounter = 1
    for i in range(1, WINNING_NUMBER):
        if lastMoveRow+i < HIGHT and lastMoveCol+i < WIDTH and S[lastMoveRow+i,lastMoveCol+i] == p:
            diskCounter += 1
        else:
            break

    for i in range(1, WINNING_NUMBER):
        if lastMoveRow-i >= 0 and lastMoveCol-i >= 0 and S[lastMoveRow-i,lastMoveCol-i] == p:
            diskCounter += 1
        else:
            break

    if diskCounter >= WINNING_NUMBER:
        return True
    ###########################################

    return False



# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print (B)

# if __name__ == '__main__':
aggregate = np.zeros((6, 7), dtype=float)


def normalize(arr):
    # return arr / np.linalg.norm(arr)
    sum = np.sum(arr.flatten())
    arr /= sum
    return arr;

def run_game():
    global aggregate
    # initialize 6x7 connect four board
    gameState = np.zeros((HIGHT,WIDTH), dtype=int)

    # initialize player number, move counter
    player = 1
    mvcntr = 1

    # initialize flag that indicates win
    noWinnerYet = True

    while move_still_possible(gameState) and noWinnerYet:
        # get player symbol
        name = symbols[player]
        print ('%s moves' % name)

        # let player move at random
        gameState, lastMoveRow, lastMoveCol = move_at_random(gameState, player)

        # print current game state
        # print_game_state(gameState)
        
        # evaluate game state
        if move_was_winning_move(gameState, player, lastMoveRow, lastMoveCol):
            # print ('player %s wins after %d moves' % (name, mvcntr))
            noWinnerYet = False
            break;

        # switch player and increase move counter
        player *= -1
        mvcntr +=  1
    if (noWinnerYet == False):
        # print 'player', player
        # print 'gameState', gameState
        # print 'clipped', np.clip(gameState * player, 0, 1)
        aggregate = np.add(aggregate, np.clip(gameState * player, 0, 1))
    # if noWinnerYet:
    #     print ('game ended in a draw') 

for i in range(10000):
    run_game()

np.set_printoptions(formatter={'float': lambda x: "{0:0.4f}".format(x)})


def plot_confusion_matrix(cm):
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('confusion matrix');
    plt.colorbar()
    plt.yticks(np.arange(6), ['0', '1', '2', '3', '4', '5', '6'], rotation=90)
    plt.xticks(np.arange(7), ['0', '1', '2', '3', '4', '5', '6', '7'])

    fmt = '.4f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    
    
print aggregate
norm = normalize(aggregate)

plot_confusion_matrix(norm)
plt.show();
