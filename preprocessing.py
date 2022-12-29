"""
Oxide Plant Simulator
"""

# Paths

PATH = '.\\inputs\\'


# Imports

import pandas as pd


# Classes

class PreProcessing:
    def __init__(self):
        self.mills = None
        self.silos = None
        self.scales = None
        self.lines = None

        self.mills_indeces = None
        self.silos_indeces = None
        self.scales_indeces = None
        self.lines_indeces = None

        self.equipments = dict()

        self.silos_supply = None

        self.data_reading()
        self.set_supply()
        self.df_to_dict()
        self.set_indeces()
        self.set_equipments()

    def data_reading(self):
        self.mills = pd.read_excel(PATH + 'dataset.xlsx', sheet_name='mills')
        self.silos = pd.read_excel(PATH + 'dataset.xlsx', sheet_name='silos')
        self.scales = pd.read_excel(PATH + 'dataset.xlsx', sheet_name='scales')
        self.lines = pd.read_excel(PATH + 'dataset.xlsx', sheet_name='lines')

    def set_supply(self):
        self.silos_supply = self.silos[['ID', 'Supply']]

    def df_to_dict(self):
        self.mills = self.mills.to_dict()
        self.silos = self.silos.to_dict()
        self.scales = self.scales.to_dict()
        self.lines = self.lines.to_dict()

    def set_indeces(self):
        self.mills_indeces = dict(zip(self.mills['ID'].values(), self.mills['ID'].keys()))
        self.silos_indeces = dict(zip(self.silos['ID'].values(), self.silos['ID'].keys()))
        self.scales_indeces = dict(zip(self.scales['ID'].values(), self.scales['ID'].keys()))
        self.lines_indeces = dict(zip(self.lines['ID'].values(), self.lines['ID'].keys()))

    def set_equipments(self):
        self.equipments['mills'] = list(self.mills['ID'].values())
        self.equipments['silos'] = list(self.silos['ID'].values())
        self.equipments['TS'] = ['TS']
        self.equipments['scales'] = list(self.scales['ID'].values())
        self.equipments['lines'] = list(self.lines['ID'].values())
