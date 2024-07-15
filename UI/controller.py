import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI

        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceLocation = None


    def handle_graph(self, e):
        lista = self._model.getMostVicini()
        self._view.txt_result.controls.append(ft.Text(f"I vertici col maggiore numero di vicini sono:"))
        for l in lista:
            self._view.txt_result.controls.append(ft.Text(f"{l[0]} -> {l[1]} vicini"))
        self._view.update_page()

    def create_graph(self, e):
        self._view.txt_result.controls.clear()
        self._view.update_page()
        provider = self._view.dd_provider.value
        if provider is None:
            self._view.create_alert("Selezionare un provider")
            return

        distanza = self._view.txt_distance.value
        if distanza == "":
            self._view.create_alert("inserire una distanza")
            return

        try:
            soglia = float(distanza)
        except ValueError:
            self._view.create_alert("Inserire una soglia numerica")
            return

        self._model.create_graph(provider, soglia)

        self._view.txt_result.controls.clear()
        n_nodi, n_archi = self._model.get_graph_detail()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato con:"
                                                      f"{n_nodi} nodi e {n_archi} archi"))
        self._view.btn_analisi_grafo.disabled = False

        self.fillDDTarget()
        self._view.update_page()


    def handle_percorso(self, e):
        self._view.txt_result.controls.clear()
        self._view.update_page()
        print(self._choiceLocation)
        target = self._choiceLocation
        if self._choiceLocation is None:
            self._view.create_alert("Selezionare un targer")
            return
        testo = self._view.txt_stringa.value
        if testo == "":
            self._view.create_alert("Attenzione stringa non inserita")
            return

        percorso, sorgente = self._model.get_cammino(target, testo)

        if len(percorso) == 0:
            self._view.txt_result.controls.append(ft.Text(f"Non esiste un percorso tra {sorgente}"
                                                          f" e {target}"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Il nodo di partenza è {sorgente}"
                                                        f" e la lunghezza del percorso è {len(percorso)}"))
            self._view.txt_result.controls.append(ft.Text(f"il percorso attraversa i seguenti nodi"))

            for p in percorso:
                self._view.txt_result.controls.append(ft.Text(f"{p[0]}"))

        self._view.update_page()


    def fillDDProvider(self):
        provider = self._model.get_provider()
        provider.sort()
        for p in provider:
            self._view.dd_provider.options.append(ft.dropdown.Option(p))

        self._view.update_page()

    def fillDDTarget(self):
        locations = self._model.get_all_locations()
        for l in locations:
            self._view.ddTarget.options.append(ft.dropdown.Option(data=l,
                                                                  text = l.Location,
                                                                  on_click=self.read_choice))

    def read_choice(self, e):

        if e.control.data is None:
            self._choiceLocation = None
        else:
            self._choiceLocation = e.control.data