import tkinter as tk
from tkinter import PhotoImage
import random

class SuperMarioGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Super Mario Quiz Game")
        self.root.geometry("1200x600")
        
        self.canvas = tk.Canvas(root, width=1200, height=600, bg="skyblue")
        self.canvas.pack()

        self.background_image = PhotoImage(file=r"C:\Users\Admin\OneDrive\Videos\Captures\mario_quiz_game\background_image.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        self.welcome_text = self.canvas.create_text(600, 100, text="Welcome to Super Mario Quiz Game!", font=("Times New Roman", 30, "bold"), fill="yellow")

        self.name_prompt = self.canvas.create_text(624, 255, text=" ENTER YOUR NAME: ", font=("Times New Roman", 15, "bold"), fill="black")

        self.name_entry = tk.Entry(root, font=("Times New Roman", 18))
        self.name_entry.place(x=500, y=270)

        self.start_button = tk.Button(root, text="Start Game", font=("Times New Roman", 20), command=self.start_game)
        self.start_button.place(x=550, y=320)

        self.canvas.itemconfig(self.welcome_text, state="normal")
        self.canvas.itemconfig(self.name_prompt, state="normal")
        self.start_button.place(x=550, y=320)

        self.player_name = ""
        self.game_started = False
        self.score = 0  

        self.score_label = None
        self.result_text = None  

        self.max_questions = 5
        self.current_question_count = 0  

        self.player_name_label = None

    def start_game(self):
        
        self.player_name = self.name_entry.get()
        
        if self.player_name == "":
            self.player_name = "Player"
        
        self.canvas.delete(self.welcome_text)
        self.canvas.delete(self.name_prompt)
        self.name_entry.place_forget()
        self.start_button.place_forget()

        self.initialize_game()

        self.score_label = self.canvas.create_text(70, 30, text=f"Score: {self.score}", font=("Times New Roman", 18, "bold"), fill="yellow")

        self.player_name_label = self.canvas.create_text(600, 480, text=self.player_name, font=("Times New Roman", 18, "bold"), fill="yellow")

    def initialize_game(self):

        self.mario_run1 = PhotoImage(file=r"C:\Users\Admin\OneDrive\Videos\Captures\mario_quiz_game\super_mario1.png")
        self.mario_run2 = PhotoImage(file=r"C:\Users\Admin\OneDrive\Videos\Captures\mario_quiz_game\super_mario2.png")

        self.brick_image = PhotoImage(file=r"C:\Users\Admin\OneDrive\Videos\Captures\mario_quiz_game\brick.png")

        self.monster_image = PhotoImage(file=r"C:\Users\Admin\OneDrive\Videos\Captures\mario_quiz_game\monster.png")

        self.ground = self.canvas.create_rectangle(0, 550, 1200, 600, fill="green")

        self.body = self.canvas.create_image(75, 525, image=self.mario_run1)
        
        self.player_speed_x = 0
        self.player_speed_y = 0
        self.is_jumping = False
        self.jump_power = 15
        self.gravity = 1

        self.scroll_speed = 5

        self.questions = [
            {"question": "WHAT IS THE COLOR OF THE SUN?", "answers": ["yellow", "green", "red"], "correct": "A"},
            {"question": "WHAT DO COWS DRINK?", "answers": ["water", "milk", "juice"], "correct": "B"},
            {"question": "WHAT IS 2 + 2?", "answers": ["3", "4", "5"], "correct": "B"},
            {"question": "WHAT IS THE CAPITAL OF FRANCE?", "answers": ["Berlin", "Paris", "Madrid"], "correct": "B"},
            {"question": "WHAT PLANET IS KNOWN AS THE RED PLANET?", "answers": ["Mars", "Venus", "Jupiter"], "correct": "A"}
        ]

        self.current_question_index = 0

        self.question_boxes = []
        self.create_question_boxes()

        self.question_text = self.canvas.create_text(600, 50, text=self.questions[self.current_question_index]["question"], font=("Times New Roman", 18, "bold"), fill="black")
        self.option_a = self.canvas.create_text(400, 100, text=f"A.) {self.questions[self.current_question_index]['answers'][0]}", font=("Times New Roman", 17, "bold"), fill="black")
        self.option_b = self.canvas.create_text(600, 100, text=f"B.) {self.questions[self.current_question_index]['answers'][1]}", font=("Times New Roman", 17, "bold"), fill="black")
        self.option_c = self.canvas.create_text(800, 100, text=f"C.) {self.questions[self.current_question_index]['answers'][2]}", font=("Times New Roman", 17, "bold"), fill="black")

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.jump)

        self.update_game()

    def move_left(self, event):
        self.player_speed_x = -self.scroll_speed
        self.update_running_animation()

    def move_right(self, event):
        self.player_speed_x = self.scroll_speed
        self.update_running_animation()

    def jump(self, event):
        if not self.is_jumping:
            self.is_jumping = True
            self.player_speed_y = -self.jump_power

    def update_running_animation(self):
        if self.player_speed_x != 0:
            current_image = self.canvas.itemcget(self.body, "image")
            new_image = self.mario_run2 if current_image == str(self.mario_run1) else self.mario_run1
            self.canvas.itemconfig(self.body, image=new_image)

    def create_question_boxes(self):
        self.question_boxes.clear()
        start_x = 1200
        spacing = 200
        letters = ['A', 'B', 'C']

        for i in range(3):
            box_x = start_x + i * spacing
            box_y = 400
            brick = self.canvas.create_image(box_x + 25, box_y + 25, image=self.brick_image)
            letter = self.canvas.create_text(box_x + 25, box_y + 25, text=letters[i], font=("Times New Roman", 20, "bold"), fill="black")
            question_mark = self.canvas.create_text(box_x + 25, box_y - 25, text="?", font=("Times New Roman", 17, "bold"), fill="black")
            
            self.question_boxes.append({
                "brick": brick,
                "letter": letter,
                "question_mark": question_mark,
                "box_hit": False,
                "answer": letters[i],
            })

    def update_game(self):

        if self.current_question_count >= self.max_questions:
            self.end_game()
            return
        
        self.player_speed_y += self.gravity
        self.canvas.move(self.body, self.player_speed_x, self.player_speed_y)

        player_coords = self.canvas.coords(self.body)
        if player_coords[1] >= 525:
            self.is_jumping = False
            self.player_speed_y = 0
            self.canvas.coords(self.body, player_coords[0], 525)

        if self.player_name_label:
            self.canvas.coords(self.player_name_label, player_coords[0], player_coords[1] - 50)  

        for box_info in self.question_boxes:
            if not box_info["box_hit"]:
                if self.check_collision(player_coords, box_info):
                    self.handle_answer(box_info)
                    box_info["box_hit"] = True 

        for box_info in self.question_boxes:
            self.canvas.move(box_info["brick"], -self.scroll_speed, 0)
            self.canvas.move(box_info["question_mark"], -self.scroll_speed, 0)
            self.canvas.move(box_info["letter"], -self.scroll_speed, 0)

            brick_coords = self.canvas.coords(box_info["brick"])

            if brick_coords[0] < -50:
                self.canvas.move(box_info["brick"], 1250, 0)
                self.canvas.move(box_info["question_mark"], 1250, 0)
                self.canvas.move(box_info["letter"], 1250, 0)

        self.player_speed_x = 0
        self.root.after(20, self.update_game)

    def check_collision(self, player_coords, box_info):
        box_coords = self.canvas.coords(box_info["brick"])
        return (
            player_coords[0] + 25 >= box_coords[0] - 25 and 
            player_coords[0] - 25 <= box_coords[0] + 25 and 
            player_coords[1] + 25 >= box_coords[1] - 25 and 
            player_coords[1] - 25 <= box_coords[1] + 25
        )

    def handle_answer(self, box_info):
 
        for box in self.question_boxes:
            self.canvas.delete(box["brick"])
            self.canvas.delete(box["letter"])
            self.canvas.delete(box["question_mark"])

        if box_info["answer"] == self.questions[self.current_question_index]["correct"]:
            self.score += 5
            result_text = "CORRECT!!!"
            result_color = "green"
        else:
            self.score -= 2
            result_text = "WRONG!!!"
            result_color = "red"

        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")

        self.result_text = self.canvas.create_text(600, 300, text=result_text, font=("Times New Roman", 20, "bold"), fill=result_color)

        self.canvas.after(500, self.canvas.delete, self.result_text)

        self.current_question_index = (self.current_question_index + 1) % len(self.questions)

        self.canvas.itemconfig(self.question_text, text=self.questions[self.current_question_index]["question"])
        self.canvas.itemconfig(self.option_a, text=f"A.) {self.questions[self.current_question_index]['answers'][0]}")
        self.canvas.itemconfig(self.option_b, text=f"B.) {self.questions[self.current_question_index]['answers'][1]}")
        self.canvas.itemconfig(self.option_c, text=f"C.) {self.questions[self.current_question_index]['answers'][2]}")

        self.create_question_boxes()

        self.current_question_count += 1

        if self.current_question_count >= self.max_questions:
            self.end_game()

    def end_game(self):
        self.canvas.delete(self.body)
        self.canvas.delete(self.question_text)
        self.canvas.delete(self.option_a)
        self.canvas.delete(self.option_b)
        self.canvas.delete(self.option_c)

        self.canvas.create_text(600, 100, text="Game Over!", font=("Times New Roman", 50, "bold"), fill="dark red")

        self.canvas.create_text(600, 150, text=f"Total Score: {self.score}", font=("Times New Roman", 20,), fill="black")

        self.canvas.create_text(600, 200, text="Thank You For Playing!", font=("Times New Roman", 20, "bold"), fill="yellow")

root = tk.Tk()
game = SuperMarioGame(root)
root.mainloop()
