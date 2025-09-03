from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from datetime import datetime, date
import random
from models.locations import locations # Locations list
from models.game import GameLogic # Scoring logic
from utils.database import SupabaseManager # Database access
import config # Configuration variables

# --- Creating the application with an instance of the class Flask ---
# app is the central object which will manage routes, configurations and extensions.
app = Flask(__name__)
app.secret_key = config.secret_key

# --- Get the Supabase connection variables from the config file ---
app.config['SUPABASE_URL'] = config.URL # os.getenv('URL')
app.config['SUPABASE_KEY'] = config.APIkey # os.getenv('APIkey')

# --- "Managers" initialisation ---
# Creating Database manager only if SUPABASE_URL is defined
try :
    db_manager = SupabaseManager()
    print("Supabase successfully connected")
except Exception as e :
    print(f"Supabase error : {e}")
    db_manager = None
    
# Points calculation logic
game_logic = GameLogic()

# -- HTML pages routes --

# @app.route() decorators are used to link an URL with a Python function (called a "view")
# Get /
@app.route('/')
def menu():
    """Home page with the main menu"""
    return render_template('menu.html')

#Redirect to game (easy)
@app.route('/game')
@app.route('/game/')
def redirect_game():
#    print("redirecting")
    return redirect(url_for("game", mode="easy"))

# Get /game/<mode>?difficulty=
@app.route('/game/<mode>')
def game(mode):
    """Main game interface"""
    # Get difficulty via the query string, default = "easy"
    difficulty = request.args.get('difficulty', 'easy')
    
    # Initialisation/Actualisation of the game session (mode, difficulty, score)
    session['game_mode'] = mode
    session['difficulty'] = difficulty
    session['score'] = session.get('score', 0) # Keep the score if already existing, else score = 0
    
    # To rend the game page with useful data in the frontend
    return render_template('game.html', 
                         mode=mode, 
                         difficulty=difficulty,
                         locations=locations)


# --- JSON API : pick up a new image ---

# Get /api/new-image
@app.route('/api/new-image')
def get_new_image():
    """API to select a new image according to the difficulty"""
    difficulty = request.args.get('difficulty', 'easy')
    
    # Prod case : if Supabase is avalaible
    if db_manager:
        # We request an image adapted to the difficulty
        image_data = db_manager.get_random_image(difficulty)

        # If no image exist for the selected difficulty
        if not image_data:
            return jsonify({
                'error': f'No image found for the difficulty {difficulty}'
            }), 404

    # Dev case : else
    else:
        # We use this hard coded sample list of images as an instance
        sample_images = [
            {
                'id': 1,
                'url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&h=400&fit=crop',
                'realm': 'Isle of Dawn',
                'area': 'Main Isle', 
                'location': 'Mural Cave',
                'difficulty': 'easy'
            },
            {
                'id': 2,
                'url': 'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=600&h=400&fit=crop',
                'realm': 'Daylight Prairie',
                'area': 'Butterfly Fields',
                'location': '',
                'difficulty': 'medium'
            },
            {
                'id': 3,
                'image': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&h=400&fit=crop',
                'realm': 'Hidden Forest',
                'area': 'Forest Clearing',
                'location': 'Plain before the First Gate',
                'difficulty': 'hard'
            }
        ]
        # Sub-list of images filtered to match the current difficulty
        filtered_images = [img for img in sample_images if img['difficulty'] == difficulty]
        # If filetered_images is not empty, then we chose a random image in it, else we pick the first image in sample_images
        image_data = random.choice(filtered_images) if filtered_images else sample_images[0]
    
    # Store the chosen image in the current session (needed for the verification of the player's answers)
    session['current_image'] = image_data
    
    # Return the image on the frontend (JSON)
    return jsonify(image_data)

# --- JSON API : daily picture ---

# Get /api/daily-image
@app.route('/api/daily-image')
def get_daily_image():
    """Return the daily picture, store it in the session"""
    today = date.today()
    
    # Prod case : daily picture is picked in Supabase
    if db_manager:
        image_data = db_manager.get_daily_image(today)

        # If no daily image is found
        if not image_data:
            return jsonify({
                'error': 'No avalaible daily picture'
            }), 404

    # Dev case : daily picture is chosen putting a seed on the current date and with a sample list
    else:
        random.seed(today.toordinal())
        sample_images = [
            {
                'id': 1,
                'url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&h=400&fit=crop',
                'realm': 'Isle of Dawn',
                'area': 'Main Isle',
                'location': 'Mural Cave',
                'difficulty': 'medium'
            }
        ]
        image_data = random.choice(sample_images)
        random.seed()  # Reinitialisation of the seed
    
    # Storing the daily picture in the current session
    session['current_image'] = image_data
    # Return the daily picture in the frontend
    return jsonify(image_data)

# --- JSON API : check the players' answer ---

# POST /api/check-answer
@app.route('/api/check-answer', methods=['POST'])
def check_answer():
    """Read the player's answer (realm, area and location), get the current image, calculate the points"""
    # Get player's answer via the query json, default answers = ''
    data = request.get_json()
    selected_realm = data.get('realm', '')
    selected_area = data.get('area', '')
    selected_location = data.get('location', '')

    # Check if the gotten realm, area and location are valid
    validation = game_logic.validate_selection(selected_realm, selected_area, selected_location)
    if not validation['valid']:
        return jsonify({'error': validation['error']}), 400
    
    # Get the image to guess, stored in the current session by /api/new-image or /api/daily-image
    current_image = session.get('current_image', {})
    # If the image is not found
    if not current_image:
        return jsonify({'error': 'No image in the current session'}), 400
    
    # Points/score calculation using the scoring logic
    points = game_logic.calculate_score(
        current_image,
        selected_realm,
        selected_area, 
        selected_location
    )
    
    # Update the total score stored in the current session
    session['score'] = session.get('score', 0) + points
    
    # Construct a detailed answer : points, total score, right answers and flags
    response = {
        'points': points,
        'total_score': session['score'],
        'correct_answer': {
            'realm': current_image.get('realm', ''),
            'area': current_image.get('area', ''),
            'location': current_image.get('location', '')
        },
        'is_correct': {
            'realm': selected_realm == current_image.get('realm', ''),
            'area': selected_area == current_image.get('area', ''),
            'location': selected_location == current_image.get('location', '') if current_image.get('location') else True
        }
    }
    
    # Return the detailed answer in the frontend
    return jsonify(response)

# --- JSON API : avalaible locations list ---

# Get /api/locations
@app.route('/api/locations')
def get_locations():
    """API to obtain the list of all the locations in Sky"""
    # Expose the structure of the locations list in the frontend
    return jsonify(locations)

# --- JSON API : reset the score to 0 ---

# GET /api/reset-score
@app.route('/api/reset-score')
def reset_score():
    """Score reinitialisation in the current session"""
    session['score'] = 0
    return jsonify({'score': 0})

# --- To run the app on a local instance ---

if __name__ == '__main__':
    # debug=True -> only on dev, automatic reloading and detailed tracebacks
    app.run(debug=True) # , host='0.0.0.0', port=int(os.getenv('PORT', 5000))