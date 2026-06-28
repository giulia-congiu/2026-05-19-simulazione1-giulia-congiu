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


 #ESERCIZIO 1: non orientato
        #nodi: artisti con almeno una traccia in una playlist
        # archi= artisti collegati se almeno 1 playlist ha tracce di entrambi e peso= playlist in common
        # def buildGraphes1(self):
        #     self._Nodies1= DAO.getnodeses1()
        #     idMapes1= {}
        #     for a in self._Nodies1:
        #         idMapes1[a.id] = a
        #         self._graph.add_node(a)
        #
        #     result = DAO.getEdgeses1(idMapes1)
        #     playlistMap= defaultdict(list)
        #     for playlist, artista in result:
        #         playlistMap[playlist].append(artista)
        #
        #     pesoarco= defaultdict(int)
        #     for playlist, artisti in playlistMap.items():
        #         for a, b in itertools.combinations(artisti,2 ):
        #             pesoarco[(a,b)] +=1
        #
        #     for (a,b), peso in pesoarco.items():
        #         self._graph.add_edge(idMapes1[a],idMapes1[b],weight=peso)


        #ESERCIZIO 2: orientato
        #NODI: clienti che hanno acquistato almeno 1 traccia rock
        #Arco: due clienti sono collegati se hanno acquistato almeno un genere in comune.
        # Verso: dal cliente che ha acquistato più tracce al cliente che ne ha acquistate meno.
        # In caso di parità inserire entrambi gli archi.
        # Peso: somma del numero di tracce acquistate dai due clienti.

        # def buildGraphes2(self):
        #     result = DAO.getresult()
        #
        #     generi = defaultdict(list)
        #     for genere, cliente in result:
        #         generi[genere].append(artista)
        #
        #     tracceCliente = defaultdict(int)
        #     for genere, cliente in result:
        #         tracceCliente[cliente] += 1
        #
        #     # trovo tutte le coppie collegate
        #     coppie = set()
        #     for genere, clienti in generi.items():
        #         for a, b in itertools.combinations(clienti, 2):
        #             coppie.add((a, b))
        #
        #     # creo archi con verso e peso
        #     for (a, b) in coppie:
        #         pop_a = tracceCliente[a]
        #         pop_b = tracceCliente[b]
        #         weight = pop_a + pop_b
        #
        #         if pop_a > pop_b:
        #             self._graph.add_edge(idMap[a], idMap[b], weight=weight)
        #         elif pop_a < pop_b:
        #             self._graph.add_edge(idMap[b], idMap[a], weight=weight)
        #         else:
        #             self._graph.add_edge(idMap[a], idMap[b], weight=weight)
        #             self._graph.add_edge(idMap[b], idMap[a], weight=weight)


        #ESERCIZIO 3
        #Costruire un grafo non orientato.
        # Nodi: album contenenti almeno 5 tracce.
        # Arco: due album sono collegati se almeno un cliente ha acquistato tracce di entrambi.
        # Peso: numero di clienti in comune.
        # def buildGraphes1(self):
        #     self._Nodies1= DAO.getnodeses1()
        #     idMapes1= {}
        #     for a in self._Nodies1:
        #         idMapes1[a.id] = a
        #         self._graph.add_node(a)
        #
        #     result = DAO.getEdgeses1(idMapes1)
        #     customerMap= defaultdict(list)
        #     for c, al in result:
        #         customerMap[c].append(al)
        #
        #     pesoarco= defaultdict(int)
        #     for c, album in customerMap.items():
        #         for a, b in itertools.combinations(album, 2):
        #             pesoarco[(a,b)]+=1
        #
        #     for (a,b) , peso in pesoarco.items():
        #         if a in idMapes1 and b in idMapes1: #controlla che gli archi siano nel grafo
        #             self._graph.add_edge(idMapes1[a],idMapes1[b],weight=peso)


        # #ESERCIZIO 8
        # #Costruire un grafo orientato.
        # #Nodi: tutti i media type.
        # #Arco: due media type sono collegati se almeno un cliente ha acquistato entrambi.
        # #Verso: dal media type con più acquisti verso quello con meno acquisti.
        # #Peso: somma degli acquisti. = poplarità
        # def buildGraphes8(self):
        #     self._nodes = DAO.getNodeses8()  # tutti i media type
        #     idMap = {}
        #     for m in self._nodes:
        #         idMap[m.id] = m
        #         self._graph.add_node(m)
        #
        #     result = DAO.getResultes8()  # (customerId, mediaTypeId)
        #
        #     # mappa cliente → lista mediaType
        #     customerMap = defaultdict(list)
        #     for cliente, mediaType in result:
        #         customerMap[cliente].append(mediaType)
        #
        #     # popolarità globale di ogni mediaType
        #     popolarita = defaultdict(int)
        #     for cliente, mediaType in result:
        #         popolarita[mediaType] += 1
        #
        #     # trovo coppie e creo archi
        #     coppie = set()
        #     for cliente, mediaTypes in customerMap.items():
        #         for a, b in itertools.combinations(mediaTypes, 2):
        #             coppie.add((a, b))
        #
        #     for (a, b) in coppie:
        #         pop_a = popolarita[a]
        #         pop_b = popolarita[b]
        #         weight = pop_a + pop_b
        #
        #         if pop_a > pop_b:
        #             self._graph.add_edge(idMap[a], idMap[b], weight=weight)
        #         elif pop_a < pop_b:
        #             self._graph.add_edge(idMap[b], idMap[a], weight=weight)
        #         else:
        #             self._graph.add_edge(idMap[a], idMap[b], weight=weight)
        #             self._graph.add_edge(idMap[b], idMap[a], weight=weight)

        #ESERCIZIO 9
        # Costruire un grafo orientato.
        # Nodi: tutti gli artisti con almeno una traccia acquistata.
        # Arco: due artisti sono collegati se almeno un cliente ha acquistato entrambi.
        # Verso: dall'artista con durata totale delle tracce maggiore verso quello con durata minore.
        # Peso: somma delle durate.
        # result = DAO.getCustomerArtist()  # (customerId, artistId)
        # durate = DAO.getDurataArtisti()  # (artistId, durata)
        # # durata già calcolata dal DAO
        # durataArtista = {}
        # for artista, durata in durate:
        #     durataArtista[artista] = durata
        #
        # # customerMap semplice, senza dict
        # customerMap = defaultdict(list)
        # for cliente, artista in result:
        #     customerMap[cliente].append(artista)
        #
        # # coppie
        # coppie = set()
        # for cliente, artisti in customerMap.items():
        #     for a, b in itertools.combinations(artisti, 2):
        #         coppie.add((a, b))
        #
        # # archi (identico a prima)
        # for (a, b) in coppie:
        #     dur_a = durataArtista[a]
        #     dur_b = durataArtista[b]
        #     weight = dur_a + dur_b
        #
        #     if dur_a > dur_b:
        #         self._graph.add_edge(idMap[a], idMap[b], weight=weight)
        #     elif dur_a < dur_b:
        #         self._graph.add_edge(idMap[b], idMap[a], weight=weight)
        #     else:
        #         self._graph.add_edge(idMap[a], idMap[b], weight=weight)
        #         self._graph.add_edge(idMap[b], idMap[a], weight=weight)