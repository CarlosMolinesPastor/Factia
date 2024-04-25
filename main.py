import flet as ft

# Importamos de flet para no tener que utilizar ft.
from flet import (
    Page,
    MainAxisAlignment,
    CrossAxisAlignment,
    AppBar,
    ElevatedButton,
    Text,
    colors,
    DatePicker,
)

# Importamos datetime
import datetime


def main(page: Page):
    page.title = "Factia"

    def route_change(route):
        # Borramos las vistas si hubiera alguna
        page.views.clear()
        # Creamos las variables para las fechas
        date_init = date_picker
        date_finish = date_picker
        # Anadimos los DatePicker en forma overlay
        page.overlay.append(date_picker)
        # HOME
        # Anadimos la vista principal con la ruta slash y añadimos los controles de la pagina: un appbar
        # y dos botones elevados, uno para añadir productos y otro para buscar por fecha
        page.views.append(
            # Creamos la vista con la ruta slash
            ft.View(
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
        # PRODUCTO
        # Si la ruta es /producto añadimos la vista con el AppBar y un botón para volver a la vista anterior
        if page.route == "/producto":
            page.views.append(
                ft.View(
                    "/producto",
                    [
                        AppBar(title=Text("Añadir Producto"), bgcolor=colors.RED_300),
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
        # BUSQUEDA
        # Si la ruta es /busqueda añadimos la vista con el AppBar y tres botones para seleccionar fechas y volver a la vista anterio
        if page.route == "/busqueda":
            page.views.append(
                ft.View(
                    "/busqueda",
                    [
                        AppBar(
                            title=Text("Busqueda de productos"), bgcolor=colors.RED_300
                        ),
                        ElevatedButton(
                            "Selecciona fecha Primera",
                            bgcolor=colors.RED_300,
                            color=colors.WHITE,
                            icon=ft.icons.CALENDAR_MONTH,
                            on_click=lambda _: date_init.pick_date(),
                        ),
                        ElevatedButton(
                            "Selecciona fecha Segunda",
                            bgcolor=colors.RED_300,
                            color=colors.WHITE,
                            icon=ft.icons.CALENDAR_MONTH,
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

    # Date picker para seleccionar fechas
    # Creamos dos funciones para cambiar la fecha y para cerrar el date picker
    def change_date(e):
        print(f"Date picker changed, value is {date_picker.value}")

    def date_picker_dismissed(e):
        print(f"Date picker dismissed, value is {date_picker.value}")
    # Creamos el date picker con las fechas de inicio y fin
    date_picker = DatePicker(
        on_change=change_date,
        on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(2020, 10, 1),
        last_date=datetime.datetime(2050, 10, 1),
    )


# Iniciamos la app
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
