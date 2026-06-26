import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapGenre = {}


    def getAllGenres(self):
            return DAO.getAllGenres()

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def buildGraph(self, genre):
        self._graph.clear()
        # aggiunge i nodi filtrati per nMin
        nodes = DAO.getAllNodes(genre, self._idMapGenre)
        for n in nodes:
            self._idMapGenre[n.ArtistId]= n

        self._graph.add_nodes_from(nodes)

        # aggiunge gli archi
        self.addEdges()

