import logging
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
## save in file
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler = logging.FileHandler('app.log')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)


# save in db
# create handler
Base = declarative_base()
engine = create_engine('sqlite:///Log.db', echo=True)


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_time = Column(DateTime, default=datetime.datetime.now())
    level_log = Column(String(50))
    message = Column(String(255))


class SQLAlchemyHandler(logging.Handler):
    def __init__(self, engine):
        logging.Handler.__init__(self)
        self.Session = sessionmaker(bind=engine)

    def emit(self, record):
        # insert data in DB
        session = self.Session()
        try:
            log = Log(level_log=record.levelname, message=record.msg)
            session.add(log)
            session.commit()
        except:
            self.handleError(record)
        finally:
            session.close()


db_handler = SQLAlchemyHandler(engine)
db_handler.setLevel(logging.DEBUG)
logger.addHandler(db_handler)


