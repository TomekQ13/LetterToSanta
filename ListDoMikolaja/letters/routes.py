from sys import stderr
from flask import Blueprint, flash, render_template, redirect, url_for, abort, request
from flask_login import current_user, login_required
from sqlalchemy.sql.elements import True_
from ListDoMikolaja import db
from ListDoMikolaja.letters.forms import LetterForm, LetterLineForm
from ListDoMikolaja.models import Letter, LetterLine, User

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
        letter_lines = LetterLine.query.filter_by(user_id=user_id).all()
    else:
        flash('Nieznany użytkownik.', 'danger')
        return redirect(url_for('main.home'))

    if int(user_id) in {x.id for x in current_user.friends}:
        is_friend = True
    else:
        is_friend = False

    return render_template('friend_letter.html', lines=letter_lines, is_friend = is_friend)

@letters.route("/letter/letter_lines", methods=['GET'])
@login_required
def letter_lines():
    existing_lines = current_user.letter_lines        
    return render_template('letter_lines.html', lines = existing_lines)

@letters.route("/letter/new_letter_line", methods=['GET', 'POST'])
@login_required
def new_letter_line():
    existing_lines = current_user.letter_lines
    form = LetterLineForm()
    if form.validate_on_submit():
        letter_line = LetterLine(user_id = current_user.id, line_content = form.line_content.data)
        db.session.add(letter_line)
        db.session.commit()
        flash('Przedmiot został dodany do listu.', 'success')
        return redirect(url_for('letters.letter_lines'))
        
    return render_template('new_letter_line.html', form=form, line = existing_lines, legend='Napisz list!')