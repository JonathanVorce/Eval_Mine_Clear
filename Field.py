import pdb
import math
import sys

_FIELD_FILE_DELIMITER = ' '

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
            _new_row = _line.strip('\n\r ').split(_FIELD_FILE_DELIMITER)
            
            # Handle the case if there was no delimiter in the field file (e.g no spaces between each character)
            _temp = []
            for _item in _new_row:
                for _ch in _item:
                    _temp.extend([_ch])
            _new_row = _temp
            
            _len = len(_new_row)
            
            # Set the number of columns
            if _len > self.n_col:
                self.n_col = _len

            # Increment total number of mines
            _n = _new_row.count('.')        # count "number of empty spaces"
            self.n_mines += ( _len - _n )   # len - "number of empty spaces" = num mines on this row

            # If there are mines, map the coordinates of the mines
            if _len - _n != 0:
                for _j, _ch in enumerate(_new_row):
                    if _ch != '.':
                        self.mines[(_j,_i)] = ord(_ch)
                
        #end for loop
        
        if ((self.n_col and self.n_col % 2 == 0) or (self.n_row and self.n_row % 2 == 0)):
            sys.exit('\n ** ERROR: The Field provided does not have a center. It has either on even number of rows or columns.')
            
        # Find the center of the field (this is where own ship is defaulted to)
        self.center_x = math.floor(self.n_col / 2)
        self.center_y = math.floor(self.n_row / 2)

    # Return Number of mines in field
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
        if self.n_mines == 0:
            self.n_row = 1
            self.n_col = 1
            self.center_x = 0
            self.center_y = 0

        else:
            _min_col, _max_col = self.Min_Max_Column_With_Mine()
            _min_row, _max_row = self.Min_Max_Row_With_Mine()

            _left_margin = _min_col
            _right_margin = (self.n_col - 1) - _max_col
            _top_margin = _min_row
            _bottom_margin = (self.n_row - 1) - _max_row

            _delta_x = 0
            _delta_y = 0
           
            # We can only trim if we trim from both top and bottom; otherwise we mess up where the center is.
            if _top_margin and _bottom_margin:

                # If the top and bottom margins are not equal we need to take the magnitude of the 
                # smaller margin off the top and bottom. 
                _min = min(_top_margin,_bottom_margin)
                self.n_row -= _min * 2
                _delta_y = _min
                
            # We can only trim if we trim from both sides (left and right); otherwise we mess up where the center is.
            if _left_margin and _right_margin:

                # If the left and right margins are not equal we need to take the magnitude of the
                # smaller margin off the left and right. 
                _min = min(_left_margin,_right_margin)
                self.n_col -= _min * 2
                _delta_x = _min

            # Move the coordinates of the mines for any space taken from the top or the left side       
            self.Adjust_Mine_Coordinates(_delta_x * -1, _delta_y * -1)

            # Readjust the coordinates of the center 
            self.center_x = math.floor(self.n_col / 2)
            self.center_y = math.floor(self.n_row / 2) 

    # Retrieve from the dictionary the index of the 
    # min/max row with at least one mine
    def Min_Max_Row_With_Mine(self):
        if self.n_mines != 0:
            _mine_coordinates = sorted(self.mines)      # sort the keys from the dictionary
            
            _min_row = _mine_coordinates[0][1]
            _max_row = _mine_coordinates[0][1]
            
            for _x,_y in _mine_coordinates:
                if _y < _min_row:
                    _min_row = _y
                if _y > _max_row:
                    _max_row = _y
        else:
            _min_row = 0
            _max_row = 0
            
        return _min_row, _max_row 
    
    # Retrieve from the dictionary the index of the 
    # min/max column with at least one mine
    def Min_Max_Column_With_Mine(self):
        if self.n_mines != 0:
            _mine_coordinates = sorted(self.mines)      # sort the keys from the dictionary

            _min_col = _mine_coordinates[0][0]
            _max_col = _mine_coordinates[len(_mine_coordinates) - 1][0]
        else:
            _min_col = 0
            _max_col = 0
        return _min_col, _max_col       

    # Wrapper for all move functions
    # The move functions are sufficiently different that combining them 
    # would result in obfuscated code
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
        
        # We will need to adjust the coordinates of the mines if:
        # 1) we took any rows off the top
        # 2) we took any columns off the left side
        self.Adjust_Mine_Coordinates(_delta_x,_delta_y)
            
    def South(self):
        _min, _max = self.Min_Max_Row_With_Mine()
        
        # All mines need to move in the -y direction equal to the number of rows 
        # that can be removed from the top of the field.
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
        return _delta_y
        
    def North(self):
        _min, _max = self.Min_Max_Row_With_Mine()
        
        # The last mine is on the last row, so we have add 2 rows to the top
        # All mines need to move +2 in the y direction
        if _max == self.n_row - 1:
            self.center_y  += 1
            self.n_row += 2
            _delta_y = 2
        
        # The last mine is on the last row - 1, so we can "remove"
        # one row from the bottom and "add" a row to the top.
        # All mines need to move +1 in the y direction
        elif _max == self.n_row - 2:
            _delta_y = 1
            
        # The last mine is on the last row - 2, so we can trim two row off the bottom
        # All mines don't move
        elif _max <= self.n_row - 3:
            self.center_y  -= 1
            self.n_row -= 2
            _delta_y = 0
        return _delta_y

    def West(self):
        _min, _max = self.Min_Max_Column_With_Mine()
        
        # If the right most mine is in the last column, we need to "add" two columns to the West side.
        # All the mines need to be shifted to the right two x-coordinates.
        if _max == self.n_col - 1:
            self.center_x += 1
            self.n_col += 2
            _delta_x = 2
        
        # If the right most mine is in the 2nd to last column, we need to add a column to the West side and,
        # also remove one from the East side. So no change to the total number of columns.
        # All the mines need to be shifted to the right one x-coordinate.
        elif _max == self.n_col - 2:
            _delta_x = 1
            
        # If the right most mine is in the 3rd to last column or more, we need to remove two columns from the East side.
        # No change to the mines' x-coordinate.
        elif _max <= self.n_col - 3:
            self.center_x  -= 1
            self.n_col -= 2
            _delta_x = 0
        return _delta_x
        
    def East(self):
        _min, _max = self.Min_Max_Column_With_Mine()
        
        # All mines need to move in the -x direction equal to the number of rows 
        # that can be removed from the left side of the field.
        _delta_x = _min * -1
        
        if _min == 0:
            self.center_x  += 1
            self.n_col += 2

        elif _min >= 2:
            self.center_x  -= 1
            self.n_col -= 2
            _delta_x = -2
        return _delta_x
    
    # Decrement all mines, if a mine is currently == 'a' we will have passed it after we fall.
    def Fall(self):
        for _xy, _mine in self.mines.items():
            if _mine == ord('a'):
                self.passed_mines = True
                self.mines[_xy] = ord('*')
                self.mines[_xy] = ord('*')
            elif _mine == ord('A'):
                self.mines[_xy] = ord('z')
            else:
                self.mines[_xy] -= 1
                    
        return self.passed_mines

    # Fire a torpedo at each coordinate relative to center of the field. 
    # If a mine appears at a target coordinate delete it from the dictionary.
    def Detonate_Torpedo(self,coordinate):
        _x , _y = coordinate
        
        _target_x = self.center_x + _x
        _target_y = self.center_y + _y
        if (_target_x < 0) or (_target_y < 0) or \
           (_target_x >= self.n_col) or (_target_y >= self.n_row):
            return
            
        # Remove the mine if it is in the dictionary
        if self.mines.__contains__((_target_x,_target_y)):
            self.n_mines -= 1
            del self.mines[(_target_x,_target_y)]

    # Start at (0,0), if no mine appears at those coordinates print '.', otherwise print the value of the mine. 
    def Print(self):
        self.Trim_Edges()
        for _y in range(self.n_row):
            _str = ''
            for _x in range(self.n_col):
                if self.mines.__contains__((_x,_y)):
                    _str += chr(self.mines[(_x,_y)])
                else:
                    _str += '.'
            print(_str)

# end class Field