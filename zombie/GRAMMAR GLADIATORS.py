import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import random
import pygame  # Import pygame

class GrammarGladiatorsGame:
    def __init__(self, root):
        pygame.mixer.init()  # Initialize the mixer module for sound
        
        self.root = root
        self.root.title("Grammar Gladiators")
        self.root.geometry("1200x600")
        
        self.game_over = False  # Flag to check if the game is over

        self.canvas = tk.Canvas(root, width=1200, height=600, bg="green")
        self.canvas.pack()

        # Load Images
        self.background_image = Image.open(r"C:\Users\Admin\OneDrive\Desktop\zombie\background_zombie.png")
        self.background_image_resized = ImageTk.PhotoImage(self.background_image.resize((1200, 600), Image.Resampling.LANCZOS))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image_resized)

        self.plant_image = ImageTk.PhotoImage(Image.open(r"C:\Users\Admin\OneDrive\Desktop\zombie\plant_image2.png").resize((100, 100), Image.Resampling.LANCZOS))
        self.plant = self.canvas.create_image(200, 500, image=self.plant_image)

        # Game Title
        self.game_title = self.canvas.create_text(600, 95, text="Welcome to Grammar Gladiators!", font=("Times New Roman", 40, "bold"), fill="yellow")

        # Player Name Entry
        self.enter_name_text = self.canvas.create_text(630, 165, text="ENTER YOUR NAME:", font=("Times New Roman", 13, "bold"), fill="black")
        self.name_entry = tk.Entry(root, font=("Times New Roman", 18))
        self.name_entry.place(x=500, y=180)

        self.start_button = tk.Button(root, text="Start Game", font=("Times New Roman", 20), command=self.start_game)
        self.start_button.place(x=550, y=250)

        # Game variables
        self.score = 0
        self.lives = 3
        self.zombie_speed = 5
        self.player_name = ""
        self.current_question_index = 0
        self.max_questions = 5
        self.zombies = []
        self.projectiles = []

        # Sample Questions
        self.questions = [
            {"question": "WHICH WORD IS A NOUN?", "answers": ["run", "apple", "quickly"], "correct": "B"},
            {"question": "WHAT IS A VERB?", "answers": ["jump", "happy", "desk"], "correct": "A"},
            {"question": "WHICH WORD DESCRIBES AN ACTION?", "answers": ["big", "throw", "green"], "correct": "B"},
            {"question": "WHICH WORD IS AN ADJECTIVE?", "answers": ["play", "joyful", "sky"], "correct": "B"},
            {"question": "WHAT IS A PRONOUN?", "answers": ["she", "bike", "run"], "correct": "A"}
        ]

        # Zombie image
        self.zombie_image = Image.open(r"C:\Users\Admin\OneDrive\Desktop\zombie\zombie.png")
        self.zombie_image_resized = ImageTk.PhotoImage(self.zombie_image.resize((100, 100), Image.Resampling.LANCZOS))

        # Load music
        self.background_music = r"C:\Users\Admin\OneDrive\Desktop\zombie\background_music.mp3"
        self.in_game_music = r"C:\Users\Admin\OneDrive\Desktop\zombie\in_game_music.mp3"
        self.game_over_music = r"C:\Users\Admin\OneDrive\Desktop\zombie\game_over_music.mp3"

        # Play background music when game runs
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)

    def start_game(self):
        self.player_name = self.name_entry.get()
        if self.player_name == "":
            self.player_name = "Player"

        # Remove entry and button
        self.name_entry.place_forget()
        self.start_button.place_forget()
        self.canvas.delete(self.enter_name_text)
        self.canvas.delete(self.game_title)

        # Stop background music and play in-game music
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.in_game_music)
        pygame.mixer.music.play(-1)

        # Display first question
        self.display_question()
        self.update_score_life()

        # Start game loop
        self.spawn_zombie()
        self.update_game()

    def update_score_life(self):
        self.canvas.delete("score_life")
        life_display = "❤️ " * self.lives
        self.canvas.create_text(200, 30, text=f"Lives: {life_display}", font=("Times New Roman", 20), fill="black", tag="score_life")
        self.canvas.create_text(95, 60, text=f"Score: {self.score}", font=("Times New Roman", 20), fill="black", tag="score_life")

    def display_question(self):
        question = self.questions[self.current_question_index]

        self.canvas.create_text(650, 70, text=question["question"], font=("Times New Roman", 30), fill="black", tag="question")

        for i, answer in enumerate(question["answers"]):
            x_pos = 450 + (i * 200)
            y_pos = 120
            self.canvas.create_text(x_pos, y_pos, text=f"{chr(65 + i)}.) {answer}", font=("Times New Roman", 18), fill="black", tag="question")

        self.answer_entry = tk.Entry(self.root, font=("Times New Roman", 16))
        self.answer_entry.place(x=500, y=220, width=200)
        self.answer_entry.focus()
        self.root.bind("<Return>", self.check_answer)

    def check_answer(self, event=None):
        typed_answer = self.answer_entry.get().strip().lower()
        correct_index = ord(self.questions[self.current_question_index]["correct"]) - 65
        correct_answer = self.questions[self.current_question_index]["answers"][correct_index].lower()

        if typed_answer == correct_answer:
            self.score += 5
        else:
            self.lives -= 1

        self.update_score_life()
        self.answer_entry.delete(0, tk.END)

        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self.canvas.delete("question")
            self.display_question()
        else:
            self.end_game()

    def spawn_zombie(self):
        if self.game_over:
            return
        
        zombie = self.canvas.create_image(1200, 500, image=self.zombie_image_resized)
        self.zombies.append(zombie)

    def update_game(self):
        if self.game_over:
            return

        self.move_zombies()

        if self.lives > 0:
            self.root.after(50, self.update_game)

    def move_zombies(self):
        for zombie in self.zombies:
            self.canvas.move(zombie, -self.zombie_speed, 0)

        for zombie in self.zombies:
            zombie_coords = self.canvas.coords(zombie)

            if zombie_coords[0] < 50:
                self.lives -= 1
                self.update_score_life()
                self.canvas.delete(zombie)
                self.zombies.remove(zombie)

            if self.is_collision(zombie_coords, self.canvas.coords(self.plant)):
                self.end_game()

        if self.lives <= 0:
            self.end_game()

    def end_game(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.game_over_music)
        pygame.mixer.music.play()

        self.game_over = True
        if hasattr(self, "answer_entry"):
            self.answer_entry.place_forget()
            self.answer_entry.destroy()

        self.root.unbind("<Return>")

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image_resized)
        self.canvas.create_text(600, 350, text="Game Over!", font=("Times New Roman", 40), fill="red")
        self.canvas.create_text(600, 400, text="Thank You For Playing!", font=("Times New Roman", 30), fill="yellow")

    def is_collision(self, coords1, coords2):
        x1, y1 = coords1
        x2, y2 = coords2
        return (x1 < x2 + 50 and x1 + 50 > x2 and y1 < y2 + 50 and y1 + 50 > y2)

root = tk.Tk()
game = GrammarGladiatorsGame(root)
root.mainloop()