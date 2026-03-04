from app import create_app
from models import db, User, ProcessPost, Prototype, Comment, EditSuggestion, Upvote

app = create_app()

def seed_data():
    with app.app_context():
        print("Checking if database needs initialization...")
        db.create_all()
        
        # Check if users already exist to avoid duplicates
        if User.query.first():
            print("Database already contains data. Skipping seeding.")
            return

        print("Adding mock users...")
        user1 = User(username='SMB_Owner_Alice', role='smb')
        user1.set_password('password123')
        user2 = User(username='AI_Dev_Bob', role='enthusiast')
        user2.set_password('password123')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        print("Adding mock posts...")
        post1 = ProcessPost(
            title='Inventory Management is a Mess',
            description='I run a small retail store and I keep track of my inventory on paper. It takes hours every week and I often make mistakes. I need a simple way to take a picture of my stock room and have AI count the items.',
            category='Retail & Inventory',
            image_url='https://images.unsplash.com/photo-1553413077-190dd305871c?q=80&w=800&auto=format&fit=crop',
            author_id=user1.id
        )
        post2 = ProcessPost(
            title='Customer Support Emails Overwhelming',
            description='We get hundreds of emails a day asking about store hours, return policies, etc. Is there a way to auto-draft replies?',
            category='Operations & HR',
            image_url='https://images.unsplash.com/photo-1596526131083-e8c633c948d2?q=80&w=800&auto=format&fit=crop',
            author_id=user1.id
        )
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()

        print("Adding mock prototype...")
        proto1 = Prototype(
            title='AI Inventory Counter',
            description='A simple web app where you upload a photo and it uses a vision model to count items and export to CSV.',
            link_url='https://example.com/proto1',
            post_id=post1.id,
            author_id=user2.id
        )
        db.session.add(proto1)
        db.session.commit()

        print("Adding mock comments...")
        comment1 = Comment(text="This is such a common problem for small retail!", author_id=user2.id, post_id=post1.id)
        db.session.add(comment1)

        print("Adding mock edit suggestion...")
        edit1 = EditSuggestion(
            suggested_title="Automated Inventory Counting with Vision AI",
            suggested_description="Clarifying that we need a solution that works on mobile phones specifically.",
            author_id=user2.id,
            post_id=post1.id
        )
        db.session.add(edit1)
        db.session.commit()

        print("Adding mock upvotes...")
        vote1 = Upvote(user_id=user2.id, post_id=post1.id)
        vote2 = Upvote(user_id=user1.id, prototype_id=proto1.id)
        db.session.add(vote1)
        db.session.add(vote2)
        db.session.commit()

        print("Database seeded successfully with mock data!")

if __name__ == '__main__':
    seed_data()
