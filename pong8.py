import turtle
import time
import random
import pygame

# pygame mixer for sound playback
pygame.mixer.init()
background_music = pygame.mixer.Sound("background.mp3")
collision_sound = pygame.mixer.Sound("collision.wav")
# Play background music on a continuous loop
background_music.play(loops=-1)

# Game Configuration
CONFIG = {
    "SCREEN_WIDTH": 1000,
    "SCREEN_HEIGHT": 700,
    "COLORS": {
        "bg": "#111122",
        "ball": "#ffaa00",
        "paddles": ["#00ffff", "#ff00ff"],
        "text": "#ffffff",
        "trail": "#ffffff"
    },
    "DIFFICULTY": {
        "speeds": [3, 4, 5, 6, 7],            # Ball speeds for levels 1-5
        "paddle_speeds": [30, 40, 50, 60, 70]   # Paddle speeds for levels 1-5
    },
    "WINNING_SCORE": 7,
    "BALL_SIZE": 1.5
}

# Game window initialization
screen = turtle.Screen()
screen.title("MegaPong Xtreme - Ultimate Showdown")
screen.bgcolor(CONFIG["COLORS"]["bg"])
screen.setup(width=CONFIG["SCREEN_WIDTH"], height=CONFIG["SCREEN_HEIGHT"])
screen.tracer(0)

# Draw center line and circle
def draw_center_elements():
    center_draw = turtle.Turtle()
    center_draw.color(CONFIG["COLORS"].get("centerline", "white"))
    center_draw.penup()
    center_draw.hideturtle()

    # Draw center line
    center_draw.goto(0, -350)
    center_draw.setheading(90)
    center_draw.pensize(3)
    for _ in range(35):
        center_draw.pendown()
        center_draw.forward(10)
        center_draw.penup()
        center_draw.forward(10)

    # Draw center circle
    center_draw.goto(100, 0)
    center_draw.pendown()
    center_draw.circle(100)
    center_draw.penup()

draw_center_elements()

# Game Entities
class TurboPaddle(turtle.Turtle):
    def __init__(self, color, position):
        super().__init__()
        self.speed(0)
        self.shape("square")
        self.color(color)
        self.my_color = color  # to Store the original color string
        self.shapesize(stretch_wid=6, stretch_len=1.5)
        self.penup()
        self.goto(position)
        self.score = 0
        self.dy = 0  # Movement direction indicator

