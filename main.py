import requests
from bs4 import BeautifulSoup
from ollama import Client

# Function to perform a Google search and get the top results
def getTopResults(query, number):
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
        # Extract and append the URLs of the top results
        for result in results:
            link = result.find('a')['href'] if result.find('a') else None
            if link:
                links.append(link)
    return links

# Function to get HTML content from a URL
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
    except requests.RequestException:
        # Print the error if the request fails
        return None

# Function to summarize HTML content using the Ollama client
def summarizeHtml(html, model='tinyllama',host="http://localhost:11434"):
    client = Client(host=host)
    response = client.chat(
        model=model, 
        messages=[{'role': 'user', 'content': 'Please summarize this HTML to a paragraph, please only include the summary in your response: \n ' + html}]
    )
    return response['message']['content']

# Function to get top summaries from Google search results
def getTopSummary(query, number, model="tinyllama", host="http://localhost:11434"):
    summaries = []
    links = getTopResults(query, number)
    for link in links:
        html = getHtmlContent(link)
        if html:
            summary = summarizeHtml(html, model=model, host=host)
            summaries.append(summary)
    return " ".join(summaries)

# Function to run Ollama inference
def runOllamaInference(message, model='llama3', smallmodel='tinyllama', host="http://localhost:11434"):
    client = Client(host=host)
    response = client.chat(
        model=model, 
        messages=[{'role': 'system', 'content': 'You have internet access. In order to search the internet, put your search query in {} and do not include any text except the query in your response.'}, {'role': 'user', 'content': message}]
    )
    
    content = response['message']['content']
    if content.startswith('{') and content.endswith('}'):
        query = content[1:-1]
        summary = getTopSummary(query, 3, model=smallmodel, host=host)
        response2 = client.chat(
            model=model, 
            messages=[{'role': 'user', 'content': summary}, {'role': 'user', 'content': message}]
        )
        return response2['message']['content']
    else:
        return content

print(runOllamaInference("Who is the current US president?", model="llama3", smallmodel="tinyllama", host="http://192.168.1.221:11434"))