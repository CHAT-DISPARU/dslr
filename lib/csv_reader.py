# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    csv_reader.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: gajanvie <gajanvie@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/08 12:07:31 by gajanvie          #+#    #+#              #
#    Updated: 2026/10/23 12:14:36 by gajanvie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import csv


def load_csv(path):
	"""lit le csv renvoie (cols, noms)
	cols dict {nom_colonne: [cells str]}
	noms list des nom ordre fichier"""
	with open(path, newline="", encoding="utf-8") as f:
		lecteur = csv.reader(f)
		try:
			noms = next(lecteur)
		except StopIteration:
			raise ValueError(f"{path} : fichier vide")
		colonnes = {nom: [] for nom in noms}
		for ligne in lecteur:
			for nom, cellule in zip(noms, ligne):
				colonnes[nom].append(cellule)
	return colonnes, noms


def to_float(cellule):
	"""str->float None si vide non num ou NaN."""
	cellule = cellule.strip()
	if cellule == "":
		return None
	try:
		valeur = float(cellule)
	except ValueError:
		return None
	if valeur != valeur:
		return None
	return valeur


def is_numeric_column(cellules):
	"""True = au moin une valeur et pas toutes vides"""
	non_vides = 0
	for c in cellules:
		if c.strip() == "":
			continue
		non_vides += 1
		if to_float(c) is None:
			return False
	return non_vides > 0


def get_numeric_columns(colonnes, noms, exclure=("Index",)):
	"""return {nom: [float ou None]}"""
	resultat = {}
	for nom in noms:
		if nom in exclure:
			continue
		if is_numeric_column(colonnes[nom]):
			resultat[nom] = [to_float(c) for c in colonnes[nom]]
	return resultat


def valid_values(valeurs):
	"""Retire les None pour mean std"""
	return [v for v in valeurs if v is not None]


def get_column_by_house(colonnes, nom_cours, nom_maison="Hogwarts House"):
	"""return  {maison: [notes valides]}"""
	if nom_cours not in colonnes:
		raise KeyError(f"Colonne inconnue : {nom_cours}")
	if nom_maison not in colonnes:
		raise KeyError(f"Colonne inconnue : {nom_maison}")

	par_maison = {}
	for maison, cellule in zip(colonnes[nom_maison], colonnes[nom_cours]):
		maison = maison.strip()
		if maison == "":
			continue
		note = to_float(cellule)
		if note is None:
			continue
		par_maison.setdefault(maison, []).append(note)
	return par_maison	

# def get_all_by_house(colonnes, noms_cours, nom_maison="Hogwarts House"):
#	"""return {cours: {maison: [notes]}}"""
#	return {cours: get_column_by_house(colonnes, cours, nom_maison)
#			for cours in noms_cours}

def get_all_by_house(colonnes, noms_cours, nom_maison="Hogwarts House"):
	"""return {cours: {maison: [notes]}}"""
	if nom_maison not in colonnes:
		raise KeyError(f"Colonne inconnue : {nom_maison}")
	for cours in noms_cours:
		if cours not in colonnes:
			raise KeyError(f"Colonne inconnue : {cours}")

	resultat = {cours: {} for cours in noms_cours}
	nb_eleves = len(colonnes[nom_maison])
	for i in range(nb_eleves):
		maison = colonnes[nom_maison][i].strip()
		if maison == "":
			continue
		for cours in noms_cours:
			note = to_float(colonnes[cours][i])
			if note is None:
				continue
			resultat[cours].setdefault(maison, []).append(note)
	return resultat
