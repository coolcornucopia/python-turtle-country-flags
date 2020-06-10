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
import math
import locale
import unicodedata # Use to sort strings with accents, see strip_accents()
import time


### CONFIGURATION ###

KEY_EXIT = "Escape"
MOUSE_BUTTON_EXIT = 2   # mouse buttons: 1 left, 2 center, 3 right
MOUSE_BUTTON_NORMAL = 1

COUNTRY_NAMES_FILENAME = "country_names"
DEFAULT_LANGUAGE = "en"

fast_draw = True

FLAG_BORDER_COL = 'black'
FLAG_DEFAULT_RATIO = 2/3  # preferred flag ratio size between width & height

FULLSCREEN = True

DEBUG = False
#DEBUG = True


### GLOBAL VARIABLES ###

# This is our "current turtle (ct)"
ct = Turtle()

# TODO (resolution, default white background)
screen = Screen()
if FULLSCREEN:
    screen.setup(width = 1.0, height = 1.0)

my_screenclicked = False
my_keypressed = False

country_names = {}  # Content depends on the language


### DRAWING PRIMITIVES ###

# Useful fonction to move the pen and reset the turtle orientation
def prepare_drawing(x, y, rotation=0):
    ct.penup()
    ct.goto(x, y)
    # The orientation is set by default to the right.
    # In standard mode: 0=east 90=north 180=west 270=south
    # In logo mode: 0=north 90=east 180=south 270=west
    # Here we are in the standard mode
    # rotation parameter is then counter-clockwise
    ct.setheading(rotation)
    ct.pendown()

def rectangle(x, y, width, height, rotation=0):
    prepare_drawing(x, y, rotation)
    # Note: we may use a loop but it does not bring that much
    ct.forward(width)
    ct.right(90)
    ct.forward(height)
    ct.right(90)
    ct.forward(width)
    ct.right(90)
    ct.forward(height)

def rectangle_filled(x, y, width, height, rotation=0):
    ct.begin_fill()
    rectangle(x, y, width, height, rotation)
    ct.end_fill()

def square(x, y, width, rotation=0):
    rectangle(x, y, width, width, rotation)

def square_filled(x, y, width, rotation=0):
    rectangle_filled(x, y, width, width, rotation)

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

# The cross is inside a "width" diameter circle
def cross(center_x, center_y, width):
    # Move on the cross left then draw
    prepare_drawing(center_x - (width / 2), center_y)
    ct.forward(width)
    # Move on the cross top then draw
    prepare_drawing(center_x, center_y + (width / 2))
    ct.right(90)
    ct.forward(width)

# This five pointed star function draws a star "standing with arms open
# horizontally" and a span of "width" and returns the coordinates and sizes
# of the surrounding rectangle, it is then easier to align the star with
# other shapes. The drawing algorithm has been adapted from
# https://stackoverflow.com/questions/26356543/turtle-graphics-draw-a-star
# TODO better document rotation (clockwise here)
def five_pointed_star(center_x, center_y, width, rotation=0):
    # https://rechneronline.de/pi/pentagon.php
    # d = width
    # a = pentagon side = 0,618 * d
    # h = height = 0,951 * d
    # ri = radius of the inscribed circle = 0,425 * d
    # rc = radius of the circumscribed circle = 0,526 * d
    d = width
    h = 0.951 * d
    rc = 0.526 * d

    # Default: angle = 144 for a straight star, we may try different
    # values for a more or less pointed star...
    angle = 144
    branch = d / 2.6
    prepare_drawing(center_x + d / 2 - branch, center_y + d / 6, rotation)

    for _ in range(5):
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
def five_pointed_star_filled(center_x, center_y, width, rotation=0):
    ct.begin_fill()
    x, y, w, h = five_pointed_star(center_x, center_y, width, rotation)
    ct.end_fill()
    return x, y, w, h

def polygon(poly):
    ct.penup()
    for x, y in poly:
        ct.goto(x, y)
        if not ct.isdown():
            ct.pendown()
    ct.goto(tuple(poly[0])) # close the polygon

def polygon_filled(poly):
    ct.begin_fill()
    polygon(poly)
    ct.end_fill()

