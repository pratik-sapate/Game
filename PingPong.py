import os
import turtle
from finger_detection import HandDetection
import cv2

screen = turtle.Screen()
screen_width, screen_height = 1500, 800
screen.title("Ping Pong Game")
screen.bgcolor('Black')
screen.setup(screen_width, screen_height)

# left slide
left_slide = turtle.Turtle()
left_slide.speed(0)
left_slide.shape('square')
left_slide.color('White')
left_slide.shapesize(stretch_wid=6, stretch_len=1)
left_slide.penup()
left_slide.goto(-1*screen_width//2+50, 0)

# right slide
right_slide = turtle.Turtle()
right_slide.speed(0)
right_slide.shape('square')
right_slide.color('White')
right_slide.shapesize(stretch_wid=6, stretch_len=1)
right_slide.penup()
right_slide.goto(screen_width//2-50, 0)

# ball
ball = turtle.Turtle()
ball.shape('circle')
ball.color('Red')
ball.speed(45)
ball.penup()
ball.dx = 5
ball.dy = -5

# writable
score = 0
writable = turtle.Turtle()
writable.speed(0)
writable.penup()
writable.color('Yellow')
writable.goto(-100, screen_height // 2 - 50)
writable.write("Score : " + str(score), font=("Courier", 24, "normal"))


hand_detection = HandDetection()
video_cam = cv2.VideoCapture(0)

while True:
    left_x, left_y, right_x, right_y = None, None, None, None
    ret, image = video_cam.read()
    image = cv2.flip(image, 1)
    image = cv2.resize(image, (screen_width, screen_height))
    wid, heigh, _ = image.shape
    # cv2.imshow('frame', image)
    left, right = hand_detection.get_point_finger_coordinate(image)
    if left != None and right == None:
        left_x, left_y = left
        left_y = -1 * int(left_y - screen_height / 2)
        left_slide.sety(left_y)
    elif left == None and right != None:
        right_x, right_y = right
        right_y = -1 * int(right_y - screen_height / 2)
        right_slide.sety(right_y)
    elif left != None and right != None:
        left_x, left_y = left
        left_y = -1 * int(left_y - screen_height / 2)
        left_slide.sety(left_y)
        right_x, right_y = right
        right_y = -1 * int(right_y - screen_height / 2)
        right_slide.sety(right_y)

    screen.update()
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    if ball.ycor() > screen.window_height() / 2:
        ball.sety(screen.window_height() / 2)
        ball.dy *= -1

    if ball.ycor() < -screen.window_height() / 2:
        ball.sety(-screen.window_height() / 2)
        ball.dy *= -1

    if ball.xcor() > screen.window_width() / 2 - 50:
        ball.goto(0, 0)
        score = 0
        ball.dy = -5

    if ball.xcor() < -screen.window_width() / 2 + 50:
        ball.goto(0, 0)
        ball.dy = -5
        score = 0

    if ball.xcor() > right_slide.xcor() - 30 and (
            right_slide.ycor() - 50 < ball.ycor() < right_slide.ycor() + 50):
        # print('right : ', right_slide.xcor(), right_slide.ycor())
        score += 1
        ball.dx *= -1
        ball.dx = ball.dx + 1 if ball.dx > 0 else ball.dx - 1

    if ball.xcor() < left_slide.xcor() + 30 and (
            left_slide.ycor() - 50 < ball.ycor() < left_slide.ycor() + 50):
        # print('left : ', left_slide.xcor(), left_slide.ycor())
        score += 1
        ball.dx *= -1
        ball.dx = ball.dx + 1 if ball.dx > 0 else ball.dx - 1
    writable.clear()
    writable.write("Score : " + str(score), font=("Courier", 24, "normal"))
