import sqlite3


def save_to_db(start_time, end_time, prompt, system_prompt, message_content):
    conn = sqlite3.connect('openai_model_handler.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO requests (start_time, end_time, prompt, system_prompt, message_content)
    VALUES (?, ?, ?, ?, ?);
    ''', (start_time, end_time, prompt, system_prompt, message_content))
    conn.commit()
    conn.close()


def setup_db():
    conn = sqlite3.connect('openai_model_handler.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time DATETIME,
        end_time DATETIME,
        prompt TEXT,
        system_prompt TEXT,
        message_content TEXT
    );
    ''')
    conn.commit()
    conn.close()
