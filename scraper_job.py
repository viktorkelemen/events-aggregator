"""
Background scraper job to fetch events and save to database
Run this as a scheduled task (cron) or separate service
"""
import sys
from datetime import datetime
from scrapers import scrape_all_sources
from database import insert_event, log_scraping_run, init_db
import traceback

def run_scraper():
    """Run the scraper and save results to database"""
    print(f"Starting scraper run at {datetime.now()}")
    
    # Initialize database if needed
    init_db()
    
    # Get all scraped events
    try:
        all_events = scrape_all_sources()
        print(f"Scraped {len(all_events)} events total")
        
        events_added = 0
        for event in all_events:
            try:
                # Generate a unique source_id if not present
                if 'source_id' not in event:
                    event['source_id'] = f"{event.get('title', '')}_{event.get('date', '')}"
                
                insert_event(event)
                events_added += 1
            except Exception as e:
                print(f"Error inserting event: {e}")
                print(f"Event: {event.get('title', 'Unknown')}")
        
        # Log successful run
        log_scraping_run(
            source='all',
            status='success',
            events_found=len(all_events),
            events_added=events_added
        )
        
        print(f"Successfully added {events_added} events to database")
        
    except Exception as e:
        error_msg = traceback.format_exc()
        print(f"Error during scraping: {error_msg}")
        
        # Log failed run
        log_scraping_run(
            source='all',
            status='failed',
            events_found=0,
            events_added=0,
            error_message=str(e)
        )
        
        sys.exit(1)

if __name__ == '__main__':
    run_scraper()

