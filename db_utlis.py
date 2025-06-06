import sqlite3
from datetime import datetime

DB_NAME = "rag_app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_application_logs():
    conn = get_db_connection()
    conn.execute(''' CREATE TABLE IF NOT EXISTS application_logs
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    user_query TEXT,
                    api_response TEXT,
                    model TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    conn.close()

def create_document_store():
    conn = get_db_connection()
    conn.execute(''' CREATE TABLE IF NOT EXISTS document_stores
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      filename TEXT,
                      uplaod_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    conn.close()

def insert_application_logs(session_id, user_query, api_response, model):
    conn = get_db_connection()
    conn.execute('INSERT INTO application_logs (session_id,user_query, gpt_response, model) VALUES (?,?,?,?)',
                 (session_id, user_query,api_response, model))
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_query, api_response FROM application_logs WHERE session_id = ? ORDER BY created_at', (session_id,))
    messages = []
    for row in cursor.fetchall():
        messages.extend([
            {"role":"human", "content":row['user_query']},
            {"role": "ai", "content": row['api_response']}
        ])

    conn.close()
    return messages

def insert_document_record(filename):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO document_stores (filename) VALUES (?)', (filename,))
    file_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return file_id

def delete_document_record(file_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM document_stores WHERE id = ?', (file_id,))
    conn.commit()
    conn.close()
    return True

def get_all_documents():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, filename, upload_timestamp FROM document_stores ORDER BY upload_timestamp DESC')
    documents = cursor.fetchall()
    conn.close()
    return [dict(doc) for doc in documents]


create_application_logs()
create_document_store()
