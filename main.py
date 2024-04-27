import flet as ft

# Importamos de flet para no tener que utilizar ft.
from flet import *

# Importamos datetime
import datetime


def main(page: Page):
    page.title = "Factia"
    page.padding = 32

    # Creamos una funcion para incrementar y decrementar el contador
    # Primero creamos un TextField con el valor 0 y lo alineamos al centro
    txt_number = TextField(value="0", text_align=TextAlign.CENTER, width=100)

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

    ####### DATE PICKER #######
    # Creamos dos funciones para cambiar la fecha y para cerrar el date picker
    def change_date(e):
        print(f"Date picker changed, value is {date_picker.value}")
        print(f"Date picker changed, value is {date_init.value.year}")
        if date_buy.value:
            tb.value = date_buy.value.strftime("%d/%m/%Y")
            print(f"Date ,date buy value is {date_buy.value}")
            page.update()

    def date_picker_dismissed(e):
        print(f"Date picker dismissed, value is {date_picker.value}")

    # Creamos el date picker con las fechas de inicio y fin
    date_picker = DatePicker(
        on_change=change_date,
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

    ####### ANCHOR #######
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
    anchor = SearchBar(
        full_screen=True,
        view_trailing=[
            FloatingActionButton(icon=icons.ADD, bgcolor=colors.RED_300, on_click=lambda _: anchor.close_view()),
        ],
        view_elevation=4,
        divider_color=colors.RED_300,
        bar_hint_text="Elige Categoria...",
        view_hint_text="Elige una categortia de las indicadas...",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=[
            ListTile(title=Text(f"Categoria {i}"), on_click=close_anchor, data=i)
            for i in range(10)
        ],
    )

    radio_button = RadioGroup(content=Column([
        Radio("Años", value="years"),
        Radio("Meses", value="months"),
    ]))

    def radio_change(e):
        print(f"radio_change {e.data}")
        print(f"radio_change {radio_button.value}")

    radio_button.on_change = radio_change

    tb = TextField(
        label="Fecha de Compra",
        border_color=colors.RED_300,
        text_align=TextAlign.CENTER,
        width=200,
        read_only=True,
        value="")

    ######## ROUTE CHANGE ########
    def route_change(route):
        # Borramos las vistas si hubiera alguna
        page.views.clear()

        page.theme = Theme(
            color_scheme=ColorScheme(
                primary=colors.RED_300)
        )

        ########  HOME ########
        # Anadimos la vista principal con la ruta slash y añadimos los controles de la pagina: un appbar
        # y dos botones elevados, uno para añadir productos y otro para buscar por fecha
        page.views.append(
            # Creamos la vista con la ruta slash
            View(
                "/",
                # Añadimos los controles de la pagina
                [
                    AppBar(title=Text("Factia"), bgcolor=colors.RED_300),
                    ElevatedButton(
                        "Anadir Producto",
                        bgcolor=colors.RED_300,
                        color=colors.WHITE,
                        on_click=lambda _: page.go("/producto"),
                    ),
                    ElevatedButton(
                        "Busqueda por Fecha",
                        bgcolor=colors.RED_300,
                        color=colors.WHITE,
                        on_click=lambda _: page.go("/busqueda"),
                    ),
                ],
                # Alineamos los controles en el centro de la pagina
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=24,
            )
        )
        ######## PRODUCTO ########
        # Si la ruta es /producto añadimos la vista con el AppBar y un botón para volver a la vista anterior
        if page.route == "/producto":
            # Al cargar la vista si el valor del radio_button es None le asignamos el valor "years"
            if radio_button.value is None:
                radio_button.value = "years"
            # Añadimos la vista con el AppBar y un botón para volver a la vista anterior
            page.views.append(
                View(
                    "/producto",
                    [
                        AppBar(title=Text("Añadir Producto"), bgcolor=colors.RED_300),
                        product_name := TextField(label="Producto", border_color=colors.RED_300,
                                                  text_align=TextAlign.CENTER, ),
                        Row([
                            ElevatedButton(
                                "Fecha de Compra",
                                bgcolor=colors.RED_300,
                                color=colors.WHITE,
                                icon=icons.CALENDAR_MONTH,
                                on_click=lambda _: date_buy.pick_date(),
                            ),
                            tb
                        ], alignment=MainAxisAlignment.CENTER,
                        ),

                        anchor,
                        Text("Tiempo de Garantia:"),
                        Row([
                            radio_button,
                            Row(
                                [
                                    IconButton(
                                        icons.REMOVE, on_click=decrement,
                                    ),
                                    txt_number,
                                    IconButton(
                                        icons.ADD, on_click=increment,
                                    ),
                                ],
                                alignment=MainAxisAlignment.CENTER,
                            ),
                        ],
                            alignment=MainAxisAlignment.CENTER
                        ),

                        ElevatedButton(
                            "Go Home",
                            bgcolor=colors.RED_300,
                            color=colors.WHITE,
                            on_click=lambda _: page.go("/"),
                        ),
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=24,
                )
            )
        # ####### BUSQUEDA ########
        # Si la ruta es /busqueda añadimos la vista con el AppBar y tres botones para
        # seleccionar fechas y volver a la vista anterio
        if page.route == "/busqueda":
            page.views.append(
                View(
                    "/busqueda",
                    [
                        AppBar(
                            title=Text("Busqueda de productos"), bgcolor=colors.RED_300
                        ),
                        ElevatedButton(
                            "Selecciona fecha Primera",
                            bgcolor=colors.RED_300,
                            color=colors.WHITE,
                            icon=icons.CALENDAR_MONTH,
                            on_click=lambda _: date_init.pick_date(),
                        ),
                        ElevatedButton(
                            "Selecciona fecha Segunda",
                            bgcolor=colors.RED_300,
                            color=colors.WHITE,
                            icon=icons.CALENDAR_MONTH,
                            on_click=lambda _: date_finish.pick_date(),
                        ),
                        ElevatedButton(
                            "Go Home",
                            bgcolor=colors.RED_300,
                            color=colors.WHITE,
                            on_click=lambda _: page.go("/"),
                        ),
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
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
app(target=main, view=AppView.WEB_BROWSER)
