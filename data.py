import os
import sqlite3

# Si no existe la carpeta data, la crea
def data_path():
    if not os.path.exists('data'):
        os.makedirs('data')

# Si no existe la base de datos, la crea
def create_table():
    if os.path.exists('data/factia.db'):
        print('Table already exists')
        return
    else:
        conn = sqlite3.connect('data/factia.db')
        print('Database blank created')
        cur = conn.cursor()
        cur.execute('CREATE TABLE product (id INTEGER PRIMARY KEY, '
                    'nombre TEXT, '
                    'categoria TEXT, '
                    'fecha_compra TEXT, '
                    'fecha_vencimiento_garantia TEXT, '
                    'imagen TEXT)')
        conn.commit()
        print('Table created')
        cur.close()


# Anade un producto a la base de datos
def add_product(nombre, categoria, fecha_compra, fecha_vencimiento_garantia, imagen):
    conn = sqlite3.connect('data/factia.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO product (nombre, categoria, fecha_compra, fecha_vencimiento_garantia, imagen) '
                'VALUES (?, ?, ?, ?, ?)', (nombre, categoria, fecha_compra, fecha_vencimiento_garantia, imagen))
    conn.commit()
    print('Anadido a la base de datos -> ', nombre, categoria, fecha_compra, fecha_vencimiento_garantia, imagen)
    cur.close()

# Devuelve todos los productos de la base de datos
def get_all_products():
    if not os.path.exists('data/factia.db') or os.stat('data/factia.db').st_size == 0:
        return []
    else:
        conn = sqlite3.connect('data/factia.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM product')
        products = cur.fetchall()
        cur.close()
        return products