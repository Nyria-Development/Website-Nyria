import json
import mysql.connector
from mysql.connector.errors import Error


class Check:
    def __init__(self):

        with open("config.json", "r") as c:
            self.__config = json.load(c)

        self.host, self.user, self.password, self.database = self.__config["mariadb"]["host"], self.__config["mariadb"]["user"], self.__config["mariadb"]["password"], self.__config["mariadb"]["database"]
        self.state_database: bool = False

    def inspect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
        except Error:
            raise Exception("Can't connect to database. Is your config right?")

        cursor = connection.cursor(prepared=True)
        cursor.execute("Show databases")
        databases = cursor.fetchall()

        for data in databases:
            if str(data[0]).lower() == "nyria":
                self.state_database = True
                print("Database faultless")
                connection.close()

        if not self.state_database:
            self.__create(connection=connection)

    @staticmethod
    def __create(connection: mysql.connector.MySQLConnection):
        cursor = connection.cursor()

        # create database Nyria
        cursor.execute("CREATE DATABASE Nyria")
        cursor.execute("USE Nyria")

        cursor.execute("CREATE TABLE bug_reports (userId BIGINT NOT NULL, reports INT NOT NULL)")
        cursor.execute("CREATE TABLE music (serverId BIGINT NOT NULL, tracksId INT NOT NULL, trackName TEXT NOT NULL)")
        cursor.execute("CREATE TABLE leveling (serverId BIGINT NOT NULL, levelSpeed INT NOT NULL)")
        cursor.execute("CREATE TABLE logs (serverId BIGINT NOT NULL, channelId BIGINT NOT NULL, log_active BIT NOT NULL, on_message BIT NOT NULL, on_reaction BIT NOT NULL, on_member_event BIT NOT NULL)")

        connection.commit()
        connection.close()
