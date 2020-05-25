#!/usr/bin/env python3
"""
Draw country flags with the Python Turtle.

Have fun!

Peace, coolcornucopia.
https://github.com/coolcornucopia/
"""
#
# Python ressources:
#   https://docs.python.org/3/library/turtle.html
#
# Wikipedia ressources:
#   https://en.wikipedia.org/wiki/List_of_aspect_ratios_of_national_flags
#   https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes

from turtle import Turtle, Screen, mainloop
import unicodedata # Use to sort strings with accents, see strip_accents()
import time

# This is our "current turtle (ct)"
ct = Turtle()

# TODO (resolution, default white background)
screen = Screen()

debug = False
#debug = True

my_screenclicked = False
my_keypressed = False

fast_draw = True

flag_border_col = 'black'

### Drawing primitives ###

# Useful fonction to move the pen and reset the turtle orientation
def prepare_drawing(x, y):
    ct.penup()
    ct.goto(x, y)
    # The orientation is set by default to the right.
    # In standard mode: 0=east 90=north 180=west 270=south
    # In logo mode: 0=north 90=east 180=south 270=west
    # Here we are in the standard mode
    ct.setheading(0)
    ct.pendown()

def rectangle(x, y, length, height):
    prepare_drawing(x, y)
    # Note: we may use a loop but it does not bring that much
    ct.forward(length)
    ct.right(90)
    ct.forward(height)
    ct.right(90)
    ct.forward(length)
    ct.right(90)
    ct.forward(height)

def rectangle_filled(x, y, length, height):
    ct.begin_fill()
    rectangle(x, y, length, height)
    ct.end_fill()

def square(x, y, length):
    rectangle(x, y, length, length)

def square_filled(x, y, length):
    rectangle_filled(x, y, length, length)

# For the circle, use the diameter instead of the radius because it is
# then easier to make objects touch themselves, avoiding x2 in user code.
def circle(center_x, center_y, diameter):
    # Move the circle center following Turtle circle() usage
    prepare_drawing(center_x, center_y - diameter / 2)
    ct.circle(diameter / 2)

def circle_filled(center_x, center_y, diameter):
    ct.begin_fill()
    circle(center_x, center_y, diameter)
    ct.end_fill()

# The cross is inside a "length" diameter circle
def cross(center_x, center_y, length):
    # Move on the cross left then draw
    prepare_drawing(center_x - (length / 2), center_y)
    ct.forward(length)
    # Move on the cross top then draw
    prepare_drawing(center_x, center_y + (length / 2))
    ct.right(90)
    ct.forward(length)


# This five pointed star function draws a star "standing with arms open
# horizontally" and a span of "length" and returns the coordinates and sizes
# of the surrounding rectangle, it is then easier to align the star with
# other shapes. The drawing algorithm has been adapted from
# https://stackoverflow.com/questions/26356543/turtle-graphics-draw-a-star
def five_pointed_star(center_x, center_y, length):
    # https://rechneronline.de/pi/pentagon.php
    # d = length
    # a = pentagon side = 0,618 * d
    # h = height = 0,951 * d
    # ri = radius of the inscribed circle = 0,425 * d
    # rc = radius of the circumscribed circle = 0,526 * d
    d = length
    h = 0.951 * d
    rc = 0.526 * d

    # Default: angle = 144 for a straight star, we may try different
    # values for a more or less pointed star...
    angle = 144
    branch = d / 2.6
    prepare_drawing(center_x + d / 2 - branch, center_y + d / 6)

    for i in range(5):
        ct.forward(branch)
        ct.right(angle)
        ct.forward(branch)
        ct.right((360 / 5) - angle)

    # Surrounding rectangle, uncomment to test
    # rectangle(center_x - d / 2, center_y + rc, d, h)
    # Circumscribed circle, uncomment to test
    # circle(center_x, center_y, rc * 2)

    # Return surrounding rectangle coordinates and sizes.
    return center_x - d / 2, center_y + rc, d, h

