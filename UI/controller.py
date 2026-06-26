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

    def handleGenreSelection(self, e):
        self._genreValue = e.control.value
        print(f"Anno selezionato: {self._yearValue}")

    def handleCreaGrafo(self, e):
        pass

    def handleCreaGrafo(self,e):
        pass

    def handleCammino(self,e):
        pass