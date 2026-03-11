import sqlite3

# database connect
con = sqlite3.connect("jarvis.db", check_same_thread=False)
cursor = con.cursor()

# create memory table
cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    content TEXT
)
""")

con.commit()


# ---------------- ADD MEMORY ----------------

def add_memory(role, content):

    cursor.execute(
        "INSERT INTO memory (role, content) VALUES (?, ?)",
        (role, content)
    )

    con.commit()


# ---------------- GET MEMORY ----------------

def get_memory():

    cursor.execute(
        "SELECT role, content FROM memory ORDER BY id DESC LIMIT 20"
    )

    rows = cursor.fetchall()

    messages = []

    for row in rows[::-1]:

        messages.append({
            "role": row[0],
            "content": row[1]
        })

    return messages