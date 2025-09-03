# Sky Picture Hunt

Sky Picture Hunt is a game about geolocalisation, inspired by Geoguessr, adapted to the universe of Sky : Children of Light.
Players have to guess the  location of given screens in the world of Sky.
In order to do so, they can navigate through the menu on the left of the screen to select the name of a realm, of an area and/or of a location where they think the image belongs.

Sky Picture Hunt has two Game modes :
- Daily Picture : a daily screen for a secret location to guess everyday.
- Picture Hunt : free mode to guess as many images as the player wants with three level of difficulties : Easy, Medium, Hard.

The points are based on the precision of the guesses : 100pts for the realm, 200pts for the area and 300pts for the location.

# Noteworthy used packages

**Flask** is a framework (set of tools and libraries aiming to simplify the creation of applications) for web applications (websites, APIs, backends).
It is said a "micro framework" as it only gives the essentials : 
- An integrated web server, 
- A routes system (associating URLs to Python functions)
- A template engine (Jinja2) to generate dynamic HTML code
- And sessions/cookies management

A **Flask application** is an instance of the **Flask class** :
`from flask import Flask`
`app = Flask(__name__)`
`if __name__ == '__main__':`
    `app.run(debug=True)`
For more information, see *app.py*. 

# Structure of the project

pichunt_project/
|- app.py               # Flask application
|- config.py            # Configuration File for important variables and parameters values
|- requirements.txt     # Python dependencies for packages
|- .gitignore           # Files to ignore by Git when pushing
|- README.md            # The documentation of the project
|
|- models/              # Main logic and datas
    |- __init__.py      # To make the folder a Python package
    |- game.py          # Game logic (scoring, ...)
    |- locations.py     # Sky locations dictionnary
|
|- routes/              # Website's routes and endpoints
    |- __init__.py      # To make the folder a Python package
    |- main.py          # Principal routes (pages)
    |- api.py           # API REST Endpoints
|
|- static/              # Static ressources
    |- css/             # CSS Scripts
        |- style.css    # Personalized Style
    |- js/              # JavaScript scripts
        |- game.js      # User logic
    |- images/          # Images of the game (dev only)
|
|- templates/           # HTML templates
    |- base.html        # Base template
    |- menu.html        # Main menu
    |- game.html        # Game interface
    |- components       # Re-usable components
        |- sidebar.html # Lateral navigation menu
        |- display.html # Images display
|
|- utils/               # Utils and helpers
    |- __init__.py      # To make the folder a Python package
    |- database.py      # Supabase connexion and requests
    |- game_logic.py    # Game utils function
|
|- pichunt/             # Generated Python (Linux) virtual environment for the project

## app.py script

This script allows us to :
- Create the Flask application
- Configurate the connection to Supabase
- Define the main routes of the application : 
    - Game interfaces (main menu, game interface),
    - Game logic (pick a random or daily image, check the player's answer and update the score)