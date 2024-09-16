class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent

    def print_board(self):
        for row in self.state:
            for val in row:
                print(val, end = ",")
            print() 
    
    def get_state(self):
        return self.state
    
    def get_parent(self):
        return self.parent