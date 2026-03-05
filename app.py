import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, ProcessPost, Prototype, Comment, EditSuggestion, Upvote, Notification

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-for-messy-ai')
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Configure Database
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Render provides postgres:// urls, but SQLAlchemy requires postgresql://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Fallback to local SQLite
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure Uploads
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def create_notification(user_id, message, link=None):
        noti = Notification(user_id=user_id, message=message, link=link)
        db.session.add(noti)
        db.session.commit()

    @app.context_processor
    def inject_notifications():
        if current_user.is_authenticated:
            unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
            notifications = Notification.query.filter_by(user_id=current_user.id).limit(5).all()
            return {"unread_count": unread_count, "nav_notifications": notifications}
        return {"unread_count": 0, "nav_notifications": []}

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user is None or not user.check_password(password):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user)
            return redirect(url_for('index'))
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            role = request.form.get('role')
            if User.query.filter_by(username=username).first():
                flash('Username already exists')
                return redirect(url_for('register'))
            user = User(username=username, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/')
    def index():
        posts = ProcessPost.query.order_by(ProcessPost.created_at.desc()).all()
        return render_template('index.html', posts=posts)

    @app.route('/post/<int:post_id>')
    def view_post(post_id):
        post = ProcessPost.query.get_or_404(post_id)
        return render_template('post_detail.html', post=post)

    @app.route('/post/new', methods=['GET', 'POST'])
    @login_required
    def new_post():
        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            category = request.form.get('category')
            image_url = request.form.get('image_url') # still support URL if provided
            
            # Handle File Upload
            if 'image_file' in request.files:
                file = request.files['image_file']
                if file and file.filename != '':
                    filename = secure_filename(f"{current_user.id}_{datetime.now().timestamp()}_{file.filename}")
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    image_url = url_for('static', filename=f'uploads/{filename}')
            
            post = ProcessPost(title=title, description=description, category=category, image_url=image_url, author_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
        
        return render_template('new_post.html')

    @app.route('/post/<int:post_id>/comment', methods=['POST'])
    @login_required
    def add_comment(post_id):
        text = request.form.get('text')
        comment = Comment(text=text, post_id=post_id, author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        
        # Notify post author
        if comment.post.author_id != current_user.id:
            create_notification(
                user_id=comment.post.author_id,
                message=f"{current_user.username} commented on your mess: {comment.post.title}",
                link=url_for('view_post', post_id=post_id)
            )
            
        return redirect(url_for('view_post', post_id=post_id))

    @app.route('/post/<int:post_id>/edit', methods=['POST'])
    @login_required
    def suggest_edit(post_id):
        suggested_title = request.form.get('title')
        suggested_description = request.form.get('description')
        
        edit_suggestion = EditSuggestion(
            suggested_title=suggested_title,
            suggested_description=suggested_description,
            post_id=post_id,
            author_id=current_user.id
        )
        db.session.add(edit_suggestion)
        db.session.commit()
        
        # Notify post author
        if edit_suggestion.post.author_id != current_user.id:
            create_notification(
                user_id=edit_suggestion.post.author_id,
                message=f"{current_user.username} suggested an edit for: {edit_suggestion.post.title}",
                link=url_for('view_post', post_id=post_id, _anchor='edits')
            )
            
        return redirect(url_for('view_post', post_id=post_id))

    @app.route('/edit/<int:edit_id>/approve', methods=['POST'])
    @login_required
    def approve_edit(edit_id):
        edit = EditSuggestion.query.get_or_404(edit_id)
        
        if edit.post.author_id == current_user.id:
            if edit.suggested_title:
                edit.post.title = edit.suggested_title
            if edit.suggested_description:
                edit.post.description = edit.suggested_description
            edit.status = 'approved'
            db.session.commit()
            
        return redirect(url_for('view_post', post_id=edit.post_id))

    @app.route('/edit/<int:edit_id>/reject', methods=['POST'])
    @login_required
    def reject_edit(edit_id):
        edit = EditSuggestion.query.get_or_404(edit_id)
        
        if edit.post.author_id == current_user.id:
            edit.status = 'rejected'
            db.session.commit()
            
        return redirect(url_for('view_post', post_id=edit.post_id))

    @app.route('/post/<int:post_id>/prototype/new', methods=['POST'])
    @login_required
    def new_prototype(post_id):
        title = request.form.get('title')
        description = request.form.get('description')
        link_url = request.form.get('link_url')
        
        prototype = Prototype(
            title=title,
            description=description,
            link_url=link_url,
            post_id=post_id,
            author_id=current_user.id
        )
        db.session.add(prototype)
        db.session.commit()
        
        # Notify post author
        if prototype.post.author_id != current_user.id:
            create_notification(
                user_id=prototype.post.author_id,
                message=f"{current_user.username} built a prototype for: {prototype.post.title}",
                link=url_for('view_post', post_id=post_id)
            )
            
        return redirect(url_for('view_post', post_id=post_id))

    @app.route('/notifications/read_all', methods=['POST'])
    @login_required
    def mark_notifications_read():
        Notification.query.filter_by(user_id=current_user.id, is_read=False).update({Notification.is_read: True})
        db.session.commit()
        return redirect(request.referrer or url_for('index'))

    @app.route('/user/<username>')
    def profile(username):
        user = User.query.filter_by(username=username).first_or_404()
        
        # Calculate stats
        posts_count = len(user.posts)
        prototypes_count = len(user.prototypes)
        
        # Sum upvotes received on posts
        post_upvotes = sum(post.upvote_count for post in user.posts)
        # Sum upvotes received on prototypes
        proto_upvotes = sum(proto.upvote_count for proto in user.prototypes)
        total_upvotes = post_upvotes + proto_upvotes
        
        return render_template('profile.html', 
                               user=user, 
                               posts_count=posts_count, 
                               prototypes_count=prototypes_count,
                               total_upvotes=total_upvotes)

    @app.route('/demo/invoice-parser')
    def demo_invoice_parser():
        return render_template('demo_invoice_parser.html')

    @app.route('/upvote/<string:item_type>/<int:item_id>', methods=['POST'])
    @login_required
    def toggle_upvote(item_type, item_id):
        # find if an upvote exists
        if item_type == 'post':
            vote = Upvote.query.filter_by(user_id=current_user.id, post_id=item_id).first()
        elif item_type == 'prototype':
            vote = Upvote.query.filter_by(user_id=current_user.id, prototype_id=item_id).first()
        else:
            return "Invalid item type", 400
            
        if vote:
            # toggle off
            db.session.delete(vote)
        else:
            # toggle on
            if item_type == 'post':
                vote = Upvote(user_id=current_user.id, post_id=item_id)
            else:
                vote = Upvote(user_id=current_user.id, prototype_id=item_id)
            db.session.add(vote)
            
        db.session.commit()
        return redirect(request.referrer or url_for('index'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
