# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = 160
paddle2_pos = 160
ACCL = 3
init_pos = [WIDTH / 2, HEIGHT / 2]
ball_pos = [WIDTH / 2, HEIGHT / 2]
vel = [2 ,-2]  # pixels per tick
STRIKE_ACCL = 0.1
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel 
    # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
   
    if direction == LEFT:
        vel[0] = random.randrange(2,4)
        vel[1] = random.randrange(-3,-1)
    else:
        vel[0] = random.randrange(-4,-2)
        vel[1] = random.randrange(-3,-1)
    
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, STRIKE_ACCL
         
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
   
    #check collision with right and left gutter
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if paddle1_pos <= ball_pos[1] and ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
             vel[0] = -(vel[0]+vel[0] * STRIKE_ACCL)
        else:
            score2 = score2 + 1
            spawn_ball(LEFT)
        
    elif ball_pos[0] >= WIDTH - ( PAD_WIDTH + BALL_RADIUS):
        if paddle2_pos <= ball_pos[1] and ball_pos[1] <= paddle2_pos + PAD_HEIGHT:
            vel[0] = -(vel[0] + vel[0] * STRIKE_ACCL)
        else:
            score1 = score1 + 1
            spawn_ball(RIGHT)    
    #check collision with top and bottom wall
    elif ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS :
       vel[1] = -vel[1]
         
    # update ball
    ball_pos[0] = ball_pos[0] + vel[0]
    ball_pos[1] = ball_pos[1] + vel[1]        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel ) <= HEIGHT - PAD_HEIGHT and (paddle1_pos + paddle1_vel ) >= 0:
        paddle1_pos = paddle1_pos + paddle1_vel
    if (paddle2_pos + paddle2_vel ) <= HEIGHT - PAD_HEIGHT and (paddle2_pos + paddle2_vel ) >= 0:
        paddle2_pos = paddle2_pos + paddle2_vel
     
    # draw paddles
    canvas.draw_polygon(([0,paddle1_pos],[8,paddle1_pos],[8,paddle1_pos + PAD_HEIGHT ],[0,paddle1_pos + PAD_HEIGHT]), 2, "Blue","Blue")
    canvas.draw_polygon(([592,paddle2_pos],[600,paddle2_pos],[600,paddle2_pos + PAD_HEIGHT ],[592,paddle2_pos + PAD_HEIGHT]), 2, "Blue","Blue")
    # draw scores
    canvas.draw_text(str(score1),[145,25],30,"White")
    canvas.draw_text(str(score2),[445,25],30,"White") 
    
def keydown(key):
    global paddle1_vel, paddle2_vel, ACCL
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = paddle2_vel - ACCL
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = paddle2_vel + ACCL
    if key ==  simplegui.KEY_MAP["w"]:
        paddle1_vel = paddle1_vel - ACCL
    if key ==  simplegui.KEY_MAP["s"]:
        paddle1_vel = paddle1_vel + ACCL
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = paddle2_vel + ACCL
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = paddle2_vel - ACCL
    if key ==  simplegui.KEY_MAP["w"]:
        paddle1_vel = paddle1_vel + ACCL
    if key ==  simplegui.KEY_MAP["s"]:
        paddle1_vel = paddle1_vel - ACCL
def restart_handler():
    score1 = score2 = 0
    new_game()
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', restart_handler)

# start frame
new_game()
frame.start()

