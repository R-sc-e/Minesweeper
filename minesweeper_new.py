import random

class Gameboard:
    def __init__(self, board_size, num_mines):
        self.length = board_size
        self.mines = num_mines
        self.board = ''
        for i in range(self.length):
            self.board += ('-'*self.length)
        self.display = ''
        self.grid_list = []
        for elem in range(pow(self.length,2)):
            x_coord = str(chr((elem%self.length)+65))
            y_coord = str(elem//self.length)
            self.grid_list.append(x_coord+y_coord)
        self.original_list = []
        for elem in range(pow(self.length,2)):
            x_coord = str(chr((elem%self.length)+65))
            y_coord = str(elem//self.length)
            self.original_list.append(x_coord+y_coord)
        self.checked_cells = []
        self.mine_coord = [] 
        self.game_state = False

    def __str__(self):
        for i in range(6):
            if i % 2 != 0:
                self.display += '  +'+('-'*self.length)+'+\n'
            elif i == 2:
                self.display += '  |'+' M:'+str("%02d"%self.mines)+' '*(self.length-5)+'|\n'
            elif i == 4:
                letter_coord = ''
                for index in range(self.length):
                    letter_coord += chr(index+65)
                self.display += '  |'+letter_coord+'|\n'
        for index in range(self.length):
            if self.length <= 10:
                self.display += ' '+str(index)+'|'+self.board[index*self.length:(index*self.length)+self.length]+'|\n'
            else:
                if index >= 10:
                    self.display += str("%02d"%index)+'|'+self.board[index*self.length:(index*self.length)+self.length]+'|\n'
                else:
                    self.display += ' '+str(index)+'|'+self.board[index*self.length:(index*self.length)+self.length]+'|\n'
        self.display += '  +'+('-'*self.length)+'+\n'
        return self.display

    def game_status(self):
        test_str = self.board
        if test_str.count('-') + test_str.count('F') == self.mines and test_str.count('O') != self.mines:
            self.game_state = False
            return 'Game won!'
        elif self.game_state == True:
            return 'Game in play, enter game choice:'
        else:
            self.game_state = False
            return 'Game lost! You hit a mine.'

    def get_cell(self, cell):
        if cell not in self.grid_list:
            return 'Error: cell doesn\'t exist!'
        cell_list = [cell[0],cell[1:]]
        index = ord(cell_list[0])-65+((self.length)*(int(cell_list[1])))
        return index

    def update_display(self):
        self.display = ''
        self.display = str(self)
        return self.display


    def flag(self, cell):
        if cell not in self.grid_list:
            return self.get_cell(cell)
        elif self.board[self.get_cell(cell)] != '-':
            print(self.update_display())
            return 'Error, can\'t flag this cell!\n'
        else:
            self.board = self.board[:self.get_cell(cell)] + 'F' + self.board[(self.get_cell(cell)+1):]
            return self.update_display()
        
    def unflag(self, cell):
        if cell not in self.grid_list:
            return self.get_cell(cell)
        elif self.board[self.get_cell(cell)] != 'F':
            print(self.display)
            print('Error, can\'t unflag this cell!\n')
        else: 
            self.board = self.board[:self.get_cell(cell)] + '-' + self.board[(self.get_cell(cell)+1):]
            return self.update_display()

    def start(self, cell):
        if self.board[self.get_cell(cell)] != '-':
            print(self.display)
            return 'Error, can\'t click this cell!\n'
        else:
            self.game_state = True
            index_of_cell = self.original_list.index(cell)
            updated_grid_list = self.grid_list
            updated_grid_list.remove(cell)
            updated_grid_list = [x for x in self.original_list if (x not in self.get_adjacent_cells(cell))]
            updated_grid_list.remove(cell)
            for mine in range(self.mines):
                coord = random.choice(updated_grid_list)
                self.mine_coord.append(coord)
            self.grid_list.insert(index_of_cell, cell)
            return self.click(cell)

    def get_adjacent_cells(self, cell):
        cell_list = [cell[0],cell[1:]]
        adjacent_cells = []
        index_of_cell = self.original_list.index(cell)
        if cell_list[1] == '0':
            if cell_list[0] == self.display[3*(5+self.length)+3]:
                adjacent_cells = [self.original_list[index_of_cell+1],self.original_list[index_of_cell+self.length],self.original_list[index_of_cell+self.length+1]]        
            elif cell_list[0] == self.display[3*(5+self.length)+3+self.length-1]:
                adjacent_cells = [self.original_list[index_of_cell-1],self.original_list[index_of_cell+self.length],self.original_list[index_of_cell+self.length-1]]
            else:
                adjacent_cells = [self.original_list[index_of_cell-1], self.original_list[index_of_cell+1]]
                for elem in range(3):
                    adjacent_cells.append(self.original_list[index_of_cell+self.length-1+elem])
        elif cell_list[1] == str(self.length-1):
            if cell_list[0] == self.display[3*(5+self.length)+3]:
                adjacent_cells = [self.original_list[index_of_cell-self.length],self.original_list[index_of_cell-self.length+1],self.original_list[index_of_cell+1]]                     
            elif cell_list[0] == self.display[3*(5+self.length)+3+self.length-1]:
                adjacent_cells = [self.original_list[index_of_cell-self.length],self.original_list[index_of_cell-self.length-1],self.original_list[index_of_cell-1]]            
            else:
                adjacent_cells = [self.original_list[index_of_cell-1], self.original_list[index_of_cell+1]]
                for elem in range(3):
                    adjacent_cells.append(self.original_list[index_of_cell-self.length-1+elem])      
        else:
            if cell_list[0] == self.display[3*(5+self.length)+3]:
                adjacent_cells = [self.original_list[index_of_cell+1]]
                for elem in range(2):
                    adjacent_cells.append(self.original_list[index_of_cell-self.length+elem])
                    adjacent_cells.append(self.original_list[index_of_cell+self.length+elem])
            elif cell_list[0] == self.display[3*(5+self.length)+3+self.length-1]:
                adjacent_cells = [self.original_list[index_of_cell-1]]
                for elem in range(2):
                    adjacent_cells.append(self.original_list[index_of_cell-self.length-elem])
                    adjacent_cells.append(self.original_list[index_of_cell+self.length-elem])
            else:
                adjacent_cells = [self.original_list[index_of_cell-1], self.original_list[index_of_cell+1]]
                for elem in range(3):
                    adjacent_cells.append(self.original_list[index_of_cell-self.length-1+elem])
                    adjacent_cells.append(self.original_list[index_of_cell+self.length-1+elem])
        return adjacent_cells

    def click(self,cell):
        if (cell in self.mine_coord):
            self.game_state = False
            for elem in self.mine_coord:
                self.board = self.board[:self.get_cell(elem)] + 'O' + self.board[(self.get_cell(elem)+1):]
            return self.update_display()
        self.checked_cells.append(cell)
        if self.board[self.get_cell(cell)] == '-':
            number = 0
            for elem in self.get_adjacent_cells(cell):
                    if (elem in self.mine_coord):
                        number += 1
            if number != 0:
                self.board = self.board[:self.get_cell(cell)] + str(number) + self.board[(self.get_cell(cell)+1):]
                return self.update_display()
            else:
                self.board = self.board[:self.get_cell(cell)] + ' ' + self.board[(self.get_cell(cell)+1):]
                for elem in [x for x in self.get_adjacent_cells(cell) if (x not in self.checked_cells)]:
                    self.click(elem)
                return self.update_display()


def game_function(grid, mines):
    game_choices = ['C','F','U']
    game = Gameboard(grid, mines)
    print(str(game),'Game choices:')
    while game.game_state == False:
        while True:
            print('Click cell: C','\nFlag cell: F','\nUnflag cell: U')
            user_choice = input('Enter game choice:')
            if user_choice in game_choices:
                break
            print('Error, choose game choice again:')
        user_coord = input('Enter coordinate:')
        if user_choice == 'F':
            print(game.flag(user_coord))
        elif user_choice == 'U':
            print(game.unflag(user_coord))
        elif user_choice == 'C':
            if user_coord not in game.grid_list:
                print(game.get_cell(user_coord),'\nError, choose game choice again:')
            else:
                print(game.start(user_coord),game.game_status())
    while game.game_state == True:
        while True:
            print('Click cell: C','\nFlag cell: F','\nUnflag cell: U')
            user_choice = input('Enter game choice:')
            if user_choice in game_choices:
                break
            print('Error, choose game choice again:')
        user_coord = input('Enter coordinate:')
        if user_choice == 'F':
            print(game.flag(user_coord), game.game_status())
        elif user_choice == 'U':
            print(game.unflag(user_coord), game.game_status())
        elif user_choice == 'C':
            if user_coord not in game.grid_list:
                print(game.get_cell(user_coord),'\nError, choose game choice again:')
            elif game.board[game.get_cell(user_coord)] != '-':
                print('Error: can\'t click this cell!')
            else:
                print(game.click(user_coord),str(game), game.game_status())

def game_mode(difficulty):
        difficulty_list = ['1','2','3','4','Easy','Medium','Hard','Custom','easy','medium','hard','custom']
        if difficulty not in difficulty_list:
            print('Error, choose game mode again:')
            difficulty = input('Enter difficulty:\n1) Easy\n2) Medium\n3) Hard\n4) Custom\n')
            game_mode(difficulty)
        else:
            if difficulty == '1' or difficulty == 'easy':
                print('Easy mode selected')
                game_function(9, 5)
            if difficulty == '4' or difficulty == 'custom':
                grid = int(input('Enter grid length: '))
                mines = int(input('Enter number of mines: '))
                if mines >= pow(grid, 2):
                    print('Error, too many mines!')
                else:
                    print('Custom mode selected')
                    game_function(grid, mines)
            if difficulty == '2' or difficulty == 'medium':
                print('Medium mode selected')
                game_function(16, 40)
            if difficulty == '3' or difficulty == 'hard':
                print('Hard mode selected')
                game_function(20, 99) 

while True:
    print('Welcome to a new game!')
    difficulty_list = ['1','2','3','4','easy','medium','hard','custom']
    difficulty = input('Enter difficulty:\n1) Easy\n2) Medium\n3) Hard\n4) Custom\n').lower()
    game_mode(difficulty)           
    while True:
        answer = str(input('Play again? (y/n): ')).lower()
        if answer in ('y', 'n', 'yes', 'no'):
            break
        print("Invalid input")
    if answer == 'y' or answer == 'yes':
        continue
    else:
        print("Goodbye")
        break


