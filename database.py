"""
Database management for Brooklyn Events Aggregator
Uses SQLite for simplicity, but can be migrated to PostgreSQL/MySQL easily
"""
import sqlite3
from datetime import datetime, timedelta
from contextlib import contextmanager
import json

DB_FILE = 'events.db'

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """Initialize the database with required tables"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                location TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                distance REAL,
                type TEXT NOT NULL,
                url TEXT,
                source TEXT NOT NULL,
                source_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(source, source_id)
            )
        ''')
        
        # Create indexes for better query performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON events(date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON events(type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON events(source)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_distance ON events(distance)')
        
        # Scraping status table (to track scraping runs)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraping_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                status TEXT NOT NULL,
                events_found INTEGER DEFAULT 0,
                events_added INTEGER DEFAULT 0,
                error_message TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')
        
        print("Database initialized successfully")

def insert_event(event):
    """Insert or update an event in the database"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Try to update existing event first
        cursor.execute('''
            UPDATE events 
            SET title = ?, description = ?, date = ?, location = ?,
                latitude = ?, longitude = ?, distance = ?, type = ?,
                url = ?, updated_at = CURRENT_TIMESTAMP
            WHERE source = ? AND source_id = ?
        ''', (
            event.get('title'),
            event.get('description'),
            event.get('date'),
            event.get('location'),
            event.get('latitude'),
            event.get('longitude'),
            event.get('distance'),
            event.get('type'),
            event.get('url'),
            event.get('source'),
            event.get('source_id')
        ))
        
        # If no rows were updated, insert new event
        if cursor.rowcount == 0:
            cursor.execute('''
                INSERT INTO events 
                (title, description, date, location, latitude, longitude, 
                 distance, type, url, source, source_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event.get('title'),
                event.get('description'),
                event.get('date'),
                event.get('location'),
                event.get('latitude'),
                event.get('longitude'),
                event.get('distance'),
                event.get('type'),
                event.get('url'),
                event.get('source'),
                event.get('source_id')
            ))
        
        return cursor.lastrowid

def get_upcoming_events(min_date=None, max_date=None, event_type=None, limit=100):
    """Get upcoming events from the database"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        query = 'SELECT * FROM events WHERE 1=1'
        params = []
        
        if min_date:
            query += ' AND date >= ?'
            params.append(min_date)
        else:
            # Default: only future events
            query += ' AND date >= datetime("now")'
        
        if max_date:
            query += ' AND date <= ?'
            params.append(max_date)
        
        if event_type:
            query += ' AND type = ?'
            params.append(event_type)
        
        query += ' ORDER BY date ASC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]

def delete_old_events(days_old=30):
    """Delete events older than specified days"""
    with get_db() as conn:
        cursor = conn.cursor()
        cutoff_date = (datetime.now() - timedelta(days=days_old)).isoformat()
        cursor.execute('DELETE FROM events WHERE date < ?', (cutoff_date,))
        return cursor.rowcount

def log_scraping_run(source, status, events_found=0, events_added=0, error_message=None):
    """Log a scraping run"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO scraping_runs 
            (source, status, events_found, events_added, error_message, completed_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (source, status, events_found, events_added, error_message))

def get_scraping_stats():
    """Get statistics about scraping runs"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                source,
                COUNT(*) as total_runs,
                SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_runs,
                SUM(events_found) as total_events_found,
                SUM(events_added) as total_events_added,
                MAX(completed_at) as last_run
            FROM scraping_runs
            GROUP BY source
        ''')
        return [dict(row) for row in cursor.fetchall()]

if __name__ == '__main__':
    # Initialize database
    init_db()
    print("Database setup complete!")

