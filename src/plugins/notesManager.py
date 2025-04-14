import os
import sqlite3
from datetime import datetime

# Define the directory for storing the database
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
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

    cursor.execute("SELECT title, content, created_at FROM notes WHERE title = ?", (title,))
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

    cursor.execute("SELECT title, created_at FROM notes ORDER BY created_at DESC")
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

def manage_notes(query: str) -> str:
    """Process user query and return appropriate notes management response"""
    query = query.lower()

    # Check for save note command
    if "save note" in query or "create note" in query or "add note" in query:
        # Extract title and content
        parts = query.split("save note", 1) if "save note" in query else query.split("create note", 1) if "create note" in query else query.split("add note", 1)
        if len(parts) < 2:
            return "Please provide a title and content for the note. Format: save note [title] [content]"

        note_text = parts[1].strip()
        # Try to extract title and content
        if ":" in note_text:
            title, content = note_text.split(":", 1)
            return save_note(title.strip(), content.strip())
        else:
            # If no colon, use the first line as title and the rest as content
            lines = note_text.split("\n", 1)
            if len(lines) == 1:
                return "Please provide both a title and content for the note."
            return save_note(lines[0].strip(), lines[1].strip())

    # Check for get note command
    elif "get note" in query or "show note" in query or "read note" in query:
        parts = query.split("get note", 1) if "get note" in query else query.split("show note", 1) if "show note" in query else query.split("read note", 1)
        if len(parts) < 2 or not parts[1].strip():
            return "Please specify which note to retrieve."
        return get_note(parts[1].strip())

    # Check for list notes command
    elif "list notes" in query or "show all notes" in query or "what notes" in query:
        return list_notes()

    # Check for update note command
    elif "update note" in query or "edit note" in query:
        parts = query.split("update note", 1) if "update note" in query else query.split("edit note", 1)
        if len(parts) < 2:
            return "Please specify which note to update and provide new content."

        note_text = parts[1].strip()
        if ":" in note_text:
            title, content = note_text.split(":", 1)
            return update_note(title.strip(), content.strip())
        else:
            return "Please provide both a title and new content for the note. Format: update note [title]: [new content]"

    # Check for delete note command
    elif "delete note" in query or "remove note" in query:
        parts = query.split("delete note", 1) if "delete note" in query else query.split("remove note", 1)
        if len(parts) < 2 or not parts[1].strip():
            return "Please specify which note to delete."
        return delete_note(parts[1].strip())

    # Check for search notes command
    elif "search notes" in query or "find notes" in query:
        parts = query.split("search notes", 1) if "search notes" in query else query.split("find notes", 1)
        if len(parts) < 2 or not parts[1].strip():
            return "Please provide a search term."
        return search_notes(parts[1].strip())

    # Check for save URL command
    elif "save url" in query:
        parts = query.split("save url", 1)
        if len(parts) < 2:
            return "Please provide a title and URL. Format: save url [title]: [url]"

        url_text = parts[1].strip()
        if ":" in url_text:
            title, url = url_text.split(":", 1)
            return save_note(title.strip(), url.strip())
        else:
            return "Please provide both a title and URL. Format: save url [title]: [url]"

    # If no specific command is recognized
    else:
        return "I can help you manage notes. You can:\n- Save a note: 'save note [title]: [content]'\n- Save a URL: 'save url [title]: [url]'\n- Get a note: 'get note [title]'\n- List all notes: 'list notes'\n- Update a note: 'update note [title]: [new content]'\n- Delete a note: 'delete note [title]'\n- Search notes: 'search notes [query]'"
