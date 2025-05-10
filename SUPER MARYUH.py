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
        self.player_speed_y += self.gravity
        self.canvas.move(self.body, self.player_speed_x, self.player_speed_y)

        player_coords = self.canvas.coords(self.body)

        if player_coords[1] >= 525:
            self.is_jumping = False
            self.player_speed_y = 0
            self.canvas.coords(self.body, player_coords[0], 525)

        for box_info in self.question_boxes:
            if not box_info["box_hit"]:
                if self.check_collision(player_coords, box_info):
                    self.handle_answer(box_info)
                    box_info["box_hit"] = True  

        for box_info in self.question_boxes:
            self.canvas.move(box_info["brick"], -self.scroll_speed, 0)
            self.canvas.move(box_info["question_mark"], -self.scroll_speed, 0)
            self.canvas.move(box_info["letter"], -self.scroll_speed, 0)  # Move the letter with the brick

            brick_coords = self.canvas.coords(box_info["brick"])

            if brick_coords[0] < -50: 
                self.canvas.move(box_info["brick"], 1250, 0)
                self.canvas.move(box_info["question_mark"], 1250, 0)
                self.canvas.move(box_info["letter"], 1250, 0)

        self.canvas.move(self.background_image, -self.scroll_speed, 0)

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
 
        correct_answer = self.questions[self.current_question_index]["correct"]
        letter = self.canvas.itemcget(box_info["letter"], "text")

        if letter == correct_answer:
            self.display_result("CORRECT!!!")
        else:
            self.display_result("WRONG!!!")

        self.delete_all_bricks()
        self.current_question_index = (self.current_question_index + 1) % len(self.questions)
        self.display_new_question()
        self.create_question_boxes()

    def delete_all_bricks(self):

        for box_info in self.question_boxes:
            self.canvas.delete(box_info["brick"])
            self.canvas.delete(box_info["letter"])
            self.canvas.delete(box_info["question_mark"])

        self.canvas.delete(self.question_text)
        self.canvas.delete(self.option_a)
        self.canvas.delete(self.option_b)
        self.canvas.delete(self.option_c)

    def display_result(self, result):
        color = "green" if result == "CORRECT!!!" else "red"
        result_text = self.canvas.create_text(600, 300, text=result, font=("Times New Roman", 30, "bold"), fill=color)

        self.root.after(1000, lambda: self.canvas.delete(result_text))

    def display_new_question(self):
        question = self.questions[self.current_question_index]
        self.question_text = self.canvas.create_text(600, 50, text=question["question"], font=("Times New Roman", 18, "bold"), fill="black")
        self.option_a = self.canvas.create_text(400, 100, text=f"A.) {question['answers'][0]}", font=("Times New Roman", 17, "bold"), fill="black")
        self.option_b = self.canvas.create_text(600, 100, text=f"B.) {question['answers'][1]}", font=("Times New Roman", 17, "bold"), fill="black")
        self.option_c = self.canvas.create_text(800, 100, text=f"C.) {question['answers'][2]}", font=("Times New Roman", 17, "bold"), fill="black")

if __name__ == "__main__":
    root = tk.Tk()
    game = SuperMarioGame(root)
    root.mainloop()
