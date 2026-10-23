# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scatter_plot.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: gajanvie <gajanvie@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/09 14:19:49 by gajanvie          #+#    #+#              #
#    Updated: 2026/10/23 10:48:05 by gajanvie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import matplotlib.pyplot as plt
from lib.csv_reader import load_csv, get_numeric_columns
from lib.maths_utils import ft_correlation
from lib.plot_style import COULEURS, TEXTE, appliquer_style


def paires_valides(xs, ys):
	"""garde eleve qui a des note dans les deux"""
	px, py = [], []
	for x, y in zip(xs, ys):
		if x is not None and y is not None:
			px.append(x)
			py.append(y)
	return px, py


def toutes_les_correlations(numeriques):
	"""correlation chaque paire cours"""
	#qu une fois
	noms = list(numeriques.keys())
	resultats = []
	for i in range(len(noms)):
		for j in range(i + 1, len(noms)):
			xs, ys = paires_valides(numeriques[noms[i]], numeriques[noms[j]])
			resultats.append((noms[i], noms[j], ft_correlation(xs, ys)))
	return resultats


def classer(resultats):
	"""triepaires |r| decroissan"""
	return sorted(resultats, key=lambda t: abs(t[2]), reverse=True)


def afficher_top(classement, n=10):
	"""n paires les plus correles"""
	print(f"{'Cours A':<30} {'Cours B':<30} {'r':>8}")
	for a, b, r in classement[:n]:
		print(f"{a:<30} {b:<30} {r:>8.4f}")


def points_par_maison(colonnes, numeriques, cours_a, cours_b, nom_maison="Hogwarts House"):
	"""renvoie {maison: ([xs], [ys])}eleves -> deux notes"""
	resultat = {}
	for i, maison in enumerate(colonnes[nom_maison]):
		maison = maison.strip()
		x = numeriques[cours_a][i]
		y = numeriques[cours_b][i]
		if maison == "" or x is None or y is None:
			continue
		xs, ys = resultat.setdefault(maison, ([], []))
		xs.append(x)
		ys.append(y)
	return resultat


def tracer(colonnes, numeriques, a, b, r):
	"""scatter plot la plus correlee, colore par maison"""
	appliquer_style()
	fig, ax = plt.subplots(figsize=(9, 6.5))
	points = points_par_maison(colonnes, numeriques, a, b)
	for maison, (xs, ys) in points.items():
		ax.scatter(xs, ys, s=14, alpha=0.7, color=COULEURS[maison], label=maison)
	ax.set_xlabel(a)
	ax.set_ylabel(b)
	ax.set_title(f"{a} vs {b}  (r = {r:.4f})")
	leg = ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12),
					ncol=4, frameon=False, markerscale=2)
	for texte in leg.get_texts():
		texte.set_color(TEXTE)
	plt.tight_layout()
	plt.show()

def main():
	if len(sys.argv) != 2:
		print("Usage: python3 scatter_plot.py <dataset_train.csv>", file=sys.stderr)
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
		print("Colonne 'Hogwarts House' absente : utilise dataset_train.csv", file=sys.stderr)
		sys.exit(1)

	numeriques = get_numeric_columns(colonnes, noms)
	if len(numeriques) < 2:
		print("Il faut au moins 2 colonnes numeriques.", file=sys.stderr)
		sys.exit(1)

	classement = classer(toutes_les_correlations(numeriques))
	print(f"Nombre de paires : {len(classement)}\n")
	afficher_top(classement)

	a, b, r = classement[0]
	print(f"\nPaire la plus similaire : {a} / {b} (r = {r:.4f})")

	points = points_par_maison(colonnes, numeriques, a, b)
	if not points:
		print("Aucune maison dans ce fichier : utilise dataset_train.csv", file=sys.stderr)
		sys.exit(1)
	tracer(colonnes, numeriques, a, b, r)


if __name__ == "__main__":
	main()