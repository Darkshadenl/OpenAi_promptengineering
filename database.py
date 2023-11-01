import sqlite3


def save_to_db(total_time, prompt, system_prompt, message_content, total_input_tokens, total_output_tokens, correct=False):
    conn = sqlite3.connect('openai_model_handler.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO requests (
        prompt,
        system_prompt,
        message_content,
        total_input_tokens,
        total_output_tokens,
        total_time,
        correct
    )
    VALUES (?, ?, ?, ?, ?, ?, ?);
    ''', (prompt, system_prompt, message_content, total_input_tokens, total_output_tokens, total_time, correct))
    conn.commit()
    conn.close()


def setup_db():
    conn = sqlite3.connect('openai_model_handler.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt TEXT,
        system_prompt TEXT,
        message_content TEXT,
        total_input_tokens INTEGER,
        total_output_tokens INTEGER,
        total_time TEXT,
        correct BOOLEAN
    );
    ''')
    conn.commit()
    conn.close()

