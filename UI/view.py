import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.dd_provider = None
        self.btn_crea_grafo = None
        self.txt_distance = None
        self.btn_analisi_grafo = None
        self.txt_result = None
        self.txt_container = None
        self.ddTarget = None

    def load_interface(self):
        # title
        self._title = ft.Text("NYC- hotspot", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW with some controls
        #row 1
        self.dd_provider = ft.Dropdown(label="provider")
        self.btn_crea_grafo = ft.ElevatedButton(text="Crea grafo", on_click=self._controller.create_graph)
        row1 = ft.Row([ft.Container(self.dd_provider, width=300),
                       ft.Container(self.btn_crea_grafo, width=200)],
                       alignment=ft.MainAxisAlignment.CENTER)
        self._controller.fillDDProvider()

        #row 2
        self._page.controls.append(row1)
        self.txt_distance = ft.TextField(
            label="distanza",
            width=200,
            hint_text="distanza"
        )
        self.btn_analisi_grafo = ft.ElevatedButton(text="Analizza grafo", on_click=self._controller.handle_graph, disabled=True)
        row2 = ft.Row([ft.Container(self.txt_distance, width=300),
                       ft.Container(self.btn_analisi_grafo, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        #row 3
        self.txt_stringa = ft.TextField(
            label="stringa",
            width=200,
            hint_text="stringa"
        )

        self.btn_calcola_percorso = ft.ElevatedButton(text="calcola percorso", on_click=self._controller.handle_percorso)
        row3 = ft.Row([ft.Container(self.txt_stringa, width=300),
                       ft.Container(self.btn_calcola_percorso, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row3)

        #row4
        self.ddTarget = ft.Dropdown(label="Target")
        row4 = ft.Row([ft.Container(self.ddTarget, width=300),
                       ft.Container(None, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row4)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
