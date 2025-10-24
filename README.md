# Art & Music Events Aggregator

A web application that aggregates upcoming art and music events for kids and adults in Brooklyn, New York, with a focus on the Prospect Heights/Park Slope area.

## Features

- **Event Aggregation**: Fetches events from multiple sources
- **Location-Based Sorting**: Sort events by distance from Prospect Heights
- **Data Caching**: Reduces API calls with 1-hour cache duration
- **Modern UI**: Beautiful, responsive design with smooth animations
- **Filtering**: Filter events by type (Art, Music, or All)

## Setup

1. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

2. Run the Flask server:
```bash
python3 app.py
```

3. Open your browser and navigate to:
```
http://localhost:5001
```

## Event Sources

The app aggregates events from multiple sources:

### Kids & Family
- Brooklyn Paper Events
- Brooklyn Public Library (Youth & Family Events)
- Brooklyn Children's Museum

### Art & Culture
- WAGMAG (Brooklyn art guide)
- ArtRabbit Brooklyn listings
- Brooklyn Art Haus

### Music & Performance
- Eventbrite Brooklyn Music
- Various Brooklyn venues

Note: Currently includes sample events that demonstrate the functionality. To add real scraping, update the `scrapers.py` file with proper HTML parsing for each source.

## Project Structure

- `app.py` - Flask backend server with API endpoints
- `index.html` - Main HTML file
- `styles.css` - CSS styling
- `app.js` - Frontend JavaScript
- `requirements.txt` - Python dependencies
- `events_cache.json` - Cache file (created automatically)

## Milestones

### ✅ Milestone 1: Basic Web App Structure
- Set up HTML, CSS, and JavaScript
- Created modern, responsive UI
- Implemented basic event display

### 🔄 Milestone 2: Event Sources
- Integrated with sample event data
- Ready for API integration
- Cache mechanism implemented

### 📋 Milestone 3: Location Filtering
- Distance calculation implemented
- Sort by distance feature
- Filter by event type

### 📋 Milestone 4: Caching
- File-based caching system
- 1-hour cache duration
- Automatic cache invalidation

## Next Steps

To integrate real event sources, update the following functions in `app.py`:
- `fetch_nyc_government_events()` - Add NYC Open Data API integration
- `fetch_external_api_events()` - Add Eventbrite, Facebook Events, etc.

## Notes

- The app currently displays sample events to demonstrate functionality
- Replace sample data with actual API integrations for production use
- Event URLs and locations are approximate and should be verified

