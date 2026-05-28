# 📝 Flask Todo List Project (CRUD + SQLite + MySQL Logging)

Flask + SQLite + jQuery를 활용한 간단한 Todo List 웹 애플리케이션입니다. 
Mariadb에 Query를 저장하려고 했으나... 제대로 적용되지 않아 실패했습니다.  

---

# 📂 프로젝트 구조
```
todo-project/
│
├── app.py
├── todo.db
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   └── login.html
│
├── static/
    ├── script.js
    └── style.css
```
---

# 🚀 프로젝트 기능

## 🔐 로그인 기능
- 회원 로그인 (session 기반)
- 기본 테스트 계정 제공

ID: admin  
PW: 1234

---

## 📌 Todo 기능 (CRUD)

- 할 일 추가 (Create)
- 할 일 조회 (Read)
- 할 일 수정 (Update)
- 할 일 삭제 (Delete)
- 완료 / 취소 토글 기능

---

## 🗄️ 데이터베이스

### 1. SQLite (실제 데이터 저장)
- member 테이블
- todolist 테이블

### 2. Mariadb (쿼리 로그 저장)
모든 SQL 실행 로그 저장

| 컬럼 | 설명 |
|------|------|
| type | select / insert / update / delete |
| sql_text | 실행된 Query |
| created_at | 실행 시간 |

---

# 🛠️ 실행 방법

## 1. 프로젝트 다운로드
```
git clone https://github.com/yangfaring19-collab/test5_Horim.git
cd test5_Horim
```
---

## 2. 가상환경 생성 및 실행
```
### Windows
python -m venv venv
venv\Scripts\activate

### Linux / Mac
python3 -m venv venv
source venv/bin/activate
```
---

## 3. 패키지 설치
```
pip install -r requirements.txt
```
---

## 4. Mariadb 설정
```
CREATE DATABASE todo_log;

USE todo_log;

CREATE TABLE query_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(10),
    sql_text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```
---

## 5. Flask 실행
```
python app.py
```
---

## 6. 브라우저 접속
```
http://localhost:5000
```
---


# ⚙️ 사용 기술

- Flask (Backend)
- SQLite (Local DB)
- Mariadb (Query Logging)
- jQuery (AJAX)
- HTML/CSS/JS

---

# 📡 API 구조

GET    /todos
POST   /todos
PUT    /todos/<id>
DELETE /todos/<id>

---

# 📌 참고 사항

- SQLite DB 자동 생성
- Mariadb 로그 서버 별도 필요
- AJAX 기반 프론트엔드
- session 기반 로그인

