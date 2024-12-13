#!/usr/bin/env python
# coding: utf-8

# In[4]:


import tkinter as tk
import random

class BreakoutGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Breakout Game")

        # Canvas dimensions
        self.canvas_width = 500
        self.canvas_height = 400

        # Initialize canvas
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()

        # Paddle properties
        self.paddle_width = 80
        self.paddle_height = 10
        self.paddle_speed = 20
        self.paddle = self.canvas.create_rectangle(
            (self.canvas_width - self.paddle_width) / 2, self.canvas_height - 20,
            (self.canvas_width + self.paddle_width) / 2, self.canvas_height - 10,
            fill="white"
        )

        # Ball properties
        self.ball_radius = 8
        self.ball = self.canvas.create_oval(
            self.canvas_width / 2 - self.ball_radius, self.canvas_height / 2 - self.ball_radius,
            self.canvas_width / 2 + self.ball_radius, self.canvas_height / 2 + self.ball_radius,
            fill="red"
        )
        self.ball_dx = random.choice([-3, 3])
        self.ball_dy = -3

        # Bricks properties
        self.brick_rows = 5
        self.brick_cols = 8
        self.brick_width = self.canvas_width / self.brick_cols
        self.brick_height = 20
        self.bricks = []
        self.create_bricks()

        # Score properties
        self.score = 0
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", fill="white", font=("Arial", 14))

        # Speed increment properties
        self.speed_increment_interval = 5000  # Increase speed every 5 seconds
        self.speed_increment_amount = 0.5
        self.root.after(self.speed_increment_interval, self.increase_speed)

        # Bind controls
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        # Start the game loop
        self.game_running = True
        self.update_game()

    def create_bricks(self):
        colors = ["red", "orange", "yellow", "green", "blue"]
        for row in range(self.brick_rows):
            for col in range(self.brick_cols):
                x1 = col * self.brick_width
                y1 = row * self.brick_height
                x2 = x1 + self.brick_width
                y2 = y1 + self.brick_height
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[row % len(colors)])
                self.bricks.append(brick)

    def move_left(self, event):
        if self.canvas.coords(self.paddle)[0] > 0:
            self.canvas.move(self.paddle, -self.paddle_speed, 0)

    def move_right(self, event):
        if self.canvas.coords(self.paddle)[2] < self.canvas_width:
            self.canvas.move(self.paddle, self.paddle_speed, 0)

    def update_game(self):
        if not self.game_running:
            return

        # Move the ball
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        ball_coords = self.canvas.coords(self.ball)

        # Bounce off walls
        if ball_coords[0] <= 0 or ball_coords[2] >= self.canvas_width:
            self.ball_dx = -self.ball_dx

        # Bounce off the top
        if ball_coords[1] <= 0:
            self.ball_dy = -self.ball_dy

        # Ball hits the paddle
        paddle_coords = self.canvas.coords(self.paddle)
        if (ball_coords[2] >= paddle_coords[0] and ball_coords[0] <= paddle_coords[2] and
                ball_coords[3] >= paddle_coords[1] and ball_coords[3] <= paddle_coords[3]):
            self.ball_dy = -self.ball_dy

        # Ball hits a brick
        for brick in self.bricks:
            brick_coords = self.canvas.coords(brick)
            if (ball_coords[2] >= brick_coords[0] and ball_coords[0] <= brick_coords[2] and
                    ball_coords[3] >= brick_coords[1] and ball_coords[1] <= brick_coords[3]):
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                self.ball_dy = -self.ball_dy
                self.score += 10
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                break

        # Game over condition
        if ball_coords[3] >= self.canvas_height:
            self.game_running = False
            self.canvas.create_text(
                self.canvas_width / 2, self.canvas_height / 2,
                text="Game Over", fill="white", font=("Arial", 24)
            )

        # Win condition
        if not self.bricks:
            self.game_running = False
            self.canvas.create_text(
                self.canvas_width / 2, self.canvas_height / 2,
                text="You Win!", fill="white", font=("Arial", 24)
            )

        # Schedule the next update
        if self.game_running:
            self.root.after(20, self.update_game)

    def increase_speed(self):
        if self.game_running:
            self.ball_dx += self.speed_increment_amount if self.ball_dx > 0 else -self.speed_increment_amount
            self.ball_dy += self.speed_increment_amount if self.ball_dy > 0 else -self.speed_increment_amount
            self.root.after(self.speed_increment_interval, self.increase_speed)

if __name__ == "__main__":
    root = tk.Tk()
    game = BreakoutGame(root)
    root.mainloop()


# In[ ]:




