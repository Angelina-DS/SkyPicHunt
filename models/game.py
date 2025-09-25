import random
from models.locations import locations

class GameLogic:
    """Sky Picture Hunt game's logic management"""
    
    def __init__(self):
        # Points system for each level of precision
        self.score_system = {
            'realm': 100,
            'area': 200,
            'location': 300
        }
    
    def calculate_score(self, correct_answer, selected_realm, selected_area, selected_location):
        """
        Calculation the score based on the precision of the answer
        
        Args:
            correct_answer (dict): the correct answer, must have the following keys : 'realm', 'area', 'location'
            selected_realm (str): selected realm by the player
            selected_area (str): selected area by the player
            selected_location (str): selected location by the player
            
        Returns:
            Score (int): total of points
        """
        score = 0
        
        # Realm verification
        # .get provides a protection if the key is absent from correct_answer
        if selected_realm == correct_answer.get('realm', ''):
            score += self.score_system['realm'] # If the realm is right, we add the according points to the score
        
        # Area verification (only if the realm was right : score is already > 0)
        if selected_area == correct_answer.get('area', '') and score > 0:
            score += self.score_system['area']
        
        # Location verification (only if the realm and area were right and if there exist a location for this area and realm)
        correct_location = correct_answer.get('location', '')
        if (correct_location and 
            selected_location == correct_location and 
            score >= self.score_system['realm'] + self.score_system['area']):
            score += self.score_system['location']
        
        return score
    
    def validate_selection(self, realm, area, location):
        """
        Checking if the player's selection matches the expected structure of the dictionnary locations.
        
        Args:
            realm (str): selected realm
            area (str): selected area
            location (str): selected location
            
        Returns:
            dict: result of the validation, respects the structure {'valid': bool, 'error':'message' (optionnal)}
        """
        if not realm:
            return {'valid': False, 'error': 'Please select a valid realm.'}
        
        if realm not in locations:
            return {'valid': False, 'error': 'Invalid realm.'}
        
        # Checking if an area is given
        if area:            
            if area not in locations[realm]:
                return {'valid': False, 'error': 'Invalid area for this realm.'}
        else:
            return {'valid': False, 'error': 'Please select a valid area.'}
        
        # Checking if a location is given
        if location:
            possible_locations = locations[realm][area] # List of the possible locations for this area
            if location not in possible_locations:
                return {'valid': False, 'error': 'Invalid location for this area.'}
        else:
            return {'valid': False, 'error': 'Please select a valid location.'}
        
        # If all the checks have been passed
        return {'valid': True}
    
    def get_difficulty_settings(self, difficulty):
        """
        Return game parameters/constraints for the selected level of difficulty.
        
        Args:
            difficulty (float) : 0.0 - 0.32 (easy), 0.33 - 0.66 (medium), 0.67 - 1.01 (hard)
            
        Returns:
            dict: parameters of the selected difficulty, return the easy difficulty ones by default
        """
        settings = {
            'easy': {
                'description': 'General and recognizable views',
                'time_limit': None,
                'hints_allowed': True,
                'range': (0.0, 0.32)
            },
            'medium': {
                'description': 'Less obvious angles',
                'time_limit': None,  # seconds
                'hints_allowed': False,
                'range': (0.33, 0.66)
            },
            'hard': {
                'description': 'Very specific details',
                'time_limit': None,
                'hints_allowed': False,
                'range': (0.67, 1.01)
            }
        }
        
        # Convert float number into a difficulty name
        if 0.0 <= difficulty < 0.33:
            difficulty_name = 'easy'
        elif 0.33 <= difficulty < 0.67:
            difficulty_name = 'medium'
        elif 0.67 <= difficulty <= 1.0:
            difficulty_name = 'hard'
        else:
            # If the value of difficulty is outside the previous bounds, return an error
            print("Error in get_difficulty_settings: Invalid difficulty value")
        
        return settings.get(difficulty_name, settings['easy'])

    def get_difficulty_range(self, difficulty):
        if difficulty.lower() == "easy":
            return (0.0, 0.33)
        elif difficulty.lower() == "medium":
            return (0.33, 0.67)
        elif difficulty.lower() == "hard":
            return (0.67, 1.01)
        else:
            print("Error in get_difficulty_range: Invalid difficulty value")
            return None

    # def get_random_location_with_details(self, difficulty='easy'):
    #     """
    #     Select a random picture with all its details according to the difficulty.
    #
    #     Returns:
    #         dict: Complete information about the location : realm, area, location, difficulty
    #     """

        # pictures = self.get_all_pictures()

        # Define the bound values for each difficulty
        # min_bound = {"easy": 0.0, "medium": 0.33, "hard": 0.67}[difficulty]
        # max_bound = {"easy": 0.33, "medium": 0.67, "hard": 1.01}[difficulty]
        # pictures = list(filter(lambda x: "rating" in x and min_bound <= x["rating"] < max_bound, pictures))

        #return random.choice(pictures) if len(pictures) > 0 else None
