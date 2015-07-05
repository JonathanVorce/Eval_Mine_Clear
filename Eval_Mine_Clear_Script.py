from __future__ import print_function
import pdb
import math
import os.path
import sys
from Field  import Field
from Script import Script
from Score  import Score

###########################################################
# main - Mine Clearing Exercise Evaluator
###########################################################
def main():
    try:
        if len(sys.argv) != 3:
            sys.exit('\n ** ERROR: The script requires two inputs: <path to Field file> <path to Script file>.')

        if not os.path.isfile(sys.argv[1]):
            sys.exit('\n ** ERROR: The field file does not exist.')

        if not os.path.isfile(sys.argv[2]):
            sys.exit('\n ** ERROR: The script file does not exist.')

        _field_file  = open(sys.argv[1])
        _script_file = open(sys.argv[2])

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
        
        print()             # print an empty line
        input()             # wait for user input
    except:
        raise
# end main()   

if __name__ == '__main__' :
    main()
