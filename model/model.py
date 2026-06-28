import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._IDMap = {}

        self._bestCammino = []
        self._bestLunghezza = 0

    def getRating(self):
        return DAO.getRating()

    def creaGrafo(self, minR, maxR):
        self._grafo.clear()
        self._IDMap = {}

        nodi = DAO.getNodi(minR, maxR)
        self._grafo.add_nodes_from(nodi)
        for n in nodi:
            self._IDMap[n.id] = n

        archi = DAO.getArchi(minR, maxR, self._IDMap)
        for a in archi:
            self._grafo.add_edge(a[0], a[1], weight=a[2])

    def getInfo(self):
        return len(self._grafo.nodes()), len(self._grafo.edges())

    def getBestArchi(self):
        archi_ordinati = sorted(self._grafo.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
        return archi_ordinati[:5]

    def getCompConn(self):
        num = nx.number_connected_components(self._grafo)
        largest_cc = max(nx.connected_components(self._grafo), key=len)
        return num, largest_cc

    def getCamminoOttimo(self):
        self._bestCammino = []
        self._bestLunghezza = 0

        for n in self._grafo.nodes():
            parziale = [n]
            self._ricorsione(parziale)

        return self._bestCammino, (self._bestLunghezza - 1)

    def _ricorsione(self, parziale):

        validi = self._getSuccessors(parziale)  # Mi calcola i successori del nodo
        if validi == []:
            if len(parziale) > self._bestLunghezza:
                self._bestCammino = copy.deepcopy(parziale)
                self._bestLunghezza = len(parziale)

        for n in validi:
            parziale.append(n)
            self._ricorsione(parziale)
            parziale.pop()

    def _getSuccessors(self, parziale):
        succ = self._grafo.neighbors(parziale[-1])  #
        validi = []

        for n in succ:
            if n not in parziale:
                if n.date_of_birth > parziale[-1].date_of_birth:
                    validi.append(n)

        return validi