class HyperBall(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(stretch_wid=CONFIG["BALL_SIZE"])
        self.color(CONFIG["COLORS"]["ball"])
        self.penup()
        self.speed(0)
        self.dx = 0
        self.dy = 0
        self.trail = []

# Gameobjects
paddle_left = TurboPaddle(CONFIG["COLORS"]["paddles"][0], (-450, 0))
paddle_right = TurboPaddle(CONFIG["COLORS"]["paddles"][1], (450, 0))
ball = HyperBall()

# text
ui = turtle.Turtle()
ui.speed(0)
ui.hideturtle()
ui.color(CONFIG["COLORS"]["text"])
ui.penup()

# Globalvariables for player names and difficulty 
player1_name = "CYBER P1"
player2_name = "NEO P2"
current_difficulty = 3

# Inputfunctions for paddlemovement
def move_paddle(paddle):
    speed = CONFIG["DIFFICULTY"]["paddle_speeds"][current_difficulty - 1]
    new_y = paddle.ycor() + (speed * paddle.dy * 0.2)
    paddle.sety(max(-280, min(280, new_y)))

def bind_keys():
    screen.listen()
    # Left Paddle Controls
    screen.onkeypress(lambda: setattr(paddle_left, 'dy', 1), "w")
    screen.onkeypress(lambda: setattr(paddle_left, 'dy', -1), "s")
    screen.onkeyrelease(lambda: setattr(paddle_left, 'dy', 0), "w")
    screen.onkeyrelease(lambda: setattr(paddle_left, 'dy', 0), "s")
    # Right Paddle Controls
    screen.onkeypress(lambda: setattr(paddle_right, 'dy', 1), "Up")
    screen.onkeypress(lambda: setattr(paddle_right, 'dy', -1), "Down")
    screen.onkeyrelease(lambda: setattr(paddle_right, 'dy', 0), "Up")
    screen.onkeyrelease(lambda: setattr(paddle_right, 'dy', 0), "Down")

def check_collisions():
    if ball.ycor() > 330:
        ball.dy = -abs(ball.dy)
        ball.sety(330)
    elif ball.ycor() < -330:
        ball.dy = abs(ball.dy)
        ball.sety(-330)
    for paddle, direction in [(paddle_left, 1), (paddle_right, -1)]:
        paddle_edge = paddle.xcor() + (30 * direction)
        if ((direction == 1 and ball.dx < 0) or (direction == -1 and ball.dx > 0)):
            if abs(ball.xcor() - paddle_edge) < 20 and abs(ball.ycor() - paddle.ycor()) < 60:
                ball.dx = -ball.dx * 1.05
                offset = (ball.ycor() - paddle.ycor()) * 0.1
                ball.dy += offset
                ball.setx(paddle_edge)
                collision_sound.play()

def update_trail():
    trail = turtle.Turtle()
    trail.shape("circle")
    trail.shapesize(stretch_wid=CONFIG["BALL_SIZE"] * 0.8)
    trail.color(CONFIG["COLORS"]["trail"])
    trail.penup()
    trail.goto(ball.pos())
    ball.trail.append(trail)
    if len(ball.trail) > 3:
        old = ball.trail.pop(0)
        old.hideturtle()
        del old

def update_ui():
    ui.clear()
    ui.goto(0, 295)
    ui.write(f"{player1_name.upper()}                   {player2_name.upper()}",
        align="center", font=("Arial Black", 24, "bold"))
    ui.goto(0, 260)
    ui.write(f"  SCORE: {paddle_left.score}                  SCORE: {paddle_right.score}  ",
        align="center", font=("Consolas", 20, "italic"))
    ui.goto(-350,300 )
    ui.write(f"LEVEL: {current_difficulty}",
        align="right", font=("Consolas", 20, "italic"))


def reset_ball():
    ball.goto(0, 0)
    ball.dx = CONFIG["DIFFICULTY"]["speeds"][current_difficulty - 1] * random.choice([1, -1])
    ball.dy = CONFIG["DIFFICULTY"]["speeds"][current_difficulty - 1] * random.choice([1, -1])
    for trail in ball.trail:
        trail.hideturtle()
    ball.trail.clear()

def game_loop():
    while True:
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)
        move_paddle(paddle_left)
        move_paddle(paddle_right)
        check_collisions()
        update_trail()
        if ball.xcor() > 500:
            paddle_left.score += 1
            reset_ball()
        elif ball.xcor() < -500:
            paddle_right.score += 1
            reset_ball()
        update_ui()
        screen.update()
        time.sleep(0.01)
        if max(paddle_left.score, paddle_right.score) >= CONFIG["WINNING_SCORE"]:
            show_victory()
            break

def show_victory():
    winner = paddle_left if paddle_left.score >= CONFIG["WINNING_SCORE"] else paddle_right
    winner_name = player1_name if paddle_left.score >= CONFIG["WINNING_SCORE"] else player2_name
    ui.goto(0, 0)
    ui.color(winner.my_color)
    ui.write(f"{winner_name.upper()} WINS!", align="center", font=("Impact", 72, "bold"))
    time.sleep(3)

def setup_game():
    global player1_name, player2_name, current_difficulty
    name1 = screen.textinput("Player 1", "Enter Left Warrior Name (default CYBER P1):")
    player1_name = name1.title() if name1 and name1.strip() != "" else "CYBER P1"
    name2 = screen.textinput("Player 2", "Enter Right Champion Name (default NEO P2):")
    player2_name = name2.title() if name2 and name2.strip() != "" else "NEO P2"
    level = screen.numinput("Challenge Level", "Enter Intensity (1-5):",
       default=current_difficulty, minval=1, maxval=5)
    current_difficulty = int(level) if level else 3
    paddle_left.score = 0
    paddle_right.score = 0
    reset_ball()
    bind_keys()

# replay loop
while True:
    setup_game()
    game_loop()
    replay = screen.textinput("Game Over", "Play again? (yes/no):")
    if not replay or not replay.strip().lower().startswith("y"):
        break

screen.bye()