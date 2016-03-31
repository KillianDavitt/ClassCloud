from app import app

from app import app, db, lm
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import PinForm
from .models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', users=u, pin_form=pin_form)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))




