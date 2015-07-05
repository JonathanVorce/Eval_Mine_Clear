import pdb

_SCRIPT_FILE_DELIMITER = ' '

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
            _new_command = _line.strip('\n\r ').split(_SCRIPT_FILE_DELIMITER)
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