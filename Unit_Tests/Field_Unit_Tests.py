import unittest
import pdb
import sys
import os.path
_CURRENT_FILE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import Field

###########################################################
# Unit test the Field class functions
#
# Field.Init()
# Field.Get_N_Mines()
# Field.Adjust_Mine_Coordinates()
# Field.Trim_Edges()
# Field.Fall()
###########################################################

class FieldTest(unittest.TestCase):

    def test_Init_Empty(self):
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_Empty.txt')
        _field = Field.Field(_file)
        _file.close()

        self.assertEqual(_field.n_mines,0)

        self.assertEqual(len(_field.mines),0)

        self.assertEqual(_field.n_col,0)
        self.assertEqual(_field.n_row,0)

        self.assertEqual(_field.center_x,0)
        self.assertEqual(_field.center_y,0)

    def test_Init_Alpha(self):
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_Alpha.txt')
        _field = Field.Field(_file)
        _file.close()

        self.assertEqual(_field.n_mines,4)

        self.assertEqual(_field.mines[(0,0)],ord('a'))
        self.assertEqual(_field.mines[(2,0)],ord('a'))
        self.assertEqual(_field.mines[(0,2)],ord('a'))
        self.assertEqual(_field.mines[(2,2)],ord('a'))

        self.assertEqual(_field.n_col,3)
        self.assertEqual(_field.n_row,3)

        self.assertEqual(_field.center_x,1)
        self.assertEqual(_field.center_y,1)
        
    def test_Init_Bottom_Justified(self):
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_3x3_Bottom_Row.txt')
        _field = Field.Field(_file)
        _file.close()

        self.assertEqual(_field.n_mines,3)

        self.assertEqual(_field.mines[(0,2)],ord('a'))
        self.assertEqual(_field.mines[(1,2)],ord('a'))
        self.assertEqual(_field.mines[(2,2)],ord('a'))

        self.assertEqual(_field.n_col,3)
        self.assertEqual(_field.n_row,3)

        self.assertEqual(_field.center_x,1)
        self.assertEqual(_field.center_y,1)
        
    def test_Init_Right_Justified(self):        
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_3x3_Right_Col.txt')
        _field = Field.Field(_file)
        _file.close()

        self.assertEqual(_field.n_mines,3)

        self.assertEqual(_field.mines[(2,0)],ord('a'))
        self.assertEqual(_field.mines[(2,1)],ord('a'))
        self.assertEqual(_field.mines[(2,2)],ord('a'))

        self.assertEqual(_field.n_col,3)
        self.assertEqual(_field.n_row,3)

        self.assertEqual(_field.center_x,1)
        self.assertEqual(_field.center_y,1)

    def test_Init_Ragged_Diagonal(self):        
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_3x3_Ragged_Diagonal.txt')
        _field = Field.Field(_file)
        _file.close()

        self.assertEqual(_field.n_mines,3)

        self.assertEqual(_field.mines[(0,0)],ord('a'))
        self.assertEqual(_field.mines[(1,1)],ord('a'))
        self.assertEqual(_field.mines[(2,2)],ord('a'))

        self.assertEqual(_field.n_col,3)
        self.assertEqual(_field.n_row,3)

        self.assertEqual(_field.center_x,1)
        self.assertEqual(_field.center_y,1)

    def test_Get_N_Mines_Zero(self):
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_Empty.txt')
        _field = Field.Field(_file)
        _file.close()
        
        self.assertEqual(_field.Get_N_Mines(),0)

    def test_Get_N_Mines_Nine(self):
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_3x3_Full_Mines.txt')
        _field = Field.Field(_file)
        _file.close()
        
        self.assertEqual(_field.Get_N_Mines(),9)

    def test_Adjust_Mine_Coordinates_zero(self):
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_Alpha.txt')
        _field = Field.Field(_file)
        _file.close()

        _field.Adjust_Mine_Coordinates(0,0)

        self.assertTrue(_field.mines.__contains__((0,0)))
        self.assertTrue(_field.mines.__contains__((2,0)))
        self.assertTrue(_field.mines.__contains__((0,2)))
        self.assertTrue(_field.mines.__contains__((2,2)))

    def test_Adjust_Mine_Coordinates_plus_one_x_plus_one_y(self):
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_Alpha.txt')
        _field = Field.Field(_file)
        _file.close()

        _field.Adjust_Mine_Coordinates(1,1)

        self.assertTrue(_field.mines.__contains__((0+1,0+1)))
        self.assertTrue(_field.mines.__contains__((2+1,0+1)))
        self.assertTrue(_field.mines.__contains__((0+1,2+1)))
        self.assertTrue(_field.mines.__contains__((2+1,2+1)))

    def test_Adjust_Mine_Coordinates_minus_one_x_minus_one_y(self):
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_Alpha.txt')
        _field = Field.Field(_file)
        _file.close()

        _field.Adjust_Mine_Coordinates(-1,-1)

        self.assertTrue(_field.mines.__contains__((0-1,0-1)))
        self.assertTrue(_field.mines.__contains__((2-1,0-1)))
        self.assertTrue(_field.mines.__contains__((0-1,2-1)))
        self.assertTrue(_field.mines.__contains__((2-1,2-1)))

    def test_Trim_Edges_Empty(self):
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_Empty.txt')
        _field = Field.Field(_file)
        _file.close()

        self.assertEqual(_field.n_col,0)
        self.assertEqual(_field.n_row,0)
        self.assertEqual(_field.Get_N_Mines(),0)
        
        _field.Trim_Edges()

        self.assertEqual(_field.n_col,1)
        self.assertEqual(_field.n_row,1)
        self.assertEqual(_field.Get_N_Mines(),0)

        self.assertEqual(_field.center_x,0)
        self.assertEqual(_field.center_y,0)

    def test_Trim_Edges_3x3_No_Mines(self):
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_3x3_No_Mines.txt')
        _field = Field.Field(_file)
        _file.close()

        self.assertEqual(_field.n_col,3)
        self.assertEqual(_field.n_row,3)
        self.assertEqual(_field.Get_N_Mines(),0)
        
        _field.Trim_Edges()

        self.assertEqual(_field.n_col,1)
        self.assertEqual(_field.n_row,1)
        self.assertEqual(_field.Get_N_Mines(),0)

        self.assertEqual(_field.center_x,0)
        self.assertEqual(_field.center_y,0)

    def test_Trim_Edges_3x3_Needs_A_Trim(self):
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_3x3_Needs_A_Trim.txt')
        _field = Field.Field(_file)
        _file.close()

        self.assertEqual(_field.n_col,13)
        self.assertEqual(_field.n_row,9)

        _field.Trim_Edges()

        self.assertEqual(_field.n_col,5)
        self.assertEqual(_field.n_row,5)

        self.assertEqual(_field.mines[(0,0)],ord('a'))
        self.assertEqual(_field.mines[(1,1)],ord('a'))
        self.assertEqual(_field.mines[(2,2)],ord('a'))

        self.assertEqual(_field.center_x,2)
        self.assertEqual(_field.center_y,2)

    def test_Fall_From_Upper_A(self):
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_Upper_A.txt')
        _field = Field.Field(_file)
        self.assertFalse(_field.Fall())
        self.assertEqual(_field.mines[(0,0)], ord('z'))
        _file.close()
        
    def test_Fall_From_Lower_a(self):
        _file = open(_CURRENT_FILE_DIR_PATH + '\\Fields\\Field_Lower_a.txt')
        _field = Field.Field(_file)
        self.assertTrue(_field.Fall())
        self.assertEqual(_field.mines[(0,0)], ord('*'))
        _file.close()
    
# end class FieldTest

if __name__ == '__main__':
    unittest.main()