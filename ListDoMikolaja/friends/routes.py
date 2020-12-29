from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_required
from ListDoMikolaja import db
from ListDoMikolaja.friends.forms import SendFriendRequestForm
from ListDoMikolaja.models import FriendRequest, User, Friends

friends = Blueprint('friends', __name__)

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

        #if users are friends already
        current_user_friends = Friends.query \
            .filter(((Friends.invited_id==current_user.id) and (Friends.accepted_id==sent_to_user.id)) \
                or ((Friends.invited_id==sent_to_user.id) and (Friends.accepted_id==current_user.id))) \
            .first()
        if current_user_friends:
            flash('Ten użytkownik już jest Twoim znajomym', 'info')
            return render_template('send_friend_request.html', form=form)

        #if the same request was already sent
        the_same_request = FriendRequest.query \
            .filter((FriendRequest.sent_by_id==current_user.id) and \
                 (FriendRequest.sent_to_id==sent_to_user.id) and \
                 (FriendRequest.status_cd==0)) \
            .first()
        if the_same_request:
            flash(f'Już wysłałeś zaproszenie do tego użytkownika. Poczekaj aż zostanie ono zaakceptowane lub odrzucone.', 'info')
            return redirect(url_for('friends.friends_page'))

        #if the opposite requrest was already sent
        opposite_request = FriendRequest.query \
            .filter((FriendRequest.sent_by_id==sent_to_user.id) and \
                 (FriendRequest.sent_to_id==current_user.id) and \
                 (FriendRequest.status_cd==0)) \
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
    #TO DO a query which returns all the friends of a user
    return render_template('friends.html', friends=friends_results)

@friends.route("/friends_requests", methods=['GET'])
@login_required
def friends_request_list():
    requests_sent = FriendRequest.query.filter(FriendRequest.sent_by_id==current_user.id)
    requests_received = FriendRequest.query.filter_by((FriendRequest.sent_to_id==current_user.id) and (FriendRequest.status_cd==0))
    return render_template('friends_request_list.html', requests_received=requests_received, requests_sent=requests_sent)