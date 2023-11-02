import sqlite3
from openai_model_handler import OpenAiModelHandler


def save_to_db(handler: OpenAiModelHandler, prompt, correct=False):
    handler_message = handler.completion.choices[0].message
    conn = sqlite3.connect('openai_model_handler.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO requests (
        model,
        prompt,
        system_prompt,
        message_content,
        total_input_tokens,
        total_output_tokens,
        total_time,
        correct
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    ''', (handler.input.model, prompt, handler.input.get_system_prompt(), handler_message.content,
          handler.total_input_tokens, handler.total_output_tokens, str(handler.total_time), correct))
    conn.commit()
    conn.close()


def setup_db():
    conn = sqlite3.connect('openai_model_handler.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT,
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

