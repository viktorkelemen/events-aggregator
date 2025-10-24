# Web Scraping Implementation Guide

## Current Implementation

The scrapers currently attempt to fetch data from these sources:

### ✅ Currently Integrated
- **Brooklyn Paper Events** - Attempts HTML parsing
- **Brooklyn Public Library** - Searches for JSON-LD structured data
- **Eventbrite** - Uses HTML parsing (consider using their API)
- **WAGMAG** - Searches for exhibition listings
- **Bargemusic** - Attempts concert scraping
- **Mommy Poppins** - Attempts event parsing

### ⚠️ Challenges with Modern Websites

Many modern websites load content dynamically using JavaScript. Simple HTTP requests with BeautifulSoup will only get the initial HTML, not the dynamically loaded content.

#### Sites That Likely Need JavaScript Rendering:
- **Eventbrite** - Heavy JavaScript for event listings
- **Mommy Poppins** - React-based site
- **Macaroni KID** - Dynamic content loading
- **Brooklyn Bridge Parents** - Likely JavaScript-rendered
- **ArtRabbit** - Modern web app
- **Bandsintown** - JavaScript-heavy
- **Oh My Rockness** - Dynamic content

## Solutions for JavaScript-Heavy Sites

### Option 1: Use Selenium (Recommended for Complex Sites)
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_with_selenium(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    # Wait for content to load
    time.sleep(3)
    
    # Now parse the HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup
```

### Option 2: Use Playwright (Modern Alternative)
```python
from playwright.sync_api import sync_playwright

def scrape_with_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        # Wait for content
        page.wait_for_selector('.event-item')
        content = page.content()
        browser.close()
        return BeautifulSoup(content, 'html.parser')
```

### Option 3: Use Official APIs (Best Practice)

#### Eventbrite API
```python
import requests

def get_eventbrite_events():
    # Requires API key from https://www.eventbrite.com/platform/api/
    url = "https://www.eventbriteapi.com/v3/events/search/"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY"
    }
    params = {
        "location.address": "Brooklyn, NY",
        "categories": "music"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()
```

#### Brooklyn Public Library API
Some libraries have APIs or RSS feeds available. Check their documentation.

## Current Limitations

1. **Fallback to Sample Data**: When HTML parsing fails or doesn't find expected structures, scrapers return sample data to demonstrate functionality.

2. **No JavaScript Rendering**: Current implementation uses only BeautifulSoup, which cannot execute JavaScript.

3. **API Keys Required**: Many services (Eventbrite, Bandsintown) require API keys for programmatic access.

## Recommendations

### Short Term
1. Add sample data from more sources
2. Document which sites have APIs available
3. Add better error handling and logging

### Medium Term
1. Integrate Eventbrite API (requires API key)
2. Add Selenium for JavaScript-heavy sites
3. Implement rate limiting to avoid being blocked

### Long Term
1. Set up a proper scraping infrastructure
2. Use message queues for asynchronous scraping
3. Monitor sites for HTML structure changes
4. Consider using scraping services like ScraperAPI or ProxyMesh

## Adding a New Scraper

1. Create a function in `scrapers.py`:
```python
def scrape_new_source():
    events = []
    try:
        url = 'https://example.com'
        headers = {'User-Agent': 'Mozilla/5.0...'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Parse HTML here
            # or use API if available
            # or fallback to sample data
        
    except Exception as e:
        print(f"Error scraping New Source: {e}")
    
    return events
```

2. Add it to `scrape_all_sources()`:
```python
all_events.extend(scrape_new_source())
```

3. Add location mappings to `geocode_location()` if needed

## Respecting Websites

- Always include a proper User-Agent header
- Add delays between requests
- Respect robots.txt
- Don't scrape too frequently
- Consider reaching out to sites for API access
- If possible, use official APIs instead of scraping

## Next Steps

To implement real scraping:

1. **Add Selenium**: `pip install selenium`
2. **Choose target sites**: Start with one or two sources
3. **Inspect HTML**: Use browser dev tools to understand structure
4. **Write parsers**: Extract title, date, location, description
5. **Test thoroughly**: Ensure parsers are robust to HTML changes
6. **Handle errors**: Gracefully handle failures
7. **Monitor**: Set up logging to detect when scrapers break

## Ethical Considerations

- Check each site's Terms of Service
- Some sites explicitly prohibit scraping
- Consider reaching out for permission or API access
- Be respectful of server resources
- Don't overload servers with requests

