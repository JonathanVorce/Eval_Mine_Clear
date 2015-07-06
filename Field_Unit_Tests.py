import unittest
import pdb
from Field import Field

class FieldTest(unittest.TestCase):

    def test_Init_Empty(self):
        _file = open('Unit_Tests\\Fields\\Field_Empty.txt')
        _field = Field(_file)
        _file.close()

        self.assertEqual(_field.n_mines,0)

        self.assertEqual(len(_field.mines),0)

        self.assertEqual(_field.n_col,0)
        self.assertEqual(_field.n_row,0)

        self.assertEqual(_field.center_x,0)
        self.assertEqual(_field.center_y,0)

    def test_Init_Alpha(self):
        _file = open('Unit_Tests\\Fields\\Field_Alpha.txt')
        _field = Field(_file)
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
        _file = open('Unit_Tests\\Fields\\Field_3x3_Bottom_Row.txt')
        _field = Field(_file)
        _file.close()

        self.assertEqual(_field.n_mines,3)

        self.assertEqual(_field.mines[(0,2)],ord('a'))
        self.assertEqual(_field.mines[(1,2)],ord('a'))
        self.assertEqual(_field.mines[(2,2)],ord('a'))

        self.assertEqual(_field.n_col,3)
        self.assertEqual(_field.n_row,3)

        self.assertEqual(_field.center_x,1)
        self.assertEqual(_field.center_y,1)
        
    def test_Init_Bottom_Justified(self):        
        _file = open('Unit_Tests\\Fields\\Field_3x3_Right_Col.txt')
        _field = Field(_file)
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
        _file = open('Unit_Tests\\Fields\\Field_3x3_Ragged_Diagonal.txt')
        _field = Field(_file)
        _file.close()

        self.assertEqual(_field.n_mines,3)

        self.assertEqual(_field.mines[(0,0)],ord('a'))
        self.assertEqual(_field.mines[(1,1)],ord('a'))
        self.assertEqual(_field.mines[(2,2)],ord('a'))

        self.assertEqual(_field.n_col,3)
        self.assertEqual(_field.n_row,3)

        self.assertEqual(_field.center_x,1)
        self.assertEqual(_field.center_y,1)

    def test_Trim_Edges(self):
        _file = open('Unit_Tests\\Fields\\Field_3x3_Needs_A_Trim.txt')
        _field = Field(_file)
        _file.close()

        self.assertEqual(_field.n_col,13)
        self.assertEqual(_field.n_row,9)
        
        _field.Trim_Edges()

        self.assertEqual(_field.n_col,5)
        self.assertEqual(_field.n_row,5)

        self.assertEqual(_field.mines[(0,0)],ord('a'))
        self.assertEqual(_field.mines[(1,1)],ord('a'))
        self.assertEqual(_field.mines[(2,2)],ord('a'))

    def test_Fall_From_A(self):
        _file = open('Unit_Tests\\Fields\\Field_Upper_a.txt')
        _field = Field(_file)
        self.assertFalse(_field.Fall())
        self.assertEqual(_field.mines[(0,0)], ord('z'))
        _file.close()
        
    def test_Fall_From_a(self):
        _file = open('Unit_Tests\\Fields\\Field_Lower_a.txt')
        _field = Field(_file)
        self.assertTrue(_field.Fall())
        self.assertEqual(_field.mines[(0,0)], ord('*'))
        _file.close()
    
# end class FieldTest

if __name__ == '__main__':
    unittest.main()