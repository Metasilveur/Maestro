class vecColor:
    def __init__(self, r, g, b):
        self.R = r
        self.G = g
        self.B = b
        

def computeVarColor(first, second, shades):
    toReturn = vecColor(0.0, 0.0, 0.0)
    
    toReturn.R = abs(first.R - second.R)/shades
    if first.R>second.R:
        toReturn.R = -1*toReturn.R
    toReturn.G = abs(first.G - second.G)/shades
    if first.G>second.G:
        toReturn.G = -1*toReturn.G
    toReturn.B = abs(first.B - second.B)/shades
    if first.B>second.B:
        toReturn.B = -1*toReturn.B
    
    return toReturn


# =============================================================================
# color1 = vecColor(255, 0, 0)
# color2 = vecColor(125, 255, 50)
# colorvars = computeVarColor(color1, color2, 300)
# 
# for i in range(300):
#     print("%d %d %d" % (color1.R + i*colorvars.R, color1.G + i*colorvars.G, color1.B + i*colorvars.B))
# =============================================================================
