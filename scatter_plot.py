# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scatter_plot.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: gajanvie <gajanvie@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/09 14:19:49 by gajanvie          #+#    #+#              #
#    Updated: 2026/10/09 14:35:11 by gajanvie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import matplotlib.pyplot as plt
from csv_reader import load_csv, get_numeric_columns
from maths_utils import ft_correlation
from plot_style import COULEURS, TEXTE, appliquer_style


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


def tracer_grille(colonnes, numeriques, classement, n_top=3):
	"""top n paires + la moins correlee, dans une seule figure"""
	choix = classement[:n_top] + [classement[-1]]
	appliquer_style()
	fig, axes = plt.subplots(2, 2, figsize=(12, 9))
	fig.suptitle("Paires de cours : des plus aux moins corrélées",
				 fontsize=14, fontweight="bold", color=TEXTE)
	for ax, (a, b, r) in zip([ax for l in axes for ax in l], choix):
		points = points_par_maison(colonnes, numeriques, a, b)
		for maison, (xs, ys) in points.items():
			ax.scatter(xs, ys, s=8, alpha=0.6, color=COULEURS[maison], label=maison)
		ax.set_xlabel(a)
		ax.set_ylabel(b)
		ax.set_title(f"r = {r:.3f}")
	handles, labels = axes[0][0].get_legend_handles_labels()
	leg = fig.legend(handles, labels, loc="lower center", ncol=4,
					frameon=False, markerscale=2, fontsize=11)
	for texte in leg.get_texts():
		texte.set_color(TEXTE)
	plt.tight_layout(rect=[0, 0.06, 1, 0.95])
	plt.savefig("scatter_plot.png", dpi=150)
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
	tracer_grille(colonnes, numeriques, classement)


if __name__ == "__main__":
	main()