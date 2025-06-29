from datetime import datetime


def get_current_time():
    """Return the current time in HH:MM format"""
    return f"The current time is {datetime.now().strftime("%H:%M")}"


def get_current_date():
    """Return the current date in DD MMM YYYY format"""
    return f"Today's date is {datetime.now().strftime("%d %b %Y")}"
