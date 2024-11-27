import copy
import json

def check_win(situation):
    if situation[0][0] == situation[0][1] and situation[0][1] == situation[0][2] and situation[0][0] != 0:
        return situation[0][0]
    elif situation[1][0] == situation[1][1] and situation[1][1] == situation[1][2] and situation[1][0] != 0:
        return situation[1][0]
    elif situation[2][0] == situation[2][1] and situation[2][1] == situation[2][2] and situation[2][0] != 0:
        return situation[2][0]
    elif situation[0][0] == situation[1][0] and situation[1][0] == situation[2][0] and situation[0][0] != 0:
        return situation[0][0]
    elif situation[0][1] == situation[1][1] and situation[1][1] == situation[2][1] and situation[0][1] != 0:
        return situation[0][1]
    elif situation[0][2] == situation[1][2] and situation[1][2] == situation[2][2] and situation[0][2] != 0:
        return situation[0][2]
    elif situation[0][0] == situation[1][1] and situation[1][1] == situation[2][2] and situation[0][0] != 0:
        return situation[0][0]
    elif situation[0][2] == situation[1][1] and situation[1][1] == situation[2][0] and situation[0][2] != 0:
        return situation[0][2]
    elif all(element != 0 for row in situation for element in row):
        return "s"
    else: 
        return "N"

class Tree:
    def __init__(self, data):
        self.children = []
        self.parent = False
        self.data = data
        self.end_probability = {"X":0, "O":0, "s":0}
        self.n_children = 0

    def save_as_list(self):
        if len(self.children) > 0:
            child_list = []
            for child in self.children:
                child_list.append(child.save_as_list())
            dict = {"children":child_list, "data":self.data, "end_probability":self.end_probability, "n_children":self.n_children}
        else:
            dict = {"children":self.children, "data":self.data, "end_probability":self.end_probability, "n_children":self.n_children}
        return dict
        

    def fix_probabilities(self, w_cond):
        if len(self.children) == 0:
            if w_cond == "X":
                self.end_probability["X"] = 1
            elif w_cond == "O":
                self.end_probability["O"] = 1
            elif w_cond == "s":
                self.end_probability["s"] = 1
        else:
            x = 0
            o = 0
            s = 0
            for child in self.children:
                x += child.end_probability["X"]
                o += child.end_probability["O"]
                s += child.end_probability["s"]
            self.end_probability = {"X":(x/self.n_children), "O":(o/self.n_children), "s":(s/self.n_children)}
        if self.parent is not False:
            self.parent.fix_probabilities(w_cond)

    def add_children(self, situations, player):
        if len(situations) > 0:
            for data in situations:
                child = Tree(data)
                child.parent = self
                self.children.append(child)
                self.n_children += 1
                w_cond = check_win(child.data)
                if w_cond == "N":
                    child.add_children(get_level_deeper(data, "X" if player == "O" else "O"), "X" if player == "O" else "O")
                else:
                    child.fix_probabilities(w_cond)
                
    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def print_tree(self):
        spaces = " " * self.get_level() * 3
        prefix =  spaces + "|__" if self.parent else ""
        print(prefix + str(self.end_probability))
        if self.children:
            for child in self.children:
                print(child.print_tree())
    
def get_level_deeper(situation, player):
    level_deeper = []
    for i in range(3):
        for j in range(3):
            sit = copy.deepcopy(situation)
            if situation[i][j] == 0:
                sit[i][j] = player
                level_deeper.append(sit)
    return level_deeper

root = Tree([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
root.add_children(get_level_deeper([[0, 0, 0], [0, 0, 0], [0, 0, 0]], "X"), "X")
data = root.save_as_list()
with open('data.json', 'w') as file:
    json.dump(data, file)
