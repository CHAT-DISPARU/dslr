# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    logreg_train.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: CHAT-DISPARU <CHAT-DISPARU@student.42.f    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/21 11:27:13 by CHAT-DISPAR       #+#    #+#              #
#    Updated: 2026/10/21 12:17:26 by CHAT-DISPAR      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import json
from csv_reader import load_csv, get_numeric_columns
from logreg_utils import (
	FEATURES, MAISONS, calculer_parametres, construire_X,
	encoder_y, entrainer_une_maison,
)

LEARNING_RATE = 0.1
ITERATIONS = 1000
FICHIER_POIDS = "weights.json"


def main():
	if len(sys.argv) != 2:
		print("Usage: python3 logreg_train.py <dataset_train.csv>", file=sys.stderr)
		sys.exit(1)
	try:
		colonnes, noms = load_csv(sys.argv[1])
	except FileNotFoundError:
		print(f"Fichier introuvable : {sys.argv[1]}", file=sys.stderr)
		sys.exit(1)
	except ValueError as e:
		print(f"Erreur : {e}", file=sys.stderr)
		sys.exit(1)

	if "Hogwarts House" not in colonnes:
		print("Colonne 'Hogwarts House' absente", file=sys.stderr)
		sys.exit(1)

	numeriques = get_numeric_columns(colonnes, noms)
	manquantes = [f for f in FEATURES if f not in numeriques]
	if manquantes:
		print(f"Features absentes du fichier : {manquantes}", file=sys.stderr)
		sys.exit(1)

	#que eleve avec maison
	garder = [i for i, m in enumerate(colonnes["Hogwarts House"]) if m.strip() != ""]
	numeriques = {f: [numeriques[f][i] for i in garder] for f in FEATURES}
	maisons_eleves = [colonnes["Hogwarts House"][i] for i in garder]

	params = calculer_parametres(numeriques, FEATURES)
	X = construire_X(numeriques, FEATURES, params, len(garder))
	print(f"X : {len(X)} eleves x {len(X[0])} colonnes (biais inclus)")

	poids = {}
	for maison in MAISONS:
		y = encoder_y(maisons_eleves, maison)
		theta, historique = entrainer_une_maison(X, y, LEARNING_RATE, ITERATIONS)
		poids[maison] = theta
		print(f"{maison:<12} cout initial {historique[0][1]:.4f} -> final {historique[-1][1]:.4f}")

	sauvegarde = {
		"features": FEATURES,
		"maisons": MAISONS,
		"params": {f: list(params[f]) for f in FEATURES},
		"poids": poids,
	}
	with open(FICHIER_POIDS, "w") as f:
		json.dump(sauvegarde, f, indent=2)
	print(f"Poids sauvegardes dans {FICHIER_POIDS}")


if __name__ == "__main__":
	main()