# A "start=0" angle corresponds to the bottom of the pie (Python
# Turtle convention).
def pie(center_x, center_y, diameter, start, end):
    # Move the circle center following Turtle circle() usage
    prepare_drawing(center_x, center_y - diameter / 2)
    # Save the initial fill context and stop it temporarily
    filling = ct.filling()
    ct.end_fill()
    # Move the turtle at the start position with the start angle
    # and save this start position
    ct.penup()
    ct.circle(diameter / 2, start)
    x, y = ct.pos()
    # Restore the filling context is necessary and draw the circle arc
    ct.pendown()
    if filling:
        ct.begin_fill()
    ct.circle(diameter / 2, end - start)
    # Close the pie slice
    ct.goto(center_x, center_y) # Go to the pie slice center
    ct.goto(x, y)               # Go to the start position

def pie_filled(center_x, center_y, diameter, start, end):
    ct.begin_fill()
    pie(center_x, center_y, diameter, start, end)
    ct.end_fill()


### HELPER FUNCTIONS FOR FLAGS DRAWING ###

# TODO better document below functions
def vertical_strips(x, y, width, height, *colors):
    nc = len(colors)
    if nc <= 0:
        # TODO Better manage error here below
        print(func_name + ": Bad color value")
        return
    w = width / nc  # TODO round?
    for i in range(nc):
        ct.color(colors[i])
        rectangle_filled(x + i * w, y, w, height)

def horizontal_strips(x, y, width, height, *colors):
    nc = len(colors)
    if nc <= 0:
        # TODO Better manage error here below
        print(func_name + ": Bad color value")
        return
    h = height / nc  # TODO round?
    for i in range(nc):
        ct.color(colors[i])
        rectangle_filled(x, y - i * h, width, h)

# TODO Document parameters
def rectangle_circle(x, y, width, height,
                     circ_center_x_r, circ_center_y_r,
                     circ_diam_r, background_col, circ_col):
    ct.color(background_col)
    rectangle_filled(x, y, width, height)
    ct.color(circ_col)
    circ_center_x = x + width * circ_center_x_r
    circ_center_y = y - height * circ_center_y_r
    diameter = width * circ_diam_r
    circle_filled(circ_center_x, circ_center_y, diameter)

# TODO Document parameters
def cross_filled(x, y, width, height,
                 cross_center_x_r, cross_center_y_r,
                 cross_width_r, cross_height_r, col):
    ct.color(col)
    w = width * cross_width_r
    h = height * cross_height_r
    x1 = x + width * cross_center_x_r - (w / 2)
    y1 = y - height * cross_center_y_r + (h / 2)
    rectangle_filled(x1, y, w, height)
    rectangle_filled(x, y1, width, h)

def rectangle_filled_color(x, y, width, height, color, rotation=0):
    ct.color(color)
    rectangle_filled(x, y, width, height, rotation)

def circle_filled_color(center_x, center_y, diameter, color):
    ct.color(color)
    circle_filled(center_x, center_y, diameter)

def five_pointed_star_filled_color(center_x, center_y, width, color, rotation=0):
    ct.color(color)
    five_pointed_star_filled(center_x, center_y, width, rotation)

def polygon_filled_color(poly, color):
    ct.color(color)
    polygon_filled(poly)

def pie_filled_color(center_x, center_y, diameter, start, end, color):
    ct.color(color)
    pie_filled(center_x, center_y, diameter, start, end)

def circle_coord(center_x, center_y, radius, angle_pc):
    angle_rad = (2 * math.pi) * angle_pc
    x = center_x + radius * math.cos(angle_rad)
    y = center_y + radius * math.sin(angle_rad)
    return x, y


### COUNTRY FLAG DRAWING FUNCTIONS ###

# Note Following functions do not take into account directly the
# aspect ratio and the border, so you can use them directly
# depending of your need... or via the class with proper aspect ratio :-)
def flag_Armenia(x, y, width, height):
    horizontal_strips(x, y, width, height, '#D90012', '#0033A0', '#F2A800')

def flag_Austria(x, y, width, height):
    horizontal_strips(x, y, width, height, '#ED2939', 'white', '#ED2939')

def flag_Bahamas(x, y, width, height):
    horizontal_strips(x, y, width, height, '#00778B', '#FFC72C', '#00778B')
    polygon_filled_color(((x, y), (x + width/2.3, y - height/2),
                          (x, y - height)), 'black')

