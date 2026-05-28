import mysql.connector
from datetime import datetime

db_config = {
    "host": "10.0.2.3",
    "user": "hancom",
    "password": "1234",
    "database": "todo_log",
    "port": 3306
}

def get_db():
    return mysql.connector.connect(**db_config)


# -----------------------------
# MariaDB에 Query 구문 저장
# -----------------------------
def log_query(query_type, sql_text):

    conn = None

    try:
        conn = get_db()

        cur = conn.cursor()

        sql = """
        INSERT INTO query_log (type, sql_text, created_at)
        VALUES (%s, %s, %s)
        """

        cur.execute(sql, (
            query_type,
            sql_text,
            datetime.now()
        ))

        conn.commit()

    except Exception as e:
        print("MySQL log error:", e)

    finally:
        if conn and conn.is_connected():
            conn.close()
        return ""
