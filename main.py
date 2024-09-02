################################
#
# #### #### #### ##### ### ####
# ##   #### #      #    #  ####
# #    #  # #      #    #  #  #
# #    #  # ####   #   ### #  #
#
# Importamos el modulo flet
import flet as ft

# Importamos datetime
import datetime

# Importamos el modulo producto
import producto as pr

# Importamos el modulo data de base de datos
import data as dt

# Importamos el modulo os
import os


# Función principal y le pasamos la pagina
def main(page: ft.Page):
    # Formateamos la pagina
    page.title = "Factia"
    page.padding = 32

    # Creamos las variables globales para después crear el objeto producto
    # Primero creamos un TextField con el valor 0 y lo alineamos al centro
    product_name = ft.TextField(
        label="Producto", border_color=ft.colors.RED_300, text_align=ft.TextAlign.CENTER
    )

    # ###### INCREMENTAR Y DECREMENTAR #######

    # Creamos un TextField con el valor 0 y lo alineamos al centro
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.CENTER, width=100)

    # Creamos dos funciones para incrementar y decrementar el contador del tiempo de garantía
    def increment(e):
        # sumamos 1 al valor del TextField
        txt_number.value = str(int(txt_number.value) + 1)  # type: ignore
        # Mostramos el valor del TextField
        print(f"increment {txt_number.value}")
        # Calculamos la fecha de garantía
        date_guarantee.value = calculate_guarantee_date().strftime("%d/%m/%Y")
        # Actualizamos la pagina
        page.update()

    def decrement(e):
        if int(txt_number.value) > 0:  # type: ignore
            txt_number.value = str(int(txt_number.value) - 1)  # type: ignore
            date_guarantee.value = calculate_guarantee_date().strftime("%d/%m/%Y")
        else:
            txt_number.value = "0"
        print(f"decrement {txt_number.value}")
        page.update()

    # ###### DATE PICKER #######

    # Creamos dos funciones para cambiar la fecha y para cerrar el date picker
    def change_date(e):
        # Impresiones de control
        print(f"Date picker changed, value is {date_picker_buy.value}")
        print(f"Date picker changed, value is {date_picker_init.value}")
        print(f"Date picker changed, value is {date_picker_finish.value}")
        # Si la fecha de inicio es distinta de None le asignamos el valor
        # al TextField de la fecha de inicio del date picker
        if date_buy.value:
            show_date.value = date_buy.value.strftime("%d/%m/%Y")
            date_guarantee.value = calculate_guarantee_date().strftime("%d/%m/%Y")
            # Impresion de control
            print(f"Date ,date buy value is {date_buy.value}")
            # Actualizamos la pagina
            page.update()
        if date_init.value:
            print(f"Date ,date init value is {date_init.value}")
            page.update()
        if date_finish.value:
            print(f"Date ,date finish value is {date_finish.value}")
            page.update()

    # Función para cerrar el date picker y le asignamos el valor
    def date_picker_dismissed(e):
        print("Date picker dismissed")

    # Creamos el date picker de la compra
    date_picker_buy = ft.DatePicker(
        # Si cambia la fecha le asignamos la funcion change_date
        on_change=change_date,
        # Si se cierra el date picker le asignamos la funcion date_picker_dismissed
        on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(2020, 10, 1),
        last_date=datetime.datetime(2050, 10, 1),
    )
    # Creamos el date picker de la compra
    date_picker_init = ft.DatePicker(
        # Si cambia la fecha le asignamos la funcion change_date
        on_change=change_date,
        # Si se cierra el date picker le asignamos la funcion date_picker_dismissed
        on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(2020, 10, 1),
        last_date=datetime.datetime(2050, 10, 1),
    )
    # Creamos el date picker de la compra
    date_picker_finish = ft.DatePicker(
        # Si cambia la fecha le asignamos la funcion change_date
        on_change=change_date,
        # Si se cierra el date picker le asignamos la funcion date_picker_dismissed
        on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(2020, 10, 1),
        last_date=datetime.datetime(2050, 10, 1),
    )

    # Creamos las variables para las fechas
    date_init = date_picker_init
    date_finish = date_picker_finish
    date_buy = date_picker_buy
    # Anadimos los DatePicker en forma overlay
    page.overlay.append(date_picker_init)
    page.overlay.append(date_picker_finish)
    page.overlay.append(date_picker_buy)

    # ###### CATEGORIAS #######

    # Funcion para cerrar la vista de la categoria
    def close_anchor(e):
        # Mostramos la categoria sin los parentesis y la coma,
        # es decir si la categoria es ('categoria',) la mostramos como categoria
        category = e.control.data
        print(f"closing view from {category}")
        anchor.close_view(category)
        anchor.value = category

    # Funcion para cambiar la categoria
    def handle_change(e):
        print(f"handle_change e.data: {e.data}")
        page.update()

    def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")

    def handle_tap(e):
        print("handle_tap")

    # Funcion para listar las categorias
    def list_category():
        # Obtenemos todas las categorias de la base de datos
        categories = dt.get_all_categories()
        print(categories)
        # Creamos una lista con las categorias
        lista = [i[0] for i in categories]
        print(lista)
        # Devolvemos la lista
        return lista

    # Funcion para añadir la categoria
    def add_category(category):
        # Añadimos la categoria a la base de datos
        dt.add_category(category)
        # Añadimos la categoria al anchor para actualizar la vista
        anchor.controls.append(
            ft.ListTile(
                title=ft.Text(category),
                on_click=close_anchor,
                data=(category),
            )
        )
        # Actualizamos el anchor\
        anchor.update()
        # Cerramos la vista de la categoria
        anchor.close_view(category)

    # Creamos un anchor para seleccionar la categoria
    anchor = ft.SearchBar(
        full_screen=True,
        view_trailing=[
            ft.FloatingActionButton(
                icon=ft.icons.ADD,
                bgcolor=ft.colors.RED_300,
                # Si clicamos en el boton añadimos la categoria
                on_click=lambda _: add_category(anchor.value),
            ),
        ],
        view_elevation=4,
        divider_color=ft.colors.RED_300,
        bar_hint_text="Elige Categoria...",
        view_hint_text="Elige una categortia de las indicadas...",
        # Si cambia la categoria le asignamos la funcion handle_change
        on_change=handle_change,
        # Si clicamos en el boton le asignamos la funcion handle_submit
        on_submit=handle_submit,
        # Si clicamos en la categoria le asignamos la funcion handle_tap
        on_tap=handle_tap,
        # Anadimos las categorias
        controls=[
            # Creamos una lista de categorias de la base de datos
            # y le asignamos la funcion close_anchor
            ft.ListTile(
                title=ft.Text(categoria),
                on_click=close_anchor,
                data=(categoria),
            )
            for categoria in list_category()
        ],
        value="",
    )

    # ###### RADIO BUTTON #######

    # Creamos un radio button con dos opciones para seleccionar los años o los meses
    radio_button = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio("Años", value="years"),
                ft.Radio("Meses", value="months"),
            ]
        )
    )

    def radio_change(e):
        if date_guarantee.value:
            date_guarantee.value = calculate_guarantee_date().strftime("%d/%m/%Y")
            page.update()
        print(f"radio_change {e.data}")
        print(f"radio_change {radio_button.value}")

    radio_button.on_change = radio_change

    # Creamos un TextField para mostrar la fecha de compra
    show_date = ft.TextField(
        label="Fecha de Compra",
        border_color=ft.colors.RED_300,
        text_align=ft.TextAlign.CENTER,
        width=200,
        read_only=True,
        value="",
    )

    # ####### ADD PRODUCT ########

    # Funcion para calcular la fecha de garantia
    def calculate_guarantee_date():
        if date_buy.value is None:
            return datetime.datetime.now()
        else:
            if radio_button.value == "years":
                return date_buy.value + datetime.timedelta(
                    days=int(txt_number.value) * 365  # type: ignore
                )
            else:
                return date_buy.value + datetime.timedelta(
                    days=int(txt_number.value) * 30  # type: ignore
                )

    # Creamos un TextField para mostrar la fecha de garantia
    date_guarantee = ft.TextField(
        label="Fecha de Garantia",
        border_color=ft.colors.RED_300,
        text_align=ft.TextAlign.CENTER,
        width=200,
        read_only=True,
        value="",
    )

    # Creamos un TextField para mostrar la fecha de garantia en formato iso
    date_guarantee_iso = ft.TextField(
        value="",
    )

    # Funcion para cambiar el formato de la fecha de garantia
    def change_date_guarantee_to_iso():
        date_guarantee_iso.value = calculate_guarantee_date().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    # Funcion de comprobacion: Si todo es correcto cambiamos el formato de la fecha de garantia
    # y devolvemos True
    def var_are_valid():
        if (
            product_name.value != ""
            and date_buy.value
            and date_guarantee.value
            and anchor.value != ""
        ):
            change_date_guarantee_to_iso()
            return True

    # Funcion para añadir el producto
    def add_product(e):
        # Validamos los campos
        if var_are_valid():
            print("Datos completos")
            # Creamos el objeto producto con los valores de los campos
            product = pr.Producto(
                product_name.value,
                anchor.value,
                date_buy.value,
                date_guarantee_iso.value,
                img.src,
            )
            # Imprimimos el objeto producto
            print(
                product.nombre,
                product.categoria,
                product.fecha_compra,
                product.fecha_vencimiento_garantia,
                product.imagen,
            )
            # Añadimos el producto a la base de datos
            dt.add_product(
                product.nombre,
                product.categoria,
                product.fecha_compra,
                product.fecha_vencimiento_garantia,
                img.src,
            )
            # Ponemos los campos a 0
            product_name.value = ""
            show_date.value = ""
            anchor.value = ""
            txt_number.value = "0"
            date_guarantee.value = ""
            remove_image(f"{selected_files.value}")
            img.src = "/icon.png"
            img.update()
            page.route = "/producto"
            # Actualizamos la pagina
            page.update()
        else:
            print("Faltan datos")
            page.update()

    ## Funcion para crear lista de productos
    def create_list_products():
        products = dt.get_all_products()
        # add ListView to a page first
        lv = ft.ListView(expand=1, spacing=10, item_extent=50, auto_scroll=True)
        for product in products:
            dt.convertToImage(product[5], f"assets/uploads/image_{product[0]}.jpg")
            lv.controls.append(
                ft.Container(
                    ft.Row(
                        [
                            ft.Text(
                                f"Num: {product[0]} \nProducto: {product[1]} \nCategoria: {product[2]} \nFecha Compra: {product[3]} \nFecha Garantia: {product[4]}",
                                color=ft.colors.WHITE,
                            ),
                            ft.Image(
                                src=f"assets/uploads/image_{product[0]}.jpg",
                                width=150,
                                height=150,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            ft.FloatingActionButton(
                                icon=ft.icons.DELETE,
                                bgcolor=ft.colors.WHITE,
                                on_click=lambda _: delete_product(product[0]),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    bgcolor=ft.colors.RED_300,
                    border=ft.border.all(1, ft.colors.RED_300),
                    border_radius=ft.border_radius.all(5),
                    # Al pulsar largo suprimimos el producto
                    # on_long_press=lambda _: dt.delete_product(product[0]),
                    on_long_press=lambda _: delete_product(product[0]),
                )
            )
            page.update()
            page.route = "/lista"
            page.update()
        return lv

    ## Funcion para borrar un producto

    def delete_product(e):
        open_dlg_eliminar()
        dt.delete_product(e)
        page.update()
        page.route = "/lista"
        page.update()
        page.route = "/"

    def close_dlg_eliminar(e):
        dlg_eliminar.open = False
        page.update()

    def open_dlg_eliminar():
        page.dialog = dlg_eliminar
        dlg_eliminar.open = True
        page.update()

    dlg_eliminar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Eliminar Producto"),
        content=ft.Text("Has eliminado el producto"),
        actions=[
            ft.TextButton(
                "Ok",
                on_click=close_dlg_eliminar,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=print("Dialog dismissed"),
    )

    ########### IMAGEN ###########

    ## Funcion para elegir la imagen del producto
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "assets/icon.png"
        )
        selected_files.update()
        upload_files(e)
        actualizar_imagen()

    def upload_files(e):
        uf = []
        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                uf.append(
                    ft.FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
            file_picker.upload(uf)

    file_picker = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(file_picker)
    selected_files = ft.Text()

    def remove_image(e):
        # Remove selected image in files picker
        os.remove(f"assets/uploads/{e}")

    # Imagen por defecto

    img = ft.Image(src=f"/icon.png", width=100, height=100, fit=ft.ImageFit.CONTAIN)

    def actualizar_imagen():
        img.src = f"assets/uploads/{selected_files.value}"
        img.update()
        page.update()

    # ####### ROUTE CHANGE ########
    def route_change(route):
        # Si la ruta es /producto añadimos la vista con el AppBar y un botón para volver a la vista anterior
        if not os.path.exists("data"):
            dt.data_path()
        dt.create_table()
        dt.create_category_table()
        # Borramos las vistas si hubiera alguna
        page.views.clear()
        # Cambiamos el tema de la pagina
        page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.RED_300))

        # #######  HOME ########

        # Anadimos la vista principal con la ruta slash y añadimos los controles de la pagina: un appbar
        # y dos botones elevados, uno para añadir productos y otro para buscar por fecha
        page.views.append(
            # Creamos la vista con la ruta slash
            ft.View(
                "/",
                # Añadimos los controles de la pagina
                [
                    ft.AppBar(
                        title=ft.Text("Factia"),
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.RED_300,
                    ),
                    ft.ElevatedButton(
                        "Anadir Producto",
                        bgcolor=ft.colors.RED_300,
                        color=ft.colors.WHITE,
                        on_click=lambda _: page.go("/producto"),
                    ),
                    ft.ElevatedButton(
                        "Lista de Productos",
                        bgcolor=ft.colors.RED_300,
                        color=ft.colors.WHITE,
                        on_click=lambda _: page.go("/lista"),
                    ),
                    ft.ElevatedButton(
                        "Busqueda por Fecha",
                        bgcolor=ft.colors.RED_300,
                        color=ft.colors.WHITE,
                        on_click=lambda _: page.go("/busqueda"),
                    ),
                ],
                # Alineamos los controles en el centro de la pagina
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=24,
            )
        )

        # ####### PRODUCTO ########
        # Si la ruta es /producto añadimos la vista con el AppBar y un botón para volver a la vista anterior
        if page.route == "/producto":
            # Al cargar la vista si el valor del radio_button es None le asignamos el valor "years"
            if radio_button.value is None:
                radio_button.value = "years"
            # Añadimos la vista con el AppBar y un botón para volver a la vista anterior
            page.views.append(
                ft.View(
                    "/producto",
                    [
                        ft.AppBar(
                            title=ft.Text("Añadir Producto"),
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.RED_300,
                            actions=[
                                ft.IconButton(
                                    ft.icons.CHECKLIST,
                                    on_click=lambda _: page.go("/lista"),
                                )
                            ],
                        ),
                        product_name,
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Fecha de Compra",
                                    bgcolor=ft.colors.RED_300,
                                    color=ft.colors.WHITE,
                                    icon=ft.icons.CALENDAR_MONTH,
                                    on_click=lambda _: date_buy.pick_date(),
                                ),
                                show_date,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        anchor,
                        ft.Text("Tiempo de Garantia:"),
                        ft.Row(
                            [
                                radio_button,
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            ft.icons.REMOVE,
                                            on_click=decrement,
                                        ),
                                        txt_number,
                                        ft.IconButton(
                                            ft.icons.ADD,
                                            on_click=increment,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                date_guarantee,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Imagen",
                                    icon=ft.icons.UPLOAD_FILE,
                                    on_click=lambda _: file_picker.pick_files(
                                        allow_multiple=False,
                                        allowed_extensions=["jpg"],
                                        dialog_title="Selecciona una imagen",
                                    ),
                                ),
                                # ft.ElevatedButton(
                                #     "Subir Imagen",
                                #     bgcolor=ft.colors.RED_300,
                                #     color=ft.colors.WHITE,
                                #     on_click=upload_files,
                                # ),
                                selected_files,
                                img,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.ElevatedButton(
                            "Añadir Producto",
                            bgcolor=ft.colors.RED_300,
                            color=ft.colors.WHITE,
                            on_click=add_product,
                        ),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=24,
                ),
            )
            page.update()

        # ####### BUSQUEDA ########
        # Si la ruta es /busqueda añadimos la vista con el AppBar y tres botones para
        # seleccionar fechas y volver a la vista anterio
        if page.route == "/busqueda":
            page.views.append(
                ft.View(
                    "/busqueda",
                    [
                        ft.AppBar(
                            title=ft.Text("Busqueda de productos"),
                            bgcolor=ft.colors.RED_300,
                            color=ft.colors.WHITE,
                        ),
                        ft.ElevatedButton(
                            "Selecciona fecha Primera",
                            bgcolor=ft.colors.RED_300,
                            color=ft.colors.WHITE,
                            icon=ft.icons.CALENDAR_MONTH,
                            on_click=lambda _: date_init.pick_date(),
                        ),
                        ft.ElevatedButton(
                            "Selecciona fecha Segunda",
                            bgcolor=ft.colors.RED_300,
                            color=ft.colors.WHITE,
                            icon=ft.icons.CALENDAR_MONTH,
                            on_click=lambda _: date_finish.pick_date(),
                        ),
                        ft.ElevatedButton(
                            "Go Home",
                            bgcolor=ft.colors.RED_300,
                            color=ft.colors.WHITE,
                            on_click=lambda _: page.go("/"),
                        ),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=24,
                )
            )

        if page.route == "/lista":
            page.views.append(
                ft.View(
                    "/lista",
                    [
                        ft.AppBar(
                            title=ft.Text("Lista de productos"),
                            bgcolor=ft.colors.RED_300,
                            color=ft.colors.WHITE,
                        ),
                        ft.ListTile(
                            title=ft.Text("Productos"),
                            on_click=lambda _: page.go("/producto"),
                        ),
                        create_list_products(),
                        ft.ElevatedButton(
                            "Go Home",
                            bgcolor=ft.colors.RED_300,
                            color=ft.colors.WHITE,
                            on_click=lambda _: page.go("/"),
                        ),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=24,
                )
            )
        page.update()

    # Funcion para volver a la vista anterior, anadimos la vista pop,
    # le decimos que la vista anterior sea la vista -1,
    # y le indicamos que vaya a la ruta
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Unimos los cambios con las funciones, es decir cuando cambia
    # la ruta le asignamos la funcion de route_change,
    # cuando queremos ir hacia atras la funcion view_pop,
    # y cuando clikamos nos desplazamos a la ruta
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


secret_key = os.getenv("FLET_SECRET_KEY", default=None)
if not secret_key:
    os.environ["FLET_SECRET_KEY"] = os.urandom(12).hex()

# Iniciamos la app
ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    assets_dir="assets",
    upload_dir="assets/uploads",
)
