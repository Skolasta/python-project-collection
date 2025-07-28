import turtle
import random

# --- SCREEN SETUP ---
# Create a screen object
screen = turtle.Screen()
screen.bgcolor("lightskyblue")
screen.title("Turtle Clicker Game")


top_height = screen.window_height() / 2
# Position the text at 90% of the top screen height
y_position = top_height * 0.9

# --- SCORE SETUP ---
# Turtle to display the score
score_turtle = turtle.Turtle()
score_turtle.hideturtle()
score_turtle.penup()
score_turtle.color("black")
# Position the score turtle at the top center
score_turtle.goto(0, y_position)

# Score variable
score = 0

def update_score():
    """Clears the old score and writes the new one."""
    score_turtle.clear()
    score_turtle.write(f"Score: {score}", align="center", font=("Arial", 22, "bold"))

# --- TIMER SETUP ---
# Turtle to display the timer
timer_turtle = turtle.Turtle()
timer_turtle.hideturtle()
timer_turtle.penup()
timer_turtle.color("darkred")
# Position the timer just below the score
timer_turtle.goto(0, y_position - 30)

# Timer variable (in seconds)
time_left = 30

def update_timer():
    """Updates the countdown timer every second."""
    global time_left
    if time_left > 0:
        time_left -= 1
        timer_turtle.clear()
        timer_turtle.write(f"Time Left: {time_left}", align="center", font=("Arial", 18, "normal"))
        # Schedule this function to run again after 1000 ms (1 second)
        screen.ontimer(update_timer, 1000)
    else:
        # Game over sequence
        clickable_turtle.hideturtle() # Hide the clickable turtle
        clickable_turtle.onclick(None)  # Disable click event
        timer_turtle.clear()
        timer_turtle.goto(0, 0)
        timer_turtle.write("Game Over!", align="center", font=("Arial", 36, "bold"))

# --- CLICKABLE TURTLE SETUP ---
# The main turtle that the player will click
clickable_turtle = turtle.Turtle()
clickable_turtle.shape("turtle")
clickable_turtle.shapesize(stretch_wid=2, stretch_len=2) # Make the turtle bigger
clickable_turtle.color("forestgreen")
clickable_turtle.speed("fastest") # Use "fastest" to avoid animation when moving
clickable_turtle.penup()

def move_turtle():
    """Moves the turtle to a new random position on the screen."""
    new_x = random.randint(-250, 250)
    new_y = random.randint(-200, 200)
    clickable_turtle.goto(new_x, new_y)

def handle_click(x, y):
    """Increases score and moves the turtle when clicked."""
    global score
    if time_left > 0: # Only allow scoring if the game is running
        score += 1
        update_score()
        move_turtle()

# Bind the click event to the handle_click function
clickable_turtle.onclick(handle_click)

# --- START THE GAME ---
update_score() # Display initial score (Score: 0)
update_timer() # Start the countdown
move_turtle()  # Move to the first random position

# Keep the window open
turtle.done()
