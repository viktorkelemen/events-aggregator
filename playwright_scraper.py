"""
Playwright-based scraper for JavaScript-heavy websites
"""
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def scrape_with_playwright(url, wait_selector=None, wait_time=3):
    """
    Scrape a JavaScript-heavy website using Playwright
    
    Args:
        url: URL to scrape
        wait_selector: CSS selector to wait for (optional)
        wait_time: Time to wait if no selector provided (default: 3 seconds)
    
    Returns:
        BeautifulSoup object with parsed HTML
    """
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Navigate to the page
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Wait for specific content or fixed time
            if wait_selector:
                try:
                    page.wait_for_selector(wait_selector, timeout=10000)
                except:
                    print(f"Warning: Selector '{wait_selector}' not found")
            else:
                time.sleep(wait_time)
            
            # Get the fully rendered HTML
            content = page.content()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            return soup
            
        except Exception as e:
            print(f"Error during Playwright scraping: {e}")
            return None
            
        finally:
            browser.close()

def scrape_eventbrite_with_playwright():
    """Scrape Eventbrite Brooklyn events using Playwright"""
    events = []
    
    try:
        url = 'https://www.eventbrite.com/b/ny--brooklyn/music'
        soup = scrape_with_playwright(url, wait_selector='.event-card', wait_time=5)
        
        if soup:
            # Look for event cards (structure may vary)
            event_cards = soup.find_all(['div', 'article'], class_=lambda x: x and 'event' in x.lower())
            
            print(f"Found {len(event_cards)} potential event cards")
            
            # Extract event data (adjust selectors based on actual HTML structure)
            for card in event_cards[:5]:  # Limit to 5 events for now
                title_elem = card.find(['h2', 'h3', 'h4'], class_=lambda x: x and 'title' in str(x).lower())
                title = title_elem.get_text(strip=True) if title_elem else None
                
                if title:
                    events.append({
                        'title': title,
                        'description': 'Brooklyn music event from Eventbrite',
                        'date': None,  # Would need to parse date
                        'location': 'Brooklyn, NY',
                        'type': 'music',
                        'url': url,
                        'source': 'Eventbrite (Playwright)',
                        'source_id': f'eventbrite_{hash(title)}'
                    })
        
    except Exception as e:
        print(f"Error scraping Eventbrite with Playwright: {e}")
    
    return events

def scrape_mommy_poppins_with_playwright():
    """Scrape Mommy Poppins events using Playwright"""
    events = []
    
    try:
        url = 'https://mommypoppins.com/new-york-city/brooklyn'
        soup = scrape_with_playwright(url, wait_selector='article', wait_time=5)
        
        if soup:
            # Look for articles or event listings
            articles = soup.find_all('article', limit=5)
            
            for article in articles:
                title_elem = article.find(['h2', 'h3'])
                title = title_elem.get_text(strip=True) if title_elem else None
                
                if title:
                    events.append({
                        'title': title,
                        'description': 'Family-friendly event in Brooklyn',
                        'date': None,
                        'location': 'Brooklyn, NY',
                        'type': 'art',
                        'url': url,
                        'source': 'Mommy Poppins (Playwright)',
                        'source_id': f'mommypoppins_{hash(title)}'
                    })
        
    except Exception as e:
        print(f"Error scraping Mommy Poppins with Playwright: {e}")
    
    return events

def scrape_macaroni_kid_with_playwright():
    """Scrape Macaroni KID Brooklyn events using Playwright"""
    events = []
    
    try:
        url = 'https://brooklynnw.macaronikid.com'
        soup = scrape_with_playwright(url, wait_time=5)
        
        if soup:
            # Look for event listings
            listings = soup.find_all(['div', 'article'], class_=lambda x: x and ('event' in str(x).lower() or 'activity' in str(x).lower()), limit=5)
            
            for listing in listings:
                title_elem = listing.find(['h2', 'h3', 'h4'])
                title = title_elem.get_text(strip=True) if title_elem else None
                
                if title:
                    events.append({
                        'title': title,
                        'description': 'Kids and family event in Brooklyn',
                        'date': None,
                        'location': 'Brooklyn, NY',
                        'type': 'art',
                        'url': url,
                        'source': 'Macaroni KID (Playwright)',
                        'source_id': f'macaronikid_{hash(title)}'
                    })
        
    except Exception as e:
        print(f"Error scraping Macaroni KID with Playwright: {e}")
    
    return events

if __name__ == '__main__':
    # Test Playwright scraping
    print("Testing Playwright scraping...")
    
    print("\n1. Testing Eventbrite:")
    eventbrite_events = scrape_eventbrite_with_playwright()
    print(f"Found {len(eventbrite_events)} events")
    
    print("\n2. Testing Mommy Poppins:")
    mommy_events = scrape_mommy_poppins_with_playwright()
    print(f"Found {len(mommy_events)} events")
    
    print("\n3. Testing Macaroni KID:")
    macaroni_events = scrape_macaroni_kid_with_playwright()
    print(f"Found {len(macaroni_events)} events")

