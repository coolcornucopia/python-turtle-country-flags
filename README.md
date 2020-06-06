# Python Turtle Country Flags :snake: :turtle:
Draw many country flags with the great Python Turtle.
Have fun!

## If you are learning Python...
If you are learning Python, please **do not simply copy/paste the source code from here because you will not really learn programming** :-(... Instead, try first to do your **programming homeworks & challenges** then come back to have a look to what I propose here... and the most important: **Have fun programming the Python Turtle :smile:**.

## Screenshots
![China flag](screenshots/flag_China.png?raw=true "flag_China")
![India flag](screenshots/flag_India.png?raw=true "flag_India")
![Japan flag](screenshots/flag_Japan.png?raw=true "flag_Japan")
![United State flag](screenshots/flag_United_States.png?raw=true "flag_United_States")
![flags (page 1)](screenshots/flag_All_page_1.png?raw=true "flag_All_page_1")

## Requirements regarding this source code
There are various ways for drawing flags, hereafter my own requirements list:
* **No Python external modules** to avoid dependencies (PIL, svg, pygame...).
* **Country flags close to original ones**.
* **Not "too complex" Python code**.
* **Country drawing flag functions as short as possible** using good and readable helpers, in order to be easily copy/paste somewhere else. Below a short example:
```Python
def flag_Bulgaria(x, y, width, height):
    horizontal_strips(x, y, width, height, 'white', '#00966E', '#D62612')

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
...
# Draw flags (simple function calls)
flag_Bulgaria(0, 0, 100, 67)
flag_China(0, 100, 100, 67)
...
```

Of course, another solution could be to download Wikipedia svg flags and to draw them with a Python svg library but it was not the goal here :smile:.

## Can I use the source code from here in my application
Yes, you can do whatever you want with the source code here. Please have a look to the [LICENSE](LICENSE) file.

## Comments, questions?
If you have comments or questions, send me a email at coolcornucopia@outlook.com.

--

Peace :smile:

coolcornucopia
