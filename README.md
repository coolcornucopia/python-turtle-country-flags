# Python Turtle Country Flags :snake: :turtle:
Draw many country flags with the great Python Turtle.
Have fun!

## If you are learning Python...
If you are learning Python, please **do not simply copy/paste the source code from here because you will not really learn programming** :-(... Instead, try first to do your **programming homeworks & challenges** then come back to have a look to what I propose here... and the most important: **Have fun programming the Python Turtle :smile:**.

## Screenshots
|     |     |     |
| :-: | :-: | :-: |
| ![Python Turtle Bahamas flag](screenshots/flag_Bahamas.png?raw=true "Python Turtle Bahamas flag") | ![Python Turtle Bangladesh flag](screenshots/flag_Bangladesh.png?raw=true "Python Turtle Bangladesh flag") | ![Python Turtle Botswana flag](screenshots/flag_Botswana.png?raw=true "Python Turtle Botswana flag") |
| ![Python Turtle Cameroon flag](screenshots/flag_Cameroon.png?raw=true "Python Turtle Cameroon flag") | ![Python Turtle China flag](screenshots/flag_China.png?raw=true "Python Turtle China flag") | ![Python Turtle Gambia flag](screenshots/flag_Gambia.png?raw=true "Python Turtle Gambia flag") |
| ![Python Turtle Greece flag](screenshots/flag_Greece.png?raw=true "Python Turtle Greece flag") | ![Python Turtle Iceland flag](screenshots/flag_Iceland.png?raw=true "Python Turtle Iceland flag") | ![Python Turtle India flag](screenshots/flag_India.png?raw=true "Python Turtle India flag") |
| ![Python Turtle Pakistan flag](screenshots/flag_Pakistan.png?raw=true "Python Turtle Pakistan flag") | ![Python Turtle Seychelles flag](screenshots/flag_Seychelles.png?raw=true "Python Turtle Seychelles flag") | ![Python Turtle Somalia flag](screenshots/flag_Somalia.png?raw=true "Python Turtle Somalia flag") |
| ![Python Turtle South Korea flag](screenshots/flag_South_Korea.png?raw=true "Python Turtle South Korea flag") | ![Python Turtle United Kingdom flag](screenshots/flag_United_Kingdom.png?raw=true "Python Turtle United Kingdom flag") | ![Python Turtle United States flag](screenshots/flag_United_States.png?raw=true "Python Turtle United States flag") |


![Python Turtle flags (page 1)](screenshots/flag_All_page_1.png?raw=true "Python Turtle country flags")

|     |     |
| :-: | :-: |
| ![Python Turtle South Korea flag animation](screenshots/flag_South_Korea_gifsicle_o3_colors_256.gif?raw=true "Python Turtle South Korea flag animation") | ![Python Turtle United Kingdom flag animation](screenshots/flag_United_Kingdom_gifsicle_o3_colors_256.gif?raw=true "Python Turtle United Kingdom flag animation") |


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

## Any questions or comments are welcome :bird:
If you have any comments or questions, feel free to send me an email at coolcornucopia@outlook.com :email:.

--

Peace

coolcornucopia :smile:
