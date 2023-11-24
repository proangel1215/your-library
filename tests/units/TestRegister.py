# from appimport db
# from config import TestConfiguration
from app import create_app as c_app, db
from flask_testing import TestCase
from app.models.User import User
from flask_wtf.csrf import generate_csrf

class TestingWhileLoggedIn(TestCase):
    def create_app(self):
        app = c_app("config.TestingConfig")
        return app

    # executed prior to each test
    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_resgister(self):
        user = User(
            email="test1@gmail.com", username="test", password_plaintext="Test123!"
        )
        assert user.email == "test1@gmail.com"
        assert user.username == "test"
        assert user.is_password_correct("Test123!") == True

        db.session.add(user)
        db.session.commit()

        response = self.client.get("/register", follow_redirects=False)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/register",
            data={
                "pseudo": "testuser",
                "email": "test@example.com",
                "password": "Test123!",
                "password_confirmation": "Test123!",
                "csrf_token": generate_csrf(),  
            },
            follow_redirects=False,
        )

        print(response.data)

        self.assertEqual(response.status_code, 302)
        assert b"home" in response.data

        user = User.query.filter_by(username='testuser').first()
        assert user is not None


#   def test_delete_post_page_li(self):
#         p_cat = PostCategory(name='froots')

#         db.session.add(p_cat)
#         db.session.commit()

#         post = Post(name='Hello', content='3fhskajlga', category_id=1, category=p_cat)
#         db.session.add(post)
#         db.session.commit()

#         response = self.client.get('/delete_post/1', follow_redirects=False)
#         self.assertEqual(response.status_code, 302)

#         deleted_post = Post.query.filter_by(name='Hello').first()

#         self.assertEqual(deleted_post, None)

#         assert post not in db.session
