import MAX7219R
from machine import Pin, SPI,freq, reset
import time

freq(160000000)
spi=SPI(1, baudrate=10000000, polarity=0, phase=0)
device=MAX7219R.Matrix8x8(spi, Pin(2), 1)
device.brightness(5)
device.fill(0)
device.show()

WIDTH = 7
LENGTH =7
GAMEOVER = 0
FRAME=0

s2 = Pin(4, Pin.IN, Pin.PULL_UP) #left
s3 = Pin(0, Pin.IN, Pin.PULL_UP) #right

ball_position=[0,3]
ball_velocity=[1,1]

pad=[[2,7],[3,7],[4,7],[5,7]]
vpad=[[2,6],[3,6],[4,6],[5,6]]

def clear_base():
    for i in range(8):
        device.dot(i,7,0)
    device.show()

def draw_pad(velocity):
    clear_base()
    for x in pad:
        x[0] =(x[0]+velocity)
    for vx in vpad:
        vx[0] =(vx[0]+velocity)        
    for x,y in pad:
        device.dot(x,y,1)
    device.show()

bricks=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],
        [0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],
        [0,2],[1,2],[2,2],[3,2],[4,2],[5,2],[6,2],[7,2]]

def make_brick():
    for a,b in bricks:
        device.dot(a,b,1)
    device.show()

def take_brick(ball):
    device.dot(ball[0],ball[1],0)
    device.show()
    bricks.remove(ball)
    
def draw_ball():
    global ball_position,GAMEOVER,FRAME
    if FRAME %3 ==0:
        device.dot(ball_position[0],ball_position[1],0)
        device.show()
        
        ball_position[0] += ball_velocity[0]
        ball_position[1] += ball_velocity[1]
        
        ball_position = [ball_position[0],ball_position[1]]
        vball_position = [ball_position[0],ball_position[1]-1]
        
        print(ball_position)
        if ball_position[0] == 7:
            ball_velocity[0] = -ball_velocity[0]
        if vball_position in bricks:
            take_brick(vball_position)
            ball_velocity[1] = -ball_velocity[1]    
        if ball_position[1] == 0 or ball_position in vpad:
            ball_velocity[1] = -ball_velocity[1]
        if ball_position[0] == 0:
            ball_velocity[0] = -ball_velocity[0]
        if ball_position[1] >= 7:
            GAMEOVER = 1
            
        device.dot(ball_position[0],ball_position[1],1)   
        device.show()
    
make_brick()
draw_pad(0)

while True:
    if GAMEOVER == 0:
        FRAME += 1
        draw_ball()       
        if s2.value() ==0:
            draw_pad(-1)
        if s3.value() ==0:
            draw_pad(1)       
        time.sleep(0.06)