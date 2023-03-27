from mysql.connector import pooling
import json


class Pool:
    def __init__(self, pool_name: str, pool_size: int):
        self.pool_name = pool_name
        self.pool_size = pool_size

        with open("config.json", "r") as c:
            self.__config = json.load(c)
        self.host, self.user, self.password, self.database = self.__config["mariadb"]["host"], self.__config["mariadb"]["user"], self.__config["mariadb"]["password"], self.__config["mariadb"]["database"]

    def create(self):
        connection_pool = pooling.MySQLConnectionPool(
            pool_size=self.pool_size,
            pool_name=self.pool_name,
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return connection_pool
