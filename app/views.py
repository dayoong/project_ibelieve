#!flask/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, session, url_for, request, g, json, make_response
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, EnrollmentForm, RoleForm, GoalForm, EditForm, RewardForm, SelectForm, TempForm, \
    NotificationForm, LetterForm
from .models import User, Temp, Relationship, Goal, Reward, Notification, Letter
from datetime import datetime, date, timedelta
from config import p
import cgi
import random

select_child = 0
today = date.today()
val = 0
success = 0
child_alert = 0


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/hello')
@login_required
def hello():
    user = g.user
    return render_template('hello.html', user=user)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user = User.query.filter_by(email=form.user_id.data).first()
        # user X
        if user is None:
            nickname = form.user_nickname.data
            email = form.user_id.data
            user = User(nickname=nickname, email=email)
            db.session.add(user)
            db.session.commit()
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(user, remember=remember_me)
            return redirect(url_for('select_role'))

        # user 0, role X
        if user.role is None:
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(user, remember=remember_me)
            return redirect(url_for('select_role'))

        # user 0, role 0, relationship 0
        if user.role == 1:
            new_r = Temp.query.filter_by(related_phone=user.phone).all()
            if new_r is not None:
                for new in new_r:
                    db.session.add(Relationship(child=user.id, parent=new.id))
                    db.session.delete(new)
                    db.session.commit()
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(user, remember=remember_me)
            check = Relationship.query.filter_by(child=user.id).first()
            if check is None:
                return redirect(url_for('stand_by'))
            return redirect(url_for('goal_list'))
        if user.role == 2:
            new_r = Temp.query.filter_by(related_phone=user.phone).all()
            if new_r is not None:
                for new in new_r:
                    db.session.add(Relationship(child=new.id, parent=user.id))
                    db.session.delete(new)
                    db.session.commit()
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(user, remember=remember_me)
            check = Relationship.query.filter_by(parent=user.id).first()
            if check is None:
                return redirect(url_for('enrollment'))
            return redirect(url_for('select_child'))
        return redirect(url_for('enrollment'))
    return render_template('login.html', form=form)


@app.route('/enrollment', methods=['GET', 'POST'])
@login_required
def enrollment():
    flag = 0
    form = EnrollmentForm()
    if form.validate_on_submit():
        if g.user.phone is None:
            g.user.phone = form.my_phone.data
            db.session.add(g.user)
            db.session.commit()

        # 입력된 사용자
        input_user = User.query.filter_by(phone=form.partner_phone.data).first()
        # 나를 찾는 사용자들
        temp_users = Temp.query.filter_by(related_phone=g.user.phone).all()
        if input_user is not None:
            if temp_users is not None:
                for temp_user in temp_users:
                    if temp_user.related_phone == input_user.phone:
                        flag = 1
                    if g.user.role == 1:
                        new_r = Relationship(child=g.user.id, parent=temp_user.id)
                        db.session.add(new_r)
                        db.session.delete(temp_user)
                        db.session.commit()
                    if g.user.role == 2:
                        new_r = Relationship(child=temp_user.id, parent=g.user.id)
                        db.session.add(new_r)
                        db.session.delete(temp_user)
                        db.session.commit()
            # 사용자이긴 Temp에는 없는 사용자
            if flag == 0:
                if g.user.role == 1:
                    new_r = Relationship(child=g.user.id, parent=input_user.id)
                    db.session.add(new_r)
                    db.session.commit()
                    print(form.add.data)
                    if form.add.data == 'add':
                        return redirect(url_for('enrollment'))
                    return redirect(url_for('goal_list'))
                if g.user.role == 2:
                    new_r = Relationship(child=input_user.id, parent=g.user.id)
                    db.session.add(new_r)
                    db.session.commit()
                    print(form.add.data)
                    if form.add.data == 'add':
                        return redirect(url_for('enrollment'))
                    return redirect(url_for('select_child'))
        # input_user가 사용자가 아닐 때
        user = Temp(user_id=g.user.id, related_phone=form.partner_phone.data)
        db.session.add(user)
        db.session.commit()
        print(form.add.data)
        if form.add.data == 'add':
            return redirect(url_for('enrollment'))
        return redirect(url_for('stand_by'))
    return render_template('enrollment.html', form=form, user=g.user)


@app.route('/stand_by')
def stand_by():
    return render_template('stand_by.html')


@app.route('/select_role', methods=['GET', 'POST'])
@login_required
def select_role():
    form = RoleForm()
    if form.validate_on_submit():
        if form.child_user.data:
            g.user.role = 1
            db.session.commit()
            return redirect(url_for('enrollment'))
        else:
            g.user.role = 2
            db.session.commit()
            return redirect(url_for('enrollment'))
    return render_template('select_role.html', form=form)


