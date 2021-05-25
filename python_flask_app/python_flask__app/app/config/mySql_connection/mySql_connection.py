import pymysql

class mysqlbase(object):    
    def __init__(self):
        print("init()")
        self.error=""
        self.status=0
    
    def Connect(self, strhost, struser, strpasswd, strdb, nport=3306):
        try:
            self.db = pymysql.connect(user=struser, passwd=strpasswd, host=strhost, db=strdb, port=nport, charset="utf8", init_command="set names utf8")                
            self.rs = self.db.cursor()
            self.status=1
            
            return True
        except Exception as e:
            self.error="Error: %s" % (e)
        except:
            self.error="Error desconocido"
        return False        
    
    def Exec(self, strsql, retrs=True):
        if self.status==1:            
            self.error=""
            try:
                print(strsql)
                self.rs.execute(strsql)
                self.db.commit()                
                if retrs:
                    result = []
                    data = self.rs.fetchone()                    
                    while (data != None):
                        result.append(data)
                        data = self.rs.fetchone()
                    return True, result
                return True, None
            except Exception as e:
                self.error="Error: %s" % (e)
        return False, None
        
    def Close(self):
        self.status=0
        try:
            self.rs.close()
        except:pass
        try:
            self.db.close()
        except:pass
 
    def getState(self):
        return self.status
    
    def getError(self):
        return self.error
       
    def getCount(self):
        if self.status:
            return self.rs.rowcount
        else:
            return -1