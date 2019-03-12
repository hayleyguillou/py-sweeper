import pickle
import os
import operator

class Scores:

    def __init__(self):
        self.high_scores = []

        if os.path.isfile('highscores.pkl'):
            with open("highscores.pkl", "rb") as h:
                self.high_scores = pickle.load(h)
       
    def save_score(self, name, score):
        new_score = (name, score)
        self.high_scores.append(new_score)
        self.high_scores.sort(key = operator.itemgetter(1))

        self.high_scores = [x for x in self.high_scores if x[1]]
        
        if len(self.high_scores) > 10:
            self.high_scores = self.high_scores[:10]



        with open("highscores.pkl","wb") as out:
            pickle.dump(self.high_scores, out)

    def print_scores(self):
        for name, score in self.high_scores:
            print("{{name:>{col_width}}} | {{score:<{col_width}}}".format(col_width=(80-3)//2).format(name=name, score=score))