class Touche:
    def __init__(self, touche, time_pos, time,octave, posy=0, posx=0, pressed=0, nature = 'blanc', px_appui=0, px_relache=0, increment=0):
        self.touche = touche
        self.time_pos = time_pos
        self.time = time
        self.octave = octave
        self.posy = posy
        self.posx = posx
        self.pressed = pressed
        self.nature = nature
        self.px_appui = px_appui
        self.px_relache = px_relache
        self.increment = increment