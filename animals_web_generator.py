import os
import requests
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Access API key and Base URL from environment variables
API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Validate API_KEY and BASE_URL
if not API_KEY:
    raise ValueError("API_KEY is not set. Please check your .env file.")
if not BASE_URL:
    raise ValueError("BASE_URL is not set. Please check your .env file.")

def fetch_data(animal_name):
    """
    Fetches the animal data for the specified animal name.

    Args:
        animal_name (str): The name of the animal to fetch data for.

    Returns:
        list: A list of animal data if successful, otherwise an empty list.
    """
    try:
        logging.info(f"Fetching data for animal: {animal_name}")
        response = requests.get(
            f"{BASE_URL}/animals",
            params={"name": animal_name},
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        response.raise_for_status()
        animals = response.json().get('animals', [])
        logging.info(f"Data fetched successfully: {len(animals)} records found.")
        return animals
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return []

if __name__ == "__main__":
    # Example usage of fetch_data
    animal_name = input("Enter the name of the animal you want to fetch data for: ").strip()
    if animal_name:
        data = fetch_data(animal_name)
        if data:
            print("Fetched animal data:")
            for animal in data:
                print(animal)
        else:
            print("No data found or an error occurred.")
    else:
        print("Animal name cannot be empty.")
