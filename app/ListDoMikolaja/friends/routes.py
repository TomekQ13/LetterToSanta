from datetime import datetime
from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_required
from ListDoMikolaja import db
from ListDoMikolaja.friends.forms import SendFriendRequestForm
from ListDoMikolaja.models import FriendRequest, User, Friends


friends = Blueprint('friends', __name__)

@friends.route("/")
@friends.route("/home")
@login_required
def home():
    return render_template('home.html')


@friends.route("/friends/request", methods=['GET', 'POST'])
@login_required
def new_friend_request():
    form = SendFriendRequestForm()    
    if form.validate_on_submit():
        sent_to_user = User.query.filter_by(username=form.username.data).first()
        #if user with this username does not exist
        if not sent_to_user:
            flash('Taki użytkownik nie istnieje.', 'danger')
            return render_template('send_friend_request.html', form=form)

        #if user tries to send a request to themselves
        if form.username == current_user.username:
            flash('Nie możesz zaprosić samego siebie :)', 'danger')
            return render_template('send_friend_request.html', form=form)

        #if users are friends already
        if form.username.data in {x.username for x in current_user.friends}:
            flash('Ten użytkownik już jest Twoim znajomym', 'info')
            return render_template('send_friend_request.html', form=form)

        #if the same request was already sent
        the_same_request = FriendRequest.query \
            .filter(FriendRequest.sent_by_id==current_user.id, \
                 FriendRequest.sent_to_id==sent_to_user.id, \
                 FriendRequest.status_cd==0) \
            .first()
        if the_same_request:
            flash(f'Zaproszenie do tego użytkownika zostało już wysłane. Poczekaj aż zostanie ono zaakceptowane lub odrzucone.', 'info')
            return redirect(url_for('friends.friends_page'))

        #if the opposite requrest was already sent
        opposite_request = FriendRequest.query \
            .filter(FriendRequest.sent_by_id==sent_to_user.id, \
                 FriendRequest.sent_to_id==current_user.id, \
                 FriendRequest.status_cd==0) \
            .first()
        if opposite_request:
            flash(f'Ten użytkownik już wysłał Ci zaproszenie. Możesz je zaakceptowac w zakładce Zaproszenia do znajomych.', 'info')
            return render_template('send_friend_request.html', form=form)
            #tutaj dodać redirect for url gdzie się akceptuje zaproszenia
    
        sent_to_id = User.query.filter_by(username=form.username.data).first().id        
        request = FriendRequest(sent_by_id=current_user.id, sent_to_id=sent_to_id)
        db.session.add(request)
        db.session.commit()
        flash('Zaproszenie zostało wysłane', 'success')
        return redirect(url_for('friends.friends_page'))

    return render_template('send_friend_request.html', form=form)

@friends.route("/friends", methods=['GET'])
@login_required
def friends_page():
    return render_template('friends.html', friends=current_user.friends)

@friends.route("/friends_requests", methods=['GET'])
@login_required
def friends_request_list():
    requests_received_0 = [x for x in current_user.requests_received if x.status_cd == 0]
    return render_template('friends_request_list.html', requests_received=requests_received_0)

@friends.route("/friends_request/decline/<int:request_id>")
def request_decline(request_id):
    friend_request = FriendRequest.query.get_or_404(request_id)
    friend_request.status_cd = 1
    friend_request.date_status_change = datetime.now()
    db.session.commit()
    flash('Zaproszenie zostało odrzucone.', 'success')
    return redirect(url_for('friends.friends_request_list'))

@friends.route("/friends_request/accept/<int:request_id>")
def request_accept(request_id):
    friend_request = FriendRequest.query.get_or_404(request_id)
    new_friend = Friends(invited_id=friend_request.sent_by_id,
        accepted_id=friend_request.sent_to_id)
    db.session.delete(friend_request)
    db.session.add(new_friend)
    db.session.commit()
    flash('Zaproszenie zostało zaakceptowane', 'success')
    return redirect(url_for('friends.friends_request_list'))

@friends.route('/friends/reserved_items')
def reserved_items():
    return render_template('reserved_items.html', reserved_items = current_user.taken_lines)

