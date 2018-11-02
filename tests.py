import server
import unittest
from server import app
from model import db, connect_to_db
from seed import load_users_and_projects, seed_data

class ProjectTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        # self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"What will your baby look like?", result.data)


    def test_new_project(self):
        result = self.client.get("/new_project")
        self.assertIn(b"Your baby prediction is on the way", result.data)

    def test_logged_out(self):
        result = self.client.get("/logged_out", follow_redirects=True)
        self.assertIn(b"What will your baby look like?", result.data)

    def test_display_register_form(self):
        result = self.client.get("/register_form")
        self.assertIn(b"Email:", result.data)

    





class TestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        # app.config['SECRET_KEY'] = 'key'
        # self.client = app.test_client()

        # with self.client as c:
        #     with c.session_transaction() as sess:
        #         sess['user_id'] = 1
        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        # load_users_and_projects()
        seed_data()

    
    def test_login(self):
        result = self.client.post("/login_form",
                                  data={'email': "jane@gmail.com", 'password': "123"},
                                  follow_redirects=True)
        self.assertIn(b"Your baby prediction is on the way", result.data)

    def test_no_known_user_login(self):
        result = self.client.post("/login_form",
                                  data={'email': "bob@gmail.com", 'password': "bob"},
                                  follow_redirects=True)
        self.assertNotIn(b"Your baby prediction is on the way", result.data)
        self.assertIn(b"Email", result.data)

        

    def test_new_registration(self):
        result = self.client.post("/register_form",
                                  data={'email': "joe@gmail.com", 'password': "joe"},
                                  follow_redirects=True)
        self.assertIn(b"Your baby prediction is on the way", result.data)
        self.assertNotIn(b"Email:", result.data)

    def test_already_registered(self):
        result = self.client.post("/register_form",
                                  data={'email': "jonathan@gmail.com", 'password': "abc"},
                                  follow_redirects=True)
        self.assertNotIn(b"Your baby prediction is on the way", result.data)
        self.assertIn(b"Email:", result.data)

    def test_results(self):
        result = self.client.get("/results/1", follow_redirects=True)
        self.assertIn(b"Here's how your baby will look like", result.data)
        self.assertIn(b"/static/upload/project_1/result.png", result.data)





    

    def tearDown(self):
        """Do at end of every test."""

        db.drop_all()
        db.session.close()


    


    # def test_games(self):
    #     """Test departments page."""

    #     result = self.client.get("/games")
    #     self.assertIn(b"Power Grid", result.data)


if __name__ == "__main__":
    unittest.main()


    