def flag_Bangladesh(x, y, width, height):
    rectangle_circle(x, y, width, height, 45/100, 1/2, 2/5,
                     '#006a4e', '#f42a41')

def flag_Belgium(x, y, width, height):
    vertical_strips(x, y, width, height, 'black', '#FAE042', '#ED2939')

def flag_Benin(x, y, width, height):
    horizontal_strips(x, y, width, height, '#FCD116', '#E8112D')
    rectangle_filled_color(x, y, width / 2.5, height, '#008751')

def flag_Bolivia(x, y, width, height):
    horizontal_strips(x, y, width, height, '#D52B1E', '#F9E300', '#007934')
    # TODO Please finalize me

def flag_Botswana(x, y, width, height):
    rectangle_filled_color(x, y, width, height, '#6DA9D2')
    rectangle_filled_color(x, y - height * 3/8, width, height/4, 'white')
    rectangle_filled_color(x, y - height/2.4, width, height/6, 'black')

def flag_Bulgaria(x, y, width, height):
    horizontal_strips(x, y, width, height, 'white', '#00966E', '#D62612')

def flag_Cameroon(x, y, width, height):
    vertical_strips(x, y, width, height, '#007A5E', '#CE1126', '#FCD116')
    five_pointed_star_filled_color(x + width/2, y - height/2, width/6, '#FCD116')

def flag_China(x, y, width, height):
    rectangle_filled_color(x, y, width, height, '#DE2910')
    bsw = width * 19 / 100 # big star width
    ssw = bsw / 3          # small star width
    ct.color('#FFDE00')
    five_pointed_star_filled(x + width * 1/6, y - height * 1/4, bsw)
    five_pointed_star_filled(x + width * 1/3, y - height * 1/10, ssw, 360-23)
    five_pointed_star_filled(x + width * 2/5, y - height * 1/5, ssw, 360-46)
    five_pointed_star_filled(x + width * 2/5, y - height * 7/20, ssw, 360-70)
    five_pointed_star_filled(x + width * 1/3, y - height * 9/20, ssw, 360-21)

def flag_Estonia(x, y, width, height):
    horizontal_strips(x, y, width, height, '#0072ce', 'black', 'white')

def flag_Finland(x, y, width, height):
    rectangle_filled_color(x, y, width, height, 'white')
    cross_filled(x, y, width, height, 65/180, 1/2, 1/6, 3/11, '#003580')

def flag_France(x, y, width, height):
    vertical_strips(x, y, width, height, '#002395', 'white', '#ED2939')

def flag_Gabon(x, y, width, height):
    horizontal_strips(x, y, width, height, '#009e60', '#fcd116', '#3a75c4')

def flag_Gambia(x, y, width, height):
    horizontal_strips(x, y, width, height, '#CE1126', 'white', '#3A7728')
    rectangle_filled_color(x, y - height/2.57, width, height/4.5, '#0C1C8C')

def flag_Germany(x, y, width, height):
    horizontal_strips(x, y, width, height, '#000', '#D00', '#FFCE00')

def flag_Greece(x, y, width, height):
    b = '#0D5EAF'
    w = 'white'
    horizontal_strips(x, y, width, height, *([b, w] * 4 + [b]))
    rectangle_filled_color(x, y, width * 0.37, height * 5/9 - 1, b)
    cross_filled(x, y, width * 0.37, height * 5/9 - 1, 1/2, 1/2,
                 1/13.5/0.37, 1/9/(5/9), w)

def flag_Iceland(x, y, width, height):
    rectangle_filled_color(x, y, width, height, '#02529C')
    cross_filled(x, y, width, height, 0.36, 1/2, 16/100, 2/9, 'white')
    cross_filled(x, y, width, height, 0.36, 1/2, 8/100, 1/9, '#DC1E35')

