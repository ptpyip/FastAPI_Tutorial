import psycopg

from psycopg.rows import dict_row
class PostDB:
    def __init__(self, db_type='Pg', connect_info=None) -> None:
        self.db = db_type
        self.connect2DB(connect_info=connect_info)
                
    def connect2DB(self, host=None, dbname=None, user=None, pwd=None, connect_info=None):
        if self.db == 'Pg':
            connect_succuss, connect_info = connect2PgDB(host, dbname,user, pwd, connect_info)
            if not connect_succuss: return False
            
            self.connect_info = connect_info
    
    def execute(self, query, params=None):
        if self.db == 'Pg':
            execute_success, results = executeWithPgDB(self.connect_info, query, params)
            return results
        

def connect2PgDB(host=None, dbname=None, user=None, password=None, connect_info=None):
    if connect_info == None:
        connect_info = f"host={host} dbname={dbname} user={user} password={password}"
        
    try:
        with psycopg.connect(connect_info, row_factory=dict_row) as conn: 
            print("success")
            return True, connect_info
    except Exception as e:
        print("Connection Failed")
        print(e)
        return False, None
        
def executeWithPgDB(connect_info, query, params=None):
    try:
        with psycopg.connect(connect_info, row_factory=dict_row) as conn: 
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                print("success")
                return True, cur.fetchall()
            
    except Exception as e:
        print("Connection Failed")
        print(e)
        return False, None
    
        

if __name__ == "__main__":
    postDB = PostDB()
    postDB.connect2DB(connect_info="host=localhost dbname=fastapiTut user=postgres password=1234")
    posts = postDB.execute("""
        SELECT * FROM "Posts"
    """)
    
    print(posts)
