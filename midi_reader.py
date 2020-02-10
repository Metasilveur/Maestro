from mido import MidiFile
from touche import Touche
from conversion import Conv
        
class Midi_Reader():    
    def translate_midi_file(self ):
        status = 0
        try:
            midi_file = MidiFile(self.file)
            for i,j in enumerate(midi_file.tracks):
                for msg in j:
                    if (msg.type == 'note_on' or msg.type == 'note_off') and (status == 0 or status == 2):
                        self.conversion_droite.append(Conv(msg.type, msg.bytes()[1], msg.time))
                    if msg.type == 'end_of_track' and len(self.conversion_droite) == 0:
                        status = 2
                    elif msg.type == 'end_of_track' and len(self.conversion_droite) > 0:
                        status = 1
                    if (msg.type == 'note_on' or msg.type == 'note_off') and status == 1:
                        self.conversion_gauche.append(Conv(msg.type, msg.bytes()[1], msg.time))
                        
        except IOError as ioerr:
            print('File error: ' + str(ioerr))
            return(None)
            
    def __init__(self, midi_File_Name):
        self.file = midi_File_Name
        self.conversion_gauche = []
        self.conversion_droite = []
        self.translate_midi_file()
    
    def verif_note_on_g(self, nb):
        for i in range(nb):
            if self.conversion_gauche[i].type != 'note_on':
                return False
        return True
    
    def verif_note_on_d(self, nb):
        for i in range(nb):
            if self.conversion_droite[i].type != 'note_on':
                return False
        return True
    
    
    def verif_blanc(self, touche):
        if(int(touche)%12 < 5):
            if((int(touche)%12)%2 == 0):
                return True
            else:
                return False
        else:
            if((int(touche)%12)%2 == 1):
                return True
            else:
                return False

    def check_midi_file_struct(self):
        print(len(self.conversion_gauche))
        if len(self.conversion_droite)>0:
            if self.verif_note_on_d(10):
                for i in range(len(self.conversion_droite)):
                    if self.conversion_droite[i].type == 'note_on':
                        cp = 1
                        if self.conversion_droite[i].note == self.conversion_droite[i+cp].note:
                            self.conversion_droite[i+cp].type = 'note_off'
                        while self.conversion_droite[i].note != self.conversion_droite[i+cp].note:
                            cp += 1
                        if cp != 1:
                            self.conversion_droite[i+cp].type = 'note_off'
        if len(self.conversion_gauche)>0:
            if self.verif_note_on_g(10):
                for i in range(len(self.conversion_gauche)):
                    if self.conversion_gauche[i].type == 'note_on':
                        cp = 1
                        if self.conversion_gauche[i].note == self.conversion_gauche[i+cp].note:
                            self.conversion_gauche[i+cp].type = 'note_off'
                        while self.conversion_gauche[i].note != self.conversion_gauche[i+cp].note:
                            cp += 1
                        if cp != 1:
                            self.conversion_gauche[i+cp].type = 'note_off'
                        
    def to_graphic_process(self, main):
        tempo = 0
        partition = []
        if main == 0:
            for i in range(len(self.conversion_droite)):
                if self.conversion_droite[i].type == 'note_on':
                    cp = 1
                    time_off = 0
                    while self.conversion_droite[i].note != self.conversion_droite[i+cp].note:
                        time_off += int(self.conversion_droite[i+cp].time)
                        cp += 1
                    time_off += int(self.conversion_droite[i+cp].time)
                    tempo += int(self.conversion_droite[i].time)
                    note_centre = int(self.conversion_droite[i].note)%12
                    if note_centre < 5:
                        if note_centre%2 == 0:
                            note_place=(note_centre/2)*30
                        else:
                            note_place=19+int(note_centre/2)*30
                    else:
                        if note_centre%2 == 1:
                            note_place=(((self.conversion_droite[i].note-5)%12)/2)*30+90
                        else:
                            note_place=(((self.conversion_droite[i].note-6)%12)/2)*30+108
                    nb_octave_px = (int(self.conversion_droite[i].note/12)-2)*210
                    if self.verif_blanc(self.conversion_droite[i].note):
                        partition.append(Touche(self.conversion_droite[i].note, int(tempo/10), int(time_off/10), int(self.conversion_droite[i].note)/12, -int(time_off/10), note_place+nb_octave_px, 0, 'blanc'))
                    else:
                        partition.append(Touche(self.conversion_droite[i].note, int(tempo/10), int(time_off/10), int(self.conversion_droite[i].note)/12, -int(time_off/10), note_place+nb_octave_px, 0, 'noir'))
                else:
                    tempo += int(self.conversion_droite[i].time)
        else:
            for i in range(len(self.conversion_gauche)):
                if self.conversion_gauche[i].type == 'note_on':
                    cp = 1
                    time_off = 0
                    while self.conversion_gauche[i].note != self.conversion_gauche[i+cp].note:
                        time_off += int(self.conversion_gauche[i+cp].time)
                        cp += 1
                    time_off += int(self.conversion_gauche[i+cp].time)
                    tempo += int(self.conversion_gauche[i].time)
                    note_centre = int(self.conversion_gauche[i].note)%12
                    if note_centre < 5:
                        if note_centre%2 == 0:
                            note_place=(note_centre/2)*30
                        else:
                            note_place=19+int(note_centre/2)*30
                    else:
                        if note_centre%2 == 1:
                            note_place=(((self.conversion_gauche[i].note-5)%12)/2)*30+90
                        else:
                            note_place=(((self.conversion_gauche[i].note-6)%12)/2)*30+108
                    nb_octave_px = (int(self.conversion_gauche[i].note/12)-2)*210
                    if self.verif_blanc(self.conversion_gauche[i].note):
                        partition.append(Touche(self.conversion_gauche[i].note, int(tempo/10), int(time_off/10), int(self.conversion_gauche[i].note)/12, -int(time_off/10), note_place+nb_octave_px, 0, 'blanc'))
                    else:
                        partition.append(Touche(self.conversion_gauche[i].note, int(tempo/10), int(time_off/10), int(self.conversion_gauche[i].note)/12, -int(time_off/10), note_place+nb_octave_px, 0, 'noir'))
                else:
                    tempo += int(self.conversion_gauche[i].time)
        return partition