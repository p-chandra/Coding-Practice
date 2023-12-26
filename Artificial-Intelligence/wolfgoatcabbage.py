'''
Pawan Chandra
CPSC:481
Project 1
'''

from search import *

class WolfGoatCabbage(Problem):

    def __init__(self,initial=frozenset({'F','W','G','C'}),goal=frozenset({})):
        super().__init__(initial, goal)

    def goal_test(self, state):
        return state == self.goal
        
    def actions(self,state):
        possible_actions = []

        if state == self.initial:
            possible_actions.append({'F','G'})
        
        elif state == {'W','C'} or state =={'G'}:
            possible_actions.append({'F'})
        
        elif state == {'W','F','C'}:
            possible_actions.append({'W','F'})
            possible_actions.append({'C','F'})
            
        elif state == {'W'} or state == {'C'}:
            possible_actions.append({'G','F'})
        
        elif state == {'G','F','C'}:
            possible_actions.append({'C','F'})
        
        elif state == {'G','F','W'}:
            possible_actions.append({'W','F'})

        elif state == {'G', 'F'}:
            possible_actions.append({'G','F'})

        return possible_actions

    def result(self, state, action):
        mutable_list = list(state)
        for elem in action:
            if elem in mutable_list:
                mutable_list.remove(elem)
            else:
                mutable_list.append(elem)
        #print("Left-Side:",list(state),"\nAction: ",action,"\nMutable: ", mutable_list, "\n")
        mutable_list = frozenset(mutable_list)
        return mutable_list

if __name__ == '__main__':
    wgc = WolfGoatCabbage()
    solution = depth_first_graph_search(wgc).solution()
    print(solution)
    solution = breadth_first_graph_search(wgc).solution()
    print(solution)
