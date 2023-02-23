from flask import Flask, render_template, request, session, redirect
import config
from zenora import APIClient


class WebsiteNyria(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.client = APIClient(token=config.TOKEN, client_secret=config.CLIENT_SECRET)
        self.config["SECRET_KEY"] = "secretkey"

        @self.route("/")
        def index():
            return render_template("index.html")

        @self.route("/login")
        def login():
            return render_template("login.html", oauth_url=config.OAUTH_URL)

        @self.route("/logout")
        def logout():
            session.clear()
            return redirect("/")

        @self.route("/oauth/callback")
        def callback():
            code = request.args["code"]
            access_token = self.client.oauth.get_access_token(code, config.REDIRECT_URL).access_token
            session["token"] = access_token
            return redirect("/dashboard")

        @self.route("/dashboard")
        def dashboard():
            if "token" in session:
                bearer_client = APIClient(session.get("token"), bearer=True)
                current_user = bearer_client.users.get_current_user()
                return render_template("dashboard.html", user=current_user)
            return redirect("/")

        @self.errorhandler(404)
        def page_not_found(error):
            return render_template('404.html'), 404


if __name__ == "__main__":
    WebsiteNyria().run(debug=True)
