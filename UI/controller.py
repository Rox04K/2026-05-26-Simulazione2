import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        opzioni = self._model.getRating()

        opzioniDD = list(map(lambda x: ft.dropdown.Option(x), opzioni))
        self._view._ddrating1.options = opzioniDD
        self._view._ddrating2.options = opzioniDD

    def handleCreaGrafo(self, e):
        r1 = self._view._ddrating1.value
        if r1 == "":
            self._view.create_alert('Attenzione selezionare un rating minimo!')
            return
        r2 = self._view._ddrating2.value
        if r2 == "":
            self._view.create_alert('Attenzione selezionare un rating massimo!')
            return

        self._view.txt_result.controls.clear()
        self._model.creaGrafo(float(r1), float(r2))
        self._view.txt_result.controls.append(ft.Text(f'Grafo correttamente creato:', color='green'))

        nodi, archi = self._model.getInfo()
        self._view.txt_result.controls.append(ft.Text(f'Numero di nodi: {nodi}'))
        self._view.txt_result.controls.append(ft.Text(f'Numero di archi: {archi}'))

        best = self._model.getBestArchi()
        self._view.txt_result.controls.append(ft.Text(f'Top 5 archi:'))
        for b in best:
            self._view.txt_result.controls.append(ft.Text(f'{b[0]} -> {b[1]} : {b[2]['weight']}'))

        num, conn = self._model.getCompConn()
        self._view.txt_result.controls.append(ft.Text(f'Il grafo ha {num} componenti connesse'))
        self._view.txt_result.controls.append(ft.Text(f'La più grande componente connessa è lunga {len(conn)}'))
        for b in conn:
            self._view.txt_result.controls.append(ft.Text(f'{b}'))

        self._view.update_page()

    def handleCammino(self, e):
        self._view.txt_result.controls.clear()

        cammino, lunghezza = self._model.getCamminoOttimo()

        self._view.txt_result.controls.append(ft.Text(f'Ho trovato un cammino lungo {lunghezza}', color='green'))
        for b in cammino:
            self._view.txt_result.controls.append(ft.Text(f'{b}'))

        self._view.update_page()