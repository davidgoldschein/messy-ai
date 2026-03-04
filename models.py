from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

db = SQLAlchemy()

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=True) # URL to click
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'smb' or 'enthusiast'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    posts = db.relationship('ProcessPost', backref='author', lazy=True)
    prototypes = db.relationship('Prototype', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    edit_suggestions = db.relationship('EditSuggestion', backref='author', lazy=True)
    upvotes = db.relationship('Upvote', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='target_user', lazy=True, order_by='Notification.created_at.desc()')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Upvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Polymorphic upvotes: either a post_id OR prototype_id will be set per row
    post_id = db.Column(db.Integer, db.ForeignKey('process_post.id'), nullable=True)
    prototype_id = db.Column(db.Integer, db.ForeignKey('prototype.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class ProcessPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='General') # Domain/Category tag
    image_url = db.Column(db.String(255), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    prototypes = db.relationship('Prototype', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)
    edit_suggestions = db.relationship('EditSuggestion', backref='post', lazy=True)
    upvotes = db.relationship('Upvote', backref='voted_post', lazy=True, cascade='all, delete-orphan')

    @property
    def upvote_count(self):
        return len(self.upvotes)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('process_post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class EditSuggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suggested_title = db.Column(db.String(120), nullable=True)
    suggested_description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending') # pending, approved, rejected
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('process_post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Prototype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('process_post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    upvotes = db.relationship('Upvote', backref='voted_prototype', lazy=True, cascade='all, delete-orphan')

    @property
    def upvote_count(self):
        return len(self.upvotes)
