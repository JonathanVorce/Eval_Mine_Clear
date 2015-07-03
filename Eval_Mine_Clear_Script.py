import pdb
import math

_SCORE_PER_MINE = 10
_SCORE_PER_SHOT = -5
_SCORE_PER_MOVE = -2
_MAX_MOVE_PENALTY_MULTIPLIER = -3
_MAX_SHOT_PENALTY_MULTIPLIER = -5
_FIELD_FILE_DELIMITER = ' '
_SCRIPT_FILE_DELIMITER = ' '

_FALLING = { 
    '.' : '.', 'a' : '*', 'b' : 'a', 'c' : 'b',
    'd' : 'c', 'e' : 'd', 'f' : 'e', 'g' : 'f',
    'h' : 'g', 'i' : 'h', 'j' : 'i', 'k' : 'j',
    'l' : 'k', 'm' : 'l', 'n' : 'm', 'o' : 'n',
    'p' : 'o', 'q' : 'p', 'r' : 'q', 's' : 'r',
    't' : 's', 'u' : 't', 'v' : 'u', 'w' : 'v',
    'x' : 'w', 'y' : 'x', 'z' : 'y', 'A' : 'z',
    'B' : 'A', 'C' : 'B', 'D' : 'C', 'E' : 'D',
    'F' : 'E', 'G' : 'F', 'H' : 'G', 'I' : 'H',
    'J' : 'I', 'K' : 'J', 'L' : 'K', 'M' : 'L',
    'N' : 'M', 'O' : 'N', 'P' : 'O', 'Q' : 'P',
    'R' : 'Q', 'S' : 'R', 'T' : 'S', 'U' : 'T',
    'V' : 'U', 'W' : 'V', 'X' : 'W', 'Y' : 'X',
    'Z' : 'Y'}	 

