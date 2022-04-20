import psycopg2

##################################################   DATABASE CONFIG   ##################################################
db_config = {'host': 'localhost',
             'user': 'nick',   
             'password': 'Ff3#g127',
             'port': '5432',
             'database':'main_db'}


##################################################   CONTEXT MANAGER   #################################################
class DBContext_Manager: 
	"""Диспетчер контекста для подключения БД"""
	def __init__(self, config: dict) -> None:
		"""Инициализация атрибутов класса UseDatabase"""
		self.config = config # параметры соеденения с базой данных

	def __enter__(self) -> 'cursor':
		self.conn = psycopg2.connect(**self.config) 
		self.cursor = self.conn.cursor()
		return self.cursor

	def __exit__(self, exc_type, exc_value, exc_trace) -> None:
		self.conn.commit() # запись в БД всех значений присвоенных атрибутам
		self.cursor.close() # закрываем курсор
		self.conn.close() # закрываем соеденение


##################################################   DATABASE CONNECTION   #############################################
class Database:
	"""Инициализция инструмента для передачи запросов к БД, основной базывый класс"""
	def __init__(self, config=db_config, context_manager=DBContext_Manager):
		self.config = config # параметры подключения к БД
		self.context_manager = context_manager # менеджер контекста БД

##################################################   DATA DEFINITION   #################################################

	def create_food_types(self):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""CREATE TABLE IF NOT EXISTS food_types (id SERIAL NOT NULL PRIMARY KEY,
																     name_ru varchar(255),
																     name_en varchar(255),
																     name_ch varchar(255),
																     order_id INT
																     )""")

	def create_foods(self):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""CREATE TABLE IF NOT EXISTS foods (id SERIAL NOT NULL PRIMARY KEY,
																internal_code INT,
																code INT,
																name_ru VARCHAR(255),
																description_ru VARCHAR(255),
																description_en VARCHAR(255),
																description_ch VARCHAR(255),
																is_vegan BOOLEAN,
																is_special BOOLEAN,
																is_publish BOOLEAN,
																cost FLOAT
																)""")

	def create_food_types_foods(self):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""CREATE TABLE IF NOT EXISTS food_types_foods (id SERIAL NOT NULL PRIMARY KEY,
																   	       food_type_id INT NOT NULL,
																   	       food_id INT NOT NULL,
																           FOREIGN KEY(food_type_id)
																               REFERENCES food_types(id)
																 	               ON DELETE CASCADE
																 	               ON UPDATE CASCADE,
																           FOREIGN KEY(food_id)
																               REFERENCES foods(id)
																 	               ON DELETE CASCADE
																 	               ON UPDATE CASCADE
																           )""")

	def create_all_tables(self):
		self.create_food_types()
		self.create_foods()
		self.create_food_types_foods()



##################################################   DATA MANIPULATION   ###############################################
	def insert_test_data(self):
		with self.context_manager(self.config) as cursor:
			# add food types
			food_types = ['Напитки', 'Выпечка', 'Категория1', 'Категория2']
			food_type_ids = {}
			for i, v in enumerate(food_types):
				cursor.execute("""INSERT INTO food_types (name_ru, name_en, name_ch, order_id) 
								  VALUES (%s, %s, %s, %s)""",
								  (v, None, None, 10*(i+1)))
				cursor.execute("""SELECT max(id) FROM food_types""")
				food_type_id =  cursor.fetchall()[0][0]
				food_type_ids[v] = food_type_id

			# add foods
			drinks = ['Чай', 'Кола', 'Спрайт', 'Байкал']
			bakery = ['bakery_name1', 'bakery_name2', 'bakery_name3']
			for i, v in enumerate(drinks + bakery):
				is_publish = False
				if i % 2 == 0:
					is_publish = True
				cursor.execute("""INSERT INTO foods 
				(internal_code, code, name_ru, description_ru, description_en, description_ch, is_vegan,
                 is_special, is_publish, cost) 
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
					((i+1)*100, i+1, v, v, None, None, False, False, is_publish, 123.00))
				cursor.execute("""SELECT max(id) FROM foods""")
				food_id =  cursor.fetchall()[0][0]

				# set connection
				if v in drinks:
					food_type_id = food_type_ids['Напитки']
					cursor.execute("""INSERT INTO food_types_foods (food_type_id, food_id)
									  VALUES (%s, %s)""", (food_type_id, food_id))
				elif v in bakery:
					food_type_id = food_type_ids['Выпечка']
					cursor.execute("""INSERT INTO food_types_foods (food_type_id, food_id)
									  VALUES (%s, %s)""", (food_type_id, food_id))


	def get_food_types(self):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT * FROM food_types""")
			return cursor.fetchall()

	def get_foods_by_food_type_id(self, food_type_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT f.id, f.internal_code, f.code, f.name_ru, f.description_ru, f.description_en, 
			f.description_ch, f.is_vegan, f.is_special, f.is_publish, f.cost
							  FROM foods AS f
							  JOIN food_types_foods AS ftf
							  ON f.id = ftf.food_id
							  WHERE ftf.food_type_id=%s""", (food_type_id,))
			return cursor.fetchall()



db = Database()

if __name__ == '__main__':
	...
	# db.create_all_tables()
	# db.insert_test_data()
	print(db.get_foods_by_food_type_id(25))




