from flask import render_template, request, Blueprint
from flask.templating import render_template_string
from flask_user import roles_required
from blog.models import Post

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
@roles_required('Admin')
def test_page():
    return render_template_string('''<h1> test page - authentication successful </h1>''')