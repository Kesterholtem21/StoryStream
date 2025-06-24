# StoryStream

StoryStream is a full-stack web app that helps users discover and save movies and books based on their genre preferences. Users can search for content, manage their favorites, leave comments, and customize their genre interests for better recommendations.

## Features
- Personalized movie and book discovery based on genres
- User authentication and login system
- Admin dashboard for content management
- Favorites list and comment system
- Dynamic search and genre preference updates

## Tech Stack
- Frontend: HTML, CSS, JavaScript, TypeScript
- Backend: Python, SQL
- Frameworks/Libraries: Flask (or Django if applicable), Bootstrap


## Getting Started
To run the app locally:

```bash
# Clone the repository
git clone https://github.com/Kesterholtem21/StoryStream.git
cd StoryStream

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables and database (if needed)
export FLASK_APP=app.py
export FLASK_ENV=development

# Run the app
flask run
