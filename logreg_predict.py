# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    logreg_predict.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: CHAT-DISPARU <CHAT-DISPARU@student.42.f    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/21 11:37:24 by CHAT-DISPAR       #+#    #+#              #
#    Updated: 2026/10/21 11:37:49 by CHAT-DISPAR      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import json
import csv
from csv_reader import load_csv, get_numeric_columns
from logreg_utils import construire_X, predire_proba


def argmax(valeurs):
	"""indice de la plus grande valeur"""
	meilleur = 0
	for k in range(1, len(valeurs)):
		if valeurs[k] > valeurs[meilleur]:
			meilleur = k
	return meilleur


def main():
	if len(sys.argv) != 3:
		print("Usage: python3 logreg_predict.py <dataset_test.csv> <weights.json>",
			  file=sys.stderr)
		sys.exit(1)
	try:
		colonnes, noms = load_csv(sys.argv[1])
		with open(sys.argv[2]) as f:
			modele = json.load(f)
	except FileNotFoundError as e:
		print(f"Fichier introuvable : {e.filename}", file=sys.stderr)
		sys.exit(1)
	except (ValueError, json.JSONDecodeError) as e:
		print(f"Erreur : {e}", file=sys.stderr)
		sys.exit(1)

	features = modele["features"]
	maisons = modele["maisons"]
	params = {f: tuple(modele["params"][f]) for f in features}

	numeriques = get_numeric_columns(colonnes, noms)
	manquantes = [f for f in features if f not in numeriques]
	if manquantes:
		print(f"Features absentes du fichier : {manquantes}", file=sys.stderr)
		sys.exit(1)

	nb = len(colonnes[noms[0]])
	X = construire_X(numeriques, features, params, nb)

	# probas[k][i] = proba que l'eleve i soit de la maison k
	probas = [predire_proba(X, modele["poids"][m]) for m in maisons]

	with open("houses.csv", "w", newline="") as f:
		writer = csv.writer(f)
		writer.writerow(["Index", "Hogwarts House"])
		for i in range(nb):
			scores = [probas[k][i] for k in range(len(maisons))]
			writer.writerow([i, maisons[argmax(scores)]])
	print(f"houses.csv ecrit : {nb} predictions")


if __name__ == "__main__":
	main()