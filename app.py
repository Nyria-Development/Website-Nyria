from flask import Flask, render_template, request, session, redirect
from zenora import APIClient
import json
import datetime


class WebsiteNyria(Flask):
    def __init__(self):
        super().__init__(__name__)

        with open("config.json", "r") as c:
            self.__config = json.load(c)

            self.__token = self.__config["TOKEN"]
            self.__client_secret = self.__config["CLIENT_SECRET"]
            self.__redirect_url = self.__config["REDIRECT_URL"]
            self.__oauth_url = self.__config["OAUTH_URL"]
            self.__secret_key = self.__config["SECRET_KEY"]

        self.client = APIClient(token=self.__token, client_secret=self.__client_secret)
        self.config["SECRET_KEY"] = self.__secret_key

        @self.route("/")
        def index():
            return render_template("index.html")

        @self.route("/login")
        def login():
            return render_template("login.html", oauth_url=self.__oauth_url)

        @self.route("/logout")
        def logout():
            session.clear()
            return redirect("/")

        @self.route("/oauth/callback")
        def callback():
            code = request.args["code"]
            access_token = self.client.oauth.get_access_token(code, self.__redirect_url).access_token
            session["token"] = access_token
            return redirect("/dashboard")

        @self.route("/dashboard")
        def dashboard():
            if "token" in session:
                current_year = datetime.date.today().year
                bearer_client = APIClient(session.get("token"), bearer=True)
                current_user = bearer_client.users.get_current_user()
                return render_template("dashboard.html", user=current_user, year=current_year)
            return redirect("/login")

        @self.errorhandler(404)
        def page_not_found(error):
            return render_template('404.html'), 404


if __name__ == "__main__":
    WebsiteNyria().run(debug=True)
