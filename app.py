from flask import Flask, render_template, request, session, redirect
from zenora import APIClient
from database.check import Check
from database.loader import level
from database.loader import log
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
            self.bot_url = self.__config["BOT_URL"]
            self.__secret_key = self.__config["SECRET_KEY"]

            self.nyria_guilds = [1078731236098449408, 533319983388819467, 1043477521473212547] #später anpassen

        self.load_guild_database_info()

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

        @self.route("/guild", methods = ['GET', 'POST'])
        def guild():
            if "token" in session:
                current_year = datetime.date.today().year
                bearer_client = APIClient(session.get("token"), bearer=True)
                current_user = bearer_client.users.get_current_user()
                guilds = bearer_client.users.get_my_guilds()
                if request.method == 'POST':
                    post_requ = int(request.form['sb'])
                    if post_requ == 1:
                        new_guilds = [guild for guild in guilds if int(guild.permissions) == 35184372088831]
                        new_title = "Guilds, where you are admin"
                    elif post_requ == 2:
                        new_guilds = [guild for guild in guilds if guild.id in self.nyria_guilds]
                        new_title = "Guilds with Nyria Bot"
                    elif post_requ == 3:
                        new_guilds = [guild for guild in guilds if guild.id in self.nyria_guilds and guild.owner]
                        new_title = "Guilds, where you are admin and Nyria Bot"
                    else:
                        new_guilds=guilds
                        new_title = "All Guilds"
                    return render_template("allGuilds.html", user=current_user, year=current_year, guilds=new_guilds,
                                           title=new_title)
                return render_template("allGuilds.html", user=current_user, year=current_year, guilds=guilds, title="All Guilds")
            return redirect("/login")

        @self.route("/guild/<guild_id>")
        def test_var(guild_id):
            if "token" in session:
                self.load_guild_database_info()
                current_year = datetime.date.today().year
                bearer_client = APIClient(session.get("token"), bearer=True)
                current_user = bearer_client.users.get_current_user()
                guilds = bearer_client.users.get_my_guilds()
                my_guild = [guild for guild in guilds if guild.id == int(guild_id)][0]
                level_status = level.get_leveling_server(int(guild_id))
                log_info = log.get_log_info(int(guild_id))
                return render_template("guild.html", user=current_user, year=current_year, guild=my_guild,
                                       level_status=level_status, log_info=log_info, bot_url=self.bot_url,
                                       nyria_guild=[True if int(guild_id) in self.nyria_guilds else False][0])
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
                return render_template("modules.html", user=current_user, year=current_year, guild=my_guild,
                                       modules=list_of_modules)
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
                return render_template("command.html", user=current_user, year=current_year, guild=my_guild,
                                       command=command_dic, module=module)
            return redirect("/login")

        @self.errorhandler(404)
        def page_not_found(error):
            return render_template('404.html'), 404

    def load_guild_database_info(self):
        level.load_leveling_servers()
        log.load_log_channels()



if __name__ == "__main__":
    #Check for Database
    Check().inspect()
    #start the web-server
    WebsiteNyria().run(debug=True)
