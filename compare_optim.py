# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    compare_optim.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: gajanvie <gajanvie@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/23 10:05:47 by gajanvie          #+#    #+#              #
#    Updated: 2026/10/23 10:05:53 by gajanvie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import matplotlib.pyplot as plt
from csv_reader import load_csv, get_numeric_columns
from logreg_utils import (
	FEATURES, calculer_parametres, construire_X, encoder_y,
	entrainer_par_lots,
)
from plot_style import TEXTE, appliquer_style

MAISON = "Gryffindor"
EPOCHS = 50


def main():
	if len(sys.argv) != 2:
		print("Usage: python3 compare_optim.py <dataset_train.csv>", file=sys.stderr)
		sys.exit(1)
	try:
		colonnes, noms = load_csv(sys.argv[1])
	except FileNotFoundError:
		print(f"Fichier introuvable : {sys.argv[1]}", file=sys.stderr)
		sys.exit(1)

	numeriques = get_numeric_columns(colonnes, noms)
	garder = [i for i, m in enumerate(colonnes["Hogwarts House"]) if m.strip() != ""]
	numeriques = {f: [numeriques[f][i] for i in garder] for f in FEATURES}
	maisons = [colonnes["Hogwarts House"][i] for i in garder]

	params = calculer_parametres(numeriques, FEATURES)
	X = construire_X(numeriques, FEATURES, params, len(garder))
	y = encoder_y(maisons, MAISON)
	m = len(X)

	configs = [
		("Batch GD (lr 0.1)", 0.1, m),
		("Mini-batch 32 (lr 0.1)", 0.1, 32),
		("SGD (lr 0.01)", 0.01, 1),
	]
	courbes = {}
	for nom, lr, taille in configs:
		print(f"Entrainement : {nom}")
		_, hist = entrainer_par_lots(X, y, lr, EPOCHS, taille)
		courbes[nom] = [c for _, c in hist]

	appliquer_style()
	fig, ax = plt.subplots(figsize=(9, 6))
	for nom, cout in courbes.items():
		ax.plot(range(1, len(cout) + 1), cout, label=nom, linewidth=2)
	ax.set_yscale("log")
	ax.set_xlabel("Epochs")
	ax.set_ylabel("Coût (log loss, échelle log)")
	ax.set_title(f"Comparaison des optimiseurs ({MAISON})")
	leg = ax.legend()
	for t in leg.get_texts():
		t.set_color(TEXTE)
	plt.tight_layout()
	plt.savefig("compare_optim.png", dpi=150)
	plt.show()


if __name__ == "__main__":
	main()