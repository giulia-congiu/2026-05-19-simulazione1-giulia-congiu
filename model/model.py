import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()

    def getAllGenres(self):
        return DAO.getAllGenres()