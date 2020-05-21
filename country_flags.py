#
# Draw country flags with the Python Turtle. Have fun!
#
# Peace, coolcornucopia.
#
# Python ressources:
#   https://docs.python.org/3/library/turtle.html
#
# Wikipedia ressources:
#   https://en.wikipedia.org/wiki/List_of_aspect_ratios_of_national_flags
#   https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes

from turtle import Turtle, Screen
import unicodedata # Use to sort strings with accents, see strip_accents()

# This is our "current turtle (ct)"
ct = Turtle()

# TODO (resolution, default white background)
screen = Screen()



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

def rectangle_3_vertical_strips(x, y, length, height,
                                  col1, col2, col3):
    l = length / 3
    ct.color(col1, col1)
    rectangle_filled(x, y, l, height)
    ct.color(col2, col2)
    rectangle_filled(x + l, y, l, height)
    ct.color(col3, col3)
    rectangle_filled(x + 2 * l, y, l, height)

def rectangle_3_horizontal_strips(x, y, length, height,
                                    col1, col2, col3):
    h = height / 3
    ct.color(col1, col1)
    rectangle_filled(x, y, length, h)
    ct.color(col2, col2)
    rectangle_filled(x, y - h, length, h)
    ct.color(col3, col3)
    rectangle_filled(x, y - 2 * h, length, h)

def rectangle_circle(rect_x, rect_y, length, height,
                     circ_center_x, circ_center_y, diameter,
                     rect_col, circ_col):
    ct.color(rect_col, rect_col)
    rectangle_filled(rect_x, rect_y, length, height)
    ct.color(circ_col, circ_col)
    circle_filled(circ_center_x, circ_center_y, diameter)


### Country flag drawing functions ###

# Note Following functions do not take into account directly the
# aspect ratio and the border, so you can use them directly
# depending of your need... or via the class with proper aspect ratio :-)
# TODO re-order by country names
def flag_Germany(x, y, length, height):
    rectangle_3_horizontal_strips(x, y, length, height,
                                    '#000', '#D00', '#FFCE00')

def flag_Armenia(x, y, length, height):
    rectangle_3_horizontal_strips(x, y, length, height,
                                    '#D90012', '#0033A0', '#F2A800')

def flag_Austria(x, y, length, height):
    rectangle_3_horizontal_strips(x, y, length, height,
                                    '#ED2939', 'white', '#ED2939')

def flag_Bangladesh(x, y, length, height):
    rectangle_circle(x, y, length, height,
                     x + length * 450/1000, y - height / 2, 2 * length / 5,
                     '#006a4e', '#f42a41')

def flag_Belgium(x, y, length, height):
    rectangle_3_vertical_strips(x, y, length, height,
                                  'black', '#FAE042', '#ED2939')

def flag_Benin(x, y, length, height):
    h = height / 2
    ct.color('#FCD116')
    rectangle_filled(x, y, length, h)
    ct.color('#E8112D')
    rectangle_filled(x, y - h, length, h)
    ct.color('#008751')
    rectangle_filled(x, y, length / 2.5, height)

def flag_Myanmar(x, y, length, height):
    rectangle_3_horizontal_strips(x, y, length, height,
                                    '#FECB00', '#34B233', '#EA2839')
    ct.color('white')
    h = 2 * height / 3
    d = h / 0.951  # See five_pointed_star_filled() computations
    five_pointed_star_filled(x + length / 2, y - height / 1.92, d)

def flag_Bolivia(x, y, length, height):
    rectangle_3_vertical_strips(x, y, length, height,
                                  'black', '#FAE042', '#ED2939')

def flag_Bulgaria(x, y, length, height):
    rectangle_3_horizontal_strips(x, y, length, height,
                                    'white', '#00966E', '#D62612')

def flag_Ivory_Coast(x, y, length, height):
    rectangle_3_vertical_strips(x, y, length, height,
                                  '#f77f00', 'white', '#009e60')

def flag_Estonia(x, y, length, height):
    rectangle_3_horizontal_strips(x, y, length, height,
                                    '#0072ce', 'black', 'white')

def flag_France(x, y, length, height):
    rectangle_3_vertical_strips(x, y, length, height,
                                  '#002395', 'white', '#ED2939')

def flag_Gabon(x, y, length, height):
    rectangle_3_horizontal_strips(x, y, length, height,
                                    '#3a75c4', '#fcd116', '#009e60')

def flag_United_States(x, y, length, height):
    # White background
    ct.color('white')
    rectangle_filled(x, y, length, height)
    # The seven red strips
    ct.color('#B22234')
    h = height / 13  # 7 red + 5 white strips = 13
    yy = y
    for i in range(7):
        rectangle_filled(x, yy , length, h)
        yy -= 2 * h
    # The blue rectangle
    ct.color('#3C3B6E')
    rectangle_filled(x, y, length / 2.5, height * 7 / 13)
    # The white stars
    # TODO is it possible to simplify the 2 loops
    ct.color('white')
    # ct.color('#717095', 'white') # false antialiasing if big flag
    elx = length / 30
    ely = length / 28
    ey = y - ely
    for yy in range(5):
        ex = x + elx
        for xx in range(6):
            five_pointed_star_filled(ex, ey, elx)
            ex += 2 * elx
        ey -= 2 * ely

    ey = y - (2 * ely)
    for yy in range(4):
        ex = x + (2 * elx)
        for xx in range(5):
            five_pointed_star_filled(ex, ey, elx)
            ex += 2 * elx
        ey -= 2 * ely

def flag_Japan(x, y, length, height):
    rectangle_circle(x, y, length, height,
                     x + length / 2, y - height / 2, 2 * length / 5,
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

flags_list.append(Flag("United States", 10/19, flag_United_States))
flag_test = flag_Myanmar

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

debug = False
#debug = True

fast_draw = True
#fast_draw = False
if fast_draw:
    # Set speed to max   # TODO useful as we use tracer(0)?
    ct.speed(0)
    # Hide the turtle
    ct.hideturtle()
    # We will manage when needed the scren update with screen.update()
    screen.tracer(False)

# Blue border, red inside
ct.color('black', 'red')

# Pen thickness
ct.pensize(1)

# Drawing primitives test (set debug = True above)
if debug:
    ct.color('black', 'red')
    ct.pensize(1)
    cross(0, 0, 40)
    circle(0, 0, 40)
    circle_filled(40, 0, 40)
    square(60, 20, 40)
    square_filled(100, 20, 40)
    if fast_draw:
        screen.update()
    k = input("Press ENTER to continue")
    rectangle(-20, -20, 80, 40)
    if fast_draw:
        screen.update()
    k = input("Press ENTER to continue")

    rectangle_filled(60, -20, 80, 40)
    #ct.color("black")
    if fast_draw:
        screen.update()
    k = input("Press ENTER to continue")

    x, y, w, h = five_pointed_star(0, -80, 40)
    rectangle(x, y, w, h) # Rectangle containing the star

    five_pointed_star_filled(40, -80, 40)
    if fast_draw:
        screen.update()
    k = input("Press ENTER to continue")
    ct.clear()


flag_border_col = 'black'

#flag_armenie(0, 0, 100, 100)
flag_test(-300, 200, 400, 400*2/3)
if fast_draw:
    screen.update()
k = input("Press ENTER to continue")
ct.clear()

if debug:
    print("Country list in alphabetical order:")
    for d in flags_list:
        print(d.country)

print("There are already " + str(len(flags_list)) +
      " flags, great job!")

draw_all_flags(100, 20)

if fast_draw:
    screen.update()
