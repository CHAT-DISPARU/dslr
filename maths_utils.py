# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    maths_utils.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: gajanvie <gajanvie@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/08 14:39:52 by gajanvie          #+#    #+#              #
#    Updated: 2026/10/08 14:51:29 by gajanvie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_count(valeurs):
	n = 0
	for _ in valeurs:
		n += 1
	return n


def ft_sum(valeurs):
	total = 0.0
	for v in valeurs:
		total += v
	return total

def ft_mean(valeurs):
	n = ft_count(valeurs)
	if n == 0:
		raise ValueError("ft_mean : liste vide")
	return ft_sum(valeurs) / n

def ft_std(valeurs):
	n = ft_count(valeurs)
	if n < 2:
		raise ValueError("ft_std : faut au moins 2 valeurs")
	mu = ft_mean(valeurs)
	somme = 0.0
	for v in valeurs:
		somme += (v - mu) ** 2
	return (somme / (n - 1)) ** 0.5


def ft_min(valeurs):
	if ft_count(valeurs) == 0:
		raise ValueError("ft_min : liste vide")
	m = valeurs[0]
	for v in valeurs:
		if v < m:
			m = v
	return m


def ft_max(valeurs):
	if ft_count(valeurs) == 0:
		raise ValueError("ft_max : liste vide")
	m = valeurs[0]
	for v in valeurs:
		if v > m:
			m = v
	return m

def ft_sort(valeurs):
	r = list(valeurs)
	for i in range(1, ft_count(r)):
		cle = r[i]
		j = i - 1
		while j >= 0 and r[j] > cle:
			r[j + 1] = r[j]
			j -= 1
		r[j + 1] = cle
	return r

def ft_percentile(valeurs_triees, p):
	"""p 0  1 liste deja trie"""
	n = ft_count(valeurs_triees)
	if n == 0:
		raise ValueError("ft_percentile : liste vide")
	pos = p * (n - 1)
	lo = int(pos)
	hi = lo + 1 if lo + 1 < n else lo
	frac = pos - lo
	return valeurs_triees[lo] + (valeurs_triees[hi] - valeurs_triees[lo]) * frac

def ft_correlation(xs, ys):
	"""Corrélation de Pearson entre deux listes de même longueur."""
	n = ft_count(xs)
	if n != ft_count(ys) or n < 2:
		raise ValueError("ft_correlation : incompatibles")
	mx = ft_mean(xs)
	ft = ft_mean(ys)
	cov = 0.0
	var_x = 0.0
	var_y = 0.0
	for x, y in zip(xs, ys):
		cov += (x - mx) * (y - ft)
		var_x += (x - mx) ** 2
		var_y += (y - ft) ** 2
	if var_x == 0 or var_y == 0:
		return 0.0 #pas correlation
	return cov / (var_x * var_y) ** 0.5

def describe_column(valeurs):
	triees = ft_sort(valeurs)
	return {
		"Count": ft_count(valeurs),
		"Mean": ft_mean(valeurs),
		"Std": ft_std(valeurs),
		"Min": ft_min(valeurs),
		"25%": ft_percentile(triees, 0.25),
		"50%": ft_percentile(triees, 0.50),
		"75%": ft_percentile(triees, 0.75),
		"Max": ft_max(valeurs),
	}