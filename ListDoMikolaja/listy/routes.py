from flask import Blueprint, flash, render_template, redirect, url_for, abort
from flask_login import current_user, login_required
from ListDoMikolaja import db
from ListDoMikolaja.listy.forms import LetterForm
from ListDoMikolaja.models import Letter

listy = Blueprint('listy', __name__)

@listy.route("/letter")
@login_required
def letter():
    letter = Letter.query.filter_by(user_id = current_user.id).first()
    return render_template('letter.html', title='Mój list', letter=letter)

@listy.route("/letter/new", methods=['GET', 'POST'])
@login_required
def new_letter():
    #if user already has a letter
    existing_letter = Letter.query.filter_by(user_id = current_user.id).first()
    if existing_letter:
        flash('Już napisałeś list. Zaktualizuj go lub usuń jeżeli chcesz zacząć od nowa.', 'warning')
        return redirect(url_for('listy.letter'))

    form = LetterForm()
    if form.validate_on_submit():
        letter = Letter(content = form.content.data, user_id = current_user.id)
        db.session.add(letter)
        db.session.commit()
        flash('List został dodany pomyślnie!', 'success')
        return redirect(url_for('listy.letter'))

    letter = Letter.query.filter_by(user_id = current_user.id).first()
    return render_template('new_letter.html', form=form, letter=letter, legend='Napisz list!')

@listy.route("/letter/delete", methods=['POST'])
def delete_letter():
    letter = Letter.query.filter_by(user_id=current_user.id).first()
    #if current_user is not an author and current user is not an admin
    if letter.author != current_user and 'Admin' not in current_user.roles_names:
        abort(403)

    db.session.delete(letter)
    db.session.commit()
    flash('List został usunięty.', 'success')
    return redirect(url_for('listy.letter'))
