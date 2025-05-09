import tkinter as tk
from tkinter import PhotoImage
import math
import random

class SuperMarioGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Super Mario Cat Game")
        self.root.geometry("1200x600")
        self.canvas = tk.Canvas(root, width=1200, height=600, bg="skyblue")
        self.canvas.pack()

        self.background_image = PhotoImage(file=r"C:\Users\Admin\OneDrive\Videos\Captures\mario_quiz_game\background_image.png")  # Change this to your background image path
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

        start_x = (1200 - (3 * 50 + 2 * 200)) // 2
        spacing = 200

        self.question_boxes = []
        letters = ['A', 'B', 'C']
        for i in range(3):
            box_x = start_x + i * spacing
            box_y = 400

            brick = self.canvas.create_image(box_x + 25, box_y + 25, image=self.brick_image)
            letter = self.canvas.create_text(box_x + 25, box_y + 25, text=letters[i], font=("Times New Roman", 17, "bold"), fill="black")
            question_mark = self.canvas.create_text(box_x + 25, box_y - 25, text="?", font=("Times New Roman", 17, "bold"), fill="black")

            self.question_boxes.append({
                "brick": brick,
                "letter": letter,
                "question_mark": question_mark,
                "box_hit": False,
                "float_counter": 0,
                "answer": 'A' if i == 0 else ('B' if i == 1 else 'C'),
                "monster": None
            })

        self.question_text = self.canvas.create_text(600, 50, text="WHAT IS THE COLOR OF THE SUN?", font=("Time New Roman", 18, "bold"), fill="black")
        self.option_a = self.canvas.create_text(400, 100, text="A.) yellow", font=("Time New Roman", 17, "bold"), fill="black")
        self.option_b = self.canvas.create_text(600, 100, text="B.) green", font=("Time New Roman", 17, "bold"), fill="black")
        self.option_c = self.canvas.create_text(800, 100, text="C.) red", font=("Time New Roman", 17, "bold"), fill="black")

        self.result_text = None

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.jump)

        self.update_game()

    def move_left(self, event):
        self.player_speed_x = -5
        self.update_running_animation()

    def move_right(self, event):
        self.player_speed_x = 5
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
                box_info["float_counter"] += 0.05
                float_y_offset = math.sin(box_info["float_counter"]) * 10
                box_x = self.canvas.coords(box_info["brick"])[0]
                self.canvas.coords(box_info["question_mark"], box_x, 375 + float_y_offset)

                if self.check_collision(player_coords, box_info):
                    self.handle_answer(box_info)

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
        if not box_info["box_hit"]:
            box_info["box_hit"] = True

            if box_info["question_mark"]:
                self.canvas.delete(box_info["question_mark"])

            if box_info["answer"] == 'A':
                self.display_result("CORRECT!!!")
                self.show_fireworks(box_info)
            else:
                self.display_result("WRONG!!!")
                self.replace_with_monster(box_info)

    def display_result(self, result):
        if self.result_text:
            self.canvas.delete(self.result_text)

        color = "green" if result == "CORRECT!!!" else "red"
        
        self.result_text = self.canvas.create_text(
            600, 300, text=result, font=("Time New Roman", 30, "bold"), fill=color
        )

    def replace_with_monster(self, box_info):
        box_x, box_y = self.canvas.coords(box_info["brick"])
        monster_y = box_y - 50
        box_info["monster"] = self.canvas.create_image(box_x, monster_y, image=self.monster_image)

    def show_fireworks(self, box_info):
        box_x, box_y = self.canvas.coords(box_info["brick"])

        for _ in range(20):
            x_offset = random.randint(-30, 30)
            y_offset = random.randint(-50, -20)
            size = random.randint(2, 5)
            color = random.choice(["red", "yellow", "orange", "green", "blue", "violet", "pink", "white"])

            self.canvas.create_oval(
                box_x + x_offset - size, box_y + y_offset - size,
                box_x + x_offset + size, box_y + y_offset + size,
                fill=color, outline=""
            )

if __name__ == "__main__":
    root = tk.Tk()
    game = SuperMarioGame(root)
    root.mainloop()
