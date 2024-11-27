import customtkinter as ctk
import copy
import json

class TicTacToe(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tic Tac Toe")
        self.geometry("300x380")

        self.current_player = "X"
        self.buttons = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.create_widgets()
        self.current_root = None

    def create_widgets(self):
        self.turn_label = ctk.CTkLabel(self, text=f"Player {self.current_player}'s turn", font=("Arial", 16))
        self.turn_label.grid(row=0, column=0, columnspan=3, pady=10)

        for i in range(3):
            for j in range(3):
                button = ctk.CTkButton(self, text=" ", width=100, height=100, command=lambda i=i, j=j: self.on_button_click(i, j))
                self.buttons[i][j] = button
                button.grid(row=j, column=i)

        self.reset_button = ctk.CTkButton(self, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=4, column=0, columnspan=3, sticky="we", pady=10)

    def change_current_root(self, sit):
        if self.current_root == None:
            self.current_root = root
        else:
            for child in self.current_root.children:
                if child.data == sit:
                    self.current_root = child
    def check_for_trick(self, player, sit):
        opposite_player = "O" if player == "X" else "X"
        if sit == [[opposite_player, 0, 0], [0, player, 0], [0, 0, opposite_player]]:
            return [True, [[opposite_player, player, 0], [0, player, 0], [0, 0, opposite_player]]]
        elif sit == [[0, 0, opposite_player], [0, player, 0], [opposite_player, 0, 0]]:
            return [True, [[0, 0, opposite_player], [0, player, 0], [opposite_player, player, 0]]]
        else:
            return [False, None]

    def on_button_click(self, i, j):
        # Here you can add any additional logic you want to handle when a button is clicked
        # For example, marking the button with the current player's symbol
        if self.buttons[i][j].cget('text') == " ":
            self.buttons[i][j].configure(text=self.current_player)
            # Toggle player
            self.current_player = "O" if self.current_player == "X" else "X"
            self.turn_label.configure(text=f"Player {self.current_player}'s turn")
            sit = self.get_situation_data()
            for child in self.current_root.children:
                if child.data == sit and len(child.children) > 0:
                    trick = self.check_for_trick(self.current_player, sit)
                    if trick[0]:
                        for i in child.children:
                            if trick[1] == i.data:
                                best_sit = i
                    else:
                        self.current_root = child
                        best_sit = child.children[0]
                        for child2 in child.children:
                            if self.current_player == "X":
                                if (best_sit.end_probability["X"] + best_sit.end_probabilty["s"]) < (child2.end_probability["X"] + child2.end_probability["s"]):
                                    best_sit = child2
                                elif check_win(child2.data) == "X":
                                    best_sit = child2
                                    break
                            elif self.current_player == "O":
                                if (best_sit.end_probability["O"] + best_sit.end_probability["s"]) < (child2.end_probability["O"] + child2.end_probability["s"]):
                                    best_sit = child2
                                elif check_win(child2.data) == "O":
                                    best_sit = child2
                                    break
                    self.current_root = best_sit
                    self.change_board_situation(best_sit)
                    break
                        
            self.current_player = "O" if self.current_player == "X" else "X"
        

    def reset_game(self):
        # Reset the game state and the button texts
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text=" ")
        self.current_player = "X"
        self.current_root = root
        self.turn_label.configure(text=f"Player {self.current_player}'s turn")

    def get_situation_data(self):
        sit = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j].cget('text') == "X":
                    sit[j][i] = "X"
                elif self.buttons[i][j].cget('text') == "O":
                    sit[j][i] = "O"
        return sit
    def change_board_situation(self, board):
        for i in range(3):
            for j in range(3):
                if board.data[j][i] != 0:     
                    self.buttons[i][j].configure(text=board.data[j][i])


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
    def __init__(self, data, children, end_probability, n_children):
        self.children = self.unwrap_json(children)
        self.data = data
        self.end_probability = end_probability
        self.n_children = n_children

    def unwrap_json(self, children):
        children_list = []
        if len(children) > 0:
            for child in children:
                child1 = Tree(child["data"], child["children"], child["end_probability"], child["n_children"])
                children_list.append(child1)
        return children_list
def get_level_deeper(situation, player):
    level_deeper = []
    for i in range(3):
        for j in range(3):
            sit = copy.deepcopy(situation)
            if situation[i][j] == 0:
                sit[i][j] = player
                level_deeper.append(sit)
    return level_deeper

def create_tree_from_data(data):
    tree = Tree()

if __name__ == "__main__":
    with open('data.json', 'r') as file:
        tree = json.load(file) 
    app = TicTacToe()
    root = Tree(tree["data"], tree["children"], tree["end_probability"], tree["n_children"])
    app.change_current_root(app.get_situation_data())    
    #maybe i should try to use only data formated as a list. if not i have to create a function that turns the data in json to Tree objects. First approach 
    #would require handling AI decision process diffrently
    app.mainloop()
    