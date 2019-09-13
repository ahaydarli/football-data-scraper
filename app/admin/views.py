from flask import abort, render_template
from flask_login import current_user, login_required

from app import app
from app.models import User

@app.route('/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_authenticated:
        abort(403)
    return render_template('/admin/dashboard.html', title='Dashboard')

@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('/admin/users.html', title='Users', users=users)