# (read five_pointed_star() above function description for details)
def five_pointed_star_filled(center_x, center_y, length):
    ct.begin_fill()
    x, y, l, h = five_pointed_star(center_x, center_y, length)
    ct.end_fill()
    return x, y, l, h


### Helper functions for drawing flags ###

# TODO better document below functions
def vertical_strips(x, y, length, height, *colors):
    nc = len(colors)
    if nc <= 0:
        # TODO Better manage error here below
        print(func_name + ": Bad color value")
        return
    l = length / nc  # TODO round?
    for i in range(nc):
        ct.color(colors[i])
        rectangle_filled(x + i * l, y, l, height)

def horizontal_strips(x, y, length, height, *colors):
    nc = len(colors)
    if nc <= 0:
        # TODO Better manage error here below
        print(func_name + ": Bad color value")
        return
    h = height / nc  # TODO round?
    for i in range(nc):
        ct.color(colors[i])
        rectangle_filled(x, y - i * h, length, h)

# TODO Document parameters
def rectangle_circle(x, y, length, height,
                     circ_center_x_r, circ_center_y_r,
                     circ_diam_r, background_col, circ_col):
    ct.color(background_col)
    rectangle_filled(x, y, length, height)
    ct.color(circ_col)
    circ_center_x = x + length * circ_center_x_r
    circ_center_y = y - height * circ_center_y_r
    diameter = length * circ_diam_r
    circle_filled(circ_center_x, circ_center_y, diameter)

# TODO Document parameters
def cross_filled(x, y, length, height,
                 cross_center_x_r, cross_center_y_r,
                 cross_length_r, cross_height_r, col):
    ct.color(col)
    l = length * cross_length_r
    h = height * cross_height_r
    x1 = x + length * cross_center_x_r - (l / 2)
    y1 = y - height * cross_center_y_r + (h / 2)
    rectangle_filled(x1, y, l, height)
    rectangle_filled(x, y1, length, h)


### Country flag drawing functions ###

# Note Following functions do not take into account directly the
# aspect ratio and the border, so you can use them directly
# depending of your need... or via the class with proper aspect ratio :-)
# TODO re-order by country names
def flag_Germany(x, y, length, height):
    horizontal_strips(x, y, length, height, '#000', '#D00', '#FFCE00')

def flag_Armenia(x, y, length, height):
    horizontal_strips(x, y, length, height, '#D90012', '#0033A0', '#F2A800')

def flag_Austria(x, y, length, height):
    horizontal_strips(x, y, length, height, '#ED2939', 'white', '#ED2939')

def flag_Bangladesh(x, y, length, height):
    rectangle_circle(x, y, length, height, 45/100, 1/2, 2/5,
                     '#006a4e', '#f42a41')

def flag_Belgium(x, y, length, height):
    vertical_strips(x, y, length, height, 'black', '#FAE042', '#ED2939')

def flag_Benin(x, y, length, height):
    h = height / 2
    ct.color('#FCD116')
    rectangle_filled(x, y, length, h)
    ct.color('#E8112D')
    rectangle_filled(x, y - h, length, h)
    ct.color('#008751')
    rectangle_filled(x, y, length / 2.5, height)

def flag_Myanmar(x, y, length, height):
    horizontal_strips(x, y, length, height, '#FECB00', '#34B233', '#EA2839')
    ct.color('white')
    h = 2 * height / 3
    d = h / 0.951  # See five_pointed_star_filled() computations
    five_pointed_star_filled(x + length / 2, y - height / 1.92, d)

def flag_Bolivia(x, y, length, height):
    vertical_strips(x, y, length, height, 'black', '#FAE042', '#ED2939')

def flag_Bulgaria(x, y, length, height):
    horizontal_strips(x, y, length, height, 'white', '#00966E', '#D62612')

def flag_Ivory_Coast(x, y, length, height):
    vertical_strips(x, y, length, height, '#f77f00', 'white', '#009e60')

def flag_Estonia(x, y, length, height):
    horizontal_strips(x, y, length, height, '#0072ce', 'black', 'white')

