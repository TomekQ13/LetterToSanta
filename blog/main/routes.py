from blog.users.utils import role_required
from flask import render_template, request, Blueprint
from flask.templating import render_template_string
from flask_login import current_user
from flask_login.utils import login_required
from blog.models import Post, Role

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts = posts)

@main.route("/about")
def about():
    return render_template('about.html', title = 'About')


@main.route("/test")
@role_required('Admin')
def test_page():
    if Role.query.filter_by(name='Admin').first() in current_user.roles:
        return render_template_string('''<h1> test page - authentication successful </h1>''')
    else:
        return render_template_string('''<h1> test page - authentication unsuccessful </h1>''')