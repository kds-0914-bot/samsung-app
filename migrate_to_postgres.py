"""
SQLite에서 PostgreSQL로 데이터 마이그레이션
"""
import sqlite3
import os
from app import app, db, User

# 1. SQLite에서 데이터 읽기
print("📥 SQLite에서 사용자 데이터 읽기...")
sqlite_users = []

if os.path.exists('app.db'):
    try:
        conn = sqlite3.connect('app.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        sqlite_users = cursor.fetchall()
        conn.close()
        print(f"✅ {len(sqlite_users)}명의 사용자를 찾았습니다.")
    except Exception as e:
        print(f"⚠️ SQLite 데이터 읽기 실패: {e}")
        print("📌 새로 시작합니다.")
else:
    print("⚠️ app.db 파일이 없습니다. 새로 생성합니다.")

# 2. PostgreSQL 테이블 생성
print("\n📊 PostgreSQL 테이블 생성 중...")
with app.app_context():
    db.create_all()
    print("✅ 테이블 생성 완료")

    # 3. 데이터 마이그레이션 (있으면)
    if sqlite_users:
        print("\n📤 데이터를 PostgreSQL로 이전 중...")
        for user_data in sqlite_users:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            db.session.add(user)

        db.session.commit()
        print(f"✅ {len(sqlite_users)}명의 사용자를 PostgreSQL로 이전했습니다!")
    else:
        print("\n📌 이전할 데이터가 없습니다.")

    # 4. 확인
    print("\n🔍 PostgreSQL의 사용자 목록:")
    print("-" * 50)
    users = User.query.all()
    if users:
        for user in users:
            print(f"ID: {user.id}, 사용자명: {user.username}, 이메일: {user.email}")
    else:
        print("현재 등록된 사용자가 없습니다.")
    print("-" * 50)
    print(f"\n✅ 마이그레이션 완료!")
