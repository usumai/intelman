from flask import Blueprint, render_template, request, redirect, url_for, session, flash

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'dlpeye':
            session['logged_in'] = True
            # Redirect to home page (or the original destination if desired)
            return redirect(url_for('pages.home'))
        else:
            flash('Incorrect password. Please try again.')
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login.login'))
