#!flask/bin/python
#-*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length
from datetime import datetime
from datetime import date


class LoginForm(Form):
    user_id = StringField('user_id', validators=[DataRequired()])
    user_nickname = StringField('user_nickname')
    remember_me = BooleanField('remember_me', default=False)

class RoleForm(Form):
    child_user = BooleanField('user_role', default=False)
    parent_user = BooleanField('user_role', default=False)


class EnrollmentForm(Form):
    my_phone = StringField('my_phone', validators=[DataRequired()])
    partner_phone = StringField('partner1_phone', validators=[DataRequired()])
    add = StringField('add', default='connect')


class GoalForm(Form):
    contents = StringField('contents', validators=[DataRequired()])
    start_date = StringField('start_date', default=date.today())
    start_day = StringField('start_day', default='day')
    start_hour = IntegerField('start_hour', default=datetime.today().hour)
    start_minute = IntegerField('start_minute', default=datetime.today().minute)
    finish_date = StringField('finish_date', default=date.today())
    finish_day = StringField('finish_day', default='day')
    finish_hour = IntegerField('finish_hour', default=datetime.today().hour)
    finish_minute = IntegerField('finish_minute', default=datetime.today().minute)
    alert_time = IntegerField('alert_time', default=10)
    alert_cycle = StringField('alert_cycle', default='minute')
    color = StringField('color')
    memo = StringField('memo')
    status = StringField('status', default='private')
    self_evaluation = TextAreaField('self_evaluation',  validators=[Length(min=0, max=140)])


class EditForm(Form):
    future_goal = StringField('future_goal', validators=[Length(min=0, max=100)])


class RewardForm(Form):
    contents = StringField('contents', validators=[DataRequired()])

class SelectForm(Form):
    select = BooleanField('select', default=False)
    id = IntegerField('id')

class TempForm(Form):
    var = IntegerField('var')
    cal = IntegerField('cal', default=1)


class NotificationForm(Form):
    state = StringField('state', default='complete')
    in_progress = StringField('in_progress', default='in_progress')


class LetterForm(Form):
    title = StringField('title')
    to_child = TextAreaField('to_child',  validators=[Length(min=0, max=500)])