import pdb

_SCORE_PER_MINE = 10
_SCORE_PER_SHOT = -5
_SCORE_PER_MOVE = -2
_MAX_MOVE_PENALTY_MULTIPLIER = -3
_MAX_SHOT_PENALTY_MULTIPLIER = -5

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