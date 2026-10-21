import sys
import matplotlib.pyplot as plt
from csv_reader import load_csv, get_numeric_columns
from maths_utils import ft_min, ft_max
from plot_style import COULEURS, TEXTE, FOND_AXES, appliquer_style

NB_BINS = 15
MAISONS = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]


def abreger(nom, n=12):
	return nom if len(nom) <= n else nom[:n - 1] + "."


def indices_par_maison(colonnes, nom_maison="Hogwarts House"):
	"""renvoi {maison: [indices des eleves]}"""
	resultat = {}
	for i, maison in enumerate(colonnes[nom_maison]):
		maison = maison.strip()
		if maison == "":
			continue
		resultat.setdefault(maison, []).append(i)
	return resultat


def bords_communs(valeurs, nb_bins):
	"""bords des intervalles pareil pour les maisons"""
	mini, maxi = ft_min(valeurs), ft_max(valeurs)
	pas = (maxi - mini) / nb_bins
	return [mini + k * pas for k in range(nb_bins + 1)]


def valeurs_valides(liste):
	"""retire les None"""
	return [v for v in liste if v is not None]


def tracer_diagonale(ax, numeriques, nom, indices):
	"""histogramme une feature, une couleur par maison"""
	bords = bords_communs(valeurs_valides(numeriques[nom]), NB_BINS)
	for maison in MAISONS:
		notes = valeurs_valides([numeriques[nom][i] for i in indices.get(maison, [])])
		if notes:
			ax.hist(notes, bins=bords, alpha=0.6, color=COULEURS[maison],
					edgecolor=FOND_AXES, linewidth=0.3)


def tracer_scatter(ax, numeriques, nom_x, nom_y, indices):
	"""scatter de nom_x (x) contre nom_y (y) colore par maison"""
	for maison in MAISONS:
		xs, ys = [], []
		for i in indices.get(maison, []):
			x = numeriques[nom_x][i]
			y = numeriques[nom_y][i]
			if x is not None and y is not None:
				xs.append(x)
				ys.append(y)
		ax.scatter(xs, ys, s=1.5, alpha=0.5, color=COULEURS[maison])


def main():
	if len(sys.argv) != 2:
		print("Usage: python3 pair_plot.py <dataset_train.csv>", file=sys.stderr)
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
	cours = list(numeriques.keys())
	n = len(cours)
	indices = indices_par_maison(colonnes)
	if not indices:
		print("Aucune maison dans ce fichier : utilise dataset_train.csv", file=sys.stderr)
		sys.exit(1)

	appliquer_style()
	fig, axes = plt.subplots(n, n, figsize=(22, 22))
	fig.suptitle("Pair plot : notes par maison", fontsize=16,
				 fontweight="bold", color=TEXTE)

	for i in range(n):
		for j in range(n):
			ax = axes[i][j]
			if i == j:
				tracer_diagonale(ax, numeriques, cours[i], indices)
			else:
				tracer_scatter(ax, numeriques, cours[j], cours[i], indices)
			ax.set_xticks([])
			ax.set_yticks([])
			ax.grid(False)
			if i == n - 1:
				ax.set_xlabel(abreger(cours[j]), fontsize=7, rotation=30)
			if j == 0:
				ax.set_ylabel(abreger(cours[i]), fontsize=7, rotation=0,
							  ha="right", va="center")

	handles = [plt.Line2D([0], [0], marker="o", linestyle="", markersize=9,
						  color=COULEURS[m]) for m in MAISONS]
	leg = fig.legend(handles, MAISONS, loc="lower center", ncol=4,
					 frameon=False, fontsize=12)
	for texte in leg.get_texts():
		texte.set_color(TEXTE)

	plt.tight_layout(rect=[0, 0.03, 1, 0.97])
	plt.savefig("pair_plot.png", dpi=120)
	plt.show()


if __name__ == "__main__":
	main()