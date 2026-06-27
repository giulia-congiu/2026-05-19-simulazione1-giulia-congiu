import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genreValue = None

    def fillDDGenre(self):
        genres = self._model.getAllGenres()
        genreDD = list(map(lambda x: ft.dropdown.Option(x), genres))
        self._view._ddGenre.options = genreDD
        self._view.update_page()

    def fillDDArtist(self):
        artisti = self._model.getArtisti()
        artistiDD = list(map(lambda x: ft.dropdown.Option(key=x.ArtistId,text=x.Name), artisti))
        self._view._ddArtist.options = artistiDD
        self._view.update_page()

    def handleCreaGrafo(self, e):
        genre = self._view._ddGenre.value
        if genre is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Selezionare un genere", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(genre)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        nodi, archi= self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi:{nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi:{archi}"))

        a, inf= self._model.getArtistaInfluente()
        self._view.txt_result.controls.append(ft.Text(f"Artista con maggiore influenza: {a} con influenza = {inf}"))

        top5= self._model.getTop5()
        self._view.txt_result.controls.append(ft.Text("Top 5 archi"))
        for t in top5:
            self._view.txt_result.controls.append(ft.Text(f"{t[0]} -----> {t[1]}: {t[2]}"))

        self.fillDDArtist()

        self._view.update_page()


    def handleCammino(self,e):
        artist = self._view._ddArtist.value
        if artist is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Selezionare un artista", color="red"))
            self._view.update_page()
            return
        path = self._model.getPath(artist)
        if path is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("nessun path trovato", color="red"))
        self._view.txt_result.controls.append(
            ft.Text(f"Lunghezza cammino max trovato:{len(path)} nodi"))
        for p in path:
            self._view.txt_result.controls.append(
                ft.Text(f"{p}"))

        self._view.update_page()