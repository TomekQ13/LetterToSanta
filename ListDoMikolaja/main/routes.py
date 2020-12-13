from flask import render_template, request, Blueprint
from flask_login import current_user, login_required


from ListDoMikolaja.models import Letter

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    listy = Letter.query.order_by(Letter.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts = listy)

@main.route("/about")
def about():
    return render_template('about.html', title = 'About')