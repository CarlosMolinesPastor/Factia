import flet as ft

# Importamos datetime
import datetime


# Funcion principal y le pasamos la pagina
def main(page: ft.Page):
    # Formateamos la pagina
    page.title = "Factia"
    page.padding = 32

    # Creamos las variables globales para despues crear el objeto producto
    # Primero creamos un TextField con el valor 0 y lo alineamos al centro
    product_name = ft.TextField(
        label="Producto",
        border_color=ft.colors.RED_300,
        text_align=ft.TextAlign.CENTER,
    )

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.CENTER, width=100)

    # Creamos dos funciones para incrementar y decrementar el contador
    def increment(e):
        txt_number.value = str(int(txt_number.value) + 1)
        print(f"increment {txt_number.value}")
        page.update()

    def decrement(e):
        if int(txt_number.value) > 0:
            txt_number.value = str(int(txt_number.value) - 1)
        else:
            txt_number.value = "0"
        print(f"decrement {txt_number.value}")
        page.update()

    # ###### DATE PICKER #######
    # Creamos dos funciones para cambiar la fecha y para cerrar el date picker
    def change_date(e):
        # Impresiones de control
        print(f"Date picker changed, value is {date_picker.value}")
        print(f"Date picker changed, value is {date_init.value.year}")
        # Si la fecha de inicio es distinta de None le asignamos el valor
        # al TextField de la fecha de inicio del date picker
        if date_buy.value:
            showDate.value = date_buy.value.strftime("%d/%m/%Y")
            # Impresion de control
            print(f"Date ,date buy value is {date_buy.value}")
            # Actualizamos la pagina
            page.update()

    # Funcion para cerrar el date picker y le asignamos el valor
    def date_picker_dismissed(e):
        print(f"Date picker dismissed, value is {date_picker.value}")

    # Creamos el date picker con las fechas de inicio y fin
    date_picker = ft.DatePicker(
        # Si cambia la fecha le asignamos la funcion change_date
        on_change=change_date,
        # Si se cierra el date picker le asignamos la funcion date_picker_dismissed
        on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(2020, 10, 1),
        last_date=datetime.datetime(2050, 10, 1),
    )
    # Creamos las variables para las fechas
    date_init = date_picker
    date_finish = date_picker
    date_buy = date_picker
    # Anadimos los DatePicker en forma overlay
    page.overlay.append(date_picker)

    # ###### ANCHOR #######
    def close_anchor(e):
        category = f"Category{e.control.data}"
        print(f"closing view from {category}")
        anchor.close_view(category)

    def handle_change(e):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")

    def handle_tap(e):
        print(f"handle_tap")

    # Creamos un anchor para seleccionar la categoria
    anchor = ft.SearchBar(
        full_screen=True,
        view_trailing=[
            ft.FloatingActionButton(
                icon=ft.icons.ADD,
                bgcolor=ft.colors.RED_300,
                on_click=lambda _: anchor.close_view(),
            ),
        ],
        view_elevation=4,
        divider_color=ft.colors.RED_300,
        bar_hint_text="Elige Categoria...",
        view_hint_text="Elige una categortia de las indicadas...",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=[
            ft.ListTile(title=ft.Text(f"Categoria {i}"), on_click=close_anchor, data=i)
            for i in range(10)
        ],
    )

    radio_button = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio("Años", value="years"),
                ft.Radio("Meses", value="months"),
            ]
        )
    )

    def radio_change(e):
        print(f"radio_change {e.data}")
        print(f"radio_change {radio_button.value}")

    radio_button.on_change = radio_change

    show_date = ft.TextField(
        label="Fecha de Compra",
        border_color=ft.colors.RED_300,
        text_align=ft.TextAlign.CENTER,
        width=200,
        read_only=True,
        value="",
    )

    # ####### ROUTE CHANGE ########
    def route_change(route):
        # Borramos las vistas si hubiera alguna
        page.views.clear()

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
                    ft.AppBar(title=ft.Text("Factia"), bgcolor=ft.colors.RED_300),
                    ft.ElevatedButton(
                        "Anadir Producto",
                        bgcolor=ft.colors.RED_300,
                        color=ft.colors.WHITE,
                        on_click=lambda _: page.go("/producto"),
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
                            title=ft.Text("Añadir Producto"), bgcolor=ft.colors.RED_300
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
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
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


# Iniciamos la app
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
