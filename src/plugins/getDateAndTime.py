from datetime import datetime

def get_current_time():
    """Return the current time in HH:MM format"""
    return datetime.now().strftime("%H:%M")

def get_current_date():
    """Return the current date in DD MMM YYYY format"""
    return datetime.now().strftime("%d %b %Y")

def get_date_time(query: str) -> str:
    """Process user query and return appropriate date/time response"""
    query = query.lower()

    if any(word in query for word in ['time', 'hour']):
        return f"The current time in 24 hour format is {get_current_time()}"
    elif any(word in query for word in ['date', 'day', 'today']):
        return f"Today's date in DD MMM YYYY format is {get_current_date()}"
    else:
        return "You either didn't ask for date or time. Or I'm wasn't able to understand it. Please be more specific."
