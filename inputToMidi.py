import pygame
from pygame.time import *
from pygame.locals import *
from test_temps import Time_Manager

class InputToMidi:
    def __init__(self):
        self.records = []
        
    def addToRecords(self, py_event):
        self.records.append(py_event);
        
        