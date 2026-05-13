# Crossfade.fm

A playlist generator that finds the musical middle ground between two songs. Pick any two tracks, and Crossfade.fm analyzes their vibes using the Last.fm API to generate a cohesive 10 or 20 song playlist that lives in the intersection of both.

## How It Works

1. Search for two songs using the search bars
2. Select your playlist size — 10 or 20 tracks
3. Hit **Generate Playlist**
4. Get a blended playlist with listen links for Spotify, Apple Music, and YouTube Music

## Vibe Analysis

Along with the playlist, Crossfade.fm breaks down the musical DNA of both songs — showing common vibes, and what makes each song unique. This is what drives the recommendations.

## Tech Stack

- **Backend:** Python, Flask
- **API:** Last.fm
- **Frontend:** HTML, CSS, JavaScript

## Setup & Installation

1. Clone the repo
git clone https://github.com/JoshVarughese/crossfade-fm.git
cd crossfade-fm

2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install flask requests python-dotenv

4. Create a `.env` file in the root directory and add your Last.fm API key
LASTFM_API_KEY=your_api_key_here
LASTFM_SECRET=your_secret_here

5. Run the app
python app.py

6. Open your browser and go to `http://localhost:5000`

## Getting a Last.fm API Key

You can get a free API key by creating an account at [last.fm/api](https://www.last.fm/api/account/create).

## Notes

- Works best with well established songs that have strong Last.fm community tag data
- Newer releases may have limited vibe analysis due to fewer community tags