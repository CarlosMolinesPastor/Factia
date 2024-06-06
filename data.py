import os
import sqlite3


# Si no existe la carpeta data, la crea
def data_path():
    if not os.path.exists("data"):
        os.makedirs("data")


# Si no existe la base de datos, la crea
def create_table():
    if os.path.exists("data/factia.db"):
        print("Table already exists")
        return
    else:
        conn = sqlite3.connect("data/factia.db")
        print("Database blank created")
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE product (id INTEGER PRIMARY KEY, "
            "nombre TEXT, "
            "categoria TEXT, "
            "fecha_compra TEXT, "
            "fecha_vencimiento_garantia TEXT, "
            "imagen TEXT)"
        )
        conn.commit()
        cur.close()


def create_category_table():
    if os.path.exists("data/categories.db"):
        print("Table already exists")
        return
    else:
        conn = sqlite3.connect("data/categories.db")
        print("Database blank created")
        cur = conn.cursor()
        cur.execute("CREATE TABLE category (id INTEGER PRIMARY KEY, " "category TEXT)")
        conn.commit()
        cur.close()


# Anade un producto a la base de datos
def add_product(nombre, categoria, fecha_compra, fecha_vencimiento_garantia, imagen):
    conn = sqlite3.connect("data/factia.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO product (nombre, categoria, fecha_compra, fecha_vencimiento_garantia, imagen) "
        "VALUES (?, ?, ?, ?, ?)",
        (nombre, categoria, fecha_compra, fecha_vencimiento_garantia, imagen),
    )
    conn.commit()
    print(
        "Anadido a la base de datos -> ",
        nombre,
        categoria,
        fecha_compra,
        fecha_vencimiento_garantia,
        imagen,
    )
    cur.close()


# Devuelve todos los productos de la base de datos
def get_all_products():
    if not os.path.exists("data/factia.db") or os.stat("data/factia.db").st_size == 0:
        return []
    else:
        conn = sqlite3.connect("data/factia.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM product")
        products = cur.fetchall()
        cur.close()
        return products


def add_category(category):
    conn = sqlite3.connect("data/categories.db")
    cur = conn.cursor()
    # Si no existe la categoria la añadimos a la base de datos
    if not cur.execute(
        "SELECT * FROM category WHERE category = ?", (category,)
    ).fetchall():
        cur.execute("INSERT INTO category (category) VALUES (?)", (category,))
        print("Añadimos categoria a la BD -> ", category)
        conn.commit()
    else:
        print("La categoria ya existe")
    cur.close()


def get_all_categories():
    if (
        not os.path.exists("data/categories.db")
        or os.stat("data/categories.db").st_size == 0
    ):
        return []
    else:
        conn = sqlite3.connect("data/categories.db")
        cur = conn.cursor()
        # Devuelve las categorias ordenadas alfabeticamente
        cur.execute("SELECT category FROM category ORDER BY category ASC")
        categories = cur.fetchall()
        cur.close()
        return categories
