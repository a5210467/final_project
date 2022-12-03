import numpy as np
import random

class Node:
    def __init__(self, state, winning, move, parent):
        self.state = state
        self.parent = parent
        self.score_total = 0
        self.visit_count = 0
        self.children = None
        self.is_winning = winning
        self.move = move
    
    def put_children(self, children):
        self.children = children

    #MCTS calculation
    def uct(self):
        if self.visit_count == 0:
            return None
        else:
            return self.score_total/self.visit_count + np.sqrt(2*np.log(self.parent.visit_count)/self.visit_count)

    
    def select_child(self):
        if self.children is None:
            return None, None
        
        else:
            win_array = [w for w in self.children if w.is_winning]
            if len(win_array) > 0:
                choose = random.choice(win_array)
                return choose, choose.move
            
            visit_count_list = [child.score_total/child.visit_count if child.visit_count > 0 else 0 for child in self.children]

            choosed_child = self.children[np.argmax(visit_count_list)]

            return choosed_child, choosed_child.move

    def get_child(self, move):
        if not self.children:
            return None
        
        for child in self.children:
            if child.move == move:
                return child
        
        print("No child exist")
