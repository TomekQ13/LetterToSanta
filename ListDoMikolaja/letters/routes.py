from flask import Blueprint, flash, render_template, redirect, url_for, abort, request
from flask_login import current_user, login_required
from sqlalchemy.sql.elements import True_
from ListDoMikolaja import db
from ListDoMikolaja.letters.forms import LetterForm, LetterLineForm
from ListDoMikolaja.models import Letter, LetterLine, User

letters = Blueprint('letters', __name__)

@letters.route("/letter/friends_letter", methods=['GET'])
@login_required
def friends_letter():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if user:
        letter_lines = LetterLine.query.filter_by(user_id=user_id).all()
    else:
        flash('Nieznany użytkownik.', 'danger')
        return redirect(url_for('friends.home'))

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
        
    return render_template('new_letter_line.html', form=form, line = existing_lines, legend='Dodaj przedmiot do listy!')

@letters.route("/letter/accept")
@login_required
def take_letter_line():
    letter_line_id = request.args.get('letter_line_id')
    letter_line = LetterLine.query.get_or_404(letter_line_id)
    if current_user.id in [x.id for x in letter_line.author.friends]:
        letter_line.taken = True
        letter_line.taken_user_id = current_user.id
        db.session.commit()
        flash('Przedmiot został zarezerwowany.', 'success')
        return redirect(url_for('letters.friends_letter', user_id=letter_line.author.id))
    else:
        flash('Musisz być znajomym użytkownika żeby zarezerwować przedmiot na jego liście.', 'danger')
        return redirect(url_for('friends.home'))

@letters.route("/letter/delete_letter_line", methods=['GET', 'POST'])
@login_required
def delete_letter_line():
    letter_line_id = request.args.get('letter_line_id')
    letter_line = LetterLine.query.get_or_404(letter_line_id)
    if current_user.id == letter_line.user_id:
        db.session.delete(letter_line)
        db.session.commit()
        flash('Przedmiot został usunięty z listy.', 'success')
    else:
        abort(403)

    return redirect(url_for('letters.letter_lines'))
        
