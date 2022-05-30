from dao.model.user import User

class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def create_user(self, user):
        user_ent = User(**user)
        self.session.add(user_ent)
        self.session.commit()
        return user_ent

