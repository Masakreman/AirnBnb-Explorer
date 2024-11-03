from flask import Flask

from blueprints.auth.auth import auth_bp
from blueprints.listings.listings import listings_bp
from blueprints.reviews.reviews import reviews_bp
from blueprints.geo.locations import locations_bp
from blueprints.users.users import users_bp
from blueprints.hosts.hosts import hosts_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(listings_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(locations_bp)
app.register_blueprint(users_bp)
app.register_blueprint(hosts_bp)

if __name__ == '__main__':
    app.run(debug=True)



