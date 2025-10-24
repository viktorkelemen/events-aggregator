// Prospect Heights coordinates (default location)
const PROSPECT_HEIGHTS = {
    lat: 40.6782,
    lng: -73.9712
};

let allEvents = [];

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    loadEvents();
    
    // Set up event listeners
    document.getElementById('sortBy').addEventListener('change', handleSort);
    document.getElementById('filterType').addEventListener('change', handleFilter);
    document.getElementById('refreshBtn').addEventListener('click', loadEvents);
});

// Load events from the backend
async function loadEvents() {
    const loadingEl = document.getElementById('loading');
    const containerEl = document.getElementById('eventsContainer');
    const weekendEl = document.getElementById('weekendEvents');
    const weekendSection = document.getElementById('weekendSection');
    
    loadingEl.classList.remove('hidden');
    containerEl.innerHTML = '';
    weekendEl.innerHTML = '';
    
    try {
        const response = await fetch('/api/events');
        if (!response.ok) {
            throw new Error('Failed to fetch events');
        }
        
        const data = await response.json();
        allEvents = data.events || [];
        
        // Separate weekend and other events
        const weekendEvents = getWeekendEvents(allEvents);
        const otherEvents = allEvents.filter(event => !weekendEvents.includes(event));
        
        // Display weekend events if any
        if (weekendEvents.length > 0) {
            weekendSection.classList.remove('hidden');
            displayEvents(weekendEvents, weekendEl);
        } else {
            weekendSection.classList.add('hidden');
        }
        
        // Display other events
        displayEvents(otherEvents, containerEl);
    } catch (error) {
        console.error('Error loading events:', error);
        containerEl.innerHTML = `
            <div class="empty-state">
                <h2>⚠️ Unable to load events</h2>
                <p>Please try again later or check your connection.</p>
            </div>
        `;
    } finally {
        loadingEl.classList.add('hidden');
    }
}

// Get events happening this weekend (Saturday and Sunday)
function getWeekendEvents(events) {
    const now = new Date();
    const today = now.getDay(); // 0 = Sunday, 6 = Saturday
    
    // Find the upcoming Saturday
    let daysUntilSaturday = (6 - today) % 7;
    if (daysUntilSaturday === 0 && today !== 6) {
        daysUntilSaturday = 7;
    }
    
    const saturday = new Date(now);
    saturday.setDate(now.getDate() + daysUntilSaturday);
    saturday.setHours(0, 0, 0, 0);
    
    const sunday = new Date(saturday);
    sunday.setDate(saturday.getDate() + 1);
    sunday.setHours(23, 59, 59, 999);
    
    return events.filter(event => {
        if (!event.date) return false;
        const eventDate = new Date(event.date);
        return eventDate >= saturday && eventDate <= sunday;
    });
}

// Display events in the container
function displayEvents(events, containerEl = null) {
    const container = containerEl || document.getElementById('eventsContainer');
    
    if (events.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h2>No events found</h2>
                <p>Try adjusting your filters or check back later.</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = events.map(event => createEventCard(event)).join('');
}

// Create HTML for a single event card
function createEventCard(event) {
    const distance = event.distance ? `${event.distance.toFixed(1)} miles away` : '';
    const date = event.date ? new Date(event.date).toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }) : 'Date TBD';
    
    return `
        <div class="event-card">
            <span class="event-type ${event.type}">${event.type.toUpperCase()}</span>
            <h3 class="event-title">${escapeHtml(event.title)}</h3>
            <div class="event-date">📅 ${date}</div>
            <div class="event-location">📍 ${escapeHtml(event.location)}</div>
            ${distance ? `<div class="event-distance">${distance}</div>` : ''}
            ${event.description ? `<div class="event-description">${escapeHtml(event.description)}</div>` : ''}
            ${event.url ? `<a href="${event.url}" target="_blank" class="event-link">More Info →</a>` : ''}
        </div>
    `;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Handle sorting
function handleSort() {
    const sortBy = document.getElementById('sortBy').value;
    const filteredEvents = getFilteredEvents();
    
    // Separate weekend and other events
    const weekendEvents = getWeekendEvents(filteredEvents);
    const otherEvents = filteredEvents.filter(event => !weekendEvents.includes(event));
    
    let sortedWeekend = [...weekendEvents];
    let sortedOther = [...otherEvents];
    
    const sortEvents = (events) => {
        let sorted = [...events];
        switch (sortBy) {
            case 'date':
                sorted.sort((a, b) => {
                    const dateA = a.date ? new Date(a.date) : new Date(0);
                    const dateB = b.date ? new Date(b.date) : new Date(0);
                    return dateA - dateB;
                });
                break;
            case 'distance':
                sorted.sort((a, b) => {
                    const distA = a.distance !== undefined ? a.distance : Infinity;
                    const distB = b.distance !== undefined ? b.distance : Infinity;
                    return distA - distB;
                });
                break;
            case 'type':
                sorted.sort((a, b) => a.type.localeCompare(b.type));
                break;
        }
        return sorted;
    };
    
    sortedWeekend = sortEvents(sortedWeekend);
    sortedOther = sortEvents(sortedOther);
    
    // Display weekend events if any
    const weekendSection = document.getElementById('weekendSection');
    if (sortedWeekend.length > 0) {
        weekendSection.classList.remove('hidden');
        displayEvents(sortedWeekend, document.getElementById('weekendEvents'));
    } else {
        weekendSection.classList.add('hidden');
    }
    
    // Display other events
    displayEvents(sortedOther);
}

// Handle filtering
function handleFilter() {
    handleSort();
}

// Get filtered events based on current filter selection
function getFilteredEvents() {
    const filterType = document.getElementById('filterType').value;
    
    if (filterType === 'all') {
        return allEvents;
    }
    
    return allEvents.filter(event => event.type === filterType);
}

