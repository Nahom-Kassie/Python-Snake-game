import turtle
import random

w = 500
h = 500
food_size = 10
delay = 100

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}

def reset():
    global snake, snake_dir, food_position
    # Clear any existing stamps before resetting
    pen.clearstamps()

    snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
    snake_dir = "up"
    food_position = get_random_food_position()
    food.goto(food_position)
    # We don't call move_snake() here because it's already running in the timer loop

def move_snake():
    global snake_dir, food_position

    new_head = snake[-1].copy()
    new_head[0] = snake[-1][0] + offsets[snake_dir][0]
    new_head[1] = snake[-1][1] + offsets[snake_dir][1]

    # Check for self-collision
    if new_head in snake:
        reset()
    else:
        snake.append(new_head)

        # Check for food collision
        if not food_collision():
            snake.pop(0) # Remove tail if no food eaten

        # Screen wrapping logic
        if snake[-1][0] > w // 2:
            snake[-1][0] -= w
        elif snake[-1][0] < - w // 2:
            snake[-1][0] += w
        elif snake[-1][1] > h // 2:
            snake[-1][1] -= h
        elif snake[-1][1] < -h // 2:
            snake[-1][1] += h

        pen.clearstamps()

        # Draw snake
        for segment in snake:
            pen.goto(segment[0], segment[1])
            pen.stamp()

        screen.update()

    # Schedule the next move
    turtle.ontimer(move_snake, delay)

def food_collision():
    global food_position
    if get_distance(snake[-1], food_position) < 20:
        food_position = get_random_food_position()
        food.goto(food_position)
        return True
    return False

def get_random_food_position():
    # Use // for integer division to avoid TypeError
    x = random.randint(- w // 2 + food_size, w // 2 - food_size)
    y = random.randint(- h // 2 + food_size, h // 2 - food_size)
    return (x, y)

def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5

def go_up():
    global snake_dir
    if snake_dir != "down":
        snake_dir = "up"

def go_right():
    global snake_dir
    if snake_dir != "left":
        snake_dir = "right"

def go_down():
    global snake_dir
    if snake_dir != "up":
        snake_dir = "down"

def go_left():
    global snake_dir
    if snake_dir != "right":
        snake_dir = "left"

# Screen setup
screen = turtle.Screen()
screen.setup(w, h)
screen.title("Snake Game")
screen.bgcolor("green")
screen.tracer(0)

# Snake pen setup
pen = turtle.Turtle("square")
pen.penup()
pen.color("white")

# Food setup
food = turtle.Turtle()
food.shape("square")
food.color("yellow")
food.shapesize(food_size / 20)
food.penup()

# Event listeners
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")

# Start the game
reset()
move_snake() # Start the movement loop
turtle.done()