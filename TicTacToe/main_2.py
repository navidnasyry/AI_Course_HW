
from copy import deepcopy
from pprint import pprint
from time import sleep




class Game:
    def __init__(self, dim) -> None:
        self.dim = dim

    def to_move(self, state):
        num_of_G = 0
        num_of_R = 0
        for row in state:
            num_of_G += row.count('G')
            num_of_R += row.count('R')
        if num_of_G <= num_of_R:
            return 'G'
        return 'R'

    def is_terminal(self, state):
        counter = 0
        for row in state:
            if row.count('_') == 0:
                counter += 1
        if counter >= self.dim : 
            return True


        for y in range(self.dim):
            for x in range(1, self.dim - 1):
                if state[y][x] == state[y][x-1] == state[y][x+1]:
                    if state[y][x] != '_':
                        return True
           

        for x in range(self.dim):
            for y in range(1, self.dim - 1):
                if state[y][x] == state[y-1][x] == state[y+1][x]:
                    if state[y][x] != '_':
                        return True
            
        for y in range(1, self.dim - 1):
            for x in range(1, self.dim - 1):
                if state[y][x] == state[y-1][x-1] == state[y+1][x+1] or state[y][x] == state[y-1][x+1] == state[y+1][x-1]:
                    if state[y][x] != '_':
                        return True
        return False



    def actions(self, state):
        all_actions = []
        for y in range(0, self.dim):
            for x in range(0, self.dim):
                if state[y][x] == '_' : 
                    new_act = (y, x)
                    all_actions.append(new_act)
        return all_actions
        

    def result(self, state, action, player):
        state[action[0]][action[1]] = player

        return state


    def utility(self, state, player):#player = 'G' or player = 'R'


        for y in range(self.dim):
            for x in range(1, self.dim - 1):
                if state[y][x] == state[y][x-1] == state[y][x+1]:
                    if state[y][x] != '_':
                        if state[y][x] == player: 
                            return -10
                        else:
                            return +10

           

        for x in range(self.dim):
            for y in range(1, self.dim - 1):
                if state[y][x] == state[y-1][x] == state[y+1][x]:
                    if state[y][x] != '_':
                        if state[y][x] == player: 
                            return -10
                        else:
                            return +10

            
        for y in range(1, self.dim - 1):
            for x in range(1, self.dim - 1):
                if state[y][x] == state[y-1][x-1] == state[y+1][x+1] or state[y][x] == state[y-1][x+1] == state[y+1][x-1]:
                    if state[y][x] != '_':
                        if state[y][x] == player: 
                            return -10
                        else:
                            return +10

        return 0


def MaxValue(game, state, player, alpha, beta):
    p = game.to_move(state)
    if game.is_terminal(state):
        return game.utility(state, player), None
    v = float('-inf')
    for a in game.actions(state):
        state_copy = deepcopy(state)
        v2, a2 = MinValue(game, game.result(state_copy, a, p), player, alpha , beta)
        if v2 > v:
            v, move = v2, a
            alpha = max(alpha, v)  
        if v >= beta : 
            return v, move
    return v, move

def MinValue(game, state, player, alpha, beta):
    p = game.to_move(state)
    if game.is_terminal(state):
        return game.utility(state, player), None
    v = float('inf')
    for a in game.actions(state):
        state_copy = deepcopy(state)
        v2, a2 = MaxValue(game, game.result(state_copy, a, p), player, alpha, beta)
        if v2 < v:
            v, move = v2, a   
            beta = min(beta, v)
        if v <= alpha:
            return v, move 
    return v, move




def AlphaBetaSearch(game, state):
    player = game.to_move(state)
    value, move = MaxValue(game, state, player, float('-inf'), float('inf'))
    return move


def GetInputFromUser(state):
    index_list = []
    choices_index = 0
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] == '_':
                print(str(choices_index) , end= ' ')
                index_list.append((i, j))
                choices_index += 1
            else:
                print(state[i][j] , end= ' ')
        print()

    while True:
        selected = int(input("Enter You Choice : "))
        if selected >= 0 and selected < choices_index : 
            return index_list[selected]
        else:
            print("Input Not Valid.")
            
def PrintMap(state, dim):
    for i in range(dim):
        for j in range(dim):
            print(str(state[i][j]) , end= ' ')
        print()


def main():
    
    
    game_mode = input("Enter game Mode (1 => user(R) & computer(G) | 2 => computer(R) & computer(G)) : ")
    dimention = int(input("Enter Your Map Dimention : "))
    #state = [['_'] * dimention] * dimention #:(((
    state = []
    for i in range(dimention):
        row = []
        for j in range(dimention):
            row.append('_')
        state.append(row)
    
    game = Game(dim= dimention)

    if game_mode == '1':
        while True:
            move = AlphaBetaSearch(game, state)
            state[move[0]][move[1]] = 'G'
            sleep(1)
            print("After Player G Action : ")
            print('Move = ' , move)
            PrintMap(state, dimention)

            if game.is_terminal(state):
                if game.utility(state, 'G') > 0:
                    print("Player G WIN !!!!!!!!!!")
                    return
                else:
                    print("Finish...There is not Winner ...:(")
                    return

            print("\nNow your turn : ")
            move = GetInputFromUser(state)
            state[move[0]][move[1]] = 'R'
            print("After Player R Action : ")
            print('Move = ' , move)
            PrintMap(state, dimention)

            if game.is_terminal(state):
                if game.utility(state, 'R') > 0:
                    print("Player R WIN !!!!!!!!!!")
                    return
                else:
                    print("Finish...There is not Winner ...:(")
                    return



        

    elif game_mode == '2':
        while True:
                
            move = AlphaBetaSearch(game, state)
            state[move[0]][move[1]] = 'G'
            sleep(1)
            print("After Player G Action : ")
            print('Move = ' , move)
            PrintMap(state, dimention)

            if game.is_terminal(state):
                if game.utility(state, 'G') > 0:
                    print("Player G WIN !!!!!!!!!!")
                    return
                else:
                    print("Finish...There is not Winner ...:(")
                    return

            move = AlphaBetaSearch(game, state)
            state[move[0]][move[1]] = 'R'
            sleep(1)
            print("After Player R Action : ")
            print('Move = ' , move)
            PrintMap(state, dimention)

            if game.is_terminal(state):
                if game.utility(state, 'R') > 0:
                    print("Player R WIN !!!!!!!!!!")
                    return
                else:
                    print("Finish...There is not Winner ...:(")
                    return

    else:
        print("Input Not Valid !!")

    return


if __name__ == "__main__":
    main()
