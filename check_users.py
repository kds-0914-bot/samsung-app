from app import app, db, User

with app.app_context():
    users = User.query.all()
    print(f"\n{'='*50}")
    print(f"{'총 사용자 수'}: {len(users)}")
    print(f"{'='*50}\n")

    if users:
        for user in users:
            print(f"ID: {user.id}")
            print(f"사용자명: {user.username}")
            print(f"이메일: {user.email}")
            print(f"-" * 50)
    else:
        print("등록된 사용자가 없습니다.")