def flag_India(x, y, width, height):
    horizontal_strips(x, y, width, height, '#F93', 'white', '#128807')
    # Draw the Ashoka Chakra (wheel of 24 spokes & half-circles)
    cx = x + width / 2
    cy = y - height / 2
    circle_filled_color(cx, cy, width * 17.8/100, '#008')
    circle_filled_color(cx, cy, width * 15.6/100, 'white')
    circle_filled_color(cx, cy, width * 3.1/100, '#008')
    # Radius of circles linked to the polygon spokes
    radius_internal = width * 12/1350
    radius_middle = width * 42.15/1350
    radius_external = width * 105/1350
    angle_spoke = 4.9 / 360 # 4.9 degrees
    for i in [x/24 for x in range(24)]:  # 0/24, 1/24, 2/24...
        ### The polygon spoke
        ct.color('#008')
        ct.penup()
        ct.goto(circle_coord(cx, cy, radius_internal, i))
        ct.pendown()
        ct.begin_fill()
        ct.goto(circle_coord(cx, cy, radius_middle, i - angle_spoke))
        ct.goto(circle_coord(cx, cy, radius_external, i))
        ct.goto(circle_coord(cx, cy, radius_middle, i + angle_spoke))
        ct.goto(circle_coord(cx, cy, radius_internal, i))
        ct.end_fill()
        # The circle
        xx, yy = circle_coord(cx, cy, radius_external, i + 0.5/24)
        circle_filled_color(xx, yy, width * 10.5/1350, '#008')

def flag_Indonesia(x, y, width, height):
    horizontal_strips(x, y, width, height, 'red', 'white')

def flag_Ivory_Coast(x, y, width, height):
    vertical_strips(x, y, width, height, '#f77f00', 'white', '#009e60')

def flag_Japan(x, y, width, height):
    rectangle_circle(x, y, width, height, 1/2, 1/2, 2/5,
                     'white', '#bc002d')
def flag_Myanmar(x, y, width, height):
    horizontal_strips(x, y, width, height, '#FECB00', '#34B233', '#EA2839')
    h = 2 * height / 3
    d = h / 0.951  # See five_pointed_star_filled() computations
    five_pointed_star_filled_color(x + width / 2, y - height / 1.9, d, 'white')

def flag_Pakistan(x, y, width, height):
    rectangle_filled_color(x, y, width * 1/4, height, 'white')
    rectangle_circle(x + width * 1/4, y, width * 3/4, height, 0.5, 0.5, 360/675, '#01411C', 'white')
    circle_filled_color(x + width * 608/900, y - height * 259/600, width * 330/900, '#01411C')
    ct.color('white')
    five_pointed_star_filled(x + width * 652/900, y - height * 216/600, width * 114/900, 23)

def flag_Russia(x, y, width, height):
    horizontal_strips(x, y, width, height, 'white', '#0039A6', '#D52B1E')

def flag_Seychelles(x, y, width, height):
    bl = (x, y - height) # bottom left
    xw = x + width
    w = width / 3
    h = height / 3
    polygon_filled_color((bl, (x, y), (x + w, y)), '#003F87')
    polygon_filled_color((bl, (x + w, y), (x + w * 2, y)), '#FCD856')
    polygon_filled_color((bl, (x + w * 2, y), (xw, y), (xw, y - h)), '#D62828')
    polygon_filled_color((bl, (xw, y - h), (xw, y - h * 2)), 'white')
    polygon_filled_color((bl, (xw, y - h * 2), (xw, y - height)), '#007a3d')

def flag_Somalia(x, y, width, height):
    rectangle_filled_color(x, y, width, height, '#4189DD')
    five_pointed_star_filled_color(x + width/2, y - height/2, width/3.28, 'white')

def flag_Sweden(x, y, width, height):
    rectangle_filled_color(x, y, width, height, '#006AA7')
    cross_filled(x, y, width, height, 3/8, 1/2, 1/8, 1/5, '#FECC00')

