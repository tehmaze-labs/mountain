# Import Flask functions
from flask import render_template

# Import other extensions
from flask_bootstrap import Bootstrap

# Import app
from .app import app

# Extensions
Bootstrap(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from mountain.rsyslog.views import mod_rsyslog

# Register blueprint(s)
app.register_blueprint(mod_rsyslog)
