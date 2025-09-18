from collections import defaultdict
from copy import deepcopy

class TicTacToe():
    def __init__(self, max_turn=0, grid_size=3, buckets=[2,2,2]):        
        self.config = {
            'max_turn': max_turn if max_turn > 0 else grid_size ** 2 * 2,
            'grid_size': grid_size,  # N x N grid
        }
        self.num_buckets = buckets
        self.reset()

    def reset(self):
        self.matrix = defaultdict(list)
        # Towards right: 0, 1, 2, ... (x-axis)
        # Towards bottom: 0, 1, 2, ... (y-axis)
        # write as 0,2 (bottom-left corner for 3x3 grid) 

        self.current_player = 1
        self.max_turn = 0
        self.buckets = {1: deepcopy(self.num_buckets), 2: deepcopy(self.num_buckets)}
        self.buckets[1][0] -= 1  # Player with first move has 1 less small bucket

    def check_valid_action(self, action):
        # action can be {bucket}_{new_pos} OR {old_pos}_{new_pos}
        bucket_or_pos, new_pos = action.split('_')
        try:
            bucket = int(bucket_or_pos)
            old_pos = (-1, -1)
        except ValueError:
            old_pos = tuple([int(v) for v in bucket_or_pos.split(',')])
            bucket = self.get_largest_bucket_info(old_pos)
        new_pos = tuple([int(v) for v in new_pos.split(',')])
        # Check position exceed grid size
        if max(new_pos) >= self.config['grid_size']:
            # print('exceed grid size')
            return False
        # Check bucket size
        if bucket > 2 or bucket < 0:
            # print('exceed bucket size')
            return False
        # Check bucket limit for the player
        if old_pos == (-1, -1):
            if self.buckets[self.current_player][bucket] < 1:
                # print('exceed bucket limit')
                return False
        else:
            # Check bucket exists at old_pos
            if not self.matrix[old_pos]:
                # print('Empty cell')
                return False
            player, size = self.matrix[old_pos][0]
            if player != self.current_player or size != bucket:
                # print('bucket not exists')
                return False
        # Check player can place the bucket at new_pos
        if self.matrix[new_pos]:
            player, size = self.matrix[new_pos][0]
            if size >= bucket:
                # print('cannot place bucket')
                return False
        return True

    def process_action(self, action):
        bucket_or_pos, new_pos = action.split('_')
        try:
            bucket = int(bucket_or_pos)
            old_pos = (-1, -1)
        except ValueError:
            old_pos = tuple([int(v) for v in bucket_or_pos.split(',')])
            bucket = self.get_largest_bucket_info(old_pos)
        new_pos = tuple([int(v) for v in new_pos.split(',')])
        if old_pos != (-1, -1):
            self.matrix[old_pos].pop(0)
            winner = self.check_winner()  # case if player removes a bucket so another player immediately wins
            if winner:
                return winner
        else:
            # minus 1 for player's bucket
            self.buckets[self.current_player][bucket] -= 1
        self.matrix[new_pos] = [(self.current_player, int(bucket))] + self.matrix[new_pos]  # (player, size)

    def get_largest_bucket_info(self, pos, info='size'):
        # get the largest bucket size of a cell, raise Error if empty
        cell = self.matrix.get(pos, [])
        if not cell:
            # No bucket exists in {pos}
            if info in ['size', 'player']:
                return -1
            return (-1, -1)  
        if info == 'size':
            return cell[0][1]  # size
        elif info == 'player':
            return cell[0][0]  # player
        return cell[0]  # (player, size)

    def get_largest_bucket(self, x, y):
        # get the largest bucket of a cell, return which player, return 0 if empty
        cell = self.matrix.get((x,y), [])
        if not cell:
            return 0
        return cell[0][0]  # player

    def check_winner(self):
        # return winner if any, return None if no winner yet
        # check if row has winner
        grid_size = self.config['grid_size']
        for y in range(grid_size):
            row = []
            for x in range(grid_size):
                row.append(self.get_largest_bucket(x,y))  # get largest bucket of each position
            # if row has winner
            if len(set(row)) == 1 and row[0] > 0:
                return row[0]

        # check if column has winner
        for x in range(grid_size):
            column = []
            for y in range(grid_size):
                column.append(self.get_largest_bucket(x,y))
            # if column has winner
            if len(set(column)) == 1 and column[0] > 0:
                return column[0]
            
        # check both diagonal has winner
        diag = []
        for i in range(grid_size):
            diag.append(self.get_largest_bucket(i,i))
        # if diagonal has winner
        if len(set(diag)) == 1 and diag[0] > 0:
            return diag[0]
        diag = []
        for i in range(grid_size):
            diag.append(self.get_largest_bucket(grid_size-i-1,i))
        # if diagonal (reverse) has winner
        if len(set(diag)) == 1 and diag[0] > 0:
            return diag[0]
        return

    def input_action(self, action):
        if not self.check_valid_action(action):
            return 'Invalid action'  # re-input action, nothing happens
        if self.max_turn < self.config['max_turn']:
            winner = self.process_action(action)
            if winner:
                return f'Player {winner} wins during player {self.current_player} moving a bucket'  # game won't contine
            winner = self.check_winner()
            if winner:
                self.reset()
                return f'Player {winner} wins'  # game won't contine
            if self.current_player == 1:
                self.current_player = 2
            else:
                self.current_player = 1
            self.max_turn += 1
            return
        else:            
            self.reset()
            return 'Draw'  # game won't contine
        
if __name__ == '__main__':
    debug_actions = [
        '2_1,1',
        '2_0,0',
        '2_2,0',
        '2_0,2',
        '1_0,1',
        '1_2,1',
        '2,0_2,1',  # Player 1 wins here
        '-1,-1_2,2',
    ]
    debug_actions = [
        '2_1,1',
        '1_2,2',
        '2_2,2',
        '1_0,0',
        '1_1,2',
        '2_1,2',
        '1_2,1',
        '2_2,1',
        '0_0,2',
        '0_2,0',
        '2,2_2,0',  # Player 2 wins immediately when player 1 moves bucket
    ]
    ttt = TicTacToe(grid_size=3, buckets=[2,2,2])
    for action in debug_actions:
        print(action)
        msg = ttt.input_action(action)
        if msg:
            print(msg)
            if msg != 'Invalid action':
                break
