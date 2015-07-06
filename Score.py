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
    def __init__(self,n_mines):
        self.n_mines = n_mines
        self.n_moves = 0
        self.n_shots = 0

    # Track the score for each command executed
    def Tally_Score(self,command):
        if command in ['north','south','east','west']:
            self.n_moves += 1
        elif command in ['alpha','beta','gamma','delta']:
            self.n_shots += 1

    # Return the score 
    def Return_Score(self):
        _move_penalty = self.n_moves * _SCORE_PER_MOVE
        _shot_penalty = self.n_shots * _SCORE_PER_SHOT

        if _move_penalty < (_MAX_MOVE_PENALTY_MULTIPLIER * self.n_mines):
            _move_penalty = _MAX_MOVE_PENALTY_MULTIPLIER * self.n_mines
        if _shot_penalty < (_MAX_SHOT_PENALTY_MULTIPLIER * self.n_mines):
            _shot_penalty = _MAX_SHOT_PENALTY_MULTIPLIER * self.n_mines

        return (self.n_mines * _SCORE_PER_MINE) + _move_penalty + _shot_penalty
# end class Score