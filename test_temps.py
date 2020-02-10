class Time_Manager:
    def __init__(self, state=0, touche=0, velocity = 0, time=0):
        self.time_start = time
        self.touche_press = touche
        self.state = state
        self.velocity = velocity