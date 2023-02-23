from typing import Sequence, Any

from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session

from schemas import BaseSchema
from models import BaseModel

def createItem(table: BaseModel, item: BaseSchema, session:Session) -> BaseModel | None:
    if not session.is_active: return None
    
    try:
        return session.execute(
            insert(table).returning(table),
            [item.dict()]
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