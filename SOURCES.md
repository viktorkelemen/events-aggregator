# Event Sources Documentation

This document describes the various event sources that can be integrated into the Brooklyn Events Aggregator.

## Kids & Family Events

### Macaroni KID Brooklyn NW
- **URL**: brooklynnw.macaronikid.com
- **Description**: Comprehensive guide to family and kids' events, classes, and activities in Brooklyn
- **Update Frequency**: Weekly
- **Content**: Local listings and event calendars

### Mommy Poppins Brooklyn
- **URL**: mommypoppins.com/new-york-city/brooklyn
- **Description**: Things to do with kids, including art programs, family outings, and seasonal events
- **Content**: Brooklyn-wide coverage

### Brooklyn Bridge Parents
- **URL**: brooklynbridgeparents.com/events
- **Description**: Local parents' site listing classes, camps, and kids' events
- **Content**: Across Brooklyn neighborhoods

### Brooklyn Paper Events
- **URL**: events.brooklynpaper.com
- **Description**: Updated local calendar with family-friendly activities, festivals, and kid-oriented programs
- **Content**: Brooklyn-wide

### Brooklyn Public Library – Youth & Family Events
- **URL**: bklynlibrary.org/event-series
- **Description**: Free arts, storytimes, and educational family programs
- **Content**: Various branch locations

### NYC Parks "Best for Kids"
- **URL**: nycgovparks.org/events/kids
- **Description**: Citywide outdoor events including park-based activities, crafts, and games
- **Content**: Many Brooklyn playgrounds

### New York Family Events Calendar
- **URL**: events.newyorkfamily.com
- **Description**: Citywide family happenings, including Brooklyn fairs, performances, and workshops

## Art & Culture

### WAGMAG
- **URL**: wagmag.org
- **Description**: Monthly Brooklyn art guide listing gallery shows, exhibitions, and performance art events
- **Neighborhoods**: Red Hook, Williamsburg, and others

### ArtRabbit Brooklyn Listings
- **URL**: artrabbit.com/all-listings/united-states/brooklyn
- **Description**: Online directory for contemporary art exhibitions and openings
- **Content**: Brooklyn galleries and venues

### Brooklyn Art Haus
- **URL**: bkarthaus.com
- **Description**: Williamsburg-based venue listing contemporary art, film, and performance events

### Brooklyn Paper Art Shows
- **URL**: events.brooklynpaper.com/things-to-do/brooklyn/art-shows
- **Description**: Regularly updated guide to art exhibitions and cultural events

### Brooklyn Children's Museum
- **URL**: brooklynkids.org/events
- **Description**: Rotating art exhibits, toddler workshops, and family craft events

## Music & Performance

### Bandsintown Brooklyn
- **URL**: bandsintown.com/c/brooklyn-ny
- **Description**: Comprehensive list of upcoming concerts, local gigs, and festivals
- **Content**: All genres and venues

### Eventbrite Brooklyn Music
- **URL**: eventbrite.com/b/ny--brooklyn/music
- **Description**: User-friendly event calendar showing concerts, open mics, and ticketed performances

### Oh My Rockness NYC
- **URL**: ohmyrockness.com
- **Description**: Indie concert calendar with recommendations for smaller shows
- **Content**: Under-the-radar Brooklyn venues

### Bargemusic
- **URL**: bargemusic.org
- **Description**: Free live classical concerts at Brooklyn Bridge Park Boathouse
- **Content**: Family-friendly programming on weekends

## Implementation Notes

To implement scraping for these sources:

1. Each source requires custom HTML parsing based on its structure
2. Many sites may have JavaScript-rendered content (consider using Selenium or Playwright)
3. Some sites may have APIs available
4. Always respect robots.txt and rate limiting
5. Consider using caching to reduce server load
6. Handle errors gracefully when sites are unavailable

## Current Implementation

The `scrapers.py` file currently includes:
- `scrape_brooklyn_paper_events()` - Sample implementation
- `scrape_brooklyn_library_events()` - Sample implementation
- `scrape_eventbrite_music()` - Sample implementation
- `scrape_wagmag_art()` - Sample implementation

These functions return sample data and should be expanded with actual HTML parsing logic.

