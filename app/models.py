# -- coding: utf-8 --
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer, index=True)
    nickname = db.Column(db.String(80), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(50))
    last_seen = db.Column(db.DateTime)
    future_goal = db.Column(db.String(100))
    alert_count = db.Column(db.Integer, default=0)
    waiting = db.relationship('Temp', backref='registrant', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def added_goals(self):
        return Goal.query.filter(self.id == Goal.user).order_by(Goal.start_date.asc()).all()

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Relationship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child = db.Column(db.Integer)
    parent = db.Column(db.Integer)

    def __repr__(self):
        return '<Relationship %d>' % (self.child)


class Temp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    related_phone = db.Column(db.String(50))

    def __repr__(self):
        return '<Temp %r>' % (self.related_phone)


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer)
    timestamp = db.Column(db.String(15))
    contents = db.Column(db.String(20))
    start_date = db.Column(db.String(10))
    start_day = db.Column(db.String(10))
    start_hour = db.Column(db.Integer)
    start_minute = db.Column(db.Integer)
    finish_date = db.Column(db.String(10))
    finish_day = db.Column(db.String(10))
    finish_hour = db.Column(db.Integer)
    finish_minute = db.Column(db.Integer)
    alert_time = db.Column(db.Integer)
    alert_cycle = db.Column(db.String(10))
    color = db.Column(db.String(10))
    memo = db.Column(db.String(150))
    status = db.Column(db.String(10))
    self_evaluation = db.Column(db.String(140))

    def __repr__(self):
        return '<Post %r>' % (self.contents)


class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer)
    child_id = db.Column(db.Integer)
    parent_status = db.Column(db.String(5))
    child_status = db.Column(db.String(5))
    contents = db.Column(db.String(50))

    def __repr__(self):
        return '<Reward %r>' % (self.contents)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    post_nickname = db.Column(db.String(80))
    goal_contents = db.Column(db.String(200))
    get_id = db.Column(db.Integer)
    goal_id = db.Column(db.Integer)
    contents = db.Column(db.String(200))
    badge = db.Column(db.Integer)

    def __repr__(self):
        return '<Reward %r>' % (self.contents)


class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer)
    parent_nickname = db.Column(db.String(80))
    child = db.Column(db.Integer)
    child_nickname = db.Column(db.String(80))
    contents = db.Column(db.String(500))
    timestamp = db.Column(db.String(15))
    title = db.Column(db.String(50))

    def __repr__(self):
        return '<Letter %r>' % (self.contents)