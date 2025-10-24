"""
Web scrapers for various Brooklyn event sources
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import json
from playwright_scraper import (
    scrape_eventbrite_with_playwright,
    scrape_mommy_poppins_with_playwright,
    scrape_macaroni_kid_with_playwright
)

# Prospect Heights coordinates for distance calculation
PROSPECT_HEIGHTS = {
    'lat': 40.6782,
    'lng': -73.9712
}

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

def geocode_location(location_text):
    """
    Simple geocoding using approximate coordinates for Brooklyn locations
    In production, use Google Maps API or similar
    """
    brooklyn_locations = {
        'prospect park': (40.6627, -73.9700),
        'williamsburg': (40.7081, -73.9571),
        'park slope': (40.6782, -73.9840),
        'prospect heights': (40.6782, -73.9712),
        'brooklyn museum': (40.6712, -73.9642),
        'brooklyn children\'s museum': (40.6694, -73.9479),
        'brooklyn bridge park': (40.6981, -73.9969),
        'red hook': (40.6773, -74.0106),
        'flatbush': (40.6529, -73.9497),
        'gowanus': (40.6779, -73.9897),
        'fort greene': (40.6915, -73.9759),
        'crown heights': (40.6697, -73.9442),
        'dumbo': (40.7033, -73.9878),
        'carroll gardens': (40.6795, -73.9996),
        'boerum hill': (40.6865, -73.9807),
    }
    
    location_lower = location_text.lower()
    for key, coords in brooklyn_locations.items():
        if key in location_lower:
            return coords
    
    # Default to Prospect Heights if not found
    return PROSPECT_HEIGHTS['lat'], PROSPECT_HEIGHTS['lng']

def scrape_brooklyn_paper_events():
    """Scrape events from Brooklyn Paper"""
    events = []
    
    try:
        url = 'https://events.brooklynpaper.com'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find event listings (structure may vary)
            event_cards = soup.find_all(['article', 'div'], class_=re.compile(r'event|listing|card', re.I))
            
            # TODO: Parse actual event data from HTML
            
    except Exception as e:
        print(f"Error scraping Brooklyn Paper: {e}")
    
    return events

def scrape_brooklyn_library_events():
    """Scrape events from Brooklyn Public Library"""
    events = []
    
    try:
        # Brooklyn Library uses dynamic content, try to find JSON-LD or API endpoints
        url = 'https://www.bklynlibrary.org/event-series'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to extract JSON-LD structured data
            json_scripts = soup.find_all('script', type='application/ld+json')
            
            # TODO: Parse JSON-LD data or use Playwright for dynamic content
                
    except Exception as e:
        print(f"Error scraping Brooklyn Library: {e}")
    
    return events

def scrape_eventbrite_music():
    """Scrape music events from Eventbrite using Playwright"""
    events = []
    
    try:
        # Use Playwright for JavaScript-heavy Eventbrite
        playwright_events = scrape_eventbrite_with_playwright()
        events.extend(playwright_events)
                
    except Exception as e:
        print(f"Error scraping Eventbrite: {e}")
    
    return events

def scrape_wagmag_art():
    """Scrape art events from WAGMAG"""
    events = []
    
    try:
        url = 'https://wagmag.org'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find exhibition listings
            exhibitions = soup.find_all(['article', 'div'], class_=re.compile(r'exhibition|show|event', re.I))
            
            # TODO: Parse actual exhibition data from HTML
                
    except Exception as e:
        print(f"Error scraping WAGMAG: {e}")
    
    return events

def scrape_bargemusic():
    """Scrape events from Bargemusic"""
    events = []
    
    try:
        url = 'https://bargemusic.org'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for upcoming concerts
            concerts = soup.find_all(['div', 'article'], class_=re.compile(r'concert|event|show', re.I))
            
            # TODO: Parse actual concert data from HTML
                
    except Exception as e:
        print(f"Error scraping Bargemusic: {e}")
    
    return events

def scrape_mommy_poppins():
    """Scrape events from Mommy Poppins Brooklyn using Playwright"""
    events = []
    
    try:
        # Use Playwright for JavaScript-heavy Mommy Poppins
        playwright_events = scrape_mommy_poppins_with_playwright()
        events.extend(playwright_events)
                
    except Exception as e:
        print(f"Error scraping Mommy Poppins: {e}")
    
    return events

def scrape_macaroni_kid():
    """Scrape events from Macaroni KID Brooklyn using Playwright"""
    events = []
    
    try:
        # Use Playwright for JavaScript-heavy Macaroni KID
        playwright_events = scrape_macaroni_kid_with_playwright()
        events.extend(playwright_events)
                
    except Exception as e:
        print(f"Error scraping Macaroni KID: {e}")
    
    return events

def scrape_all_sources():
    """Scrape events from all sources"""
    all_events = []
    
    # Scrape from different sources
    all_events.extend(scrape_brooklyn_paper_events())
    all_events.extend(scrape_brooklyn_library_events())
    all_events.extend(scrape_eventbrite_music())
    all_events.extend(scrape_wagmag_art())
    all_events.extend(scrape_bargemusic())
    all_events.extend(scrape_mommy_poppins())
    all_events.extend(scrape_macaroni_kid())
    
    # Add distance to each event
    for event in all_events:
        lat, lng = geocode_location(event['location'])
        event['distance'] = calculate_distance(
            PROSPECT_HEIGHTS['lat'], PROSPECT_HEIGHTS['lng'],
            lat, lng
        )
    
    return all_events

