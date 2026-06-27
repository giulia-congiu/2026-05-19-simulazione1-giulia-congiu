import copy
import itertools
from collections import defaultdict

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self.idMap = {}
        self._artisti = None
        self._bestPath = []
        self._bestScore = 0

    def getArtisti(self):
        return self._artisti

    def getTop5(self):
        edges = self._graph.edges(data=True)
        top5= []
        for e in edges:
            top5.append((e[0], e[1], e[2]["weight"]))
        top5.sort(key = lambda x: x[2], reverse = True)
        return top5[:5]

    def getAllGenres(self):
            return DAO.getAllGenres()

    def getPath(self, v0):
        self._bestPath = []
        parziale = [self.idMap[int(v0)]]
        for v in self._graph.successors(self.idMap[int(v0)]):  # primo vicino aggiunto fuori
            if self._graph.has_node(v):
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()
        return self._bestPath

    def _ricorsione(self, parziale):
        # ogni parziale è valida — salvo subito se migliore
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        # espansione con vincolo peso decrescente
        for v in self._graph.successors(parziale[-1]):
            pesoE = self._graph[parziale[-1]][v]["weight"]
            if self._graph[parziale[-2]][parziale[-1]]["weight"] < pesoE and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getArtistaInfluente(self):
        bestinf= 0
        best = None
        for n in self._artisti:
            out = 0  # somma dei pesi degli archi uscenti
            for u, v, dati in self._graph.out_edges(n, data=True):
                # u: nodo di partenza (sempre n)
                # v: nodo di arrivo
                # dati: dizionario degli attributi dell'arco es. {"weight": 100}
                out += dati["weight"]

            in_ = 0  # somma dei pesi degli archi entranti
            for u, v, dati in self._graph.in_edges(n, data=True):
                in_ += dati["weight"]
            score = out - in_
            if score > bestinf:
                bestinf = score
                best = n
        return bestinf, best





    def buildGraph(self, genre):
        self._graph.clear()
        # aggiunge i nodi filtrati per nMin
        self._artisti = DAO.getAllNodes(genre)
        for a in self._artisti:
            self.idMap[a.ArtistId] = a

        self._graph.add_nodes_from(self._artisti)

        custom_artist_list = DAO.getCustomerArtistCounts(genre)
        customer_map=defaultdict(dict)
        #Se cerchi un cliente che non esiste ancora, crea automaticamente un dizionario vuoto {} per lui

        # Raggruppo i dati per cliente. Il risultato finale è una mappa nidificata
        # dove puoi trovare rapidamente cosa ha ascoltato ogni singolo utente.
        for customer_id, artist_id, ntracks in custom_artist_list:
            customer_map[customer_id][artist_id] = ntracks

        artist_popularity = defaultdict(int)
        for customer, artists in customer_map.items():
            for artist_id, ntracks in artists.items():
                artist_popularity[artist_id] += ntracks
        #.items() restituisce una vista delle coppie chiave-valore di un dizionario,
        # sotto forma di tuple del tipo (chiave, valore).

        for customer, artist in customer_map.items():
            for a, b in itertools.combinations(artist.keys(), 2):
                #itertoold dà coppie di elementi della lista, senza ripetizioni e senza invertire ordine
                #prendo tutti gli artisti ascoltati da quel cliente e genero possibili coppie di due di artisti
                popA= artist_popularity[a]
                popB = artist_popularity[b]
                pesotot= popA + popB

                if popA > popB:
                    self._graph.add_edge(self.idMap[a], self.idMap[b], weight=pesotot)
                elif popA<popB:
                    self._graph.add_edge(self.idMap[b],self.idMap[a], weight=pesotot)
                else:
                    self._graph.add_edge(self.idMap[a], self.idMap[b], weight=pesotot)
                    self._graph.add_edge(self.idMap[b], self.idMap[a], weight=pesotot)
