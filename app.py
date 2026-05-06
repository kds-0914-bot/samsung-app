import os
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

app = Flask(__name__)

# Configuration
# Azure에서는 SQLite 사용 (PostgreSQL 구성 완료 후 DATABASE_URL로 변경 가능)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.environ.get('ENVIRONMENT') == 'production':
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'samsung-secret-key-2026')

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    posts = db.relationship('Post', backref='category', lazy=True, cascade='all, delete-orphan')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='posts')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='comments')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create categories
        categories = [
            Category(name='병원 소식', description='병원의 주요 소식과 공지사항'),
            Category(name='기술 토론', description='의료 기술 및 인프라 관련 토론'),
            Category(name='자유 게시판', description='자유로운 주제의 토론'),
            Category(name='채용 정보', description='채용 공고 및 관련 정보'),
        ]
        db.session.add_all(categories)
        db.session.commit()

        # Create sample user
        sample_user = User(
            username='demo',
            password=generate_password_hash('demo123'),
            email='demo@samsung.co.kr'
        )
        db.session.add(sample_user)
        db.session.commit()

        # Create sample posts
        posts = [
            Post(
                title='Azure 클라우드 인프라 구축 완료',
                content='Samsung Seoul Hospital의 클라우드 인프라가 Microsoft Azure에 성공적으로 구축되었습니다.',
                category_id=1,
                user_id=sample_user.id,
                views=125
            ),
            Post(
                title='AI 기반 스마트 시스템 도입',
                content='병원 내 AI 로봇과 환자 모니터링 시스템이 도입되었습니다.',
                category_id=2,
                user_id=sample_user.id,
                views=89
            ),
            Post(
                title='새로운 팀 구성원을 환영합니다',
                content='첨단인프라운영팀에 새로운 팀원이 합류했습니다. 환영합니다!',
                category_id=3,
                user_id=sample_user.id,
                views=45
            ),
        ]
        db.session.add_all(posts)
        db.session.commit()

@app.before_request
def redirect_to_https():
    if os.environ.get('ENVIRONMENT') == 'production':
        if request.headers.get('X-Forwarded-Proto', 'http') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)

@app.after_request
def add_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    return response

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('board'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('board'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('board'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('board'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password:
            return render_template('signup.html', error='All fields are required')

        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')

        if User.query.filter_by(username=username).first():
            return render_template('signup.html', error='Username already exists')

        if User.query.filter_by(email=email).first():
            return render_template('signup.html', error='Email already exists')

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('board'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/board')
@login_required
def board():
    category_id = request.args.get('category_id', type=int)
    search_query = request.args.get('search', '')

    query = Post.query

    if category_id:
        query = query.filter_by(category_id=category_id)

    if search_query:
        query = query.filter(Post.title.ilike(f'%{search_query}%') | Post.content.ilike(f'%{search_query}%'))

    posts = query.order_by(Post.created_at.desc()).all()
    categories = Category.query.all()

    return render_template('board.html', posts=posts, categories=categories, current_category=category_id, search_query=search_query)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('category_id', type=int)

        if not title or not content or not category_id:
            categories = Category.query.all()
            return render_template('new_post.html', categories=categories, error='All fields are required')

        post = Post(
            title=title,
            content=content,
            category_id=category_id,
            user_id=session['user_id']
        )
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('view_post', post_id=post.id))

    categories = Category.query.all()
    return render_template('new_post.html', categories=categories)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.views += 1
    db.session.commit()

    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            comment = Comment(
                content=content,
                post_id=post_id,
                user_id=session['user_id']
            )
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('view_post', post_id=post_id))

    return render_template('post.html', post=post)

@app.route('/hospital')
def hospital():
    return render_template('hospital.html')

@app.route('/developer')
def developer():
    return render_template('developer.html')

if __name__ == '__main__':
    init_db()
    if os.environ.get('ENVIRONMENT') == 'production':
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
    else:
        app.run(debug=True)
