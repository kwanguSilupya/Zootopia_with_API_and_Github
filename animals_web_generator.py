from dotenv import load_dotenv
import os
import requests
# Load .env file
load_dotenv()
# Access the API_KEY from environment variables
API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://example.com/api'
def fetch_data(animal_name):
    """
    Fetches the animal data for the specified animal name.
    """
    try:
        response = requests.get(
            f"{BASE_URL}/animals",
            params={"name": animal_name},
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        response.raise_for_status()
        return response.json().get('animals', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
