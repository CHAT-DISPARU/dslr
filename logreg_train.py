# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    logreg_train.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: gajanvie <gajanvie@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/21 11:27:13 by CHAT-DISPAR       #+#    #+#              #
#    Updated: 2026/10/23 09:55:46 by gajanvie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import json
from lib.csv_reader import load_csv, get_numeric_columns
from lib.logreg_utils import (
	FEATURES, MAISONS, calculer_parametres, construire_X,
	encoder_y, entrainer_une_maison, entrainer_par_lots,
)

LEARNING_RATE = 0.1
ITERATIONS = 1000
EPOCHS = 100
TAILLE_MINI_BATCH = 32
FICHIER_POIDS = "weights.json"
MODES = ("batch", "sgd", "minibatch")

def main():
	if len(sys.argv) not in (2, 3):
		print("Usage: python3 logreg_train.py <dataset_train.csv> [batch|sgd|minibatch]", file=sys.stderr)
		sys.exit(1)
	mode = sys.argv[2] if len(sys.argv) == 3 else "batch"
	if mode not in MODES:
		print(f"Mode inconnu : {mode} (choix : {', '.join(MODES)})", file=sys.stderr)
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
		if mode == "batch":
			theta, historique = entrainer_une_maison(X, y, LEARNING_RATE, ITERATIONS)
		elif mode == "sgd":
			theta, historique = entrainer_par_lots(X, y, 0.01, EPOCHS, 1)
		else:
			theta, historique = entrainer_par_lots(X, y, LEARNING_RATE, EPOCHS, TAILLE_MINI_BATCH)
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