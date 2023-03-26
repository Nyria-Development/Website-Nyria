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
                my_guild = bearer_client.users.get_my_guilds()
                print(my_guild)
                return render_template("dashboard.html", user=current_user, year=current_year, guild=my_guild)
            return redirect("/login")

        @self.route("/test")
        def test():
            if "token" in session:
                current_year = datetime.date.today().year
                bearer_client = APIClient(session.get("token"), bearer=True)
                current_user = bearer_client.users.get_current_user()
                my_guild = bearer_client.users.get_my_guilds()
                return render_template("include.html", user=current_user, year=current_year, guild=my_guild)
            return redirect("/login")

        @self.route("/guild")
        def guild():
            if "token" in session:
                current_year = datetime.date.today().year
                bearer_client = APIClient(session.get("token"), bearer=True)
                current_user = bearer_client.users.get_current_user()
                guilds = bearer_client.users.get_my_guilds()
                return render_template("allGuilds.html", user=current_user, year=current_year, guild=guilds)
            return redirect("/login")

        @self.route("/guild/<guild_id>")
        def test_var(guild_id):
            if "token" in session:
                current_year = datetime.date.today().year
                bearer_client = APIClient(session.get("token"), bearer=True)
                current_user = bearer_client.users.get_current_user()
                guilds = bearer_client.users.get_my_guilds()
                my_guild = [guild for guild in guilds if guild.id == int(guild_id)][0]
                return render_template("guild.html", user=current_user, year=current_year, guild=my_guild)
            return redirect("/login")

        @self.route("/profile")
        def profile():
            if "token" in session:
                current_year = datetime.date.today().year
                bearer_client = APIClient(session.get("token"), bearer=True)
                current_user = bearer_client.users.get_current_user()
                my_guild = bearer_client.users.get_my_guilds()
                return render_template("profile.html", user=current_user, year=current_year, guild=my_guild)
            return redirect("/login")

        @self.route("/help")
        def help():
            if "token" in session:
                current_year = datetime.date.today().year
                bearer_client = APIClient(session.get("token"), bearer=True)
                current_user = bearer_client.users.get_current_user()
                my_guild = bearer_client.users.get_my_guilds()
                return render_template("help.html", user=current_user, year=current_year, guild=my_guild)
            return redirect("/login")

        @self.route("/command-list")
        def modules():
            if "token" in session:
                current_year = datetime.date.today().year
                bearer_client = APIClient(session.get("token"), bearer=True)
                current_user = bearer_client.users.get_current_user()
                my_guild = bearer_client.users.get_my_guilds()
                with open("static/files/commands.json", 'r') as f:
                    command_list = json.load(f)
                    list_of_modules = list({command['module']: command['module'] for command in command_list}.values())
                return render_template("modules.html", user=current_user, year=current_year, guild=my_guild, modules=list_of_modules)
            return redirect("/login")

        @self.route("/command-list/<module>")
        def commands(module):
            if "token" in session:
                current_year = datetime.date.today().year
                bearer_client = APIClient(session.get("token"), bearer=True)
                current_user = bearer_client.users.get_current_user()
                my_guild = bearer_client.users.get_my_guilds()
                with open("static/files/commands.json", 'r') as f:
                    command_list = json.load(f)
                    module_commands = [command for command in command_list if command['module'] == module]
                    print(module_commands)
                return render_template("commands.html", user=current_user, year=current_year, guild=my_guild,
                                       commands=module_commands, module=module)
            return redirect("/login")

        @self.route("/command-list/<module>/<command_name>")
        def command(module, command_name):
            if "token" in session:
                current_year = datetime.date.today().year
                bearer_client = APIClient(session.get("token"), bearer=True)
                current_user = bearer_client.users.get_current_user()
                my_guild = bearer_client.users.get_my_guilds()
                with open("static/files/commands.json", 'r') as f:
                    command_list = json.load(f)
                    command_dic = [command for command in command_list if command['command_name'] == command_name][0]
                    print(command_dic)
                return render_template("command.html", user=current_user, year=current_year, guild=my_guild,
                                       command=command_dic, module=module)
            return redirect("/login")

        @self.errorhandler(404)
        def page_not_found(error):
            return render_template('404.html'), 404


if __name__ == "__main__":
    WebsiteNyria().run(debug=True)
