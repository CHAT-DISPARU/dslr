# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    logreg_utils.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: gajanvie <gajanvie@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/21 11:18:50 by CHAT-DISPAR       #+#    #+#              #
#    Updated: 2026/10/23 09:55:49 by gajanvie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import math
import random
from csv_reader import valid_values
from maths_utils import ft_mean, ft_std

FEATURES = [
	"Herbology",
	"Defense Against the Dark Arts", #pas astro car r = -1
	"Ancient Runes",
	"Charms",
	"Divination",
	"Muggle Studies",
	"History of Magic",
	"Transfiguration",
	"Potions",
	"Flying",
]
MAISONS = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
EPSILON = 1e-15


def sigmoid(z):
	"""sigmoide stable"""
	if z >= 0:
		return 1 / (1 + math.exp(-z))
	e = math.exp(z)
	return e / (1 + e)


def calculer_parametres(numeriques, features):
	"""{feature: (mean, std)} calcs sur train sans none"""
	params = {}
	for f in features:
		valides = valid_values(numeriques[f])
		m = ft_mean(valides)
		s = ft_std(valides)
		if s == 0:
			s = 1.0 #pas de/0
		params[f] = (m, s)
	return params


def construire_X(numeriques, features, params, nb_eleves):
	"""matrice X biais 1 colonne None -> moyenne0  standardisation"""
	X = []
	for i in range(nb_eleves):
		ligne = [1.0]
		for f in features:
			v = numeriques[f][i]
			m, s = params[f]
			ligne.append(0.0 if v is None else (v - m) / s)
		X.append(ligne)
	return X


def encoder_y(maisons, maison):
	"""1.0 si eleve est dans maison sinon 0.0"""
	return [1.0 if m.strip() == maison else 0.0 for m in maisons]


def produit_scalaire(a, b):
	"""somme des a[k] * b[k]"""
	total = 0.0
	for k in range(len(a)):
		total += a[k] * b[k]
	return total


def predire_proba(X, theta):
	"""h(x) pour chaque ligne de X"""
	return [sigmoid(produit_scalaire(ligne, theta)) for ligne in X]


def calculer_cout(h, y):
	"""log loss : -1/m * somme(y log h + (1-y) log(1-h))"""
	total = 0.0
	for hi, yi in zip(h, y):
		hi = ft_min_max(hi)
		total += yi * math.log(hi) + (1 - yi) * math.log(1 - hi)
	return -total / len(y)


def ft_min_max(p):
	"""borne probabilite entre EPSILON et 1 - EPSILON (evite log(0))"""
	if p < EPSILON:
		return EPSILON
	if p > 1 - EPSILON:
		return 1 - EPSILON
	return p


def calculer_gradient(X, h, y):
	"""gradient : X^T (h - y) / m, boucles a la main"""
	m = len(X)
	grad = [0.0] * len(X[0])
	for ligne, hi, yi in zip(X, h, y):
		erreur = hi - yi
		for k in range(len(ligne)):
			grad[k] += erreur * ligne[k]
	return [g / m for g in grad]


def entrainer_une_maison(X, y, lr=0.1, iterations=1000):
	"""descente de gradient batch. return (theta, historique_du_cout)"""
	theta = [0.0] * len(X[0])
	historique = []
	for it in range(iterations):
		h = predire_proba(X, theta)
		grad = calculer_gradient(X, h, y)
		for k in range(len(theta)):
			theta[k] -= lr * grad[k]
		if it % 50 == 0 or it == iterations - 1:
			historique.append((it, calculer_cout(h, y)))
	return theta, historique

def entrainer_par_lots(X, y, lr=0.1, epochs=100, taille_batch=32, graine=42):
	"""descente de gradient batch lots.
	taille_batch = 1=SGD, k=mini-batch, len(X)=batch GD.
	return (theta, historique)historique = [(epoch, cout)]"""
	rng = random.Random(graine)
	m = len(X)
	theta = [0.0] * len(X[0])
	indices = list(range(m))
	historique = []
	for epoch in range(epochs):
		rng.shuffle(indices)
		for debut in range(0, m, taille_batch):
			lot = indices[debut:debut + taille_batch]
			Xb = [X[i] for i in lot]
			yb = [y[i] for i in lot]
			h = predire_proba(Xb, theta)
			grad = calculer_gradient(Xb, h, yb)
			for k in range(len(theta)):
				theta[k] -= lr * grad[k]
		historique.append((epoch, calculer_cout(predire_proba(X, theta), y)))
	return theta, historique