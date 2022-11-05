try:
    import uuid

    from datetime import datetime
    import os
    import logging

    from functools import wraps
    from enum import Enum
    from abc import ABC, abstractmethod
    from logging import StreamHandler

    import psycopg2
    import psycopg2.extras as extras
    import sqlalchemy as db

    from faker import Faker

except Exception as e:
    raise Exception("Error : {}".format(e))

DATA = {
    "AURORA_DB_SERVER": "XXXXXX",
    "AURORA_DB_PORT": "5432",
    "AURORA_DB_UID": "XXXX",
    "AURORA_DB_PWD": "XXXX",
    "AURORA_DB_DATABASE": "postgres",
}
for key, value in DATA.items():
    os.environ[key] = value


class Logging(object):
    def __init__(self):
        format = "[%(asctime)s] %(name)s %(levelname)s %(message)s"
        # Logs to file
        logging.basicConfig(
            filename="logfile",
            filemode="a",
            format=format,
            level=logging.INFO,
        )
        self.logger = logging.getLogger("python")
        formatter = logging.Formatter(
            format,
        )
        # Logs to Console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)


global logger
logger = Logging()


def error_handling_with_logging(argument=None):
    def real_decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            function_name = function.__name__
            response = None
            try:
                if kwargs == {}:
                    response = function(self)
                else:
                    response = function(self, **kwargs)
            except Exception as e:
                response = {
                    "status": -1,
                    "error": {"message": str(e), "function_name": function.__name__},
                }
                logger.logger.info(response)
            return response

        return wrapper

    return real_decorator


class Settings(object):
    """settings class"""

    def __init__(
            self,
            port="",
            server="",
            username="",
            password="",
            timeout=100,
            database_name="",
            connection_string="",
            collection_name="",
            **kwargs,
    ):
        self.port = port
        self.server = server
        self.username = username
        self.password = password
        self.timeout = timeout
        self.database_name = database_name
        self.connection_string = connection_string
        self.collection_name = collection_name


class DatabaseAurora():
    """Aurora database class"""

    def __init__(self, data_base_settings):
        self.data_base_settings = data_base_settings
        self.client = psycopg2.connect(
            host=self.data_base_settings.server,
            port=self.data_base_settings.port,
            database=self.data_base_settings.database_name,
            user=self.data_base_settings.username,
            password=self.data_base_settings.password,
        )

    @error_handling_with_logging()
    def insert_many(self, query, data):
        self.query = query
        cursor = self.client.cursor()
        cursor.executemany(self.query, data)
        self.client.commit()
        cursor.close()
        return {"statusCode": 200, "data": True}

    @error_handling_with_logging()
    def insert_many_execute_batches(self, query, data):
        self.query = query
        cursor = self.client.cursor()
        extras.execute_batch(cursor, self.query, data)
        self.client.commit()
        cursor.close()
        return {"statusCode": 200, "data": True}


class DatabaseAuroraSqlAlchemy():
    """Aurora database class"""

    def __init__(self, data_base_settings):
        self.data_base_settings = data_base_settings
        self.client = db.create_engine(
            f'postgresql://{self.data_base_settings.username}:{self.data_base_settings.password}@{self.data_base_settings.server}:5432/{self.data_base_settings.database_name}')
        self.metadata = db.MetaData()

    @error_handling_with_logging()
    def insert_many(self, query, data):
        result = self.client.execute(query, data)
        return {"statusCode": 200, "data": True}


class Connector(Enum):
    DB_AURORA_PSYCOPG2 = DatabaseAurora(
        data_base_settings=Settings(
            port=os.getenv("AURORA_DB_PORT"),
            server=os.getenv("AURORA_DB_SERVER"),
            username=os.getenv("AURORA_DB_UID"),
            password=os.getenv("AURORA_DB_PWD"),
            database_name=os.getenv("AURORA_DB_DATABASE"),
        )
    )
    DB_AURORA_SqlAlchemy = DatabaseAuroraSqlAlchemy(
        data_base_settings=Settings(
            port=os.getenv("AURORA_DB_PORT"),
            server=os.getenv("AURORA_DB_SERVER"),
            username=os.getenv("AURORA_DB_UID"),
            password=os.getenv("AURORA_DB_PWD"),
            database_name=os.getenv("AURORA_DB_DATABASE"),
        ))


class DataGenerator(object):

    @staticmethod
    def get_data():
        faker = Faker()

        name = faker.name().split(" ")
        first_name = name[0]
        last_name = name[1]
        address = faker.address()
        text = faker.text()
        id = uuid.uuid4().__str__()
        city = faker.city()
        state = faker.state()

        _ = {
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "text": text,
            "id": id,
            "city": city,
            "state": state
        }
        return _


