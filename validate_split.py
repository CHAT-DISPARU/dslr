# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    validate_split.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: gajanvie <gajanvie@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/21 11:42:02 by CHAT-DISPAR       #+#    #+#              #
#    Updated: 2026/10/23 10:05:22 by gajanvie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import random
from csv_reader import load_csv, get_numeric_columns
from logreg_utils import entrainer_par_lots
from logreg_utils import (
	FEATURES, MAISONS, calculer_parametres, construire_X,
	encoder_y, entrainer_une_maison, predire_proba,
)

LEARNING_RATE = 0.1
ITERATIONS =3000
RATIO_TRAIN = 0.8
EPOCHS = 100
TAILLE_MINI_BATCH = 32
MODES = ("batch", "sgd", "minibatch")

def argmax(valeurs):
	meilleur = 0
	for k in range(1, len(valeurs)):
		if valeurs[k] > valeurs[meilleur]:
			meilleur = k
	return meilleur


def sous_ensemble(numeriques, indices):
	return {f: [numeriques[f][i] for i in indices] for f in FEATURES}


def main():
	if len(sys.argv) not in (2, 3):
		print("Usage: python3 validate_split.py <dataset_train.csv> [batch|sgd|minibatch]", file=sys.stderr)
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

	numeriques = get_numeric_columns(colonnes, noms)
	maisons_col = colonnes["Hogwarts House"]
	indices = [i for i, m in enumerate(maisons_col) if m.strip() != ""]

	random.seed(42)
	random.shuffle(indices)
	coupe = int(len(indices) * RATIO_TRAIN)
	idx_train, idx_val = indices[:coupe], indices[coupe:]
	print(f"train : {len(idx_train)} eleves   validation : {len(idx_val)} eleves")

	num_train = sous_ensemble(numeriques, idx_train)
	num_val = sous_ensemble(numeriques, idx_val)
	params = calculer_parametres(num_train, FEATURES)
	X_train = construire_X(num_train, FEATURES, params, len(idx_train))
	X_val = construire_X(num_val, FEATURES, params, len(idx_val))
	maisons_train = [maisons_col[i] for i in idx_train]
	vrai_val = [maisons_col[i].strip() for i in idx_val]

	probas = []
	for maison in MAISONS:
		y = encoder_y(maisons_train, maison)
		if mode == "batch":
			theta, hist = entrainer_une_maison(X_train, y, LEARNING_RATE, ITERATIONS)
			print(maison, hist[-1][1])
		elif mode == "sgd":
			theta, _ = entrainer_par_lots(X_train, y, 0.01, EPOCHS, 1)
		else:
			theta, _ = entrainer_par_lots(X_train, y, LEARNING_RATE, EPOCHS, TAILLE_MINI_BATCH)
		probas.append(predire_proba(X_val, theta))
	bonnes = 0
	for i in range(len(idx_val)):
		scores = [probas[k][i] for k in range(len(MAISONS))]
		if MAISONS[argmax(scores)] == vrai_val[i]:
			bonnes += 1
		else :
			print(f"erreur : vrai={vrai_val[i]:<11} predit={MAISONS[argmax(scores)]}")
	acc = bonnes / len(idx_val)
	print(f"Accuracy validation : {acc * 100:.2f} %  ({'OK' if acc >= 0.98 else 'SOUS LES 98 %'})")


if __name__ == "__main__":
	main()



# Gryffindor	0,48
# Hufflepuff	0,49
# Ravenclaw		0,53
# Slytherin		0,50

# Gryffindor	0,01
# Hufflepuff	0,02
# Ravenclaw		0,97
# Slytherin		0,00