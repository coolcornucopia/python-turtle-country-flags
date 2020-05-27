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


### CONFIGURATION ###

KEY_EXIT = "Escape"
MOUSE_BUTTON_EXIT = 2   # mouse buttons: 1 left, 2 center, 3 right
MOUSE_BUTTON_NORMAL = 1

COUNTRY_NAMES_FILENAME = "country_names"
DEFAULT_LANGUAGE = "en"

fast_draw = True

flag_border_col = 'black'

debug = False
#debug = True


### GLOBAL VARIABLES ###

# This is our "current turtle (ct)"
ct = Turtle()

# TODO (resolution, default white background)
screen = Screen()

my_screenclicked = False
my_keypressed = False

country_names = {}  # Content depends on the language


### DRAWING PRIMITIVES ###

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

def rectangle(x, y, width, height):
    prepare_drawing(x, y)
    # Note: we may use a loop but it does not bring that much
    ct.forward(width)
    ct.right(90)
    ct.forward(height)
    ct.right(90)
    ct.forward(width)
    ct.right(90)
    ct.forward(height)

def rectangle_filled(x, y, width, height):
    ct.begin_fill()
    rectangle(x, y, width, height)
    ct.end_fill()

def square(x, y, width):
    rectangle(x, y, width, width)

def square_filled(x, y, width):
    rectangle_filled(x, y, width, width)

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
def five_pointed_star(center_x, center_y, width):
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
def five_pointed_star_filled(center_x, center_y, width):
    ct.begin_fill()
    x, y, w, h = five_pointed_star(center_x, center_y, width)
    ct.end_fill()
    return x, y, w, h


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


### COUNTRY FLAG DRAWING FUNCTIONS ###

# Note Following functions do not take into account directly the
# aspect ratio and the border, so you can use them directly
# depending of your need... or via the class with proper aspect ratio :-)
# TODO re-order by country names
def flag_Germany(x, y, width, height):
    horizontal_strips(x, y, width, height, '#000', '#D00', '#FFCE00')

def flag_Armenia(x, y, width, height):
    horizontal_strips(x, y, width, height, '#D90012', '#0033A0', '#F2A800')

def flag_Austria(x, y, width, height):
    horizontal_strips(x, y, width, height, '#ED2939', 'white', '#ED2939')

def flag_Bangladesh(x, y, width, height):
    rectangle_circle(x, y, width, height, 45/100, 1/2, 2/5,
                     '#006a4e', '#f42a41')

def flag_Belgium(x, y, width, height):
    vertical_strips(x, y, width, height, 'black', '#FAE042', '#ED2939')

def flag_Benin(x, y, width, height):
    h = height / 2
    ct.color('#FCD116')
    rectangle_filled(x, y, width, h)
    ct.color('#E8112D')
    rectangle_filled(x, y - h, width, h)
    ct.color('#008751')
    rectangle_filled(x, y, width / 2.5, height)

def flag_Myanmar(x, y, width, height):
    horizontal_strips(x, y, width, height, '#FECB00', '#34B233', '#EA2839')
    ct.color('white')
    h = 2 * height / 3
    d = h / 0.951  # See five_pointed_star_filled() computations
    five_pointed_star_filled(x + width / 2, y - height / 1.92, d)

def flag_Bolivia(x, y, width, height):
    vertical_strips(x, y, width, height, 'black', '#FAE042', '#ED2939')

def flag_Bulgaria(x, y, width, height):
    horizontal_strips(x, y, width, height, 'white', '#00966E', '#D62612')

def flag_Ivory_Coast(x, y, width, height):
    vertical_strips(x, y, width, height, '#f77f00', 'white', '#009e60')

def flag_Estonia(x, y, width, height):
    horizontal_strips(x, y, width, height, '#0072ce', 'black', 'white')

def flag_France(x, y, width, height):
    vertical_strips(x, y, width, height, '#002395', 'white', '#ED2939')

def flag_Gabon(x, y, width, height):
    horizontal_strips(x, y, width, height, '#3a75c4', '#fcd116', '#009e60')

def flag_Sweden(x, y, width, height):
    ct.color("#006AA7")
    rectangle_filled(x, y, width, height)
    cross_filled(x, y, width, height, 6/16, 5/10,
                 1/8, 1/5, '#FECC00')


def flag_United_States(x, y, width, height):
    # Red & white strips
    r = '#B22234'
    w = 'white'
    horizontal_strips(x, y, width, height, r, w, r, w, r, w, r, w, r, w,
                      r, w, r)
    # The blue rectangle
    # Note - 1 in y-axis for a better alignment
    ct.color('#3C3B6E')
    rectangle_filled(x, y, width / 2.5, 7 * height / 13 - 1)
    # The white stars
    ct.color('white')
    #ct.color('#717095', 'white') # false antialiasing if big flag
    star_width = width / 30
    star_height = width / 28
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

