import copy
from opcode import cmp_op

from networkx.algorithms.richclub import rich_club_coefficient

from database.DAO import DAO
import networkx as nx

from model.sighting import Sighting


class Model:
    def __init__(self):
        self._graph=nx.DiGraph()
        self._idMap={}
        self.nodes=[]
        self.bestCammino=[]
        self.maxPunteggio=0
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)

    def getYears(self):
        return DAO.getYears()

    def getShapes(self):
        return DAO.getShapes()

    def buildGraph(self,anno,forma):
        self._graph.clear()
        self.nodes = DAO.getNodes(anno,forma)
        for n in self.nodes:
            self._idMap[n.id] = n

        self._graph.add_nodes_from(self.nodes)

        allEdges = DAO.getEdges(anno, forma,self._idMap)
        for e in allEdges:
            self._graph.add_edge(e[0], e[1])

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(list(self._graph.edges))

    def getNumCompConnesse(self):
        return nx.number_weakly_connected_components(self._graph)

    def getMaxComp(self):
        conn = list(nx.weakly_connected_components(self._graph))
        conn.sort(key=lambda x: len(x), reverse=True)
        return conn[0]

    def getCamminoMaxPunteggio(self):
        self.bestCammino = []
        self.maxPunteggio = 0
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)

        for n in self.nodes:
            self._occorrenze_mese[n.datetime.month]+=1
            successivi=self.getSuccessiviDurataCrescente(n)
            self.ricorsione([n],successivi)
            self._occorrenze_mese[n.datetime.month]=-1
        return self.bestCammino, self.maxPunteggio

    def getSuccessiviDurataCrescente(self,nodo: Sighting):
        successivi=self._graph.successors(nodo)
        succAmm=[]
        for s in successivi:
            if s.duration>nodo.duration and self._occorrenze_mese[s.datetime.month]<3:
                succAmm.append(s)
        return succAmm

    def ricorsione(self,parziale: list[Sighting],successivi: list[Sighting]):
        if len(successivi)==0:
            if self.getPunteggio(parziale)>self.maxPunteggio:
                self.maxPunteggio=self.getPunteggio(parziale)
                self.bestCammino=copy.deepcopy(parziale)
            return
        else:
            for n in successivi:
                parziale.append(n)
                self._occorrenze_mese[n.datetime.month]+=1
                nuoviSucc=self.getSuccessiviDurataCrescente(n)
                self.ricorsione(parziale, nuoviSucc)
                self._occorrenze_mese[n.datetime.month] -= 1
                parziale.pop()


    def getPunteggio(self,cammino: list[Sighting]):
        punteggio=0
        for n in range(len(cammino)):
            punteggio+=100
            if(n!=0 and cammino[n].datetime.month==cammino[n-1].datetime.month):
                punteggio+=200
        return punteggio



