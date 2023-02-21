from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

FASTAPI_TUT_DATABASE_URL = "postgresql://postgres:1234@localhost/fastapiTut"

"host=localhost dbname=fastapiTut user=postgres password=1234"
def getPostgresURL(dbms, postgresserver, dbname, user, pwd):
    return f"{dbms}://{user}:{pwd}@{postgresserver}/{dbname}"

def main():
    engine = create_engine(
        url=FASTAPI_TUT_DATABASE_URL, echo=True
    )
    
    SessionLocal = sessionmaker(engine, autoflush=False,autobegin=False)
    Base = declarative_base()