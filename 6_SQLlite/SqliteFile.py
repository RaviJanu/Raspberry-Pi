#!!AUM!!
import sqlite3
import time

#FPID integer,Name varchar(20),Age integer,Gender varchar(20),Addhar varchar(20),PAN varchar(20),Mobile varchar(15),Address varchar(20),VoteStatus integer

class sqlclass:
    def __init__(self,filename,tablename):
        self.filename = filename
        self.tablename = tablename
    def create_new(self,col_name_type):
        conn = sqlite3.connect(self.filename)
        print ('connect return : '+str(conn))
        conn.execute("CREATE TABLE "+self.tablename+"("+col_name_type+");")
        conn.commit()
        conn.close()

    def insert(self,dataarray):
        query = sqlite3.connect(self.filename)
        print ('query return : '+str(query))
        
        data_str = "'" + str(dataarray[0])
        for i in range(1, len(dataarray)):
            data_str = data_str + "','" + str(dataarray[i])
        data_str = data_str + "'"
        
        query.execute("INSERT INTO "+self.tablename+" VALUES("+data_str+")")      
        query.commit()
        query.close()

    def displayall(self,col_name):
        query = sqlite3.connect(self.filename)
        print ('query return : '+str(query))
        
        data_str = str(col_name[0])
        for i in range(1, len(col_name)):
            data_str = data_str + ", " + str(col_name[i])
        print data_str
        cursor = query.execute("SELECT "+data_str+" from "+self.tablename)
        print ('cursor return : '+str(cursor))
        print('=======================================================')
        for row in cursor:
            for i in range (0,len(col_name)):
                print col_name[i]+" = ", row[i]
            print "****\n****\n"
        print('=======================================================')
        query.close()
        
        
    def displayid(self,col_name,col_id):
        query = sqlite3.connect(self.filename)
        print ('query return : '+str(query))
        
        data_str = str(col_name[0])
        for i in range(1, len(col_name)):
            data_str = data_str + ", " + str(col_name[i])
        print data_str
        cursor = query.execute("SELECT "+data_str+" from "+self.tablename)
        print ('cursor return : '+str(cursor))

        return_list = range(len(col_name))
        print('=======================================================')
        for row in cursor:
            if row[0] == col_id:
                for i in range (0,len(col_name)):
                    print col_name[i]+" = ", row[i]
                    return_list[i] =  row[i]
                query.close()
                return return_list
        print('=======================================================')
        query.close()
        return 0


    def delet(self,col_name,delet_id):
        conn = sqlite3.connect(self.filename)
        print ('connect return : '+str(conn))
        conn.execute("DELETE from "+self.tablename+" where "+col_name+" = "+str(delet_id)+";")
        conn.commit()
        print "Total number of rows deleted :", connect.total_changes
        conn.close()

    def update(self,col_name,col_id,updateto,update_value):
        conn = sqlite3.connect(self.filename)
        conn.execute("UPDATE "+self.tablename+" set "+updateto+" = "+str(update_value)+" where "+col_name+" = "+str(col_id))
        conn.commit()
        print "Total number of rows updated :", conn.total_changes
        conn.close()

    def return_curser(self,col_name):
        query = sqlite3.connect(self.filename)
        data_str = str(col_name[0])
        for i in range(1, len(col_name)):
            data_str = data_str + ", " + str(col_name[i])
        print data_str
        cursor = query.execute("SELECT "+data_str+" from "+self.tablename)
        print ('cursor return : '+str(cursor))
        return query,cursor

    def close_comm(self,connection):
        connection.close()
        print 'connection closed'
        




        


if __name__ == "__main__":
    first = sqlclass('Firsttest.db','Test1')
    secound  = sqlclass('Firsttest.db','Test2')
    first.create_new('FPID integer,Name varchar(20),Age integer,Gender varchar(20),Addhar varchar(20),PAN varchar(20),Mobile varchar(15),Address varchar(20),VoteStatus integer')
    secound.create_new('FPID integer,Name varchar(20),Age integer,VoteStatus integer')
    first_data_list = [2,"Ravi",25,"Male","Addhar","PAN","9029690630","Goregaon",0]
    sec_data_list   = [1,"Janu",20,5]                      
    first.insert(first_data_list)
    secound.insert(sec_data_list)

    first_data_list = ['FPID','Name','Age','Gender','Addhar','PAN','Mobile','Address','VoteStatus']
    first.displayall(first_data_list)
    sec_data_list = ['FPID','Name','Age','VoteStatus']
    secound.displayall(sec_data_list)
    secound.update('FPID',5,'VoteStatus',2)
    list_print = secound.displayid(sec_data_list,1)
    print list_print

