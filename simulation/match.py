import numpy as np
from dateutil.parser import parse

from db.match_table import insert

def insert_match(match):
    db_obj = match.to_dict()
    db_obj["year"] = parse(db_obj["date"]).year
    db_obj["simulation"] = True
    return insert(**db_obj)

class Match():
    def __init__(self, data, win_or_lose=False):
        self.id = data["id"]
        self.home_team = data.get("home_team", None)
        self.away_team = data.get("away_team", None)
        self.home_score = data.get("home_score", None)
        self.away_score = data.get("away_score", None)
        self.tournament = data.get("tournament", "FIFA World Cup")
        self.group = data.get("group", None)
        self.date = data.get("date", None)
        self.outcome_probabilities = None
        self.outcome = None
        self.win_or_lose = win_or_lose

        self.feature_vector = None

    def set_feature_vector(self, x):
        self.feature_vector = x

    def set_outcome_probabilties(self, outcome_probabilities):
        assert len(outcome_probabilities) > 2
        self.outcome_probabilities = outcome_probabilities

    def set_score(self, home_score, away_score):
        self.home_score = home_score
        self.away_score = away_score

    def set_outcome_from_score(self):
        if self.home_score > self.away_score:
            self.outcome = 1
        elif self.home_score == self.away_score:
            self.outcome = 0
        else:
            self.outcome = -1

    def set_outcome(self, outcome):
        self.outcome = outcome

    def get_outcome_probabilties(self):
        return self.outcome_probabilities

    def get_outcome_from_probabilites(self):
        return np.argmax(self.outcome_probabilities) - 1

    def get_outcome(self):
        outcome = None
        if self.outcome is None:
            outcome = self.get_outcome_from_probabilites()
        else:
            outcome = self.outcome

        if self.win_or_lose and outcome == 0:
            home_win_prob = self.outcome_probabilities[2]
            away_win_prob = self.outcome_probabilities[0]
            total = home_win_prob + away_win_prob
            outcome = int(np.random.choice([-1, 1], 1, p=[away_win_prob/total, home_win_prob/total])[0])

        return outcome

    def to_dict(self):
        return {
            "home_team": self.home_team,
            "away_team": self.away_team,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "tournament": self.tournament,
            "date": self.date
        }

    def flip_and_copy(self):
        data = {
            "home_team": self.away_team,
            "away_team": self.home_team,
            "home_score": self.away_score,
            "away_score": self.home_score,
            "tournament": self.tournament,
            "date": self.date,
            "id": self.id
        }
        return Match(data, self.win_or_lose)
