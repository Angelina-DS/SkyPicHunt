import supabase
from supabase import create_client, Client, ClientOptions
import random
from datetime import date, datetime, timedelta
import config

class SupabaseManager():
    def __init__(self):
        """Initialize Supabase client connection"""
        try :
            # Create the Supabase client
            supabase = create_client(config.URL, config.APIkey)

            # User connection with email and password
            auth_response = supabase.auth.sign_in_with_password({
                "email": config.email,
                "password": config.password
            })

            # Get the JWT token
            # token = auth_response.session.access_token

            # Re-create the client with the Authorization header and token
            # self.supabase : Client = create_client(config.URL, config.APIkey, options=ClientOptions(global_headers={"Authorization": f"Bearer {token}"}))
            print("Supabase client initialized sucessfully")
        except Exception as e :
            print(f"Supabase client initialization error : {e}")
            raise

    def test_connection(self):
        """
        Tests the Supabase/database connection
        
        Returns:
            bool: True if connection works, False otherwise
        """
        try:
            response = self.supabase.table('Pichunt_images').select('count').execute()
            print(f"Connection test successful : {len(response.data) + 1} images in database.")
            return True

        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    def get_random_image(self, difficulty=0):
        """
        Get a random image based on a difficulty level.

        Args :
            difficulty (float) : 0.0 - 0.32 (easy), 0.33 - 0.66 (medium), 0.67 - 1.01 (hard)
        
        Returns :
            dict : the image and its information : id, url, realm, area, location, difficulty, appeared
        """
        try :
            # Query, similar to SQL, to get the images filtering on the difficulty
            # eq operator for 'equal'
            response = self.supabase.table("Pichunt_images").select('*').eq('difficulty', difficulty).execute()

            if not reponse.data :
                print(f"No image found for difficulty : {difficulty}")
                return

            # Select an image randomly among the ones we got via the request
            random_image = random.choice(response.data)

            return {
                'id' : random_image['id'],
                'url' : random_image['image'],
                'realm' : random_image['realm'],
                'area' : random_image['area'],
                'location' : random_image['location'] or '',
                'difficulty' : random_image['difficulty']
            }
        
        except Exception as e :
            print(f"Error while getting a random image for the difficulty : {e}")
            return None


    def get_supabase_daily(self):
        """
        Get the daily image based on the current date
        
        Args :
            date (date) : current date
        
        Returns :
            dict : the selected image for the daily challenge and its information : id, url, realm, area, location, difficulty, appeared
        """
        # Calculate the limit date for filtering
        today = datetime.now()
        one_year_ago = today - timedelta(days=365)
        date = one_year_ago.strftime('%Y-%m-%d')  # Expected by Supabase ISO format

        try :
            # Get all images without filtering on difficulty (daily's difficulty will vary)
            # But on filtering on the "appeared" date that has to be a year ago or more
            # or operator for 'select images that comply with this condition OR this one'
            # lte operator for 'less than or equal'
            response = self.supabase.table("Pichunt_images").select('*').filter("appeared", "is", "null").execute()

            if not response.data :
                print(f"No image found for the daily on date : {today.strftime('%Y-%m-%d')}")
                return
            
            daily_image = random.choice(response.data)

            # Updating the column "appeared" in the Supabase table for the daily_image (filtering on the id)
            self.supabase.table("Pichunt_images").update({'appeared': today.strftime('%Y-%m-%d')}).eq('id', daily_image['id']).execute()

            return {
                'id' : daily_image['id'],
                'url' : daily_image['image'],
                'realm' : daily_image['realm'],
                'area' : daily_image['area'],
                'location' : daily_image['location'] or '',
                'difficulty' : daily_image['difficulty'],
                'appeared' : daily_image['appeared']
            }

        except Exception as e :
            print(f"Error while getting a daily image for the current date : {e}")