from entities.User import User

class ModelUser():

    @classmethod
    def login(cls, db, username, password):

        try:
            cursor = db.connection.cursor()
            sql = 'SELECT * FROM users WHERE username = %s'

            cursor.execute(sql, (username,))
            row = cursor.fetchone()

            if row:
                id = row[0]
                username = row[1]
                password = User.check_password(row[2], password)

                user = User(id, username, password)

                return user
            else:
                return None

        except Exception as e:

            raise Exception(e)


    @classmethod
    def get_by_id(cls, db, id):

        try:
            cursor = db.connection.cursor()
            sql = 'SELECT id, username FROM users WHERE id = %s'

            cursor.execute(sql, (id,))
            row = cursor.fetchone()

            if row:
                id = row[0]
                username = row[1]

                logged_user = User(id, username, None)

                return logged_user
            else:
                return None

        except Exception as e:

            raise Exception(e)
    @classmethod
    def register(cls, db, username, password):

        hashed_pass = User.generate_hash(password)
        cursor = db.connection.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_pass))
        db.connection.commit()

    @classmethod
    def get_productos(cls, db):
        cursor = db.connection.cursor()
        cursor.execute('SELECT * from productos')
        data = cursor.fetchall()

        if data:
            return data
        else:
            return None
        
    @classmethod 
    def add_producto(cls,db, nombre, cantidad, precio, descripcion, foto ):

        cursor = db.connection.cursor()
        cursor.execute('INSERT INTO productos (nombre, foto, cantidad, precio, descripcion) VALUES (%s, %s, %s, %s, %s)', (nombre, foto, cantidad, precio, descripcion))
        db.connection.commit()

    @classmethod
    def delete_product(cls, db, id):

        cursor = db.connection.cursor()
        cursor.execute('DELETE FROM productos WHERE id = %s',(id,))
        db.connection.commit()
