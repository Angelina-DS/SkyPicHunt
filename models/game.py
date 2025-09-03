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
        
        # Checking if a location is given
        if location:
            possible_locations = locations[realm][area] # List of the possible locations for this area
            if location not in possible_locations:
                return {'valid': False, 'error': 'Invalid location for this area.'}
        
        # If all the checks have been passed
        return {'valid': True}
    
    def get_difficulty_settings(self, difficulty):
        """
        Return game parameters/constraints for the selected level of difficulty.
        
        Args:
            difficulty (str): 'easy', 'medium', 'hard'
            
        Returns:
            dict: parameters of the selected difficulty, return the easy difficulty ones by default
        """
        settings = {
            'easy': {
                'description': 'General and recognizable views',
                'time_limit': None,
                'hints_allowed': True
            },
            'medium': {
                'description': 'Less obvious angles',
                'time_limit': None,  # seconds
                'hints_allowed': False
            },
            'hard': {
                'description': 'Very specific details',
                'time_limit': None,
                'hints_allowed': False
            }
        }
        
        return settings.get(difficulty, settings['easy'])
    
    def get_random_location_with_details(self, difficulty='easy'):
        """
        Select a random location with all its details according to the difficulty.
        
        Returns:
            dict: Complete information about the location : realm, area, location, difficulty
        """
        
        if difficulty == 'easy':
            # Areas avec beaucoup de locations facilement identifiables
            candidate_locations = []
            for realm, areas in locations.items():
                for area, locations in areas.items():
                    if len(locations) >= 2:  # Areas avec plusieurs locations
                        for location in locations:
                            candidate_locations.append({
                                'realm': realm,
                                'area': area, 
                                'location': location,
                                'difficulty': difficulty
                            })
        
        elif difficulty == 'medium':
            # Toutes les locations spécifiques
            candidate_locations = []
            for realm, areas in locations.items():
                for area, locations in areas.items():
                    if locations:  # Au moins une location
                        for location in locations:
                            candidate_locations.append({
                                'realm': realm,
                                'area': area,
                                'location': location, 
                                'difficulty': difficulty
                            })
        
        else:  # hard
            # Areas sans locations spécifiques (plus difficile)
            candidate_locations = []
            for realm, areas in locations.items():
                for area, locations in areas.items():
                    candidate_locations.append({
                        'realm': realm,
                        'area': area,
                        'location': '',  # Pas de location spécifique
                        'difficulty': difficulty
                    })
        
        return random.choice(candidate_locations) if candidate_locations else None