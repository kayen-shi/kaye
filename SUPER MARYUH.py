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

        # Background image
        self.background_image = PhotoImage(file=r"C:\Users\Admin\OneDrive\Videos\Captures\mario_quiz_game\background_image.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        # Initial screen (Welcome and name input)
        self.welcome_text = self.canvas.create_text(600, 100, text="Welcome to Super Mario Quiz Game!", font=("Times New Roman", 30, "bold"), fill="black")
        self.name_prompt = self.canvas.create_text(600, 150, text="Enter your name:", font=("Times New Roman", 20), fill="black")

        # Create an Entry widget for the player's name
        self.name_entry = tk.Entry(root, font=("Times New Roman", 18))
        self.name_entry.place(x=500, y=200)

        # Create a start button that will trigger the game
        self.start_button = tk.Button(root, text="Start Game", font=("Times New Roman", 20), command=self.start_game)
        self.start_button.place(x=550, y=250)

        # Hide game elements initially
        self.canvas.itemconfig(self.welcome_text, state="normal")
        self.canvas.itemconfig(self.name_prompt, state="normal")
        self.start_button.place(x=550, y=250)

        # Other game variables
        self.player_name = ""
        self.game_started = False
        self.score = 0  # Initialize the score

        # Initialize score (but do not display it yet)
        self.score_label = None
        self.result_text = None  # This will be used for the "CORRECT!!!" or "WRONG!!!" messages

        # Max number of questions before game over
        self.max_questions = 5
        self.current_question_count = 0  # Keeps track of how many questions the player has answered

        # Initialize player name label (but don't display yet)
        self.player_name_label = None

    def start_game(self):
        # Get the player's name from the text entry
        self.player_name = self.name_entry.get()
        
        if self.player_name == "":  # Check if the player entered a name
            self.player_name = "Player"
        
        # Hide the welcome screen and show the game elements
        self.canvas.delete(self.welcome_text)
        self.canvas.delete(self.name_prompt)
        self.name_entry.place_forget()
        self.start_button.place_forget()

        # Initialize game components
        self.initialize_game()

        # Display the score label once the game starts
        self.score_label = self.canvas.create_text(70, 30, text=f"Score: {self.score}", font=("Times New Roman", 18, "bold"), fill="yellow")

        # Display the player's name above Mario and make it follow him
        self.player_name_label = self.canvas.create_text(600, 480, text=self.player_name, font=("Times New Roman", 18, "bold"), fill="black")

    def initialize_game(self):
        # Mario running images
        self.mario_run1 = PhotoImage(file=r"C:\Users\Admin\OneDrive\Videos\Captures\mario_quiz_game\super_mario1.png")
        self.mario_run2 = PhotoImage(file=r"C:\Users\Admin\OneDrive\Videos\Captures\mario_quiz_game\super_mario2.png")

        # Brick image
        self.brick_image = PhotoImage(file=r"C:\Users\Admin\OneDrive\Videos\Captures\mario_quiz_game\brick.png")

        # Monster image
        self.monster_image = PhotoImage(file=r"C:\Users\Admin\OneDrive\Videos\Captures\mario_quiz_game\monster.png")

        # Ground
        self.ground = self.canvas.create_rectangle(0, 550, 1200, 600, fill="green")

        # Mario's body
        self.body = self.canvas.create_image(75, 525, image=self.mario_run1)
        
        # Movement and Jumping settings
        self.player_speed_x = 0
        self.player_speed_y = 0
        self.is_jumping = False
        self.jump_power = 15
        self.gravity = 1

        # For scrolling the screen
        self.scroll_speed = 5

        # List of questions
        self.questions = [
            {"question": "WHAT IS THE COLOR OF THE SUN?", "answers": ["yellow", "green", "red"], "correct": "A"},
            {"question": "WHAT DO COWS DRINK?", "answers": ["water", "milk", "juice"], "correct": "B"},
            {"question": "WHAT IS 2 + 2?", "answers": ["3", "4", "5"], "correct": "B"},
            {"question": "WHAT IS THE CAPITAL OF FRANCE?", "answers": ["Berlin", "Paris", "Madrid"], "correct": "B"},
            {"question": "WHAT PLANET IS KNOWN AS THE RED PLANET?", "answers": ["Mars", "Venus", "Jupiter"], "correct": "A"}
        ]

        # Initialize the first question index
        self.current_question_index = 0

        # List of question boxes (bricks with questions)
        self.question_boxes = []
        self.create_question_boxes()

        # Text to display the current question
        self.question_text = self.canvas.create_text(600, 50, text=self.questions[self.current_question_index]["question"], font=("Times New Roman", 18, "bold"), fill="black")
        self.option_a = self.canvas.create_text(400, 100, text=f"A.) {self.questions[self.current_question_index]['answers'][0]}", font=("Times New Roman", 17, "bold"), fill="black")
        self.option_b = self.canvas.create_text(600, 100, text=f"B.) {self.questions[self.current_question_index]['answers'][1]}", font=("Times New Roman", 17, "bold"), fill="black")
        self.option_c = self.canvas.create_text(800, 100, text=f"C.) {self.questions[self.current_question_index]['answers'][2]}", font=("Times New Roman", 17, "bold"), fill="black")

        # Key bindings
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
        self.question_boxes.clear()  # Clear old question boxes
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
        # Check for game over condition
        if self.current_question_count >= self.max_questions:
            self.end_game()
            return

        # Update player's movement
        self.player_speed_y += self.gravity
        self.canvas.move(self.body, self.player_speed_x, self.player_speed_y)

        # Make Mario land on the ground
        player_coords = self.canvas.coords(self.body)
        if player_coords[1] >= 525:
            self.is_jumping = False
            self.player_speed_y = 0
            self.canvas.coords(self.body, player_coords[0], 525)

        # Move the player's name label to follow Mario, also during jumping
        if self.player_name_label:
            self.canvas.coords(self.player_name_label, player_coords[0], player_coords[1] - 50)  # Adjusted to follow Mario's vertical position

        # Check for collisions with bricks and handle correct/wrong answer
        for box_info in self.question_boxes:
            if not box_info["box_hit"]:
                if self.check_collision(player_coords, box_info):
                    self.handle_answer(box_info)
                    box_info["box_hit"] = True  # Mark this brick as hit

        # Move all bricks to simulate circular movement
        for box_info in self.question_boxes:
            self.canvas.move(box_info["brick"], -self.scroll_speed, 0)
            self.canvas.move(box_info["question_mark"], -self.scroll_speed, 0)
            self.canvas.move(box_info["letter"], -self.scroll_speed, 0)

            brick_coords = self.canvas.coords(box_info["brick"])

            if brick_coords[0] < -50:  # If the brick moves off the left edge
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
        # Delete all question boxes (bricks, letters, question marks)
        for box in self.question_boxes:
            self.canvas.delete(box["brick"])
            self.canvas.delete(box["letter"])
            self.canvas.delete(box["question_mark"])

        # Check if answer is correct or wrong
        if box_info["answer"] == self.questions[self.current_question_index]["correct"]:
            self.score += 5
            result_text = "CORRECT!!!"
            result_color = "green"
        else:
            self.score -= 2
            result_text = "WRONG!!!"
            result_color = "red"

        # Update the score display
        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")

        # Display result text
        self.result_text = self.canvas.create_text(600, 300, text=result_text, font=("Times New Roman", 20, "bold"), fill=result_color)

        # Immediate transition to Game Over
        self.canvas.after(500, self.canvas.delete, self.result_text)

        # Update the question index
        self.current_question_index = (self.current_question_index + 1) % len(self.questions)

        # Update the question and options
        self.canvas.itemconfig(self.question_text, text=self.questions[self.current_question_index]["question"])
        self.canvas.itemconfig(self.option_a, text=f"A.) {self.questions[self.current_question_index]['answers'][0]}")
        self.canvas.itemconfig(self.option_b, text=f"B.) {self.questions[self.current_question_index]['answers'][1]}")
        self.canvas.itemconfig(self.option_c, text=f"C.) {self.questions[self.current_question_index]['answers'][2]}")

        # Create new bricks with updated questions
        self.create_question_boxes()

        # Increase the count of answered questions
        self.current_question_count += 1

        # Check if the game is over after answering the maximum number of questions
        if self.current_question_count >= self.max_questions:
            self.end_game()

    def end_game(self):
        # Remove the player, the question, and the options
        self.canvas.delete(self.body)
        self.canvas.delete(self.question_text)
        self.canvas.delete(self.option_a)
        self.canvas.delete(self.option_b)
        self.canvas.delete(self.option_c)

        # Display "Game Over" text at the top
        self.canvas.create_text(600, 100, text="Game Over!", font=("Times New Roman", 30, "bold"), fill="red")
        
        # Display final score above the restart button
        self.canvas.create_text(600, 150, text=f"Final Score: {self.score}", font=("Times New Roman", 20, "bold"), fill="black")

        # Display "Thank you for playing" message
        self.canvas.create_text(600, 200, text="Thank you for playing!", font=("Times New Roman", 20, "bold"), fill="black")

# Initialize the tkinter window
root = tk.Tk()
game = SuperMarioGame(root)
root.mainloop()
