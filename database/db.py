import sqlite3

class Database:


	def __init__(self,db_name,table=None):
		self.db_name = db_name
		self.db = sqlite3.connect(db_name)
		self.db_table = table


	#Add table
	def add_table(self,table_name):

            self.db.execute("""
                        CREATE TABLE IF NOT EXISTS {} (
                        commentId VARCHAR PRIMARY KEY,
                        text TEXT,
                        time DATE,
                        likeCount INT,
                        author VARCHAR,
                        channel VARCHAR,
                        authorIsChannelOwner BOOLEAN);""".format(table_name))


    #Insert from a df
	def insert(self,table_name,data):
            for i,row in data.iterrows():
                self.db.execute("INSERT INTO " + table_name + " (commentId,text,time,likeCount,author,channel,authorIsChannelOwner) VALUES (?,?,?,?,?,?,?)",(row.commentId,row.text, row.time, row.likeCount,row.author,row.channel,row.authorIsChannelOwner))
            self.db.commit()


    #drop table
	def drop_table(self,table_name):
		self.db.execute("DROP TABLE {}".format(table_name))
		self.db.commit()


	#get items from db
	#first argument is table name
	#second argument is condition
    # third argument is the query
	def get_items(self,table_name, statement=None, query=None):
			self.items = self.db.execute("SELECT * FROM {} {}{}".format(table_name, statement, query))
			return list(self.items)

	#return list of tables
	def get_tables(self):
		self.tables = self.db.execute("SELECT name FROM sqlite_master")
		return list(self.tables)

	#execute sqlite query's
	def query(self,query_string):
		self.db.execute(query_string);
		self.db.commit()

	#close database connection
	def close_connection(self):
		self.db.close()
