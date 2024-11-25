from myproject import app,db,serve_data

from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user

from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out!')
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    print('form')
    if request.method == "POST":
        if form.validate_on_submit():
            # Grab the user from our User Models table
            user = User.query.filter_by(email=form.email.data).first()
            
            if user.check_password(form.password.data) and user is not None:
                #Log in the user
                login_user(user)
                flash('Logged in successfully.')

                # If a user was trying to visit a page that requires a login
                # flask saves that URL as 'next'.
                next = request.args.get('next')

                # So let's now check if that next exists, otherwise we'll go to
                # the welcome page.
                if next == None or not next[0]=='/':
                    next = url_for('welcome_user')

                return redirect(next)
            else:
                print('Smth went wrong on checking password and user existance in db')
        else:
            print("Something went wrong. Validation not passed")   
            # Check that the user was supplied and the password is right
            # The verify_password method comes from the User object
            # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

            
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        try:
            User.check_username()
        except:
            flash('Username already exists in database. Try different username.')

        try: 
            User.check_email()
        except:
            flash('Email adress already exists in database. Try different email.')        
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    else:
        print('Something went wrong on registration')
    return render_template('register.html', form=form)


@app.route('/graph', methods=['GET'])
def graph():
    script, div = serve_data.provide_basic_plot()
    return render_template('graph.html',script=script, div = div)





if __name__=='__main__':
    app.run(debug=True, port = 5050)