@app.route('/select_child', methods=['GET', 'POST'])
@login_required
def select_child():
    children = Relationship.query.filter_by(parent=g.user.id).all()
    list = []
    for child in children:
        tmp = User.query.filter_by(id=child.child).first()
        list.append(tmp)
    return render_template('select_child.html', list=list)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/new_goal', methods=['GET', 'POST'])
@login_required
def new_goal():
    form = GoalForm()
    if form.validate_on_submit():
        goal = Goal(user=g.user.id, timestamp=date.today(), contents=form.contents.data,
                    start_date=form.start_date.data, start_day=form.start_day.data, start_hour=form.start_hour.data,
                    start_minute=form.start_minute.data, finish_date=form.finish_date.data,
                    finish_day=form.finish_day.data, finish_hour=form.finish_hour.data,
                    finish_minute=form.finish_minute.data, alert_time=form.alert_time.data,
                    alert_cycle=form.alert_cycle.data, color=form.color.data, memo=form.memo.data,
                    status=form.status.data)
        db.session.add(goal)
        db.session.commit()
        return redirect(url_for('goal_list'))
    return render_template('new_goal.html', form=form, user=g.user)


@app.route('/future_goal_edit', methods=['GET', 'POST'])
def future_goal_edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.future_goal = form.future_goal.data
        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for('goal_list'))
    return render_template('future_goal_edit.html', form=form)


@app.route('/goal_list', methods=['GET', 'POST'])
@app.route('/goal_list/<int:id>', methods=['GET', 'POST'])
@login_required
def goal_list(id=id):
    global today
    global val
    global success
    success = 0
    val = 0
    today = date.today()
    list = []
    find_child = ''
    form = NotificationForm()
    if g.user.role == 1:
        future_goal = g.user.future_goal
        goals = Goal.query.filter(Goal.start_date <= today)
        # goal_count = 0
        for goal in goals:
            if goal.finish_date >= str(today) and goal.user == g.user.id:
                list.append(goal)
                # goal_count += 1
    if g.user.role == 2:
        global select_child
        select_child = id
        print('goal_list')
        print(select_child)
        find_child = User.query.filter_by(id=select_child).first()
        future_goal = find_child.future_goal
        goals = Goal.query.filter(Goal.start_date <= today)
        for goal in goals:
            if goal.finish_date >= str(today) and goal.user == find_child.id and goal.status == 'public':
                list.append(goal)
    return render_template('goal_list.html', future_goal=future_goal, list=list, id=select_child,
                           user=g.user, today=today, val=val, form=form, find_child=find_child)


@app.route('/prevGoal', methods=['GET', 'POST'])
@app.route('/prevGoal/<int:id>', methods=['GET', 'POST'])
def prevGoal(id=id):
    global today
    global val
    val = 1
    list = []
    form = NotificationForm()
    if g.user.role == 1:
        today = today - timedelta(1)
        goals = Goal.query.filter(Goal.start_date <= today)
        for goal in goals:
            if goal.finish_date >= str(today) and goal.user == g.user.id:
                list.append(goal)
    if g.user.role == 2:
        today = today - timedelta(1)
        global select_child
        select_child = id
        print(select_child)
        print(select_child)
        child = User.query.filter_by(id=id).first()
        goals = Goal.query.filter(Goal.start_date <= today)
        for goal in goals:
            if goal.finish_date >= str(today) and goal.user == child.id and goal.status == 'public':
                list.append(goal)
    return render_template('prevGoal.html', list=list, id=select_child, user=g.user, today=today, val=val, form=form)


@app.route('/nextGoal', methods=['GET', 'POST'])
@app.route('/nextGoal/<int:id>', methods=['GET', 'POST'])
def nextGoal(id=id):
    global today
    global val
    val = 2
    list = []
    form = NotificationForm()
    if g.user.role == 1:
        today = today + timedelta(1)
        goals = Goal.query.filter(Goal.start_date <= today)
        for goal in goals:
            if goal.finish_date >= str(today) and goal.user == g.user.id:
                list.append(goal)
    if g.user.role == 2:
        today = today + timedelta(1)
        global select_child
        select_child = id
        print(select_child)
        print(select_child)
        child = User.query.filter_by(id=id).first()
        goals = Goal.query.filter(Goal.start_date <= today)
        for goal in goals:
            if goal.finish_date >= str(today) and goal.user == child.id and goal.status == 'public':
                list.append(goal)
    return render_template('nextGoal.html', list=list, id=select_child, user=g.user, today=today, val=val, form=form)


@app.route('/progressbar/<int:count>', methods=['GET', 'POST'])
def progressbar(count):
    global success
    success += 1
    result = (round(success / (count * 1.0), 3)) * 100
    print(success)
    print(count)
    print(result)
    return render_template('progressbar.html', percent=result)


