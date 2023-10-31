import sqlite3


def save_to_db(start_time, end_time, prompt, system_prompt, message_content, correct=False):
    conn = sqlite3.connect('openai_model_handler.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO requests (start_time, end_time, prompt, system_prompt, message_content, correct)
    VALUES (?, ?, ?, ?, ?, ?);
    ''', (start_time, end_time, prompt, system_prompt, message_content, correct))
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
    cursor.execute('''
        ALTER TABLE requests ADD COLUMN correct BOOLEAN;
        ''')
    conn.commit()
    conn.close()