###########################################################    
# map of the mines locations and tracks center of field (own ship location) 
#
# NOTE: delimiter for field file can be specified by changing _FIELD_FILE_DELIMITER
###########################################################
class Field:
    def __init__(self,file):
        self.mines = {}
        self.n_mines = 0
        self.n_row = 0      # y-coordinates
        self.n_col = 0      # x-coordinates
        self.passed_mines = False
        self.center_x = 0
        self.center_y = 0

        _lines = file.readlines()
        self.n_row = len(_lines)
        for _i, _line in enumerate(_lines):
        
            # NOTE: delimiter for field file can be specified by changing _FIELD_FILE_DELIMITER
            _new_row = _line.strip('\n ').split(_FIELD_FILE_DELIMITER)
            _len = len(_new_row)
            
            if _len > self.n_col:
                self.n_col = _len

            _n = _new_row.count('.')
            self.n_mines += ( _len - _n )
            if _len - _n != 0:
                for _j, _cuboid in enumerate(_new_row):
                    if _cuboid != '.':
                        self.mines[(_j,_i)] = _cuboid
                
        
        # Find the center of the field (this is where own ship is defaulted to)
        self.center_x = math.floor(self.n_col / 2)
        self.center_y = math.floor(self.n_row / 2)
    
    def Get_N_Mines(self):
        return self.n_mines
    
    # Adjust the coordinates of the mines 
    def Adjust_Mine_Coordinates(self,delta_x,delta_y):
        if delta_x or delta_y:
            _new_mines_locations = {}
            for _xy, _mine in self.mines.items():
                _x = _xy[0]
                _y = _xy[1]
                _new_mines_locations[(_x + delta_x, _y + delta_y)] = _mine
            
            # Over write the mines with the new keys
            self.mines = _new_mines_locations
        
    # We should only print the minimum field size to show all mines and correctly
    # place the ship at the center of the field.
    def Trim_Edges(self):
        _min_col, _max_col = self.Min_Max_Column_With_Mine()
        _min_row, _max_row = self.Min_Max_Row_With_Mine()
        
        _left_margin = _min_col
        _right_margin = (self.n_col - 1) - _max_col
        _top_margin = _min_row
        _bottom_margin = (self.n_row - 1) - _max_row
        
        _delta_x = 0
        _delta_y = 0
        
        # We can only trim if we trim from both top and bottom; otherwise we mess up the where the center is.
        if _top_margin and _bottom_margin:
            if _top_margin == _bottom_margin:
                self.n_row -= _top_margin + _bottom_margin
                _delta_y = _top_margin
            else:
                
                # If the top and bottom margins are not equal we need to take the magnitude of the 
                # smaller margin off the top and bottom, but only if it is divisible by 2. 
                _min = min(_top_margin,_bottom_margin)
                if _min % 2 != 0:
                    _min -= 1
                self.n_row -= _min * 2
                _delta_y = _min
            
        # We can only trim if we trim from both sides; otherwise we mess up the where the center is.
        if _left_margin and _right_margin:
            if _left_margin == _right_margin:
                self.n_col -= _left_margin + _right_margin
                _delta_x = _left_margin
            else:
            
                # If the left and right margins are not equal we need to take the magnitude of the 
                # smaller margin off the left and right, but only if it is divisible by 2. 
                _min = min(_left_margin,_right_margin)
                if _min % 2 != 0:
                    _min -= 1
                self.n_col -= _min * 2
                _delta_x = _min
            
        # move the coordinates of the mines for any space taken from the top or the left side       
        self.Adjust_Mine_Coordinates(_delta_x * -1, _delta_y * -1)
        
        # readjust the coordinates of the center 
        self.center_x = math.floor(self.n_col / 2)
        self.center_y = math.floor(self.n_row / 2) 
        
    # Retrieves from the dictionary the index of the 
    # min/max row with at lease one mine
    def Min_Max_Row_With_Mine(self):
        # sort the keys from the dictionary
        _mine_coordinates = sorted(self.mines)
        _min_col = _mine_coordinates[0][1]
        _max_col = _mine_coordinates[0][1]
        for _x,_y in _mine_coordinates:
            if _y < _min_col:
                _min_col = _y
            if _y > _max_col:
                _max_col = _y
        return _min_col, _max_col 
    
    # Retrieves from the dictionary the index of the 
    # min/max column with at lease one mine
    def Min_Max_Column_With_Mine(self):
        # sort the keys from the dictionary
        _mine_coordinates = sorted(self.mines)
        _north_west_mine = _mine_coordinates[0]
        _south_east_mine = _mine_coordinates[len(_mine_coordinates) - 1]
        _min_row = _north_west_mine[0]
        _max_row = _south_east_mine[0]
        return _min_row, _max_row       
    
    # Wrapper for all command functions
    def Command(self,command):
        _functions = {
            'north' : self.Move,
            'south' : self.Move,
            'east'  : self.Move,
            'west'  : self.Move,
            ''      : self.Move, # Fall
            'alpha' : self.Fire,
            'beta'  : self.Fire,
            'gamma' : self.Fire,
            'delta' : self.Fire}

        _f = _functions[command]
        _f(command)
    
    # Wrapper for all move functions
    def Move(self,direction):
        _delta_x = 0
        _delta_y = 0
        if direction == 'north':
            _delta_y = self.North()
        elif direction == 'south':
            _delta_y = self.South()
        elif direction == 'east':
            _delta_x = self.East()
        elif direction == 'west':
            _delta_x = self.West()
        else:
            self.Fall()
            
        self.Adjust_Mine_Coordinates(_delta_x,_delta_y)
            
    def South(self):
        _min, _max = self.Min_Max_Row_With_Mine()
        _delta_y = _min * -1
        
        # The first mine is on row 0, so we have to add 2 rows to the bottom
        if _min == 0:
            self.center_y  += 1
            self.n_row += 2

        # The first mine is on row 2+, so we can trim 2 rows off the top
        elif _min >= 2:
            self.center_y  -= 1
            self.n_row -= 2
            _delta_y = -2
        return _delta_y     # We will need to adjust the coordinates of the mines if we took any rows off the top.
        
    def North(self):
        _min, _max = self.Min_Max_Row_With_Mine()
        
        # The last mine is on the last row, so we have add 2 rows to the top
        if _max == self.n_row - 1:
            self.center_y  += 1
            self.n_row += 2
            _delta_y = 2
        
        # The last mine is on the last row - 1, so we can "remove"
        # one row from the bottom and add one to the top
        elif _max == self.n_row - 2:
            _delta_y = 1
            
        # The last mine is on the last row - 2, so we can trim two row off the bottom
        elif _max <= self.n_row - 3:
            self.center_y  -= 1
            self.n_row -= 2
            _delta_y = 0
        return _delta_y
                                    
    def West(self):
        _min, _max = self.Min_Max_Column_With_Mine()
        
        if _max == self.n_col - 1:
            self.center_x += 1
            self.n_col += 2
            _delta_x = 2
        elif _max == self.n_col - 2:
            _delta_x = 1
        elif _max <= self.n_col - 3:
            self.center_x  -= 1
            self.n_col -= 2
            _delta_x = 0
        return _delta_x
        
    def East(self):
        _min, _max = self.Min_Max_Column_With_Mine()
        _delta_x = _min * -1
        
        if _min == 0:
            self.center_x  += 1
            self.n_col += 2

        elif _min >= 2:
            self.center_x  -= 1
            self.n_col -= 2
            _delta_x = -2
        return _delta_x
    
    # Increment all mines, if a mine is currently == 'a' we will have passed it after we fall.
    def Fall(self):
        for _xy, _mine in self.mines.items():
            if _mine == 'a':
                self.passed_mines = True
            self.mines[_xy] = _FALLING[_mine]
                    
        return self.passed_mines

    # Fire a torpedo at each coordinate relative to center of the field. 
    # If a mine appears at a target coordinate delete it from the dictionary.
    def Fire(self,pattern):
        _coordinates = {
            'alpha' : [(-1,-1),(-1, 1),( 1,-1),( 1, 1)],
            'beta'  : [(-1, 0),( 0,-1),( 0, 1),( 1, 0)],
            'gamma' : [(-1, 0),( 0, 0),( 1, 0)]        ,
            'delta' : [( 0,-1),( 0, 0),( 0, 1)]        }

        for _x, _y in _coordinates[pattern]:
            _target_x = self.center_x + _x
            _target_y = self.center_y + _y
            if (_target_x < 0) or (_target_y < 0) or \
               (_target_x >= self.n_col) or (_target_y >= self.n_row):
                continue
            
            # Remove the mine if it is in the dictionary
            if self.mines.__contains__((_target_x,_target_y)):
                self.n_mines -= 1
                del self.mines[(_target_x,_target_y)]
    
    # Start at (0,0), if no mine appears at those coordinates print '.', otherwise print the value of the mine. 
    def Print(self,show_own_ship=False):
        if self.n_mines:
            self.Trim_Edges()
            for _y in range(self.n_row):
                _str = ''
                for _x in range(self.n_col):
                        if show_own_ship and _x == self.center_x and _y == self.center_y:
                            _str += str(_x)
                        elif self.mines.__contains__((_x,_y)):
                            _str += self.mines[(_x,_y)]
                        else:
                            _str += '.'
                print(_str)
        else:
            print ('.')
