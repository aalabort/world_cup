import argparse
import functools
import random
import time
import socket
import numpy as np
import pandas as pd

from features.data_provider import get_whole_dataset, set_feature_columns, other_features
from simulation.predictor import OutcomePredictor
from simulation.simulation import run_simulation, run_actual_tournament_simulation
from db.simulation_table import store_simulation_results
from models.outcome_model import get_model

parser = argparse.ArgumentParser()
parser.add_argument('--actual', action="store_true")
parser.add_argument('--limited-features', action="store_true")
args = parser.parse_args()

if args.limited_features:
    set_feature_columns(other_features)

X, y = get_whole_dataset("home_win")

print("Feature set shape:", X.shape)

for i in range(0, 100):
    model = get_model(X=X, y=y)
    predictor = OutcomePredictor(model)

    if args.actual:
        prefix = "matchlevel"
        print(f"Running match-level tournament simulation: {i}")

        match_template = pd.read_csv('data/original/wc_2018_games_real.csv')
        run_actual_tournament_simulation(match_template, predictor)
    else:
        prefix = "full"
        print(f"Running full tournament simulation: {i}")

        match_template = pd.read_csv('data/original/wc_2018_games.csv')
        run_simulation(match_template, predictor)

if args.limited_features:
    prefix = prefix + "_limfeatures"

filename = f"data/simulations/{prefix}_outcome_{socket.gethostname()}_{round(time.time())}_simulation.csv"
store_simulation_results(filename)
