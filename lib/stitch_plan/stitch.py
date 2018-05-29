from ..utils.geometry import Point


class Stitch(Point):
    def __init__(self, x, y, color=None, jump=False, stop=False, trim=False, no_ties=False):
        self.x = x
        self.y = y
        self.color = color
        self.jump = jump
        self.trim = trim
        self.stop = stop
        self.no_ties = no_ties

    def __repr__(self):
        return "Stitch(%s, %s, %s, %s, %s, %s, %s)" % (self.x, self.y, self.color, "JUMP" if self.jump else " ", "TRIM" if self.trim else " ", "STOP" if self.stop else " ", "NO TIES" if self.no_ties else " ")

    def copy(self):
        return Stitch(self.x, self.y, self.color, self.jump, self.stop, self.trim, self.no_ties)