def flag_United_Kingdom(x, y, width, height):
    rectangle_filled_color(x, y, width, height, '#012169')
    r = x + width   # right-x
    b = y - height  # bottom-y
    w = width / 27  # 1 unit on x-axis related to the diagonal
    h = height / 27 # 1 unit on y-axis related to the diagonal
    # Cross of Saint Andrew
    polygon_filled_color(((x, y), (x, y - 3*h), (r - 3*w, b), (r, b), (r, b + 3*h), (x + 3*w, y)), 'white')
    polygon_filled_color(((x, b), (x + 3*w, b), (r, y - 3*h), (r, y), (r - 3*w, y), (x, b + 3*h)), 'white')
    # Cross of Saint Patrick
    polygon_filled_color(((x, y), (x, y - 2*h), (x +  7*w, y - 9*h), (x + 9*w, y - 9*h)), '#C8102E')
    polygon_filled_color(((r, b), (r, b + 2*h), (r -  7*w, b + 9*h), (r - 9*w, b + 9*h)), '#C8102E')
    polygon_filled_color(((x, b), (x + 2*w, b), (x + 11*w, b + 9*h), (x + 9*w, b + 9*h)), '#C8102E')
    polygon_filled_color(((r, y), (r - 2*w, y), (r - 11*w, y - 9*h), (r - 9*w, y - 9*h)), '#C8102E')
    # Cross of Saint George
    cross_filled(x, y, width, height, 1/2, 1/2, 1/6, 1/3, 'white')
    cross_filled(x, y, width, height, 1/2, 1/2, 1/10, 1/5, '#C8102E')

def flag_United_States(x, y, width, height):
    # 7 Red & 6 white strips
    r = '#B22234'
    w = 'white'
    horizontal_strips(x, y, width, height, *([r, w] * 6 + [r])) # r,w,r,w...,r
    # The blue rectangle
    # Note - 1 in y-axis for a better alignment
    rectangle_filled_color(x, y, width / 2.5, 7 * height / 13 - 1, '#3C3B6E')
    # The white stars
    ct.color('white')
    #ct.color('#717095', 'white') # false antialiasing if big flag
    star_width = width / 32.5
    star_height = height / 18.6
    star_width_between = width / 15
    star_y = y - star_height
    stars_in_row = 5
    for _ in range(9):                 # vertical loop
        if stars_in_row == 6:          # switch between 5 & 6 row stars
            stars_in_row = 5
            star_x = x + star_width_between
        else:
            stars_in_row = 6
            star_x = x + (star_width_between / 2)
        for _ in range(stars_in_row):  # horizontal loop
            five_pointed_star_filled(star_x, star_y, star_width)
            star_x += star_width_between
        star_y -= star_height


### FLAGS MANAGEMENT FUNCTIONS ###

class Flag(object):
    def __init__(self, country_code, ratio, drawing_func):
        self.country_code = country_code
        self.ratio = ratio
        self.drawing_func = drawing_func

    def draw(self, x, y, width, height):
        self.drawing_func(x, y, width, height)

    def draw_ratio(self, x, y, width):
        self.drawing_func(x, y, width, width * self.ratio)

# Dictionnary of all the flags (the key is the flag drawing function)
flags_dict = dict()
flags_dict[flag_Armenia]       = Flag( 51,  1/2 , flag_Armenia)
flags_dict[flag_Austria]       = Flag( 40,  2/3 , flag_Austria)
flags_dict[flag_Bahamas]       = Flag( 44,  1/2 , flag_Bahamas)
flags_dict[flag_Bangladesh]    = Flag( 50,  3/5 , flag_Bangladesh)
flags_dict[flag_Belgium]       = Flag( 56, 13/15, flag_Belgium)
flags_dict[flag_Benin]         = Flag(204,  2/3 , flag_Benin)
flags_dict[flag_Bolivia]       = Flag( 68, 15/22, flag_Bolivia)
flags_dict[flag_Botswana]      = Flag( 72,  2/3 , flag_Botswana)
flags_dict[flag_Bulgaria]      = Flag(100,  3/5 , flag_Bulgaria)
flags_dict[flag_Cameroon]      = Flag(120,  2/3 , flag_Cameroon)
flags_dict[flag_China]         = Flag(156,  2/3 , flag_China)
flags_dict[flag_Estonia]       = Flag(233,  7/11, flag_Estonia)
flags_dict[flag_Finland]       = Flag(246, 11/18, flag_Finland)
flags_dict[flag_France]        = Flag(250,  2/3 , flag_France)
flags_dict[flag_Gabon]         = Flag(266,  3/4 , flag_Gabon)
flags_dict[flag_Gambia]        = Flag(270,  2/3 , flag_Gambia)
flags_dict[flag_Germany]       = Flag(276,  3/5 , flag_Germany)
flags_dict[flag_Greece]        = Flag(300,  2/3 , flag_Greece)
flags_dict[flag_Iceland]       = Flag(352, 18/25, flag_Iceland)
flags_dict[flag_India]         = Flag(356,  2/3 , flag_India)
flags_dict[flag_Indonesia]     = Flag(360,  2/3 , flag_Indonesia)
flags_dict[flag_Ivory_Coast]   = Flag(384,  2/3 , flag_Ivory_Coast)
flags_dict[flag_Japan]         = Flag(392,  2/3 , flag_Japan)
flags_dict[flag_Myanmar]       = Flag(104,  2/3 , flag_Myanmar)
flags_dict[flag_Pakistan]      = Flag(586,  2/3 , flag_Pakistan)
flags_dict[flag_Russia]        = Flag(643,  2/3 , flag_Russia)
flags_dict[flag_Seychelles]    = Flag(690,  1/2 , flag_Seychelles)
flags_dict[flag_Somalia]       = Flag(706,  2/3 , flag_Somalia)
flags_dict[flag_Sweden]        = Flag(752,  5/8 , flag_Sweden)
flags_dict[flag_United_Kingdom]= Flag(826,  1/2 , flag_United_Kingdom)
flags_dict[flag_United_States] = Flag(840, 10/19, flag_United_States)


