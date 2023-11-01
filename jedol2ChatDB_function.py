

import sqlite3 #확장 프로그램  SQLite3 Editor 사용
from datetime import datetime
import jedol1Fun as jshs

def setup_db():
    # chat.db가 없는 경우 생성  
    conn = sqlite3.connect('sqlite3.chat.db')
    db = conn.cursor()
    # 테이블 생성
    db.execute('''
        CREATE TABLE IF NOT EXISTS chat_data(
            id INTEGER PRIMARY KEY,
            token TEXT,
            name TEXT DEFAULT '',
            history TEXT DEFAULT '',
            date TEXT DEFAULT ''
        )
        ''')
    conn.commit()
    conn.close()
    
def new_user(token):
    conn = sqlite3.connect('sqlite3.chat.db')
    db = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.execute("INSERT INTO chat_data (token, date, history, name) VALUES (?, ?, ?, ?)",(token, current_time, '', ''))
    conn.commit()
    conn.close()

def query_history(token):
    conn = sqlite3.connect('sqlite3.chat.db')
    db = conn.cursor()
    db.execute("SELECT * FROM chat_data WHERE token=?", (token,))
    row = db.fetchall()
    conn.close()
    if row is not None and len(row)>0 :
        return row[0][3]
    else:
        return ""

def update_history(token, new_chat,max_token):
    conn = sqlite3.connect('sqlite3.chat.db')
    db = conn.cursor()
    
    # 현재 history 값을 가져오기
    db.execute("SELECT history FROM chat_data WHERE token=?", (token,))
    row = db.fetchone()
    
    if row is not None:
        current_history = row[0] if row[0] is not None else ""
        new_content = "\n\n " + new_chat
        combined_content = current_history + new_content
        
        # 토큰 길이가 1000개를 초과하면, 불필요한 부분을 잘라냄
        while jshs.tiktoken_len(combined_content) > max_token:
            _ , remainder = combined_content.split('\n\n ', 1) # 두분으로 나누워 앞부분을 사용안함 
            combined_content = remainder
        
        # 업데이트 쿼리 실행
        db.execute("UPDATE chat_data SET history=? WHERE token=?", (combined_content, token))
        conn.commit()
    else:
        print("Token not found user ADD!")
        new_user(token)
        update_history(token, new_chat,max_token)
        
    
    conn.close()

if __name__ == "__main__":
    token="run-jedolChatDB_function" 
    setup_db()
    conn = sqlite3.connect('sqlite3.chat.db')
    db = conn.cursor()
    db.execute("SELECT * FROM chat_data")
    rows = db.fetchall()
    for row in rows:
          print(row[3])
    # print(jshs.tiktoken_len(rows[0][3]))
    db.close()
    conn.close()