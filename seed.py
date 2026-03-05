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
        user3 = User(username='Tech_Lead_Charlie', role='enthusiast')
        user3.set_password('password123')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
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
        post3 = ProcessPost(
            title='Legacy ERP System Integration',
            description='We have a 15-year-old on-premise ERP system that holds all our critical business logic and customer data. We want to build modern web interfaces and mobile apps for our sales team, but the ERP has no REST APIs, only SOAP endpoints that are poorly documented. Need a middleware solution or AI agent that can auto-generate API wrappers by analyzing the WSDL and database schemas.',
            category='IT & Infrastructure',
            image_url='https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=800&auto=format&fit=crop',
            author_id=user1.id
        )
        post4 = ProcessPost(
            title='Automated Quality Control in Manufacturing',
            description='Our assembly line produces thousands of small electronic components daily. Currently, human inspectors sample a small percentage for micro-defects like solder bridges or misaligned chips. We have cameras installed but traditional computer vision algorithms create too many false positives. Looking for an AI vision model that can be fine-tuned on our defect dataset and run on edge devices for real-time inspection.',
            category='Manufacturing',
            image_url='https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=800&auto=format&fit=crop',
            author_id=user1.id
        )
        post5 = ProcessPost(
            title='Dynamic Fleet Routing and Logistics',
            description='Our delivery fleet operates 50 trucks daily. We use static routes that do not account for real-time traffic, sudden weather changes, or urgent dispatch requests mid-route. We need a system that can ingest real-time GPS paths, traffic data APIs, and delivery priorities to dynamically reroute drivers and update customer ETAs automatically.',
            category='Logistics & Supply Chain',
            image_url='https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=800&auto=format&fit=crop',
            author_id=user1.id
        )
        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.add(post4)
        db.session.add(post5)
        db.session.commit()
        # The main demo post
        post6 = ProcessPost(
            title='Extracting data from messy PDF invoices',
            description='Our accounting department receives hundreds of invoices per week. Some are PDFs, some are photos of paper receipts. Currently humans have to read them and type the vendor, total amount, and line items into our ledger. This is incredibly slow and error-prone. Is there a way to automate this using AI?',
            category='Finance & Accounting',
            image_url='https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?q=80&w=800&auto=format&fit=crop',
            author_id=user1.id
        )
        db.session.add(post6)
        db.session.commit()

        print("Adding mock prototype...")
        proto1 = Prototype(
            title='AI Inventory Counter',
            description='A simple web app where you upload a photo and it uses a vision model to count items and export to CSV.',
            link_url='https://example.com/proto1',
            post_id=post1.id,
            author_id=user2.id
        )
        proto2 = Prototype(
            title='Interactive Invoice Extractor Demo',
            description='I built a working prototype that uses an OCR pipeline to extract the structured JSON data from your invoices. Try uploading one now!',
            link_url='/demo/invoice-parser',
            post_id=post6.id,
            author_id=user3.id
        )
        db.session.add(proto1)
        db.session.add(proto2)
        db.session.commit()

        print("Adding mock comments...")
        comment1 = Comment(text="This is such a common problem for small retail!", author_id=user2.id, post_id=post1.id)
        db.session.add(comment1)

        # New comments proposing solutions for the complex problems
        comment2 = Comment(text="For the ERP integration, you could use a tool like Zeep in Python to parse the WSDL, and then use an LLM to map the SOAP methods to RESTful endpoints. I've built something similar using FastAPI.", author_id=user2.id, post_id=post3.id)
        comment3 = Comment(text="Are you open to using local open-source LLMs? We could set up a secure gateway that translates the SOAP payloads without sending sensitive data to cloud APIs.", author_id=user3.id, post_id=post3.id)
        
        comment4 = Comment(text="Traditional CV is definitely tricky here. Have you looked into YOLOv8 or an Anomaly Detection model like PatchCore? They tend to perform much better on micro-defects and can run on Jetson Nanos at the edge.", author_id=user3.id, post_id=post4.id)
        
        comment5 = Comment(text="For the fleet routing, Google's OR-Tools combined with a real-time traffic API like Mapbox or Google Maps could solve this. The tricky part is pushing the dynamic updates to the drivers seamlessly.", author_id=user2.id, post_id=post5.id)
        
        comment6 = Comment(text="I just tried the prototype linked above, it works flawlessly on my test receipts! What LLM is powering this?", author_id=user1.id, post_id=post6.id)
        
        db.session.add_all([comment2, comment3, comment4, comment5, comment6])
        db.session.commit()

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
        vote3 = Upvote(user_id=user1.id, prototype_id=proto2.id)
        vote4 = Upvote(user_id=user2.id, post_id=post6.id)

        
        vote3 = Upvote(user_id=user2.id, post_id=post3.id)
        vote4 = Upvote(user_id=user3.id, post_id=post4.id)
        vote5 = Upvote(user_id=user1.id, post_id=post5.id)
        
        db.session.add_all([vote1, vote2, vote3, vote4, vote5])
        db.session.commit()

        print("Database seeded successfully with mock data!")

if __name__ == '__main__':
    seed_data()
