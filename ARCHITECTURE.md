# Recommended Architecture for Web Scraping

## Current Setup (Simple)

Right now, the app scrapes events on-demand when requested. This is fine for development but not scalable.

## Recommended Architecture

### 1. **Database-Backed Architecture** ✅ (Implementation provided)

**Why use a database?**
- **Performance**: Cache scraped data instead of scraping on every request
- **Deduplication**: Avoid duplicate events across multiple sources
- **Reliability**: If a site is down, still serve cached data
- **Analytics**: Track scraping success rates, popular events, etc.
- **Scheduling**: Run scrapers at specific times, not on-demand

**Structure:**
```
scraper_job.py (runs periodically)
    ↓
scrapers.py (fetches events)
    ↓
database.py (saves to SQLite)
    ↓
app.py (serves from database)
```

### 2. **Scheduling Options**

#### Option A: Cron Job (Unix/Mac)
```bash
# Run scraper every hour
0 * * * * cd /path/to/events-aggregator && python3 scraper_job.py
```

#### Option B: Python Scheduled Task
```python
import schedule
import time

schedule.every().hour.do(run_scraper)

while True:
    schedule.run_pending()
    time.sleep(60)
```

#### Option C: Systemd Timer (Linux)
Create `/etc/systemd/system/scraper.service`:
```ini
[Unit]
Description=Brooklyn Events Scraper

[Service]
Type=oneshot
User=youruser
WorkingDirectory=/path/to/events-aggregator
ExecStart=/usr/bin/python3 scraper_job.py
```

Create `/etc/systemd/system/scraper.timer`:
```ini
[Unit]
Description=Run scraper hourly

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
```

### 3. **For JavaScript-Heavy Sites**

Many modern sites require JavaScript rendering. Use these tools:

#### Option A: Selenium + Chrome Headless
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_with_selenium(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    time.sleep(3)  # Wait for JS to load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup
```

**Installation:**
```bash
pip install selenium
# Download ChromeDriver from https://chromedriver.chromium.org/
```

#### Option B: Playwright (Recommended)
```python
from playwright.sync_api import sync_playwright

def scrape_with_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector('.event-card')  # Wait for content
        content = page.content()
        browser.close()
        return BeautifulSoup(content, 'html.parser')
```

**Installation:**
```bash
pip install playwright
playwright install chromium
```

#### Option C: Puppeteer + API
Set up a Node.js service that uses Puppeteer to render pages and expose an API endpoint your Python scraper can call.

### 4. **Recommended Tools by Site**

| Site | Tool | Why |
|------|------|-----|
| Eventbrite | API | Official API available (requires key) |
| Brooklyn Paper | BeautifulSoup | Static HTML |
| Brooklyn Library | API/RSS | Check for feed availability |
| Mommy Poppins | Selenium/Playwright | JavaScript-heavy |
| Macaroni KID | Selenium/Playwright | Dynamic content |
| WAGMAG | BeautifulSoup | Static exhibition listings |
| Bargemusic | BeautifulSoup | Likely static |

### 5. **Rate Limiting & Etiquette**

```python
import time
from datetime import datetime

class RateLimiter:
    def __init__(self, delay_seconds=2):
        self.delay = delay_seconds
        self.last_request = {}
    
    def wait_if_needed(self, source):
        if source in self.last_request:
            elapsed = (datetime.now() - self.last_request[source]).seconds
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)
        self.last_request[source] = datetime.now()

# Usage
rate_limiter = RateLimiter(delay_seconds=3)
for source in sources:
    rate_limiter.wait_if_needed(source)
    scrape(source)
```

### 6. **Error Handling & Retry Logic**

```python
from functools import wraps
import time

def retry(max_attempts=3, delay=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=5)
def scrape_source(url):
    # scraping code
    pass
```

### 7. **Monitoring & Alerts**

#### Option A: Email Notifications
```python
import smtplib
from email.mime.text import MIMEText

def send_alert(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = 'alerts@example.com'
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    server.send_message(msg)
    server.quit()
```

#### Option B: Slack Webhook
```python
import requests

def send_slack_alert(message):
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    requests.post(webhook_url, json={"text": message})
```

### 8. **Deployment Options**

#### Option A: Single Server
- Run scraper job on cron
- Flask app serves from database
- Simple but single point of failure

#### Option B: Microservices
- Scraper service: Runs scrapers, saves to database
- API service: Flask app serving events
- Database: PostgreSQL or MySQL
- Redis: For caching frequently accessed data

#### Option C: Serverless (AWS Lambda)
- Lambda function runs scrapers on schedule
- Stores data in DynamoDB or RDS
- API Gateway serves events
- Scales automatically

### 9. **Database Migration Path**

When you outgrow SQLite, migrate to PostgreSQL:

```python
# database.py
import os
import psycopg2

def get_db():
    # Auto-detect environment
    if os.getenv('DATABASE_URL'):
        # Production: PostgreSQL
        return psycopg2.connect(os.getenv('DATABASE_URL'))
    else:
        # Development: SQLite
        return sqlite3.connect(DB_FILE)
```

### 10. **Next Steps**

1. **Test the database setup:**
   ```bash
   python3 database.py  # Initialize database
   python3 scraper_job.py  # Run scraper once
   ```

2. **Set up scheduling:**
   ```bash
   # Add to crontab
   crontab -e
   # Add: 0 * * * * cd /path/to/project && python3 scraper_job.py
   ```

3. **For JS-heavy sites, install Selenium:**
   ```bash
   pip install selenium
   # Download ChromeDriver
   ```

4. **Monitor and iterate:**
   - Check scraping_runs table for success rates
   - Monitor error logs
   - Adjust scraping frequency based on data freshness needs

### 11. **Best Practices**

- ✅ Use official APIs when available
- ✅ Respect robots.txt
- ✅ Add delays between requests
- ✅ Handle errors gracefully
- ✅ Log all scraping attempts
- ✅ Monitor for HTML structure changes
- ✅ Keep User-Agent headers realistic
- ✅ Cache aggressively (reduce load on target sites)
- ❌ Don't scrape too frequently
- ❌ Don't ignore site ToS
- ❌ Don't share API keys publicly

