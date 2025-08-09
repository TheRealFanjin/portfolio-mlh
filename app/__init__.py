import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import datetime
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("FLASK_ENV") == 'testing':
    print('Running in testing mode')
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)


else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
        )





class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


# Only connect and create tables in non-testing environments
if os.getenv("FLASK_ENV") != "testing" and not mydb.is_closed():
    mydb.connect()
    mydb.create_tables([TimelinePost])

pages = [('Hobbies', 'hobbies'), ('Experience', 'experience')]
@app.route('/')
def index():
    return render_template('index.html', title="Fanjin Meng - MLH Fellow", url=os.getenv("URL"), pages=pages)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        name = request.form['name']
    except KeyError:
        return "Invalid name", 400
    email = request.form['email']
    if '@' not in email or '.' not in email.split('@')[-1]:
        return "Invalid email", 400
    content = request.form['content']
    if not content:
        return "Invalid content", 400
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
            ]
    }

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")
@app.route('/hobbies')
def hobbies():
    hobbies = [{
        'name': 'Planespotting',
        'description': 'I love watching airplanes at airports, and generally anything about airliners! I also love flight simming. I have over 700 hours in Microsoft Flight Simulator flying airliners like the Airbus A320 and Boeing 777.',
        'images': [{'name': 'planespotting.jpg', 'width': 200, 'height': 135}]
    }, {
        'name': 'Gaming',
        'description': 'I play many video games like Microsoft Flight Simulator, Gran Turismo 7, Fortnite, Terraria, and Cyberpunk 2077. I mostly play on PC but I have a PS5 for Gran Turismo 7.',
        'images': [
            {'name': 'Cyberpunk.jpg', 'width': 291, 'height': 342},
            {'name': 'fortnite.jpg', 'width': 200, 'height': 112.5}
        ]
    }, {
        'name': 'PC Building',
        'description': 'I really enjoy building PCs. My current PC build is a Gigabyte Aorus RTX 5090 with a Ryzen 7 7800X3D and 64GB of DDR5-6400 RAM. The 32GB of VRAM on the 5090 is great for Microsoft Flight Simulator and using local LLMs!',
        'images': [{'name': 'pc.jpeg', 'width': 150, 'height': 200}]
    }]
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"), pages=pages, hobbies=hobbies)

@app.route('/experience')
def experience():
    experiences = [
        {
            'title': 'MLH Production Engineering Fellow',
            'location': 'Remote',
            'dates': 'June 2025 - September 2025',
            'description': 'Current Fellowship'
        },
        {
            'title': 'Codepath WEB101 Participant',
            'location': 'Remote',
            'dates': 'February 2025 - April 2025',
            'description': 'Utilized pair programming techniques with a group of peers on hands-on activities each week, learning and exploring the basics of web development'
        }
    ]
    return render_template('experience.html', title="Experience", url=os.getenv("URL"), pages=pages, experiences=experiences)