def flag_Japan(x, y, width, height):
    rectangle_circle(x, y, width, height, 1/2, 1/2, 2/5,
                     'white', '#bc002d')


### FLAGS MANAGEMENT FUNCTIONS ###

class Flag:
    ratio_variable = False  # TODO find a better way
    ratio_default = 2/3
    def __init__(self, country_code, ratio, drawing_func):
        self.country_code = country_code
        if self.ratio_variable:
            self.ratio = ratio
        else:
            self.ratio = self.ratio_default
        self.drawing_func = drawing_func

    def draw(self, x, y, width):
        self.drawing_func(x, y, width,
                                width * self.ratio)


# List of all the flags
# TODO re-order by country names
flags_list = list()
flags_list.append(Flag(276,  3/5 , flag_Germany))
flags_list.append(Flag( 51,  1/2 , flag_Armenia))
flags_list.append(Flag( 40,  2/3 , flag_Austria))
flags_list.append(Flag( 50,  3/5 , flag_Bangladesh))
flags_list.append(Flag( 56, 13/15, flag_Belgium))
flags_list.append(Flag(204,  2/3 , flag_Benin))
flags_list.append(Flag(104,  3/3 , flag_Myanmar))

flags_list.append(Flag( 68, 15/22, flag_Bolivia))
flags_list.append(Flag(100,  3/5 , flag_Bulgaria))
flags_list.append(Flag(384,  2/3 , flag_Ivory_Coast))
flags_list.append(Flag(233,  7/11, flag_Estonia))
flags_list.append(Flag(250,  2/3 , flag_France))
flags_list.append(Flag(266,  3/4 , flag_Gabon))

flags_list.append(Flag(752, 10/19, flag_Sweden))
flags_list.append(Flag(840, 10/19, flag_United_States))

flags_list.append(Flag(392,  2/3 , flag_Japan))


# Function to remove accents, useful for sorting, else "États-Unis" (fr)
# will be the last of the sorting list in French
# https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string/518232#518232
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')


# TODO improve sorting (by name vs by country code)
# Flag list alphabetical sort thanks to a lambda function
#flags_list.sort(key=lambda x: strip_accents(x.country))

# Flag list sort thanks to a lambda function
flags_list.sort(key=lambda x: x.country_code)


def draw_all_flags(width, border, affiche_texte = False):
    # on récupère la taille de la fenètre
    window_width = screen.window_width()
    window_height = screen.window_height()
    #setup(window_width * 1.0, window_height * 1.0)
    #print(screensize(), screen.window_width(), screen.window_height())
    flags_num = len(flags_list)
    x_start = -(window_width / 2) + border # TODO rename border please
    y_start = (window_height / 2) - border
    flags_horiz_max = int((window_width - 2 * border) / width)
    print(flags_horiz_max)
    # TODO rename border_inside
    border_inside = (window_width - (2 * border)) - (flags_horiz_max * width)
    border_inside /= (flags_horiz_max - 1)
    if border_inside < 5:
        flags_horiz_max -= 1
        border_inside = (window_width - (2 * border)) - (flags_horiz_max * width)
        border_inside /= (flags_horiz_max - 1)
    x = x_start
    y = y_start
    print(x,y, border_inside)
    for i in range(flags_num):
        # Get the flag and draw it
        d = flags_list[i]
        d.draw(x, y, width)
        # Draw the flag border
        ct.color(flag_border_col) # TODO find a better way for color config
        rectangle(x, y, width, width * d.ratio)
        # Next flag
        x += width + border_inside
        if x > (window_width / 2) - border - width:
            x = x_start
            y -= width * 2/3 + border_inside

# Helper function to avoid to test everytime if the country_names
# dictionnary is empty or a country code is missing
def get_country_name(code):
    if code in country_names:
        return country_names[code]
    else:
        return ""

def load_country_names(language):
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
    my_exit()

def my_onscreenclick(x, y):
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
    screen.onscreenclick(my_exit_mouse, btn = MOUSE_BUTTON_EXIT)
    screen.onkey(my_exit, KEY_EXIT)

    screen.onscreenclick(my_onscreenclick, btn = MOUSE_BUTTON_NORMAL)
    screen.onkeypress(my_onkeypress)
    my_screenclicked = False
    my_keypressed = False

    screen.listen()
    frame()


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

    language = "en"
    if not load_country_names(language):
        if not load_country_names(DEFAULT_LANGUAGE):
            print("No country name files found!")
        else:
            print("Use default \"" + DEFAULT_LANGUAGE + "\" language")

    if debug:
        print("Country list in alphabetical order:")
        for d in flags_list:
            print("{:03d}".format(d.country_code),
                  get_country_name(d.country_code))

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

