
from typing import Any, Optional, Sequence

import psycopg
from psycopg import Cursor
from psycopg.rows import dict_row

from sqlalchemy import create_engine
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from config import USE_ORM
from schemas import BaseSchema
from models import BaseModel


def getPostgresURL(dbms, postgresserver, dbname, user, pwd):
    return f"{dbms}://{user}:{pwd}@{postgresserver}/{dbname}"

class Connection():
    
    def __init__(self, db_url, use_orm=USE_ORM) -> None:
        if not use_orm: 
            return
        
        engine = create_engine(
            url=db_url, echo=True
        )
        
        BaseModel.metadata.create_all(engine)
        
        self.SessionLocal = sessionmaker(engine, autobegin=False)
    
    def __call__(self):
        with self.SessionLocal() as db:
            with db.begin():
                yield db
                
class DeirectConnection(Connection):
    connect_url:str 
    
    def __init__(self, db_url) -> None:
        super().__init__(db_url, use_orm=False)
        self.db_url = self.testConnection(connect_url=db_url)
        
        if (self.connect_url == None): 
            raise Exception
         
    def __call__(self):
        with psycopg.connect(self.db_url, row_factory=dict_row) as conn: 
                with conn.cursor() as cur:
                    yield cur     
              
    def testConnection(connect_url):  
        try:
            with psycopg.connect(connect_url, row_factory=dict_row) as conn: 
                return connect_url
        except Exception as e:
            print("Connection Failed")
            print(e)
            return None
        

def execute(db: Session | Cursor, query, params=Optional[dict], fetching_all=True):
    try:
        if isinstance(db, Cursor):
            db.execute(query, tuple(params.values()))
            results = db.fetchall() if fetching_all else db.fetchone()
            
            return results
        
        elif isinstance(db, Session):
            reeults = db.execute(text(query).bindparams(params)).scalars()
            rows = reeults.all() if fetching_all else reeults.first()
            
            return rows
            
    except Exception as e:
        print("Connection Failed")
        print(e)
        return None
    
    
def createItem(table: BaseModel, item: dict, session:Session) -> BaseModel | None:
    if not session.is_active: return None
    
    try:
        return session.execute(
            insert(table).returning(table),
            [item]
        ).scalars().first()
    
    except Exception as e:
        print(e)
        return None

def readAllItem(table: BaseModel, session: Session) -> Sequence | None:
    try:
        results = session.execute(
            select(table).order_by(table.id)
        ).scalars().all()
        
        if len(results) == 0:
            return None
        else:
            return results
            
    except Exception as e:
        print(e)
        return None
    
def readItemById(table: BaseModel, item_id, session: Session)-> BaseModel | None:
    try:
        return session.execute(
            select(table).where(table.id == item_id)
        ).scalars().first()
        
    except Exception as e:
        print(e)
        return None
    
def updateItemById(table: BaseModel, item_id, set_values:dict, session: Session)-> BaseModel | None:
    try:
        return session.execute(
            update(table)
            .where(table.id == item_id)
            .values(set_values)
            .returning(table)
        ).scalars().first()
            
    except Exception as e:
        print(e)
        return None
    
def deleteItemById(table: BaseModel, item_id, session: Session)-> BaseModel | None:
    try:
        return session.execute(
            delete(table)
            .where(table.id == item_id)
            .returning(table)
        ).scalars().first()
            
    except Exception as e:
        print(e)
        return None
        
if __name__ == "__main__":
    # db = setConnection()
    # # posts = db.execute("""
    # #     SELECT * FROM "Posts"
    # # """, fetching_all=False)
 
    # posts = db.execute(
    #     select(models.Post)
    # )
    # print(posts)
    ...