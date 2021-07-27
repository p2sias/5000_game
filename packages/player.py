class Player:
    pseudo = ""
    points = 0

    def __init__(self, pseudo):
        self.pseudo = pseudo

    def score(self):
        return self.points

    def addPoints(self, points):
        """
            Seriously ?!?! I really need to explain that ?
        """
        print("\n[INFO] + " + str(points) + " pour " + self.pseudo)
        self.points += points

        if self.points >= 5000:
            return True
        else:
            return False
    