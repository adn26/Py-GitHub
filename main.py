from flask import render_template, Flask, request
import requests
from dotenv import load_dotenv # type: ignore
import os

def configure():
    load_dotenv()

app = Flask(__name__)

# GitHub Token 
headers = {"Authorization":f"Bearer {os.getenv('api_key')}"}

url = "https://api.github.com/search/repositories"


# Function to get all python related repos
def get_data(page):
    repos = []
    params = {
        "q":"language:Python",
        "sort":"stars",
        "order":"desc",
        "per_page":10,    # Repos per page
        "page":page,
        }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if 'items' in data:
        repos = data['items']    # Get the items for the current page
               
    return repos

@app.route("/")

def home():
    configure()
    # Get current page number, default to page 1 if not set
    page = request.args.get('page', 1, type=int)
    
    # Fetching repositories for the current page
    data = get_data(page)

    # Determine if there are more pages to display "Next" button
    next_page = page + 1
    prev_page = page - 1 if page > 1 else None

    # Check if there are any previous or next pages to enable/disable buttons
    has_previous_page = prev_page is not None
    has_next_page = len(data) == 10  # Check if the current page has a full set of results

    # Render the results on the webpage
    return render_template(
        "index.html", 
        repos=data, 
        next_page=next_page, 
        prev_page=prev_page, 
        has_previous_page=has_previous_page,
        has_next_page=has_next_page
    )
if __name__ == "__main__":
    app.run(debug=True)