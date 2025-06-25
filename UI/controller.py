from calendar import month

import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDAnno(self):
        years = self._model.getYears()
        for y in years:
            self._view.ddyear.options.append(ft.dropdown.Option(y))
        self._view.update_page()

    def fillDDForma(self):
        shapes = self._model.getShapes()
        for s in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.update_page()

    def handle_graph(self, e):
        anno=self._view.ddyear.value
        shape=self._view.ddshape.value
        self._model.buildGraph(anno,shape)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodes()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model.getNumEdges()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Il grafo ha: {self._model.getNumCompConnesse()} componenti connesse"))
        self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande è costituita da {len(self._model.getMaxComp())} nodi:"))
        for n in self._model.getMaxComp():
            self._view.txt_result1.controls.append(ft.Text(n))
        self._view.update_page()

    def handle_path(self, e):
        cammino,punteggio=self._model.getCamminoMaxPunteggio()
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Punteggio totale del percorso ottentuto: {punteggio}"))
        self._view.txt_result2.controls.append(ft.Text(f"I nodi del percorso ottenuto sono:"))
        for n in cammino:
            self._view.txt_result2.controls.append(ft.Text(f"{n.id}: {n.duration} -- {n.datetime.month}"))
        self._view.update_page()