def flag_France(x, y, length, height):
    vertical_strips(x, y, length, height, '#002395', 'white', '#ED2939')

def flag_Gabon(x, y, length, height):
    horizontal_strips(x, y, length, height, '#3a75c4', '#fcd116', '#009e60')

def flag_Sweden(x, y, length, height):
    ct.color("#006AA7")
    rectangle_filled(x, y, length, height)
    cross_filled(x, y, length, height, 6/16, 5/10,
                 1/8, 1/5, '#FECC00')


def flag_United_States(x, y, length, height):
    # Red & white strips
    r = '#B22234'
    w = 'white'
    horizontal_strips(x, y, length, height, r, w, r, w, r, w, r, w, r, w,
                      r, w, r)
    # The blue rectangle
    # Note - 1 in y-axis for a better alignment
    ct.color('#3C3B6E')
    rectangle_filled(x, y, length / 2.5, 7 * height / 13 - 1)
    # The white stars
    ct.color('white')
    #ct.color('#717095', 'white') # false antialiasing if big flag
    star_width = length / 30
    star_height = length / 28
    star_y = y - star_height
    stars_in_row = 5
    for yy in range(9):
        if stars_in_row == 6:  # switch between 5 & 6 row stars
            stars_in_row = 5
            star_x = x + (2 * star_width)
        else:
            stars_in_row = 6
            star_x = x + star_width
        for xx in range(stars_in_row):
            five_pointed_star_filled(star_x, star_y, star_width)
            star_x += 2 * star_width
        star_y -= star_height

def flag_Japan(x, y, length, height):
    rectangle_circle(x, y, length, height, 1/2, 1/2, 2/5,
                     'white', '#bc002d')


### FLAGS MANAGEMENT FUNCTIONS ###

class Flag:
    ratio_variable = False  # TODO find a better way
    ratio_default = 2/3
    def __init__(self, country, ratio, drawing_func):
        self.country = country # TODO better manage country names (language)
        if self.ratio_variable:
            self.ratio = ratio
        else:
            self.ratio = self.ratio_default
        self.drawing_func = drawing_func

    def draw(self, x, y, length):
        self.drawing_func(x, y, length,
                                length * self.ratio)


# List of all the flags
# TODO re-order by country names
flags_list = list()
flags_list.append(Flag("Germany", 3/5, flag_Germany))
flags_list.append(Flag("Armenia", 1/2, flag_Armenia))
flags_list.append(Flag("Austria", 2/3, flag_Austria))
flags_list.append(Flag("Bangladesh", 3/5, flag_Bangladesh))
flags_list.append(Flag("Belgium", 13/15, flag_Belgium))
flags_list.append(Flag("Benin", 2/3, flag_Benin))
flags_list.append(Flag("Myanmar", 3/3, flag_Myanmar))

flags_list.append(Flag("Bolivia", 15/22, flag_Bolivia))
flags_list.append(Flag("Bulgaria", 3/5, flag_Bulgaria))
flags_list.append(Flag("Ivory Coast", 2/3, flag_Ivory_Coast))
flags_list.append(Flag("Estonia", 7/11, flag_Estonia))
flags_list.append(Flag("France", 2/3, flag_France))
flags_list.append(Flag("Gabon", 3/4, flag_Gabon))

flags_list.append(Flag("Sweden", 10/19, flag_Sweden))
flags_list.append(Flag("United States", 10/19, flag_United_States))

flags_list.append(Flag("Japan", 2/3, flag_Japan))


# Function to remove accents, useful for sorting, else "États-Unis" (fr)
# will be the last of the sorting list in French
# https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string/518232#518232
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

# Flag list alphabetical sort thanks to a lambda function
flags_list.sort(key=lambda x: strip_accents(x.country))


