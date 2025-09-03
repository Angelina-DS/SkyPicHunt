from models.locations import locations

class GameLogic:
    """Gestion de la logique du jeu Sky Geoguessr - Version adaptée"""
    
    def __init__(self):
        self.score_system = {
            'realm': 100,
            'area': 200,
            'location': 300
        }
    
    def calculate_score(self, correct_answer, selected_realm, selected_area, selected_location):
        """
        Calculer le score basé sur la précision de la réponse
        
        Args:
            correct_answer (dict): La bonne réponse
            selected_realm (str): Realm sélectionné par le joueur
            selected_area (str): Area sélectionnée par le joueur  
            selected_location (str): Location sélectionnée par le joueur
            
        Returns:
            int: Points obtenus
        """
        points = 0
        
        # Vérifier le realm
        if selected_realm == correct_answer.get('realm', ''):
            points += self.score_system['realm']
        
        # Vérifier l'area (seulement si le realm est correct)
        if selected_area == correct_answer.get('area', '') and points > 0:
            points += self.score_system['area']
        
        # Vérifier la location (seulement si area est correcte et location existe)
        correct_location = correct_answer.get('location', '')
        if (correct_location and 
            selected_location == correct_location and 
            points >= self.score_system['realm'] + self.score_system['area']):
            points += self.score_system['location']
        
        return points
    
    def validate_selection(self, realm, area, location):
        """
        Valider que la sélection du joueur est cohérente avec la nouvelle structure
        
        Args:
            realm (str): Realm sélectionné
            area (str): Area sélectionnée
            location (str): Location sélectionnée
            
        Returns:
            dict: Résultat de la validation
        """
        if not realm:
            return {'valid': False, 'error': 'Veuillez sélectionner un realm'}
        
        if realm not in locations:
            return {'valid': False, 'error': 'Realm invalide'}
        
        if not area:
            return {'valid': False, 'error': 'Veuillez sélectionner une area'}
            
        # Nouvelle structure : locations[realm] est directement un dict d'areas
        if area not in locations[realm]:
            return {'valid': False, 'error': 'Area invalide pour ce realm'}
        
        # Vérifier la location si fournie
        if location:
            available_locations = locations[realm][area]  # Plus simple !
            if location not in available_locations:
                return {'valid': False, 'error': 'Location invalide pour cette area'}
        
        return {'valid': True}
    
    def get_difficulty_settings(self, difficulty):
        """
        Obtenir les paramètres selon la difficulté
        
        Args:
            difficulty (str): 'easy', 'medium', 'hard'
            
        Returns:
            dict: Paramètres de difficulté
        """
        settings = {
            'easy': {
                'description': 'Vues générales et reconnaissables',
                'time_limit': None,
                'hints_allowed': True
            },
            'medium': {
                'description': 'Angles moins évidents',
                'time_limit': 60,  # secondes
                'hints_allowed': False
            },
            'hard': {
                'description': 'Détails très spécifiques',
                'time_limit': 30,
                'hints_allowed': False
            }
        }
        
        return settings.get(difficulty, settings['easy'])
    
    def get_random_location_with_details(self, difficulty='easy'):
        """
        Obtenir une location aléatoire avec tous ses détails
        Utile pour générer des questions
        
        Returns:
            dict: Information complète sur la location
        """
        import random
        
        # Filtrer selon la difficulté
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