# Function to remove accents, useful for sorting, else "États-Unis" (fr)
# will be the last of the sorting list in French
# https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string/518232#518232
def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

# Sort the flags dictionnary by country code
sorted(flags_dict.items(), key=lambda x: x[1].country_code)


def draw_all_flags(width, border, country_names=False, ratio=False):
    global flags_dict
    # Get window size
    window_width = screen.window_width()
    window_height = screen.window_height()
    #setup(window_width * 1.0, window_height * 1.0)
    #print(screensize(), screen.window_width(), screen.window_height())
    flags_num = len(flags_dict)
    x_start = -(window_width / 2) + border # TODO rename border please
    y_start = (window_height / 2) - border
    flags_horiz_max = int((window_width - 2 * border) / width)
    print(flags_horiz_max)
    # TODO rename border_inside
    border_inside = (window_width - (2 * border)) - (flags_horiz_max * width)
    border_inside /= (flags_horiz_max - 1)
    if border_inside < border:
        flags_horiz_max -= 1
        border_inside = (window_width - (2 * border)) - (flags_horiz_max * width)
        border_inside /= (flags_horiz_max - 1)
    x = x_start
    y = y_start
    print(x, y, border_inside)
    for i in flags_dict:
        # Get the flag and draw it
        flag = flags_dict[i]
        if ratio:
            h = width * flag.ratio
            flag.draw_ratio(x, y, width)
        else:
            h = width * FLAG_DEFAULT_RATIO
            flag.draw(x, y, width, h)
        # Draw the flag border
        ct.color(FLAG_BORDER_COL) # TODO find a better way for color config
        rectangle(x, y, width, h)
        # Add the flag name
        if country_names:
            ct.penup()
            ct.goto(x + width / 2, y)
            name = get_country_name(flag.country_code)
            ct.write(name, align="center", font=("Arial", 11, "normal"))
        # Next flag
        x += width + border_inside
        if x > (window_width / 2) - border - width:
            x = x_start
            y -= width * 2/3 + border_inside # TODO 2/3 here is not so nice

# Helper function to avoid to test everytime if the country_names
# dictionnary is empty or a country code is missing
def get_country_name(code):
    global country_names
    name = ""
    if code in country_names:
        name = country_names[code]

    return name

def load_country_names(language):
    global country_names
    country_names.clear()
    filename = COUNTRY_NAMES_FILENAME + '.' + language
    try:
        with open(filename) as fh:
            for line in fh:
                if line.startswith("#"): # Ignore commented lines
                    continue
                code, country_name = line.rstrip().split(";")
                country_names[int(code)] = country_name

    except FileNotFoundError as fnf_error:
        print(fnf_error)
        return False
    except AssertionError as error:
        print(error)
        return False

    #print(country_names)
    return True


### EVENTS MANAGEMENT ###

def my_exit():
    print("Bye")
    screen.bye()

def my_exit_mouse(x, y):
    #pylint: disable=unused-argument
    my_exit()

