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
    try:
        db.create_all()

        # Check if demo user already exists
        if User.query.filter_by(username='demo').first():
            return  # Database already initialized

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
            username='AAH00007',
            password=generate_password_hash('demo123'),
            email='kimdaesuk@naver.com'
        )
        db.session.add(sample_user)
        db.session.commit()

        # Create sample posts
        posts = [
            Post(
                title='HIMSS CCMM 6단계 세계 최초 인증 획득',
                content='삼성서울병원이 미국 보건의료정보관리시스템협회(HIMSS)가 주관하는 의료 서비스 연속성 성숙도 모델(CCMM) 6단계 인증을 세계 최초로 획득했습니다.\n\n진료 전·후 데이터 통합 관리 및 웨어러블 연동 구현으로 HIMSS 디지털 성숙도 모델 전 분야 인증을 받았으며, 이는 세계 유일한 성과입니다.\n\nCCMM은 환자가 필요할 때 끊김 없이 진료를 받을 수 있도록 병원과 병원, 병원과 환자 사이에 진료 정보가 안전하고 자유롭게 오가는 전용 고속도로가 얼마나 잘 구축되어 있는지를 평가하는 것입니다.',
                category_id=1,
                user_id=sample_user.id,
                views=245
            ),
            Post(
                title='PACS 시스템 클라우드 전환 완료',
                content='삼성서울병원은 PACS 시스템을 클라우드로 전환하여 비용 절감과 보안 강화를 동시에 달성했습니다.\n\n1994년 개원 당시부터 필름 없는 병원을 목표로 PACS 시스템을 도입한 이후, 약 100여 대의 장비에서 생성되는 방대한 이미지 데이터(일일 700GB, 연 143TB)를 AWS S3 클라우드 저장소를 활용하여 관리하고 있습니다.\n\nAI 기반 의료 분석 및 협력 병원과의 정보 공유라는 미래 가치를 실현하기 위한 전략적 선택으로, 약 4년에 걸쳐 진행되었으며 연간 69% 이상의 비용 절감 효과가 예상됩니다.',
                category_id=2,
                user_id=sample_user.id,
                views=156
            ),
            Post(
                title='AI 기반 스마트 물류 시스템 운영',
                content='삼성서울병원은 AI를 기반으로 한 차세대 혁신인 AI Transformation(AX)을 의료 전 영역에 도입하고 있습니다.\n\n병원 내 물류 업무 중 약 75%가 로봇을 통해 자동화되어 운영되고 있으며, 이는 다음과 같이 구성됩니다:\n\n1. AGV 기반 자동 배송: 진료재료, 약품, 소모품을 병동 간 자동 이송\n2. 스마트 카트: 실시간 재고 정보 반영 및 자동 보충\n3. 통합 관제 센터: 로봇 위치, 카트 상태, 물류 흐름 실시간 모니터링\n\n의료진의 물류 수송 업무 부담이 크게 경감되어 진료에 더욱 집중할 수 있는 환경을 조성했습니다.',
                category_id=2,
                user_id=sample_user.id,
                views=189
            ),
            Post(
                title='AI 기반 환자 위험 감시 시스템 도입',
                content='삼성서울병원은 환자의 안전과 진료 품질을 강화하기 위해 AI 기반 환자 감시 시스템을 순차적으로 도입했습니다.\n\nEMR 및 사진 데이터를 통합 분석하여 환자 상태 변화를 탐지하고 의료진에게 조기 경보를 제공하는 지능형 안전관리 체계로, 기존 수동적 모니터링에서 벗어나 데이터 기반 예측형 감시(Predictive Monitoring)로 전환했습니다.\n\n욕창·낙상 예측 모델 및 임상 악화 예측 모델이 병실, 응급실 전 영역에 걸쳐 통합되어 중증 악화, 낙상, 욕창 등 주요 안전사고의 예방 가능성을 높였습니다.',
                category_id=2,
                user_id=sample_user.id,
                views=167
            ),
            Post(
                title='차세대 스마트 병실 시스템 개발',
                content='삼성서울병원은 병실을 데이터 기반의 지능형 치료공간으로 전환하기 위한 차세대 스마트병실 시스템을 개발 중입니다.\n\n병상 내·외부에서 생성되는 생체신호, 행동, 영상, 환경 데이터를 통합하여 환자의 상태를 연속적으로 인식하고 AI를 통해 맞춤형 중재를 수행합니다.\n\n웨어러블 센서, 다중모달 AI, 아바타 인터페이스를 유기적으로 연결하여 단순한 모니터링을 넘어 병실이 하나의 지능형 진료 플랫폼으로 기능하도록 설계되어 의료진의 업무 효율성, 환자 경험, 연구 데이터 품질을 동시에 개선할 수 있습니다.',
                category_id=2,
                user_id=sample_user.id,
                views=134
            ),
            Post(
                title='박승우 원장, HIMSS 2025 기조연설',
                content='박승우 삼성서울병원 원장이 미국 라스베이거스에서 열린 세계 최대 의료IT 콘퍼런스 HIMSS 2025에서 아시아 병원 최초로 기조연설을 했습니다.\n\n삼성서울병원은 HIMSS의 6개 인증 중 EMRAM, INFRAM, DIAM, AMAM 4개 분야에서 최고인 7단계를 달성했으며, 디지털헬스지표(DHI) 조사에서도 400점 만점을 기록했습니다.\n\n박 원장은 삼성 DNA와 조직원들의 혁신 마인드, 상향식 통제 대신 수평적 협업 문화를 성공의 핵심으로 강조했습니다.',
                category_id=1,
                user_id=sample_user.id,
                views=312
            ),
            Post(
                title='이노베이션 하스피탈10 얼라이언스(iH10) 출범',
                content='삼성서울병원이 주도하여 글로벌 최고 수준 병원 10곳이 참여하는 이노베이션 하스피탈10 얼라이언스(iH10)를 출범했습니다.\n\n미국, 프랑스, 덴마크, 이탈리아, 홍콩, 대만 등 세계 각국의 의료기관이 참여하며, IT 프로젝트 성공사례는 물론 실패 경험까지 공유하면서 혁신 여정의 시간을 단축할 것으로 예상됩니다.\n\n한국 병원이 주도하여 세계 각국 의료기관과 IT혁신 이니셔티브를 만든 것은 이번이 처음으로, 글로벌 의료 혁신을 선도하는 삼성서울병원의 위상을 입증합니다.',
                category_id=1,
                user_id=sample_user.id,
                views=223
            ),
        ]
        db.session.add_all(posts)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Database initialization error: {e}")

_db_initialized = False

@app.before_request
def initialize_database():
    global _db_initialized
    if not _db_initialized:
        init_db()
        _db_initialized = True

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

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != session['user_id']:
        return redirect(url_for('board'))

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('board'))

@app.route('/hospital')
def hospital():
    return render_template('hospital.html')

@app.route('/developer')
def developer():
    return render_template('developer.html')

if __name__ == '__main__':
    if os.environ.get('ENVIRONMENT') == 'production':
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
    else:
        app.run(debug=True)