@app.route('/parent_reward', methods=['GET', 'POST'])
def parent_reward():
    print('parent_reward')
    global select_child
    print(select_child)
    form = RewardForm()
    sform = SelectForm()
    rewards = []
    if g.user.role == 1:
        parents = Relationship.query.filter_by(child=g.user.id).all()
        for parent in parents:
            rewards += Reward.query.filter_by(parent_id=parent.parent).all()
    if g.user.role == 2:
        rewards = Reward.query.filter_by(parent_id=g.user.id).all()
        for reward in rewards:
            if reward.child_id is not select_child:
                rewards.remove(reward)
        print(rewards)
    if form.validate_on_submit():
        reward = Reward(parent_id=g.user.id, child_id=select_child, parent_status='false',
                        child_status='false', contents=form.contents.data)
        db.session.add(reward)
        db.session.commit()
        return redirect(url_for('parent_reward'))
    return render_template('parent_reward.html', form=form, user=g.user, rewards=rewards, sform=sform)


@app.route('/notification_test')
def notify_test():
    return render_template('notification_test.html')


@app.route('/to_child', methods=['GET', 'POST'])
@app.route('/to_child/<int:id>', methods=['GET', 'POST'])
def to_child(id=id):
    global select_child
    select_child = id
    form = LetterForm()
    user = g.user
    letters = []
    find_child = ''
    print(user)
    if user.role == 2:
        list = Letter.query.filter_by(parent=user.id)
        if list is not None:
            for e in list:
                if e.child == select_child:
                    letters.append(e)
        letters.reverse()
        find_child = User.query.filter_by(id=select_child).first()
        if form.validate_on_submit():
            letter = Letter(parent=user.id, parent_nickname=user.nickname, child=find_child.id, child_nickname=find_child.nickname,
                            contents=form.to_child.data, timestamp=date.today(), title=form.title.data)
            db.session.add(letter)
            db.session.commit()
            return redirect(url_for('to_child', id=id))
    if user.role == 1:
        letters = Letter.query.filter_by(child=user.id).all()
        letters.reverse()
    print(letters)
    return render_template('to_child.html', form=form, user=user, find_child=find_child, letters=letters)


@app.route('/letter/<int:id>', methods=['GET', 'POST'])
def letter(id=id):
    l = Letter.query.filter_by(id=id).first()
    return render_template('letter.html', l=l)

@app.route('/notification', methods=['POST'])
def trigger_notification():
    print('start')
    global child_alert
    child_alert += 1
    message = cgi.escape(request.form['message'])
    user_id = cgi.escape(request.form['user_id'])
    goal_id = cgi.escape(request.form['goal_id'])
    p.trigger('notifications', 'new_notification', {'message': message})
    if message == 'complete':
        print('complete')
        relations = Relationship.query.filter_by(child=g.user.id).all()
        goal = Goal.query.filter_by(id=goal_id).first()
        if goal.status == 'public':
            for relation in relations:
                ntf = Notification(post_id=user_id, get_id=relation.parent, goal_id=goal_id, contents='complete',
                                   post_nickname=g.user.nickname, goal_contents=goal.contents)
                user = User.query.filter_by(id=relation.parent).first()
                user.alert_count = child_alert
                db.session.add(user)
                db.session.add(ntf)
                db.session.commit()
    print('finishi')
    return "Notification triggered!"


@app.route('/parent_alert/<int:id>', methods=['GET', 'POST'])
def parent_alert(id=id):
    global select_child
    select_child = id
    user = g.user
    find_child = User.query.filter_by(id=select_child).first()
    user.alert_count = 0
    db.session.add(user)
    db.session.commit()
    alert_list = Notification.query.filter_by(get_id=g.user.id).all()
    return render_template('parent_alert.html', alert_list=alert_list, find_child=find_child, user=user)


@app.route('/parent_link/<int:id>', methods=['GET', 'POST'])
def parent_link(id=id):
    global select_child
    select_child = id
    user = g.user
    find_child = User.query.filter_by(id=select_child).first()
    return render_template('parent_link.html', user=user, find_child=find_child)


@app.route('/article1', methods=['GET', 'POST'])
def article1():
    return render_template('article1.html')


@app.route('/article2', methods=['GET', 'POST'])
def article2():
    return render_template('article2.html')


# @app.route('/self_evaluation', methods=['GET', 'POST'])
@app.route('/self_evaluation/<int:id>', methods=['GET', 'POST'])
@login_required
def self_evaluation(id=id):
    print(id)
    print('enter')
    form = GoalForm()
    print('form')
    if form.validate_on_submit():
        print(form.self_evaluation.data)
        g = Goal.query.filter_by(id=id).first()
        g.self_evaluation = form.self_evaluation.data
        db.session.add(g)
        db.session.commit()
        return redirect(url_for('goal_list'))
    return render_template('self_evaluation.html', form=form)
