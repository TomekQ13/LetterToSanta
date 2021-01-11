from sys import stderr
from flask import Blueprint, flash, render_template, redirect, url_for, abort, request
from flask_login import current_user, login_required
from sqlalchemy.sql.elements import True_
from ListDoMikolaja import db
from ListDoMikolaja.letters.forms import LetterForm
from ListDoMikolaja.models import Letter, User

letters = Blueprint('letters', __name__)

@letters.route("/letter")
@login_required
def letter():
    letter = Letter.query.filter_by(user_id = current_user.id).first()
    return render_template('letter.html', title='Mój list', letter=letter)

@letters.route("/letter/new", methods=['GET', 'POST'])
@login_required
def new_letter():
    #if user already has a letter
    existing_letter = Letter.query.filter_by(user_id = current_user.id).first()
    if existing_letter:
        flash('Już napisałeś list. Zaktualizuj go lub usuń jeżeli chcesz zacząć od nowa.', 'warning')
        return redirect(url_for('letters.letter'))

    form = LetterForm()
    if form.validate_on_submit():
        letter = Letter(content = form.content.data, user_id = current_user.id)
        db.session.add(letter)
        db.session.commit()
        flash('List został dodany pomyślnie!', 'success')
        return redirect(url_for('letters.letter'))

    letter = Letter.query.filter_by(user_id = current_user.id).first()
    return render_template('new_letter.html', form=form, letter=letter, legend='Napisz list!')

@letters.route("/letter/delete", methods=['POST'])
@login_required
def delete_letter():
    letter = Letter.query.filter_by(user_id=current_user.id).first()
    #if current_user is not an author and current user is not an admin
    if letter.author != current_user and 'Admin' not in current_user.roles_names:
        abort(403)

    db.session.delete(letter)
    db.session.commit()
    flash('List został usunięty.', 'success')
    return redirect(url_for('letters.letter'))

@letters.route("/letter/friends_letter", methods=['GET'])
@login_required
def friends_letter():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if user:
        letter = Letter.query.filter_by(user_id=user_id).first()
    else:
        flash('Nieznany użytkownik.', 'danger')
        return redirect(url_for('main.home'))

    if int(user_id) in {x.id for x in current_user.friends}:
        is_friend = True
    else:
        is_friend = False

    return render_template('friend_letter.html', letter=letter, is_friend = is_friend)
