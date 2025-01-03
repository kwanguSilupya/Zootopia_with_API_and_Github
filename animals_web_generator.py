import os
import requests
from dotenv import load_dotenv
import logging
from jinja2 import Environment, FileSystemLoader

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


def fetch_animal_data(animal_name):
    """
    Fetches the animal data for the specified animal name.

    Args:
        animal_name (str): The name of the animal to fetch data for.

    Returns:
        list: A list of animal data if successful, otherwise an empty list.
    """
    try:
        logging.info(f"Fetching data for animal: {animal_name}")
        headers = {"X-Api-Key": API_KEY}
        params = {"name": animal_name}

        # Make the API request
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for HTTP issues

        animal_data = response.json()  # Parse JSON response
        if animal_data:  # Check if the data is non-empty
            logging.info(f"Data fetched successfully: {len(animal_data)} record(s) found.")
            return animal_data
        else:
            logging.warning("No data found for the specified animal.")
            return []
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return []
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        return []


def generate_html(fetched_data):
    """
    Generates HTML file from the fetched data using Jinja2 template.

    Args:
        fetched_data (list): The data to display in the HTML file.
    """
    # Create a Jinja2 environment and load templates from the current directory
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('animals_template.html')

    # Render the template with fetched data
    html_content = template.render(animals=fetched_data)

    # Save the rendered HTML to a file
    with open("animal_data.html", "w") as f:
        f.write(html_content)

    print("HTML file generated successfully!")


if __name__ == "__main__":
    # Example usage of fetch_animal_data
    animal_name_input = input("Enter the name of the animal you want to fetch data for: ").strip()
    if animal_name_input:
        fetched_data = fetch_animal_data(animal_name_input)
        if fetched_data:
            generate_html(fetched_data)  # Generate the HTML with the fetched data
        else:
            print("No data found or an error occurred.")
    else:
        print("Animal name cannot be empty.")