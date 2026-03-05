from app import create_app
from models import db, User, ProcessPost, Prototype, Comment, EditSuggestion, Upvote

app = create_app()

def seed_data():
    with app.app_context():
        print("Checking if database needs initialization...")
        db.create_all()
        
        print("Checking if database needs initialization...")
        db.create_all()

        print("Adding mock users...")
        def get_or_create_user(username, role='enthusiast'):
            user = User.query.filter_by(username=username).first()
            if not user:
                user = User(username=username, role=role)
                user.set_password('password123')
                db.session.add(user)
                db.session.commit()
            return user

        user1 = get_or_create_user('SMB_Owner_Alice', 'smb')
        user2 = get_or_create_user('AI_Dev_Bob', 'enthusiast')
        user3 = get_or_create_user('Tech_Lead_Charlie', 'enthusiast')
        user4 = get_or_create_user('Data_Nerd_Dave', 'enthusiast')
        user5 = get_or_create_user('Operations_Olivia', 'smb')


        print("Adding mock posts...")
        def get_or_create_post(title, description, category, image_url, author_id):
            post = ProcessPost.query.filter_by(title=title).first()
            if not post:
                post = ProcessPost(
                    title=title,
                    description=description,
                    category=category,
                    image_url=image_url,
                    author_id=author_id
                )
                db.session.add(post)
                db.session.commit()
            return post

        post1 = get_or_create_post(
            title='Inventory Management is a Mess',
            description='I run a small retail store and I keep track of my inventory on paper. It takes hours every week and I often make mistakes. I need a simple way to take a picture of my stock room and have AI count the items.',
            category='Retail & Inventory',
            image_url='https://images.unsplash.com/photo-1553413077-190dd305871c?q=80&w=800&auto=format&fit=crop',
            author_id=user1.id
        )
        post2 = get_or_create_post(
            title='Customer Support Emails Overwhelming',
            description='We get hundreds of emails a day asking about store hours, return policies, etc. Is there a way to auto-draft replies?',
            category='Operations & HR',
            image_url='https://images.unsplash.com/photo-1596526131083-e8c633c948d2?q=80&w=800&auto=format&fit=crop',
            author_id=user1.id
        )
        post3 = get_or_create_post(
            title='Legacy ERP System Integration',
            description='We have a 15-year-old on-premise ERP system that holds all our critical business logic and customer data. We want to build modern web interfaces and mobile apps for our sales team, but the ERP has no REST APIs, only SOAP endpoints that are poorly documented. Need a middleware solution or AI agent that can auto-generate API wrappers by analyzing the WSDL and database schemas.',
            category='IT & Infrastructure',
            image_url='https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=800&auto=format&fit=crop',
            author_id=user1.id
        )
        post4 = get_or_create_post(
            title='Automated Quality Control in Manufacturing',
            description='Our assembly line produces thousands of small electronic components daily. Currently, human inspectors sample a small percentage for micro-defects like solder bridges or misaligned chips. We have cameras installed but traditional computer vision algorithms create too many false positives. Looking for an AI vision model that can be fine-tuned on our defect dataset and run on edge devices for real-time inspection.',
            category='Manufacturing',
            image_url='https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=800&auto=format&fit=crop',
            author_id=user1.id
        )
        post5 = get_or_create_post(
            title='Dynamic Fleet Routing and Logistics',
            description='Our delivery fleet operates 50 trucks daily. We use static routes that do not account for real-time traffic, sudden weather changes, or urgent dispatch requests mid-route. We need a system that can ingest real-time GPS paths, traffic data APIs, and delivery priorities to dynamically reroute drivers and update customer ETAs automatically.',
            category='Logistics & Supply Chain',
            image_url='https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=800&auto=format&fit=crop',
            author_id=user1.id
        )
        
        # The main demo post
        post6 = get_or_create_post(
            title='Extracting data from messy PDF invoices',
            description='Our accounting department receives hundreds of invoices per week. Some are PDFs, some are photos of paper receipts. Currently humans have to read them and type the vendor, total amount, and line items into our ledger. This is incredibly slow and error-prone. Is there a way to automate this using AI?',
            category='Finance & Accounting',
            image_url='https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?q=80&w=800&auto=format&fit=crop',
            author_id=user1.id
        )

        print("Adding mock prototype...")
        def get_or_create_prototype(title, description, link_url, post_id, author_id):
            proto = Prototype.query.filter_by(title=title).first()
            if not proto:
                proto = Prototype(
                    title=title,
                    description=description,
                    link_url=link_url,
                    post_id=post_id,
                    author_id=author_id
                )
                db.session.add(proto)
                db.session.commit()
            return proto

        proto1 = get_or_create_prototype(
            title='AI Inventory Counter',
            description='A simple web app where you upload a photo and it uses a vision model to count items and export to CSV.',
            link_url='https://example.com/proto1',
            post_id=post1.id,
            author_id=user2.id
        )
        proto2 = get_or_create_prototype(
            title='Interactive Invoice Extractor Demo',
            description='I built a working prototype that uses an OCR pipeline to extract the structured JSON data from your invoices. Try uploading one now!',
            link_url='/demo/invoice-parser',
            post_id=post6.id,
            author_id=user3.id
        )

        def get_or_create_comment(text, author_id, post_id):
            comment = Comment.query.filter_by(text=text, author_id=author_id, post_id=post_id).first()
            if not comment:
                comment = Comment(text=text, author_id=author_id, post_id=post_id)
                db.session.add(comment)
                db.session.commit()
            return comment

        get_or_create_comment("This is such a common problem for small retail!", user2.id, post1.id)
        get_or_create_comment("I've seen some vision APIs that handle this, but they are expensive for small shops.", user4.id, post1.id)
        get_or_create_comment("For the ERP integration, you could use a tool like Zeep in Python to parse the WSDL, and then use an LLM to map the SOAP methods to RESTful endpoints.", user2.id, post3.id)
        get_or_create_comment("Are you open to using local open-source LLMs? We could set up a secure gateway with Llama 3.", user3.id, post3.id)
        get_or_create_comment("Traditional CV is definitely tricky here. Have you looked into YOLOv10?", user3.id, post4.id)
        get_or_create_comment("For the fleet routing, Google's OR-Tools combined with Mapbox could work.", user2.id, post5.id)
        get_or_create_comment("Does the ERP system have a database we can query directly or is it strictly accessible via SOAP?", user4.id, post3.id)
        get_or_create_comment("I've tried similar things in manufacturing. Lighting conditions are usually the biggest hurdle for CV.", user4.id, post4.id)
        get_or_create_comment("We are currently using a similar system for 10 trucks, scaling to 50 is definitely a challenge.", user5.id, post5.id)
        get_or_create_comment("I just tried the prototype linked above, it works flawlessly on my test receipts! What LLM is powering this?", user1.id, post6.id)
        get_or_create_comment("This invoice parser could save us 20 hours a week in data entry!", user5.id, post6.id)
        get_or_create_comment("Are the extracted line items accurate for handwritten invoices too?", user4.id, post6.id)

        print("Adding mock edit suggestion...")
        edit1_title = "Automated Inventory Counting with Vision AI"
        edit1_desc = "Clarifying that we need a solution that works on mobile phones specifically."
        if not EditSuggestion.query.filter_by(suggested_title=edit1_title, post_id=post1.id).first():
            edit1 = EditSuggestion(
                suggested_title=edit1_title,
                suggested_description=edit1_desc,
                author_id=user2.id,
                post_id=post1.id
            )
            db.session.add(edit1)
            db.session.commit()

        print("Adding mock upvotes...")
        def get_or_create_upvote(user_id, post_id=None, prototype_id=None):
            if post_id:
                vote = Upvote.query.filter_by(user_id=user_id, post_id=post_id).first()
            else:
                vote = Upvote.query.filter_by(user_id=user_id, prototype_id=prototype_id).first()
                
            if not vote:
                if post_id:
                    vote = Upvote(user_id=user_id, post_id=post_id)
                else:
                    vote = Upvote(user_id=user_id, prototype_id=prototype_id)
                db.session.add(vote)
                db.session.commit()
            return vote

        get_or_create_upvote(user2.id, post_id=post1.id)
        get_or_create_upvote(user1.id, prototype_id=proto1.id)
        get_or_create_upvote(user1.id, prototype_id=proto2.id)
        get_or_create_upvote(user2.id, post_id=post6.id)
        get_or_create_upvote(user2.id, post_id=post3.id)
        get_or_create_upvote(user3.id, post_id=post4.id)
        get_or_create_upvote(user1.id, post_id=post5.id)

        print("Database seeded successfully with mock data!")

if __name__ == '__main__':
    seed_data()