def my_onscreenclick(x, y):
    #pylint: disable=unused-argument
    global my_screenclicked
    my_screenclicked = True
    #print("my_screenclicked =", my_screenclicked, x, y)

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
    screen.onscreenclick(my_exit_mouse, btn=MOUSE_BUTTON_EXIT)
    screen.onkey(my_exit, KEY_EXIT)

    screen.onscreenclick(my_onscreenclick, btn=MOUSE_BUTTON_NORMAL)
    screen.onkeypress(my_onkeypress)
    global my_screenclicked
    global my_keypressed
    my_screenclicked = False
    my_keypressed = False

    screen.listen()
    frame()


### SCREEN UPDATE HELPERS ###

# TODO rename me + test all parameters
def update_configure(fast=True, speed=2):
    global fast_draw
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
    global fast_draw
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
    # Get window size
    win_w = screen.window_width()
    win_h = screen.window_height()
    w = win_w * 90/100 # remove 5% borders
    h = w * FLAG_DEFAULT_RATIO
    flag_function_name(-w/2, h/2, w, h)
    # Add a border
    ct.color(FLAG_BORDER_COL)
    rectangle(-w/2, h/2, w, h)

def test_flag_class(flag_function_name, ratio=False):
    # Get window size
    win_w = screen.window_width()
    win_h = screen.window_height()
    w = win_w * 90/100 # remove 5% borders
    # Get the flag element and draw it according to its size ratio
    flag = flags_dict[flag_function_name]
    if ratio:
        h = w * flag.ratio
        flag.draw_ratio(-w/2, h/2, w)
    else:
        h = w * FLAG_DEFAULT_RATIO
        flag.draw(-w/2, h/2, w, h)
    # Add a border
    ct.color(FLAG_BORDER_COL)
    rectangle(-w/2, h/2, w, h)

def screenshot(filename="screenshot"):
    # Screenshot
    # Note: The last drawing call is not captured in the screenshot
    # so the workaround consists in adding an extra command (here penup).
    # TODO Discuss with the communauty about this weird behaviour...
    ct.penup()
    filename += ".eps"
    screen.getcanvas().postscript(file=filename, colormode='color')
    print("Screenshot done, filename =", filename)


### MAIN ###

def main():
    # Black border, red inside
    ct.color('black', 'red')
    # Pen thickness
    ct.pensize(1)

    update_configure(True)  # TODO Does not work

    install_event_management()

    # Load country names according to the language
    # Note: below commented lines are for debugging languages
    #locale.setlocale(locale.LC_ALL, "en_US.utf8")
    #locale.setlocale(locale.LC_ALL, "fr_FR.utf8")
    #locale.setlocale(locale.LC_ALL, "it_IT.utf8")
    #locale.setlocale(locale.LC_ALL, "de_DE.utf8")
    loc = locale.getlocale()
    language = loc[0].split("_", 1)[0]  # convert "en_US" to "en"
    #print(loc[0], language)

    if not load_country_names(language):
        if not load_country_names(DEFAULT_LANGUAGE):
            print("No country name files found!")
        else:
            print("Use default \"" + DEFAULT_LANGUAGE + "\" language")

    if DEBUG:
        print("\nCountry list in country code order:")
        for key, value in flags_dict.items():
            print("{:03d}".format(value.country_code),
                  get_country_name(value.country_code))

        print("\nCountry list in alphabetical order:")
        # Make a copy before modifying it
        tmp_flags_dict = flags_dict.copy()
        # Flag dict alphabetical sort thanks to a lambda function
        sorted(tmp_flags_dict.items(), key=lambda x:
               strip_accents(get_country_name(x[1].country_code)))
        for key, value in tmp_flags_dict.items():
            print(get_country_name(value.country_code) + "(" +
                  "{:03d}".format(value.country_code) + ")")
        del tmp_flags_dict

        print("\nThere are already " + str(len(flags_dict)) +
              " flags, great job!\n")

    #test_primitives()
    #test_flag(flag_Armenia)
    #test_flag_class(flag_United_States, False)
    #test_flag_class(flag_France, True)
    #screenshot("flag_France")
    draw_all_flags(160, 60, country_names=True, ratio=False)
    update_do()
    return "Ready"

if __name__ == "__main__":
    msg = main()
    print(msg)
    mainloop()
