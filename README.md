# Sky Picture Hunt

***Sky Picture Hunt*** is a game about geolocalisation, inspired by Geoguessr, adapted to the universe of <u>*Sky : Children of Light*</u>. <br>
Players have to guess the  location of given screens in the world of Sky. <br>
In order to do so, they can navigate through the menu on the left of the screen to select the name of a realm, of an area and/or of a location where they think the image belongs. <br>

Sky Picture Hunt has **two Game modes** : <br>
- **Daily Picture** : a daily screen for a secret location to guess everyday. <br>
- **Picture Hunt** : free mode to guess as many images as the player wants with three level of difficulties : Easy, Medium, Hard. <br>

The points are based on the precision of the guesses : <br>
1. **100pts** for the realm, <br>
2. **200pts** for the area, <br>
3. **300pts** for the location <br>

# Structure of the project

pichunt_project/ <br>
|- app.py               # Flask application <br>
|- config.py            # Configuration File for important variables and parameters values <br>
|- requirements.txt     # Python dependencies for packages <br>
|- .gitignore           # Files to ignore by Git when pushing <br>
|- README.md            # The documentation of the project <br>
| <br>
|- models/              # Main logic and datas <br>
    |- __init__.py      # To make the folder a Python package <br>
    |- game.py          # Game logic (scoring, ...) <br>
    |- locations.py     # Sky locations dictionnary <br>
| <br>
|- routes/              # Website's routes and endpoints <br>
    |- __init__.py      # To make the folder a Python package <br>
    |- main.py          # Principal routes (pages) <br>
    |- api.py           # API REST Endpoints <br>
| <br>
|- static/              # Static ressources <br>
    |- css/             # CSS Scripts <br>
        |- style.css    # Personalized Style <br>
    |- js/              # JavaScript scripts <br>
        |- game.js      # User logic <br>
    |- images/          # Images of the game (dev only) <br>
| <br>
|- templates/           # HTML templates <br>
    |- base.html        # Base template <br>
    |- menu.html        # Main menu <br>
    |- game.html        # Game interface <br>
    |- components       # Re-usable components <br>
        |- sidebar.html # Lateral navigation menu <br>
        |- display.html # Images display <br>
| <br>
|- utils/               # Utils and helpers <br>
    |- __init__.py      # To make the folder a Python package <br>
    |- database.py      # Supabase connexion and requests <br>
    |- game_logic.py    # Game utils function <br>
| <br>
|- pichunt/             # Generated Python (Linux) virtual environment for the project <br>

## Noteworthy used packages

**Flask** is a framework (set of tools and libraries aiming to simplify the creation of applications) for web applications (websites, APIs, backends). <br>
It is said a "micro framework" as it only gives the essentials : <br>
- An integrated web server, <br>
- A routes system (associating URLs to Python functions) <br>
- A template engine (Jinja2) to generate dynamic HTML code <br>
- And sessions/cookies management <br>

A **Flask application** is an instance of the **Flask class** : <br>
`from flask import Flask` <br>
`app = Flask(__name__)` <br>
`if __name__ == '__main__':` <br>
    `app.run(debug=True)` <br>
For more details, see *app.py*. <br>

## app.py script

This script allows us to : <br>
- Create the Flask application <br>
- Configurate the connection to Supabase <br>
- Define the main routes of the application : <br>
    - Game interfaces (main menu, game interface), <br>
    - Game logic (pick a random or daily image, check the player's answer and update the score) <br>