# end class Field

###########################################################
# A list of instructions extracted from a supplied script file 
# NOTE: delimiter for script file can be specified by changing _SCRIPT_FILE_DELIMITER
###########################################################
class Script:
    def __init__(self,file):
        self.instructions = []
        self.n_steps = 0
        
        _lines = file.readlines()
        for _line in _lines:
        
            # NOTE: delimiter for script file can be specified by changing _SCRIPT_FILE_DELIMITER
            _new_command = _line.strip('\n').split(_SCRIPT_FILE_DELIMITER)
            self.instructions.append(_new_command)
            self.n_steps += 1
    
    # Return the number of steps (each step consists of an instruction with 1 or more commands)
    def Get_N_Steps(self):      
        return self.n_steps
        
    # Print the instruction (each instruction (or step) consists of 1 or more commands)
    def Print_Instruction(self,step):
        str = ''
        for _command in self.instructions[step-1]:
            str += _command + ' '
        print(str)
    
    # Pass the command(s) in the instruction to the function in the parameter list
    def Pass_Instruction_Into_Provided_Function(self,step,func):
        for _command in self.instructions[step-1]:
            func(_command)
# end class Script 

###########################################################
# class for tracking the score
#
# NOTE: the various multipliers can be modified as need: _SCORE_PER_MINE, _SCORE_PER_MOVE, _SCORE_PER_SHOT, _MAX_MOVE_PENALTY_MULTIPLIER, _MAX_SHOT_PENALTY_MULTIPLIER
###########################################################
class Score:
    def __init__(self,n_mines,n_steps):
        self.initial_mines = n_mines
        self.initial_steps = n_steps
        self.n_moves = 0
        self.n_shots = 0
        self.running_score = n_mines * _SCORE_PER_MINE
        self.max_num_of_moves_counted_as_penalty = self.initial_mines * _MAX_MOVE_PENALTY_MULTIPLIER / _SCORE_PER_MOVE
        self.max_num_of_shots_counted_as_penalty = self.initial_mines * _MAX_SHOT_PENALTY_MULTIPLIER / _SCORE_PER_SHOT

    # Track the score for each command executed
    def Tally_Score(self,command):
        if command in ['north','south','east','west']:
            if self.n_moves < self.max_num_of_moves_counted_as_penalty:
                self.running_score += _SCORE_PER_MOVE
            self.n_moves += 1
        elif command in ['alpha','beta','gamma','delta']:
            if self.n_shots < self.max_num_of_shots_counted_as_penalty:
                self.running_score += _SCORE_PER_SHOT
            self.n_shots += 1
	
    # Return the score 
    def Return_Score(self):
        return str(self.running_score)
