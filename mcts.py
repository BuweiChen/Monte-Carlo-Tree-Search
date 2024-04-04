import math
import random
import time
from collections import deque

def mcts_policy(cpu_time):
    """ takes the allowed CPU time in seconds and returns a function 
        that takes a position and returns the move suggested by running 
        MCTS for that amount of time starting with that position.

    Args:
        cpu_time (int): the allowed CPU time in seconds
    """
    
    def policy(state):
        """ a function that takes a position and returns the move suggested 
            starting with that position

        Args:
            state (State): a position of a game

        Returns:
            one of the actions in the list returned by get_actions for this 
            state: the calculated optimal move
        """
        start_time = time.time()
        state_children = {}
        state_visits = {}
        state_rewards = {}
        
        def choose_path_to_leaf(s):
            """chooses a path to the next leaf to explore in MCTS using UCB

            Args:
                s (State): a position
                
            Returns:
                deque: the path taken to get the leaf, including the leaf
            """
            path = deque()
            curr_state = s
            
            while True:
                path.append(curr_state)
                if curr_state.is_terminal() or curr_state not in state_children:
                    break
                max_ucb = float('-inf')
                next_state = None
                
                total_visits = sum(state_visits[s] for s in state_children[curr_state])
                for st, child in state_children[curr_state]:
                    if child not in state_visits:
                        next_state = child
                        break
                    mean_reward = state_rewards[child] / state_visits[child]
                    ucb_score = mean_reward + math.sqrt(2 * math.log(total_visits) / state_visits[child])
                    if ucb_score > max_ucb:
                        max_ucb = ucb_score
                        next_state = child

                if next_state is None:
                    raise Exception
                
                curr_state = next_state
                
            return path
        
        
        
        def get_best_move(s):
            """get the best move of the given state

            Args:
                s (State): a position

            Returns:
                action: an action from the state
            """
            all_moves = s.get_actions()
            best_move = None
            best_move_reward = float('-inf') 
            for move in all_moves:
                successor_state = s.successor(move)
                move_reward = state_rewards[successor_state]
                if move_reward > best_move_reward:
                    best_move = move
                    best_move_reward = move_reward
            return best_move
        
        while time.time() - start_time < cpu_time:
            path = choose_path_to_leaf(state)
            leaf = path.pop()
            payoff = play_to_terminal()
            backpropagate(path, payoff)
        
        
        return get_best_move(state)
    return policy