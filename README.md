# kaye
COMRPOG


       
import tkinter as tk
from tkinter import PhotoImage
import math

class SuperMarioGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Super Mario Cat Game")
        self.root.geometry("1200x600")
        self.canvas = tk.Canvas(root, width=1200, height=600, bg="skyblue")
        self.canvas.pack()
        
        # Load Mario body (You need to replace 'mario.png' with an actual image file path)
        self.mario_run1 = PhotoImage(file=r"C:\Users\Admin\OneDrive\Videos\Captures\mario_quiz_game\super_mario1.png")
        self.mario_run2 = PhotoImage(file=r"C:\Users\Admin\OneDrive\Videos\Captures\mario_quiz_game\super_mario2.png")

        # Load Brick image (replace with the correct path to your brick image)
        self.brick_image = PhotoImage(file=r"C:\Users\Admin\OneDrive\Videos\Captures\mario_quiz_game\brick.png")
        
        # Create ground
        self.ground = self.canvas.create_rectangle(0, 550, 1200, 600, fill="green")

        # Create Mario-like body
        self.body = self.canvas.create_image(75, 525, image=self.mario_run1)  # Start with the first running frame
        
        self.player_speed_x = 0
        self.player_speed_y = 0
        self.is_jumping = False
        self.jump_power = 15
        self.gravity = 1

        # Centered positions
        start_x = (1200 - (3 * 50 + 2 * 200)) // 2
        spacing = 200

        # Create 3 brick boxes with letters inside
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
                "answer": 'A' if i == 0 else ('B' if i == 1 else 'C')
            })

        # Center the question
        self.question_text = self.canvas.create_text(600, 50, text="WHAT IS THE COLOR OF THE SUN?", font=("Time New Roman", 18, "bold"), fill="black")

        # Display multiple-choice options
        self.option_a = self.canvas.create_text(400, 100, text="A.) yellow", font=("Time New Roman", 17, "bold"), fill="black")
        self.option_b = self.canvas.create_text(600, 100, text="B.) green", font=("Time New Roman", 17, "bold"), fill="black")
        self.option_c = self.canvas.create_text(800, 100, text="C.) red", font=("Time New Roman", 17, "bold"), fill="black")

        # Create a label to display "CORRECT" or "WRONG"
        self.result_text = None

        # Bind keys
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.jump)

        # Game loop
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
        # Switch between running images for animation effect when moving left or right
        if self.player_speed_x != 0:
            if self.player_speed_x > 0:
                # Moving right, alternate between run images
                if self.canvas.itemcget(self.body, "image") == str(self.mario_run1):
                    self.canvas.itemconfig(self.body, image=self.mario_run2)
                else:
                    self.canvas.itemconfig(self.body, image=self.mario_run1)
            else:
                # Moving left, alternate between run images (mirror effect if needed)
                if self.canvas.itemcget(self.body, "image") == str(self.mario_run1):
                    self.canvas.itemconfig(self.body, image=self.mario_run2)
                else:
                    self.canvas.itemconfig(self.body, image=self.mario_run1)

    def update_game(self):
        # Apply gravity
        self.player_speed_y += self.gravity

        # Update player position
        self.canvas.move(self.body, self.player_speed_x, self.player_speed_y)
        player_coords = self.canvas.coords(self.body)

        # Ground collision
        if player_coords[1] >= 525:
            self.is_jumping = False
            self.player_speed_y = 0
            self.canvas.coords(self.body, player_coords[0], 525)

        # Floating question marks
        for box_info in self.question_boxes:
            if not box_info["box_hit"]:
                box_info["float_counter"] += 0.05
                float_y_offset = math.sin(box_info["float_counter"]) * 10
                box_x = self.canvas.coords(box_info["brick"])[0]
                self.canvas.coords(box_info["question_mark"], box_x, 375 + float_y_offset)

        # Stop horizontal movement if no key is pressed
        self.player_speed_x = 0

        # Repeat game loop
        self.root.after(20, self.update_game)

if __name__ == "__main__":
    root = tk.Tk()
    game = SuperMarioGame(root)
    root.mainloop()
