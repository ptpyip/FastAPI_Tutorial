import psycopg

class PostDB:
    def __init__(self, db_type='Pg') -> None:
        self.db = db_type
                
    def connect2DB(self, host=None, dbname=None, user=None, pwd=None, connect_info=None):
        if self.db == 'Pg':
            connect_succuss, connect_info = connect2PgDB(host, dbname,user, pwd, connect_info)
            if not connect_succuss: return False
            
            self.connect_info = connect_info
    
    def execute(self, sql_cmd):
        if self.db == 'Pg':
            execute_success, results = executeWithPgDB(self.connect_info, sql_cmd)
            return results
        

def connect2PgDB(host=None, dbname=None, user=None, password=None, connect_info=None):
    if connect_info == None:
        connect_info = f"host={host} dbname={dbname} user={user} password={password}"
        
    try:
        with psycopg.connect(connect_info) as conn: 
            print("success")
            return True, connect_info
    except Exception as e:
        print("Connection Failed")
        print(e)
        return False, None
        
def executeWithPgDB(connect_info, cmd):
    try:
        with psycopg.connect(connect_info) as conn: 
            with conn.cursor() as cur:
                cur.execute(cmd)
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
