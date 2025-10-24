from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from scrapers import scrape_all_sources

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
    
    # NYC Open Data API for events (example endpoint)
    # Note: You'll need to replace this with actual API endpoints
    try:
        # This is a placeholder - you'll need to implement actual API calls
        # For now, we'll return some sample events
        
        sample_events = [
            {
                'title': 'Contemporary Art Gallery Opening',
                'description': 'Exhibition of modern art by emerging Brooklyn artists',
                'date': (datetime.now() + timedelta(days=2)).isoformat(),
                'location': '132 Grand St, Brooklyn, NY 11249',
                'type': 'art',
                'url': 'https://example.com'
            },
            {
                'title': 'Jazz Night at Blue Note Brooklyn',
                'description': 'Live jazz performance featuring local musicians',
                'date': (datetime.now() + timedelta(days=3)).isoformat(),
                'location': '131 W 3rd St, Brooklyn, NY 11249',
                'type': 'music',
                'url': 'https://example.com'
            },
            {
                'title': 'Kids Art Workshop at Brooklyn Children\'s Museum',
                'description': 'Interactive art workshop for kids aged 7-12',
                'date': (datetime.now() + timedelta(days=4)).isoformat(),
                'location': '145 Brooklyn Ave, Brooklyn, NY 11213',
                'type': 'art',
                'url': 'https://www.brooklynkids.org/'
            },
            {
                'title': 'Photography Exhibit: Brooklyn Streets',
                'description': 'Black and white photography exhibition showcasing Brooklyn street scenes',
                'date': (datetime.now() + timedelta(days=5)).isoformat(),
                'location': '123 Flatbush Ave, Brooklyn, NY 11217',
                'type': 'art',
                'url': 'https://example.com'
            },
            {
                'title': 'Indie Rock Concert at Music Hall',
                'description': 'Local indie bands performing original music',
                'date': (datetime.now() + timedelta(days=6)).isoformat(),
                'location': '456 7th Ave, Brooklyn, NY 11215',
                'type': 'music',
                'url': 'https://example.com'
            },
            {
                'title': 'Sculpture Garden Installation Opening',
                'description': 'Outdoor sculpture exhibition in Prospect Park',
                'date': (datetime.now() + timedelta(days=7)).isoformat(),
                'location': 'Prospect Park, Brooklyn, NY',
                'type': 'art',
                'url': 'https://www.prospectpark.org/'
            },
            {
                'title': 'Classical Music Concert at Brooklyn Museum',
                'description': 'String quartet performing classical favorites',
                'date': (datetime.now() + timedelta(days=8)).isoformat(),
                'location': '200 Eastern Pkwy, Brooklyn, NY 11238',
                'type': 'music',
                'url': 'https://www.brooklynmuseum.org/'
            },
            {
                'title': 'Abstract Painting Workshop',
                'description': 'Adult painting class focusing on abstract techniques',
                'date': (datetime.now() + timedelta(days=9)).isoformat(),
                'location': '789 Atlantic Ave, Brooklyn, NY 11238',
                'type': 'art',
                'url': 'https://example.com'
            }
        ]
        
        # Add weekend events (Saturday and Sunday)
        now = datetime.now()
        days_until_saturday = (5 - now.weekday()) % 7 or 7
        saturday = now + timedelta(days=days_until_saturday)
        sunday = saturday + timedelta(days=1)
        
        weekend_events = [
            {
                'title': 'Weekend Art Walk in Prospect Heights',
                'description': 'Self-guided art gallery tour featuring local artists',
                'date': saturday.isoformat(),
                'location': 'Prospect Heights, Brooklyn, NY',
                'type': 'art',
                'url': 'https://example.com'
            },
            {
                'title': 'Sunday Jazz Brunch at Brooklyn Museum',
                'description': 'Live jazz music with brunch at the museum café',
                'date': sunday.isoformat(),
                'location': '200 Eastern Pkwy, Brooklyn, NY 11238',
                'type': 'music',
                'url': 'https://www.brooklynmuseum.org/'
            },
            {
                'title': 'Kids Weekend Workshop: Clay Sculpting',
                'description': 'Hands-on clay sculpting workshop for kids aged 7-12',
                'date': saturday.isoformat(),
                'location': 'Park Slope Library, Brooklyn, NY',
                'type': 'art',
                'url': 'https://example.com'
            }
        ]
        
        sample_events.extend(weekend_events)
        
        # Add sample location coordinates (approximate)
        sample_locations = [
            {'lat': 40.7058, 'lng': -73.9468},  # Grand St, Williamsburg
            {'lat': 40.7037, 'lng': -73.9544},  # W 3rd St, Brooklyn
            {'lat': 40.6694, 'lng': -73.9479},  # Brooklyn Children's Museum
            {'lat': 40.6824, 'lng': -73.9782},  # Flatbush Ave
            {'lat': 40.6616, 'lng': -73.9794},  # 7th Ave Park Slope
            {'lat': 40.6627, 'lng': -73.9700},  # Prospect Park
            {'lat': 40.6712, 'lng': -73.9642},  # Brooklyn Museum
            {'lat': 40.6865, 'lng': -73.9807},  # Atlantic Ave
            {'lat': 40.6782, 'lng': -73.9712},  # Prospect Heights (Weekend Art Walk)
            {'lat': 40.6712, 'lng': -73.9642},  # Brooklyn Museum (Sunday Jazz)
            {'lat': 40.6616, 'lng': -73.9794}   # Park Slope Library (Clay Sculpting)
        ]
        
        for i, event in enumerate(sample_events):
            if i < len(sample_locations):
                loc = sample_locations[i]
                distance = calculate_distance(
                    PROSPECT_HEIGHTS['lat'], PROSPECT_HEIGHTS['lng'],
                    loc['lat'], loc['lng']
                )
                event['distance'] = distance
        
        events.extend(sample_events)
        
    except Exception as e:
        print(f"Error fetching NYC government events: {e}")
    
    return events

def fetch_external_api_events():
    """Fetch events from external APIs like Eventbrite, Facebook Events, etc."""
    events = []
    
    # Placeholder for additional event sources
    # In a real implementation, you would make API calls to:
    # - Eventbrite API
    # - Facebook Events API
    # - Meetup API
    # - Various Brooklyn-specific event websites
    
    return events

@app.route('/api/events')
def get_events():
    """API endpoint to get aggregated events"""
    
    # Try to load from cache first
    cached_events = load_cache()
    if cached_events:
        return jsonify({'events': cached_events})
    
    # Fetch events from multiple sources
    all_events = []
    
    # Scrape from web sources
    try:
        scraped_events = scrape_all_sources()
        all_events.extend(scraped_events)
    except Exception as e:
        print(f"Error scraping events: {e}")
    
    # Fetch from NYC government/data sources (keep as fallback)
    all_events.extend(fetch_nyc_government_events())
    
    # Fetch from external APIs
    all_events.extend(fetch_external_api_events())
    
    # Save to cache
    save_cache(all_events)
    
    return jsonify({'events': all_events})

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

if __name__ == '__main__':
    # Ensure cache directory exists
    Path(CACHE_FILE).parent.mkdir(parents=True, exist_ok=True)
    
    app.run(debug=True, port=5001)

