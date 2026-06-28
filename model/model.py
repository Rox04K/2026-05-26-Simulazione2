import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._IDMap = {}

        self._bestCammino = []
        self._bestPunteggio = 0

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

    def getCamminoOttimo(self, nodo):
        self._bestCammino = []
        self._bestPunteggio = 0  # float('inf) se devo minimizzare qualcosa
        # EVENTUALI ALTRE CONDIZIONI CHE POTREBBERO ESSERE UTILI

        # ATTENZIONE! Se vuole che massimizzo la lunghezza del cammino:
        self._bestLunghezza = 0

        # SE HO UN NODO DI PARTENZA
        parziale = [self._IDMap[nodo]]
        self._ricorsione(parziale)

        # SE NON HO UN NODO DI PARTENZA
        for n in self._grafo.neighbors():
            parziale = [n]
            self._ricorsione(parziale)

        return self._bestCammino, self._bestPunteggio

        # ATTENZIONE! Se vuole che massimizzo la lunghezza del cammino, poi ritorno:
        # return self._bestCammino, (self._bestLunghezza - 1)  #Il -1 ci da il numero di archi

    def _ricorsione(self, parziale, limite):
        ''' METODO RICORSIVO VERO E PROPRIO, COMPOSTO DA PIù PASSAGGI:
            - CALCOLO I NODI VALIDI SECONDO LE SPECIFICHE DEL PROBLEMA
            - CONTROLLO SE HO ANCORA NODI DA VERIFICARE O SE SONO ARRIVATA ALLA FINE DELLA MIA RICORSIONE
            - CONTROLLO SE LA MIA SOLUZIONE VALIDA è ANCHE OTTIMA E AGGIORNO
            - CONTROLLO SE RISPETTO DEI VINCOLI (AD ESEMPIO MASSIMO 4 NODI ECC.) ALTRIMENTI return
            - CICLO SU VALIDI PER APPLICARE LE CONDIZIONI DI RICORSIONE '''

        validi = self._getSuccessors(parziale)  # Mi calcola i successori del nodo
        if validi == []:
            pesoAttuale = self._peso(
                parziale)  # calcolo il nuovo punteggio (oppure se non ho un punteggio non lo metto)
            if pesoAttuale > self._bestPunteggio:  # se devo massimizzare. Se devo minimizzare metterò <
                self._bestCammino = copy.deepcopy(parziale)
                self._bestPunteggio = pesoAttuale

            ''' ATTENZIONE SE MI CHIEDE IL CAMMINO DI LUNGHEZZA MASSIMA DEVO PRIMA CONTROLLARE OGNI VOLTA CHE È PIù LUNGO
                E AGGIORNARE, POI POSSO CONTROLLARE IL PESO A PARITà DI LUNGHEZZA'''

        ''' SE HO UN NODO DI ARRIVO DEVO TERMINARE SIA SE ARRIVO AL NODO DI ARRIVO 
            CHE SE ARRIVO ALLA LUNGHEZZA MASSIMA SENZA AVERE IL NODO DI ARRIVO CHE 
            VOLEVO'''
        if parziale[-1].product_id == end:
            if len(parziale) - 1 == limite:
                pesoAttuale = self._peso(parziale)
                if pesoAttuale > self._bestPunteggio:
                    self._bestCammino = copy.deepcopy(parziale)
                    self._bestPunteggio = pesoAttuale
                return
            else:
                return

        if len(parziale) - 1 == limite:
            return

        if len(parziale) == limite:  # eventuale condizione di terminazione
            # check
            return

        for n in validi:  # continuo la mia ricorsione
            parziale.append(n)
            self._ricorsione(parziale)
            parziale.pop()

    def _getSuccessors(self, parziale):
        ''' PRENDE TUTTI I VICINI DEL GRAFO E CONTROLLA SE POSSONO ESSERE CONSIDERATI NELLA RICORSIONE'''
        succ = self._grafo.successors(parziale[-1])  # self._grafo.neighbors() nel caso di Graph()
        validi = []

        for n in succ:
            if n not in parziale:  # condizione di non ripetibilita di un nodo (NON VOGLIO CICLI)

                ''' INSERIRE QUI IL CONTROLLO SUI NODI CHE DEVE ESSERE FATTO. ALCUNI ESEMPI:'''
                # controllo del peso sugli archi:
                if len(parziale) >= 2:
                    if self._grafo[parziale[-1]][n]['weight'] < self._grafo[parziale[-2]][parziale[-1]][
                        'weight']:  # strettamente decrescente
                        validi.append(n)
                else:
                    validi.append(n)

                # controllo su caratteristiche del nodo:
                if n.duration > parziale[-1].duration:  # strettamente crescente
                    validi.append(n)

        return validi
