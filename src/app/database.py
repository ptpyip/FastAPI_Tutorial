
import psycopg

from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import models as models

from psycopg.rows import dict_row

FASTAPI_TUT_DATABASE_URL = "postgresql://postgres:1234@localhost/fastapiTut"
USE_ORM = True

def getPostgresURL(dbms, postgresserver, dbname, user, pwd):
    return f"{dbms}://{user}:{pwd}@{postgresserver}/{dbname}"

class PostgresDB:
    connect_url:str
    
    def __init__(self, connect_url) -> None:
        self.connect_url = testConnection(connect_url=connect_url)
        if (self.connect_url == None): raise Exception
                
    
    def execute(self, query, params=None, fetching_all=True):
        try:
            with psycopg.connect(self.connect_url, row_factory=dict_row) as conn: 
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    results = cur.fetchall() if fetching_all else cur.fetchone()
                    conn.commit()   # commit changes
                    print("success")
            
            return results
                
        except Exception as e:
            print("Connection Failed")
            print(e)
            return None
    
def testConnection(connect_url):  
    try:
        with psycopg.connect(connect_url, row_factory=dict_row) as conn: 
            return connect_url
    except Exception as e:
        print("Connection Failed")
        print(e)
        return None

def connect():
    if not USE_ORM: 
        return PostgresDB(connect_url=FASTAPI_TUT_DATABASE_URL)
    engine = create_engine(
        url=FASTAPI_TUT_DATABASE_URL, echo=True
    )
    
    models.Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(engine, autoflush=False,autobegin=False)
    return SessionLocal()

if __name__ == "__main__":
    db = connect()
    # posts = db.execute("""
    #     SELECT * FROM "Posts"
    # """, fetching_all=False)
 
    posts = db.execute(
        select(models.Post)
    )
    print(posts)