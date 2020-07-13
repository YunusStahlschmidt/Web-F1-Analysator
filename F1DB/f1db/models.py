from F1DB.f1db import cursor, login_manager
from flask_login import UserMixin


logged_in_user = []


@login_manager.user_loader
def load_user(user_id):
    if len(logged_in_user) != 0:
        user = logged_in_user[0]
        return user
    else:
        return None


class User(UserMixin):
    id = ""
    username = ""
    email = ""
    password = ""
    type = ""
    points_of_week = ""
    week = ""
    image_file = ""

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.username}')"


class Post:
    def __init__(self, id, title, date_posted, content, user_id):
        self.id = id
        self.title = title
        self.date_posted = date_posted
        self.content = content
        self.author, self.author_img = self.get_post_author(user_id)
        self.author_id = user_id

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    def get_post_author(self, user_id):
        cursor.execute(f"select user_name, user_img from users where user_id={user_id}")
        author = cursor.fetchone()
        return author[0], author[1]


class Result:
    def __init__(self, table, data, headings):
        self.table = table
        self.data = data
        self.headings = headings
