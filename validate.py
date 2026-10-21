# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    validate.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: CHAT-DISPARU <CHAT-DISPARU@student.42.f    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/21 11:40:03 by CHAT-DISPAR       #+#    #+#              #
#    Updated: 2026/10/21 11:40:27 by CHAT-DISPAR      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import csv


def lire_houses(chemin):
	"""lit Index,Hogwarts House -> {index: maison}"""
	with open(chemin, newline="", encoding="utf-8") as f:
		lecteur = csv.reader(f)
		entete = next(lecteur, None)
		if entete is None or [c.strip() for c in entete] != ["Index", "Hogwarts House"]:
			raise ValueError(f"{chemin} : en-tete attendu 'Index,Hogwarts House'")
		resultat = {}
		for ligne in lecteur:
			if len(ligne) != 2:
				raise ValueError(f"{chemin} : ligne invalide {ligne}")
			resultat[ligne[0].strip()] = ligne[1].strip()
	return resultat


def accuracy(predit, vrai):
	"""(bonnes predictions) / (total) compte a la main"""
	bonnes = 0
	for idx, maison in vrai.items():
		if predit.get(idx) == maison:
			bonnes += 1
	return bonnes / len(vrai)


def matrice_confusion(predit, vrai, maisons):
	"""{vraie_maison: {maison_predite: nombre}}"""
	matrice = {v: {p: 0 for p in maisons} for v in maisons}
	for idx, v in vrai.items():
		p = predit.get(idx)
		if v in matrice and p in matrice[v]:
			matrice[v][p] += 1
	return matrice


def afficher_confusion(matrice, maisons):
	print(f"{'vrai \\ predit':<14}" + "".join(f"{m[:10]:>12}" for m in maisons))
	for v in maisons:
		print(f"{v:<14}" + "".join(f"{matrice[v][p]:>12}" for p in maisons))


def main():
	if len(sys.argv) != 3:
		print("Usage: python3 validate.py <houses.csv> <verite.csv>", file=sys.stderr)
		sys.exit(1)
	try:
		predit = lire_houses(sys.argv[1])
		vrai = lire_houses(sys.argv[2])
	except FileNotFoundError as e:
		print(f"Fichier introuvable : {e.filename}", file=sys.stderr)
		sys.exit(1)
	except ValueError as e:
		print(f"Erreur : {e}", file=sys.stderr)
		sys.exit(1)

	if set(predit) != set(vrai):
		print(f"Attention : {len(predit)} predictions pour {len(vrai)} reponses attendues",
			  file=sys.stderr)

	maisons = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
	acc = accuracy(predit, vrai)
	print(f"Accuracy : {acc * 100:.2f} %  ({'OK' if acc >= 0.98 else 'SOUS LES 98 %'})\n")
	afficher_confusion(matrice_confusion(predit, vrai, maisons), maisons)


if __name__ == "__main__":
	main()