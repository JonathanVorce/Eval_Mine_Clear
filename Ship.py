import pdb

###########################################################    
# definition of ship
#
# constructor requires:
#       a defined field class object <Field>
#       definitions for movements commands <dictionary>
#       definitions for fire pattern commands <dictionary>
#
# Supplied commands should take the form of:
#       # pattern name and a list of x/y offsets measured from ownship position
#       fire_commands = {
#           'fire_pattern1' : [(x1,y1),(x2,y2),(x2,y2), ...],
#           'fire_pattern2' : [(x1,y1),(x2,y2),(x2,y2), ...],
#            ...                                            }
#
#       # move name and a list of composite moves
#       # valid values are: 'north', 'south', 'east', 'west', ''
#       move_commands = {}
#           'NW' : [ 'north', 'west' ],
#           'NE' : [ 'north', 'east' ],
#            ...                         }
###########################################################
class Ship:
    def __init__(self,field_def,move_cmds={},fire_cmds={}):
        self.field = field_def
        self.fire_commands = {}
        self.move_commands = {
            'north' : ['north'],
            'south' : ['south'],
            'east'  : ['east' ],
            'west'  : ['west' ],
            ''      : [''     ]}  # Fall


        self.fire_commands.update(fire_cmds)
        self.move_commands.update(move_cmds)

    # Wrapper for all command functions
    def Command(self,command):
        _cmd_list = []
        if self.move_commands.get(command):
            _cmd_list = self.move_commands[command]
            _f = self.field.Move
        elif self.fire_commands.get(command):
            _cmd_list = self.fire_commands[command]
            _f = self.field.Detonate_Torpedo

        # Iterate through the list of movement commands or firing coordinates 
        for i in _cmd_list:
            _f(i)

#end class Ship class