def main_psycopg2_executemany():
    helper = Connector.DB_AURORA_PSYCOPG2.value
    datagen_helper = DataGenerator()

    insert_many_batch_size = [100, 500, 1000, 10000, 30000, 50000]
    library_name = "psycopg2"
    method = "executemany"

    for batch in insert_many_batch_size:
        query = """INSERT INTO public.test 
                                    ( 
                                    first_name, 
                                    last_name,
                                    address,
                                    text,
                                    id,
                                    city,
                                    state
                                    ) 
                                VALUES (%s, %s, %s, %s, %s, %s,%s)"""

        values = [tuple(DataGenerator.get_data().values()) for i in range(0, batch)]

        start_time = datetime.now()
        logger.logger.info(" Library {} | Batch Size : {} | Start Time {} ".format(library_name, batch, start_time))

        response = helper.insert_many(query=query, data=values)

        end_time = datetime.now()
        logger.logger.info(" Library {} | Batch Size : {} | End Time {} ".format(library_name, batch, end_time))

        total_time = end_time - start_time

        logger.logger.info(f"""
        ---------------------------
                    Report
        ---------------------------
        
        Library                     : {library_name}
        Batch Size                  : {batch}
        Total Execution Time        : {total_time}
        Total Execution Time Sec    : {total_time.total_seconds()}
        Total Execution Time MS    : {total_time.total_seconds() * 1000}
        
        """)


def main_sqlalchemy_execute_many():
    helper = Connector.DB_AURORA_SqlAlchemy.value
    datagen_helper = DataGenerator()

    insert_many_batch_size = [100, 500, 1000, 10000, 30000, 50000]
    library_name = "sqlalchemy"
    method = "insert many"

    for batch in insert_many_batch_size:
        schema = db.Table(
            'test1',
            db.MetaData(),
            db.Column('first_name', db.String(255), nullable=False),
            db.Column('last_name', db.String(255), nullable=False),
            db.Column('address', db.String(255), nullable=False),
            db.Column('text', db.String(255), nullable=False),
            db.Column('id', db.String(255), nullable=False),
            db.Column('city', db.String(255), nullable=False),
            db.Column('state', db.String(255), nullable=False)
        )
        query = db.insert(schema)

        values = [tuple(DataGenerator.get_data().values()) for i in range(0, batch)]

        start_time = datetime.now()
        logger.logger.info(" Library {} | Batch Size : {} | Start Time {} ".format(library_name, batch, start_time))

        response = helper.insert_many(query=query, data=values)

        end_time = datetime.now()
        logger.logger.info(" Library {} | Batch Size : {} | End Time {} ".format(library_name, batch, end_time))

        total_time = end_time - start_time

        logger.logger.info(f"""
        ---------------------------
                    Report
        ---------------------------
        
        Library                     : {library_name}
        Batch Size                  : {batch}
        Total Execution Time        : {total_time}
        Total Execution Time Sec    : {total_time.total_seconds()}
        Total Execution Time MS    : {total_time.total_seconds() * 1000}
        
        """)


def main_psycopg2_execute_batches():
    helper = Connector.DB_AURORA_PSYCOPG2.value
    datagen_helper = DataGenerator()
    method = "execute_batch"

    insert_many_batch_size = [100, 500, 1000, 10000, 30000, 50000]
    library_name = "psycopg2"

    for batch in insert_many_batch_size:
        query = """INSERT INTO public.test 
                                    ( 
                                    first_name, 
                                    last_name,
                                    address,
                                    text,
                                    id,
                                    city,
                                    state
                                    ) 
                                VALUES (%s, %s, %s, %s, %s, %s,%s)"""

        values = [tuple(DataGenerator.get_data().values()) for i in range(0, batch)]

        start_time = datetime.now()
        logger.logger.info(" Library {} | Batch Size : {} | Start Time {} ".format(library_name, batch, start_time))

        response = helper.insert_many_execute_batches(query=query, data=values)

        end_time = datetime.now()
        logger.logger.info(" Library {} | Batch Size : {} | End Time {} ".format(library_name, batch, end_time))

        total_time = end_time - start_time

        logger.logger.info(f"""
        ---------------------------
                    Report
        ---------------------------
        
        Library                     : {library_name}
        method                      : {method}
        Batch Size                  : {batch}
        Total Execution Time        : {total_time}
        Total Execution Time Sec    : {total_time.total_seconds()}
        Total Execution Time MS    : {total_time.total_seconds() * 1000}
        
        """)


if __name__ == "__main__":
    pass

