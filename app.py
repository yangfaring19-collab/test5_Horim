from flask import Flask, render_template, request, jsonify, session, redirect
from flask_cors import CORS
import sqlite3
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret_key_for_session"
CORS(app)

DB_PATH = "todo.db"


# -----------------------------
# DB 연결 함수
# -----------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# DB 초기화
# -----------------------------
def init_db():
    conn = get_db()
    cur = conn.cursor()

    # member 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS member (
        idx INTEGER PRIMARY KEY AUTOINCREMENT,
        uname TEXT,
        uid TEXT UNIQUE,
        upwd TEXT,
        datetime TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # todo 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS todolist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        uid TEXT,
        completed INTEGER DEFAULT 0,
        datetime TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 테스트 계정
    cur.execute("SELECT * FROM member WHERE uid=?", ("admin",))
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO member (uname, uid, upwd) VALUES (?, ?, ?)",
            ("관리자", "admin", "1234")
        )

    conn.commit()
    conn.close()

    
# -----------------------------
# MariaDB에 Query 구문 저장
# -----------------------------
def log_query(query_type, sql_text):

    conn = None

    try:
        conn = mysql.connector.connect(
            host="10.0.2.3",
            user="hancom",
            password="1234",   # ← 본인 MySQL 비밀번호
            database="todo_log"
        )

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


# -----------------------------
# 페이지
# -----------------------------
@app.route("/")
def index():
    if "uid" not in session:
        return redirect("/login")
    return render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


# -----------------------------
# 로그인
# -----------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    uid = data.get("uid")
    upwd = data.get("upwd")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM member WHERE uid=? AND upwd=?",
        (uid, upwd)
    )
    log_query(
        "SELECT * FROM member WHERE uid=? AND upwd=?",
        (uid, upwd)
    )

    user = cur.fetchone()
    conn.close()

    if user:
        session["uid"] = uid
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})


# -----------------------------
# TODO 목록 조회 (GET)
# -----------------------------
@app.route("/todos", methods=["GET"])
def get_todos():
    if "uid" not in session:
        return jsonify([])
    
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM todolist WHERE uid=? ORDER BY id DESC",
        (session["uid"],)
    )

    log_query(
        "select",
        f"SELECT * FROM todolist WHERE uid='{session['uid']}'"
    )

    rows = cur.fetchall()
    conn.close()

    todos = []
    for row in rows:
        todos.append({
            "id": row["id"],
            "title": row["title"],
            "completed": row["completed"]
        })

    return jsonify(todos)


# -----------------------------
# TODO 추가 (POST)
# -----------------------------
@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.json
    title = data.get("title")

    if not title:
        return jsonify({"error": "empty"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO todolist (title, uid) VALUES (?, ?)",
        (title, session["uid"])
    )
    log_query(
        "INSERT INTO todolist (title, uid) VALUES (?, ?)",
        (title, session["uid"])
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})


# -----------------------------
# TODO 수정 (PUT)
# -----------------------------
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.json

    conn = get_db()
    cur = conn.cursor()

    # title 수정
    if "title" in data:
        cur.execute(
            "UPDATE todolist SET title=? WHERE id=? AND uid=?",
            (data["title"], todo_id, session["uid"])
        )
        log_query(
            "UPDATE todolist SET title=? WHERE id=? AND uid=?",
            (data["title"], todo_id, session["uid"])
        )

    # completed 토글
    elif "completed" in data:
        cur.execute(
            "UPDATE todolist SET completed=? WHERE id=? AND uid=?",
            (data["completed"], todo_id, session["uid"])
        )
        log_query(
            "UPDATE todolist SET completed=? WHERE id=? AND uid=?",
            (data["completed"], todo_id, session["uid"])
        )

    conn.commit()
    conn.close()

    return jsonify({"success": True})


# -----------------------------
# TODO 삭제 (DELETE)
# -----------------------------
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM todolist WHERE id=? AND uid=?",
        (todo_id, session["uid"])
    )
    log_query(
        "DELETE FROM todolist WHERE id=? AND uid=?",
        (todo_id, session["uid"])
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})


# -----------------------------
# 로그아웃
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")



# -----------------------------
# 실행
# -----------------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0')