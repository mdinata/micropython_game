import max7219
from machine import Pin, SPI, freq
import utime

#increase CPU clock to 160 MHz
freq(160000000)

#initiate the SPI connection of led matrix
spi=SPI(1, baudrate=10000000, polarity=0, phase=0)
device=max7219.Matrix8x8(spi, Pin(2), 1)
device.fill(0)
device.brightness(10)
utime.sleep(0.1)
device.show()

def getbase(angle):
    if angle==0:
        base_x=0
        base_y=0
    elif angle==180:
        base_x=7
        base_y=7
    return (base_x,base_y)

#rotate the display orientation to 180 degrees
axis=getbase(180)
base_x=axis[0]
base_y=axis[1]

global num_list
num_list=[]

global num_sum
num_sum=0

def dot(x,y,f):
    device.pixel(base_x-x,base_y-y,f)
    device.show()

def clear_font(column):
    font = [(0,1),(0,2),(0,3),(1,1),(1,3),(2,1),(2,3),(3,1),(3,2),(3,3),(4,1),(4,3),(5,1),(5,3),(6,1),(6,2),(6,3)]
    if column == 2:
        for x,y in font:
            dot(x,y+4,0)
    else:
        for x,y in font:
            dot(x,y,0)

#font placed in 1st column
def get_font(value):
    if value == 0:
        font = [(1,1),(1,2),(1,3),(2,1),(2,3),(3,1),(3,3),(4,1),(4,3),(5,1),(5,2),(5,3)]
    if value == 1:
        font = [(1,3),(2,3),(3,3),(4,3),(5,2),(5,3)]
    if value == 2:
        font = [(1,1),(1,2),(1,3),(2,1),(3,1),(3,2),(3,3),(4,3),(5,1),(5,2),(5,3)]
    if value == 3:
        font = [(1,1),(1,2),(1,3),(2,3),(3,1),(3,2),(3,3),(4,3),(5,1),(5,2),(5,3)]
    if value == 4:
        font = [(1,3),(2,3),(3,1),(3,2),(3,3),(4,1),(4,3),(5,1),(5,3)]
    if value == 5:
        font = [(1,1),(1,2),(1,3),(2,3),(3,1),(3,2),(3,3),(4,1),(5,1),(5,2),(5,3)]
    if value == 6:
        font = [(1,1),(1,2),(1,3),(2,1),(2,3),(3,1),(3,2),(3,3),(4,1),(5,1),(5,2),(5,3)]
    if value == 7:
        font = [(1,3),(2,3),(3,3),(4,3),(5,1),(5,2),(5,3)]
    if value == 8:
        font = [(1,1),(1,2),(1,3),(2,1),(2,3),(3,1),(3,2),(3,3),(4,1),(4,3),(5,1),(5,2),(5,3)]
    if value == 9:
        font = [(1,1),(1,2),(1,3),(2,3),(3,1),(3,2),(3,3),(4,1),(4,3),(5,1),(5,2),(5,3)]
    return font

def draw(count):
    num_list.insert(0,count)
    num_sum=str(sum(num_list))
    print(num_sum)

    #if one digit, display the font on the 2nd column (y+4)
    if len(num_sum) == 1:
        #clearing font on the 2nd column
        clear_font(2)
	font=get_font(int(num_sum))
	for x,y in font:
            dot(x,y+4,1)

    #if two digits, display the first digit on 1st column and 2nd digit on 2nd column 
    if len(num_sum) > 1:
        clear_font(1)
        clear_font(2)
        for order, value in enumerate(num_sum):
            font=get_font(int(value))
            for x,y in font:
                if order == 0:
                    dot(x,y,1)
                elif order == 1:
                    dot(x,y+4,1)

    return num_sum
