import os
import sqlite3
from datetime import datetime

# Define the directory for storing the database
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "notes.db")

# Initialize the database


def init_db():
    """Initialize the SQLite database with the notes table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create notes table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


# Initialize the database when the module is imported
init_db()


def save_note(title, content):
    """Save a note with the given title and content"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if a note with this title already exists
    cursor.execute("SELECT id FROM notes WHERE title = ?", (title,))
    existing_note = cursor.fetchone()

    current_time = datetime.now().isoformat()

    if existing_note:
        # Update existing note
        cursor.execute(
            "UPDATE notes SET content = ?, updated_at = ? WHERE title = ?",
            (content, current_time, title)
        )
        conn.commit()
        conn.close()
        return f"Note '{title}' updated successfully."
    else:
        # Insert new note
        cursor.execute(
            "INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (title, content, current_time, current_time)
        )
        conn.commit()
        conn.close()
        return f"Note '{title}' saved successfully."


def get_note(title):
    """Retrieve a note by its title"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT title, content, created_at FROM notes WHERE title = ?", (title,))
    note = cursor.fetchone()

    conn.close()

    if not note:
        return f"No note found with title '{title}'."

    title, content, created_at = note
    return f"Note: {title}\nCreated: {created_at}\n\n{content}"


def list_notes():
    """List all available notes"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT title, created_at FROM notes ORDER BY created_at DESC")
    notes = cursor.fetchall()

    conn.close()

    if not notes:
        return "No notes found."

    notes_list = []
    for title, created_at in notes:
        # Format the date to be more readable
        date_obj = datetime.fromisoformat(created_at)
        formatted_date = date_obj.strftime("%Y-%m-%d")
        notes_list.append(f"- {title} (created: {formatted_date})")

    return "Available notes:\n" + "\n".join(notes_list)


def update_note(title, content):
    """Update an existing note"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if the note exists
    cursor.execute("SELECT id FROM notes WHERE title = ?", (title,))
    if not cursor.fetchone():
        conn.close()
        return f"No note found with title '{title}'."

    # Update the note
    current_time = datetime.now().isoformat()
    cursor.execute(
        "UPDATE notes SET content = ?, updated_at = ? WHERE title = ?",
        (content, current_time, title)
    )

    conn.commit()
    conn.close()

    return f"Note '{title}' updated successfully."


def delete_note(title):
    """Delete a note by its title"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if the note exists
    cursor.execute("SELECT id FROM notes WHERE title = ?", (title,))
    if not cursor.fetchone():
        conn.close()
        return f"No note found with title '{title}'."

    # Delete the note
    cursor.execute("DELETE FROM notes WHERE title = ?", (title,))

    conn.commit()
    conn.close()

    return f"Note '{title}' deleted successfully."


def search_notes(query):
    """Search for notes containing the query in title or content"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    search_pattern = f"%{query}%"
    cursor.execute(
        "SELECT title, created_at FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY created_at DESC",
        (search_pattern, search_pattern)
    )
    notes = cursor.fetchall()

    conn.close()

    if not notes:
        return f"No notes found matching '{query}'."

    notes_list = []
    for title, created_at in notes:
        # Format the date to be more readable
        date_obj = datetime.fromisoformat(created_at)
        formatted_date = date_obj.strftime("%Y-%m-%d")
        notes_list.append(f"- {title} (created: {formatted_date})")

    return f"Notes matching '{query}':\n" + "\n".join(notes_list)
