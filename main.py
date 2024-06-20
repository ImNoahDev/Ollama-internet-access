import requests
from bs4 import BeautifulSoup

# Function to perform a Google search and get the top 5 results
def getTopResuts(query, number):
    links = []
    # Create the Google search URL
    url = f"https://www.google.com/search?q={query}"
    # Define the user-agent to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # Send the GET request to Google
    response = requests.get(url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        # Find all the search result divs
        results = soup.find_all('div', class_='g')[:int(number)]
        # Extract and print the titles and URLs of the top 5 results
        for index, result in enumerate(results, start=1):
            link = result.find('a')['href'] if result.find('a') else "No link"
            links.append(link)
    return links

import requests

def getHtmlContent(url):
    try:
        # Define the user-agent to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Send the GET request to the URL
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        response.raise_for_status()

        # Return the HTML content
        return response.text

    except requests.RequestException as e:
        # Print the error if the request fails
        return None
