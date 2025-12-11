from config.mysqlconnection import connectToMySQL

DB = "imagenes_db"

class Imagen:
    def __init__(self, data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.ruta = data['ruta']
        self.created_at = data['created_at']

    @classmethod
    def guardar(cls, data):
        query = """
        INSERT INTO imagenes (titulo, ruta)
        VALUES (%(titulo)s, %(ruta)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def obtener_todas(cls):
        query = "SELECT * FROM imagenes ORDER BY id DESC;"
        results = connectToMySQL(DB).query_db(query)
        return [cls(r) for r in results] if results else []
