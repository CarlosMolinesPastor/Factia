import os
import sqlite3
from PIL import Image


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, "rb") as file:
        blobData = file.read()
    return blobData


# Convierte el binario a imagen
def convertToImage(data, filename):
    # Convert binary data to proper image
    with open(filename, "wb") as file:
        file.write(data)
    img = Image.open(filename)
    print(img)


# Si no existe la carpeta data, la crea
def data_path():
    if not os.path.exists("data"):
        os.makedirs("data")


# Si no existe la base de datos, la crea
def create_table():
    if os.path.exists("data/factia.db"):
        print("Table factia already exists")
        return
    else:
        # si no existe la base de datos la crea
        conexion = sqlite3.connect("data/factia.db")
        print("Database blank created")
        # Creamos el cursor para poder ejecutar las sentenciaqs sql
        cursor = conexion.cursor()
        # Creamos la tabla product con los campos id, nombre, categoria, fecha_compra, fecha_vencimiento_garantia
        cursor.execute(
            "CREATE TABLE product (id INTEGER PRIMARY KEY, "
            "nombre TEXT, "
            "categoria TEXT, "
            "fecha_compra TEXT, "
            "fecha_vencimiento_garantia TEXT, "
            "imagen BLOB)"
        )
        # Guardamos los cambios
        conexion.commit()
        # Cerramos el cursor
        cursor.close()


def create_category_table():
    if os.path.exists("data/categories.db"):
        print("Table categories already exists")
        return
    else:
        conexion = sqlite3.connect("data/categories.db")
        print("Base de datos creada categories.db")
        cursor = conexion.cursor()
        cursor.execute(
            "CREATE TABLE category (id INTEGER PRIMARY KEY, " "category TEXT)"
        )
        conexion.commit()
        cursor.close()


# Anade un producto a la base de datos
def add_product(nombre, categoria, fecha_compra, fecha_vencimiento_garantia, imagen):
    conexion = sqlite3.connect("data/factia.db")
    cursor = conexion.cursor()
    # Conertimos la imagen a binario para introducirla en la base de datos
    print("Imagen: ", imagen)
    image = convertToBinaryData(imagen)
    cursor.execute(
        "INSERT INTO product (nombre, categoria, fecha_compra, fecha_vencimiento_garantia, imagen) "
        "VALUES (?, ?, ?, ?, ?)",
        (nombre, categoria, fecha_compra, fecha_vencimiento_garantia, image),
    )
    conexion.commit()
    print(
        "Anadido a la base de datos -> ",
        nombre,
        categoria,
        fecha_compra,
        fecha_vencimiento_garantia,
        imagen,
    )
    cursor.close()


# Devuelve todos los productos de la base de datos
def get_all_products():
    if not os.path.exists("data/factia.db") or os.stat("data/factia.db").st_size == 0:
        return []
    else:
        conexion = sqlite3.connect("data/factia.db")
        cursor = conexion.cursor()
        query = "SELECT * FROM product"
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            print("Id: ", row[0])
            print("Nombre: ", row[1])
            print("Categoria: ", row[2])
            print("Fecha de compra: ", row[3])
            print("Fecha de vencimiento de la garantia: ", row[4])
            # convertToImage(row[5], f"data/image_{row[5]}.jpg")
            # print("Imagen: ", img)
        cursor.close()
        return records


# Añadir una categoria
def add_category(category):
    conexion = sqlite3.connect("data/categories.db")
    cursor = conexion.cursor()
    # Si no existe la categoria la añadimos a la base de datos
    if not cursor.execute(
        "SELECT * FROM category WHERE category = ?", (category,)
    ).fetchall():
        cursor.execute("INSERT INTO category (category) VALUES (?)", (category,))
        print("Añadimos categoria a la BD -> ", category)
        conexion.commit()
    else:
        print("La categoria ya existe")
    cursor.close()


def get_all_categories():
    if (
        not os.path.exists("data/categories.db")
        or os.stat("data/categories.db").st_size == 0
    ):
        return []
    else:
        conexion = sqlite3.connect("data/categories.db")
        cursor = conexion.cursor()
        # Devuelve las categorias ordenadas alfabeticamente
        cursor.execute("SELECT category FROM category ORDER BY category ASC")
        categories = cursor.fetchall()
        cursor.close()
        return categories


def delete_product(id):
    conexion = sqlite3.connect("data/factia.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM product WHERE id = ?", (id,))
    conexion.commit()
    cursor.close()
    print("Producto eliminado de la base de datos -> ", id)
