import copy
import random

from geopy.distance import distance

import networkx as nx

from database.DAO import DAO
class Model:
    def __init__(self):
        self._provider = []
        self._nodes = []
        #self._edges = []
        self._grafo = nx.Graph()
        self._location = []


    def get_provider(self):
        self._provider = DAO.get_all_provider()
        return self._provider

    def create_graph(self, provider, soglia):
        self._grafo.clear()
        self._nodes.clear()
        #self._edges.clear()
        self._location.clear()
        self._location = DAO.get_localita(provider)
        self._nodes = self._location
        self._grafo.add_nodes_from(self._location)
        for u in self._nodes:
            for v in self._nodes:
                if u!=v:
                    distanza = distance((u.Latitude, u.Longitude), (v.Latitude, v.Longitude))
                    if distanza < soglia:
                        self._grafo.add_edge(u, v, weight=distanza)

    def get_cammino(self, target, substring):
        sources = self.getMostVicini()
        source = sources[random.randint(0, len(sources) - 1)][0]
        if not nx.has_path(self._grafo, source, target):
            print(f"{source} e {target} non sono connessi.")
            return [], source

        self._bestPath = []
        self._bestLen = 0
        parziale = [source]

        self.ricorsione(parziale, target, substring)
        return self._bestPath, source

    def ricorsione(self, parziale, target, substring):
        #condizione di terminazione
        if parziale[-1] == target:
            if len(parziale) > self._bestLen:
                self._bestPath = copy.deepcopy(parziale)
                return

        #ricorsione
        for v in self._grafo.neighbors(parziale[-1]):
            if v not in parziale and substring not in v.Location:
                parziale.append(v)
                self.ricorsione(parziale, target, substring)
                parziale.pop()

    def getMostVicini(self):
        lista = []
        for v in self._nodes:

            lista.append((v, len(list(self._grafo.neighbors(v)))))
        lista.sort(key=lambda x: x[1], reverse=True)
        result2 = [x for x in lista if x[1] == lista[0][1]]
        return result2


    def get_graph_detail(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_all_locations(self):
        return self._grafo.nodes