# end class Score

###########################################################
# main - Mine Clearing Exercise Evaluator
###########################################################
def main():
    try:
        _input = input( '# NOTE: delimiter for field file can be specified by changing _FIELD_FILE_DELIMITER\n\n' + 
                        'Please enter (on one line) the paths to the following files: field sript:\n').split()
    
        _field_file  = open(_input[0])
        _script_file = open(_input[1])
    
        # Read each line from the field file and create a field object
        # Read each line from the script file and create a script object 
        _field  = Field(_field_file)
        _script = Script(_script_file)
        
        _n_steps = _script.Get_N_Steps()    
        _score = Score(_field.n_mines,_n_steps)
        
        #
        # Execute script
        #   Print step #
        #   print field
        #   print instruction(s)
        #   execute instructions 
        #   score instructions
        #   fall one space
        #   print field after instructions
        #   exit if done or if failed
        #
        _fail = False
        _n_steps_executed = 0
        for _step in range(1,_script.Get_N_Steps() + 1):
            
            # Print Step #
            print('Step ' + str(_step) + '\n')
            
            # Print field
            _field.Print()
            print()         # print an empty line
        
            # Print instructions
            _script.Print_Instruction(_step)
            print()         # print an empty line
            
            # Execute instructions
            _script.Pass_Instruction_Into_Provided_Function(_step,_field.Command)
            _n_steps_executed += 1 
            
            # Score instructions
            _script.Pass_Instruction_Into_Provided_Function(_step,_score.Tally_Score)
    
            # Fall through the field, if we pass a mine we have failed
            _fail = _field.Fall()  
            
            # Print the field after the instructions have been executed and we have fallen
            _field.Print()
            print()         # print an empty line
            
            if _fail:
                print('fail (' + str(0) +')')
                break
            elif _field.Get_N_Mines() == 0:
                if _n_steps_executed < _n_steps:
                    print('pass  (' + str(1) +')')
                else:
                    print('pass  (' + _score.Return_Score() +')')
                break
        # end for loop 
        
        if _field.Get_N_Mines() != 0 and not _fail:
            print('fail (' + str(0) +')')  
        
        print()
        input()
    except:
        raise
# end main()   

if __name__ == '__main__' :
    main()
