import unittest
import os
os.environ['FLASK_ENV'] = "testing"
from app import app, TimelinePost
from peewee import SqliteDatabase


test_db = SqliteDatabase(':memory:')

class AppTestCase(unittest.TestCase):
    def setUp(self):
        TimelinePost._meta.database = test_db
        test_db.bind([TimelinePost], bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables([TimelinePost])

        self.client = app.test_client()
    def tearDown(self):
        # Drop tables and close the test database
        test_db.drop_tables([TimelinePost])
        test_db.close()
    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Fanjin Meng - MLH Fellow</title>" in html

        image_path = './app/static/img/profile.jpeg'
        # Check if the file exists
        self.assertTrue(os.path.exists(image_path), f"Image {image_path} does not exist.")

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        


    def test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html


