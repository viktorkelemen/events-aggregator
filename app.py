from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from scrapers import scrape_all_sources
from database import get_upcoming_events, init_db, get_scraping_stats

app = Flask(__name__, static_folder='.')
CORS(app)

# Prospect Heights coordinates
PROSPECT_HEIGHTS = {
    'lat': 40.6782,
    'lng': -73.9712
}

# Cache file path
CACHE_FILE = 'events_cache.json'
CACHE_DURATION = timedelta(hours=1)

def load_cache():
    """Load events from cache if available and not expired"""
    if not os.path.exists(CACHE_FILE):
        return None
    
    try:
        with open(CACHE_FILE, 'r') as f:
            cache_data = json.load(f)
        
        cache_time = datetime.fromisoformat(cache_data['timestamp'])
        if datetime.now() - cache_time < CACHE_DURATION:
            return cache_data['events']
    except Exception as e:
        print(f"Error loading cache: {e}")
    
    return None

def save_cache(events):
    """Save events to cache"""
    try:
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'events': events
        }
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f, indent=2)
    except Exception as e:
        print(f"Error saving cache: {e}")

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two coordinates using Haversine formula"""
    from math import radians, sin, cos, sqrt, atan2
    
    R = 3959  # Earth's radius in miles
    
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lng = radians(lng2 - lng1)
    
    a = sin(delta_lat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c

def fetch_nyc_government_events():
    """Fetch events from NYC Open Data (example API)"""
    events = []
    
    # TODO: Implement NYC Open Data API integration
    # NYC Open Data: https://opendata.cityofnewyork.us/
    # Events API: https://data.cityofnewyork.us/browse?tags=events
    
    return events

def fetch_external_api_events():
    """Fetch events from external APIs like Eventbrite, Facebook Events, etc."""
    events = []
    
    # TODO: Implement API integrations:
    # - Eventbrite API: https://www.eventbrite.com/platform/api/
    # - Facebook Events API: https://developers.facebook.com/docs/graph-api
    # - Meetup API: https://www.meetup.com/meetup_api/
    # Note: These APIs require authentication keys
    
    return events

@app.route('/api/events')
def get_events():
    """API endpoint to get aggregated events from database"""
    
    try:
        # Get events from database
        events = get_upcoming_events(limit=100)
        
        # Convert datetime objects to ISO strings for JSON serialization
        for event in events:
            if 'created_at' in event:
                del event['created_at']
            if 'updated_at' in event:
                del event['updated_at']
        
        return jsonify({'events': events})
    except Exception as e:
        print(f"Error fetching events from database: {e}")
        return jsonify({'events': [], 'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """API endpoint to get scraping statistics"""
    try:
        stats = get_scraping_stats()
        return jsonify({'stats': stats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    app.run(debug=True, port=5001)

