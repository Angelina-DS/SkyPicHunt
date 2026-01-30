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
            self.supabase = create_client(config.URL, config.APIkey)

            # User connection with email and password
            auth_response = self.supabase.auth.sign_in_with_password({
                "email": config.email,
                "password": config.password
            })

            # Get the JWT token
            token = auth_response.session.access_token

            # Re-create the client with the Authorization header and token
            self.supabase : Client = create_client(config.URL, config.APIkey, options=ClientOptions(headers={"Authorization": f"Bearer {token}"}))
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
            print(f"Connection test successful : {response.data[0]['count'] if response.data and 'count' in response.data[0] else 'unknown'} images in database.")
            return True

        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    def get_random_image(self, game_logic, difficulty="Easy"):
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
            difficulty_range = game_logic.get_difficulty_range(difficulty)
            response = self.supabase.table("Pichunt_images").select('*').gte("difficulty", difficulty_range[0]).lt("difficulty", difficulty_range[1]).execute()

            if not response.data :
                print(f"No image found for difficulty : {difficulty}")
                return None

            # Select an image randomly among the ones we got via the request
            random_image = random.choice(response.data)

            return {
                'id' : random_image['id'],
                'url' : random_image['image'],
                'realm' : random_image['realm'],
                'area' : random_image['area'],
                'location' : random_image['location'] or '',
                'difficulty' : random_image['difficulty'],
                'rating_count': random_image['rating_count']
            }
        
        except Exception as e :
            print(f"Error while getting a random image for the difficulty : {e}")
            raise


    def get_supabase_daily(self):
        """
        Get the daily image based on the current date
        
        Returns :
            dict : the selected image for the daily challenge and its information : id, url, realm, area, location, difficulty, appeared
        """
        # Calculate the limit date for filtering
        today = datetime.now()
        today_date = today.strftime('%Y-%m-%d')
        one_year_ago = today - timedelta(days=365)
        date = one_year_ago.strftime('%Y-%m-%d')  # Expected by Supabase ISO format

        try :
            # Check whether there is a daily image already:
            response = self.supabase.table("Pichunt_images").select("*").eq("appeared", today_date).execute()
            if response.data:
                daily_image = response.data[0]

            else:
                # Get all images without filtering on difficulty (daily's difficulty will vary)
                # But on filtering on the "appeared" date that has to be a year ago or more
                # or operator for 'select images that comply with this condition OR this one'
                # lte operator for 'less than or equal'
                response = self.supabase.table("Pichunt_images").select('*').filter("appeared", "is", "null").execute()

                if not response.data:
                    response = self.supabase.table("Pichunt_images").select('*').order("appeared", nullsfirst=False).execute()
                    if not response.data:
                        print(f"No image found for the daily on date : {today.strftime('%Y-%m-%d')}")
                        return None
                    else:
                        daily_image = response.data[0]
                else:
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
                'appeared' : daily_image['appeared'],
                'rating_count' : daily_image['rating_count']
            }

        except Exception as e :
            print(f"Error while getting a daily image for the current date : {e}")
            raise

    def get_preview_image(self, type:str, realm:str, area:str="", location:str="") -> dict|None:
        try:
            print("get preview image for:",type,": ", realm, ",", area, ",", location)
            query = self.supabase.table("Preview_images").select("*").eq("Type", type.capitalize()).eq("Realm", realm)
            if type.capitalize() in ["Area", "Location"]:
                query = query.eq("Area", area)
            if type.capitalize() == "Location":
                query = query.eq("Location", location)
            response = query.execute()
            print("response: ", response, "data:", response.data)
            if response.data:
                return {
                    "id": response.data[0]["id"],
                    "url": response.data[0]["URL"],
                    "type": response.data[0]["Type"],
                    "realm": response.data[0]["Realm"],
                    "area": response.data[0]["Area"],
                    "location": response.data[0]["Location"],
                }
        except Exception as e:
            print(f"Error while getting a preview image : {e}")
            raise

    def add_rating(self, picture_id:int, rating:int):
        response = self.supabase.table("Pichunt_images").select("*").eq("id", picture_id).execute()
        if response.data:
            rating_float = 0.25*rating-0.25
            difficulty_before, rating_count_before=response.data[0]["difficulty"], response.data[0]["rating_count"]
            difficulty_now = (1.0*difficulty_before*rating_count_before+rating_float)/(rating_count_before+1)
            response = self.supabase.table("Pichunt_images").update({"difficulty":difficulty_now, "rating_count": rating_count_before+1}).eq("id", picture_id).execute()
            if response.data:
                print("updated ratings: "+str(response.data))
                return True
            else:
                print("error: ", response)
        else:
            print("error: ", response)
