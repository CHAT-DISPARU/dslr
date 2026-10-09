# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    describe.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: gajanvie <gajanvie@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/08 14:52:59 by gajanvie          #+#    #+#              #
#    Updated: 2026/10/09 14:11:50 by gajanvie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
from csv_reader import load_csv, get_numeric_columns, valid_values
from maths_utils import describe_column

LIGNES = ["Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]
COURS_PAR_BLOC = 4
LARGEUR = 16
LABEL = 6


def abreger(nom, n=LARGEUR - 1):
	return nom if len(nom) <= n else nom[:n - 1] + "."


def afficher(stats_par_cours):
	noms = list(stats_par_cours.keys())

	for debut in range(0, len(noms), COURS_PAR_BLOC):
		bloc = noms[debut:debut + COURS_PAR_BLOC]

		print(" " * LABEL + "".join(f"{abreger(n):>{LARGEUR}}" for n in bloc))
		for ligne in LIGNES:
			valeurs = "".join(f"{stats_par_cours[n][ligne]:>{LARGEUR}.6f}" for n in bloc)
			print(f"{ligne:<{LABEL}}" + valeurs)

		if debut + COURS_PAR_BLOC < len(noms):
			print()

def main():
	if len(sys.argv) != 2:
		print("Usage: python3 describe.py <dataset.csv>", file=sys.stderr)
		sys.exit(1)

	try:
		colonnes, noms = load_csv(sys.argv[1])
	except FileNotFoundError:
		print(f"Fichier introuvable : {sys.argv[1]}", file=sys.stderr)
		sys.exit(1)
	except ValueError as e:
		print(f"Erreur : {e}", file=sys.stderr)
		sys.exit(1)

	numeriques = get_numeric_columns(colonnes, noms)
	if not numeriques:
		print("Aucune colonne numérique trouvée.", file=sys.stderr)
		sys.exit(1)

	stats = {}
	for nom, valeurs in numeriques.items():
		valides = valid_values(valeurs)
		if len(valides) < 2:
			continue
		stats[nom] = describe_column(valides)

	afficher(stats)


if __name__ == "__main__":
	main()
