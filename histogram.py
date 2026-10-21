# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    histogram.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: CHAT-DISPARU <CHAT-DISPARU@student.42.f    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/08 17:17:44 by gajanvie          #+#    #+#              #
#    Updated: 2026/10/21 13:01:32 by CHAT-DISPAR      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import matplotlib.pyplot as plt
from csv_reader import load_csv, get_numeric_columns, get_all_by_house
from maths_utils import ft_mean, ft_std, ft_min, ft_max
from plot_style import COULEURS, ACCENT, TEXTE, FOND_AXES, appliquer_style

NB_BINS = 20


def toutes_les_notes(par_maison):
	"""fusionne liste maisons"""
	toutes = []
	for notes in par_maison.values():
		toutes.extend(notes)
	return toutes


def score_homogeneite(par_maison):
	"""ecar moyenne entre maison / (std global) si etit = homogene"""
	moyennes = [ft_mean(n) for n in par_maison.values()]
	return (ft_max(moyennes) - ft_min(moyennes)) / ft_std(toutes_les_notes(par_maison))


def bords_communs(toutes, nb_bins):
	"""bord des intervalle identique pour les maisons"""
	mini, maxi = ft_min(toutes), ft_max(toutes)
	pas = (maxi - mini) / nb_bins
	return [mini + i * pas for i in range(nb_bins + 1)]


def main():
	if len(sys.argv) != 2:
		print("Usage: python3 histogram.py <dataset_train.csv>", file=sys.stderr)
		sys.exit(1)
	try:
		colonnes, noms = load_csv(sys.argv[1])
	except FileNotFoundError:
		print(f"Fichier introuvable : {sys.argv[1]}", file=sys.stderr)
		sys.exit(1)
	except ValueError as e:
		print(f"Erreur : {e}", file=sys.stderr)
		sys.exit(1)

	cours = list(get_numeric_columns(colonnes, noms).keys())
	data = get_all_by_house(colonnes, cours)
	if not any(data.values()):
		print("Pas maison dans ce fichier : utilise dataset_train.csv", file=sys.stderr)
		sys.exit(1)

	scores = {c: score_homogeneite(data[c]) for c in cours}
	classement = sorted(scores.items(), key=lambda t: t[1])
	meilleur = classement[0][0]

	print("Classement (petit score = homogène) :")
	for nom, s in classement:
		print(f"  {nom:<32} {s:.3f}")
	print(f"\nCours le plus homogène : {meilleur}")

	appliquer_style()
	fig, axes = plt.subplots(4, 4, figsize=(16, 11))
	fig.suptitle("Distribution des notes par maison", fontsize=14, fontweight="bold", color=TEXTE)
	cases = [ax for ligne in axes for ax in ligne]

	for ax, nom in zip(cases, cours):
		bords = bords_communs(toutes_les_notes(data[nom]), NB_BINS)
		for maison, notes in data[nom].items():
			ax.hist(notes, bins=bords, alpha=0.6, label=maison,
					color=COULEURS[maison], edgecolor=FOND_AXES, linewidth=0.4)
		ax.set_title(f"{nom} ({scores[nom]:.2f})",
					 color=ACCENT if nom == meilleur else TEXTE)
		ax.tick_params(labelsize=7)

	for ax in cases[len(cours):]:
		ax.axis("off")

	handles, labels = cases[0].get_legend_handles_labels()
	leg = fig.legend(handles, labels, loc="lower right", fontsize=12)
	for texte in leg.get_texts():
		texte.set_color(TEXTE)
	plt.tight_layout(rect=[0, 0, 1, 0.96])
	plt.savefig("histogram.png", dpi=150)
	plt.show()


if __name__ == "__main__":
	main()