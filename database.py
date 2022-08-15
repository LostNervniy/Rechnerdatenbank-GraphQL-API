from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import scoped_session, sessionmaker

connection_string = 'postgresql+psycopg2://[USERNAME]:[PASSWORD]@[IP]:[PORT]/[SCHEMA]'
engine = create_engine(connection_string)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


Base = declarative_base(cls=DeferredReflection)
Base.query = db_session.query_property()

print("Hello from database.py")
