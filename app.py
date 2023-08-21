import keyss
from twilio.rest import Client
from datetime import timedelta
from flask import (
    Flask, 
    redirect, 
    render_template, 
    request, 
    session, 
    url_for
)
from flask_login import (
    LoginManager,
    UserMixin,
    current_user, 
    login_required,
    login_user,
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='your secret here', 
    SQLALCHEMY_DATABASE_URI='sqlite:///users.db'
)
app.permanent_session_lifetime = timedelta(minutes=30)
db = SQLAlchemy(app)

client = Client(keyss.account_sid, keyss.auth_token)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    # Delete all tables and their contents.
    db.drop_all()
    # Create the database tables and add users.
    db.create_all()
    
    # If you want to add more users, add them here.
    user2 = User(username='Djeilqnka')
    user3 = User(username='Velko')
    user1 = User(username='Haris')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

@app.before_request
def before_request():
    session.permanent = True

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Search user by username and log in.
        username = request.form.get('username')
        # Return the first user that matches the username.
        # If no matching username is found, return None.
        user = User.query.filter_by(username=username).first()
        if user:
            # The user was found and will be logged in.
            login_user(user)
            # A forwarding takes place.
            return redirect(url_for('index'))
    return render_template('indextwo.html')

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    print(f'{current_user.username} is logged in.')
    message = ()
    if request.method == 'POST':       
        msgval = request.form.get('msg')
        if msgval:
            message = client.messages.create(
            body = msgval,
            from_ = keyss.twillio_number,
            to = keyss.my_number
            )
        else:
            msgvall = request.form.get('exa')
            if msgvall:
                message = client.messages.create(
                body = msgvall,
                from_ = keyss.twillio_number,
                to = keyss.my_number
                )

    return render_template('index.html', content=message, name = current_user.username)

if __name__ == "__main__":
    app.run(debug=True)