def draw_all_flags(length, border, affiche_texte = False):
    # on récupère la taille de la fenètre
    window_width = screen.window_width()
    window_height = screen.window_height()
    #setup(window_width * 1.0, window_height * 1.0)
    #print(screensize(), screen.window_width(), screen.window_height())
    flags_num = len(flags_list)
    x_start = -(window_width / 2) + border # TODO rename border please
    y_start = (window_height / 2) - border
    flags_horiz_max = int((window_width - 2 * border) / length)
    print(flags_horiz_max)
    # TODO rename border_inside
    border_inside = (window_width - (2 * border)) - (flags_horiz_max * length)
    border_inside /= (flags_horiz_max - 1)
    if border_inside < 5:
        flags_horiz_max -= 1
        border_inside = (window_width - (2 * border)) - (flags_horiz_max * length)
        border_inside /= (flags_horiz_max - 1)
    x = x_start
    y = y_start
    print(x,y, border_inside)
    for i in range(flags_num):
        # Get the flag and draw it
        d = flags_list[i]
        d.draw(x, y, length)
        # Draw the flag border
        ct.color(flag_border_col) # TODO find a better way for color config
        rectangle(x, y, length, length * d.ratio)
        # Next flag
        x += length + border_inside
        if x > (window_width / 2) - border - length:
            x = x_start
            y -= length * 2/3 + border_inside


### MAIN STARTS HERE BELOW ###

def my_onscreenclick(x, y):
    global my_screenclicked
    my_screenclicked = True
    #print("my_screenclicked =", my_screenclicked)

def my_onkeypress():
    global my_keypressed
    my_keypressed = True
    #print("my_keypressed =", my_keypressed)

def frame():
    print("frame...")
    #screen.update()
    screen.ontimer(frame, 1000) # TODO hard coded value

def wait_click_or_key():
    while not my_screenclicked and not my_keypressed:
        screen.update()
        time.sleep(0.5)

def install_event_management():
    # Install event capture
    screen.onscreenclick(my_onscreenclick)
    screen.onkeypress(my_onkeypress)
    my_screenclicked = False
    my_keypressed = False
    frame()


def uninstall_event_manager():
    # Remove events
    screen.onscreenclick(None)
    screen.onkeypress(None)


### SCREEN UPDATE HELPERS ###

# TODO rename me + test all parameters
def update_configure(fast = True, speed = 2):
    fast_draw = fast
    if fast_draw:
        # Set speed to max   # TODO useful as we use tracer(0)?
        ct.speed(0)
        # Hide the turtle
        ct.hideturtle()
        # We will manage when needed the scren update with screen.update()
        screen.tracer(False)
    else:
        ct.speed(speed)
        ct.showturtle() # TODO not useful
        screen.tracer(True) # TODO not useful

def update_do():
    if fast_draw:
        screen.update()


### TEST HELPERS ###

def test_primitives():
    ct.color('black', 'red')
    ct.pensize(1)
    cross(0, 0, 40)
    circle(0, 0, 40)
    circle_filled(40, 0, 40)
    square(60, 20, 40)
    square_filled(100, 20, 40)
    rectangle(-20, -20, 80, 40)
    rectangle_filled(60, -20, 80, 40)
    x, y, w, h = five_pointed_star(0, -80, 40)
    rectangle(x, y, w, h) # Rectangle containing the star
    five_pointed_star_filled(40, -80, 40)

def test_flag(flag_function_name):
    flag_function_name(-300, 200, 400, 400*2/3)


### MAIN ###

def main():
    # Black border, red inside
    ct.color('black', 'red')
    # Pen thickness
    ct.pensize(1)

    update_configure(True)

    install_event_management()

    screen.onkey(screen.bye, "Escape") # TODO please document
    screen.listen()

    if debug:
        print("Country list in alphabetical order:")
        for d in flags_list:
            print(d.country)

        print("There are already " + str(len(flags_list)) +
              " flags, great job!")

    #test_primitives()
    #test_flag(flag_Armenia)
    draw_all_flags(100, 20)
    update_do()
    return "Ready"

if __name__ == "__main__":
    msg = main()
    print(msg)
    mainloop()

