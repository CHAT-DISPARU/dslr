# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_csv.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: gajanvie <gajanvie@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/08 12:30:02 by gajanvie          #+#    #+#              #
#    Updated: 2026/10/08 12:53:23 by gajanvie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
from csv_reader import (
    load_csv,
    get_numeric_columns,
    valid_values,
    get_column_by_house,
    get_all_by_house,
)


def titre(texte):
    print(f"\n{'=' * 60}\n{texte}\n{'=' * 60}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 test_csv.py <dataset.csv>", file=sys.stderr)
        sys.exit(1)

    try:
        colonnes, noms = load_csv(sys.argv[1])
    except FileNotFoundError:
        print(f"Fichier introuvable : {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)

    nb_lignes = len(colonnes[noms[0]])

    # ------------------------------------------------------------
    titre("1. Lecture du CSV")
    print("Colonnes :", len(noms))
    print("Lignes   :", nb_lignes)

    longueurs = {len(v) for v in colonnes.values()}
    ok = len(longueurs) == 1
    print("Toutes les colonnes ont la même longueur :", "OK" if ok else "ERREUR", longueurs)

    # ------------------------------------------------------------
    titre("2. Colonnes numériques")
    numeriques = get_numeric_columns(colonnes, noms)
    print(f"{len(numeriques)} colonnes numériques :")
    for nom, vals in numeriques.items():
        nb_valides = len(valid_values(vals))
        print(f"  {nom:<32} {nb_valides:>5} valides / {len(vals)}"
              f"   ({len(vals) - nb_valides} manquantes)")

    cours = list(numeriques.keys())

    # ------------------------------------------------------------
    titre("3. get_column_by_house (un cours)")
    if not cours:
        print("Aucun cours numérique, test sauté.")
        return
    premier = cours[0]
    par_maison = get_column_by_house(colonnes, premier)
    if not par_maison:
        print("Aucune maison trouvée (normal pour dataset_test.csv).")
    else:
        print(f"Cours : {premier}")
        for maison, notes in par_maison.items():
            print(f"  {maison:<12} {len(notes):>4} notes   première : {notes[0]}")
        total = sum(len(n) for n in par_maison.values())
        attendu = len(valid_values(numeriques[premier]))
        print(f"  Somme des effectifs : {total}  /  valides du cours : {attendu}",
              "OK" if total == attendu else "(différent : élèves sans maison ?)")

    # ------------------------------------------------------------
    titre("4. get_all_by_house (tous les cours)")
    tout = get_all_by_house(colonnes, cours)
    if not any(tout.values()):
        print("Aucune donnée par maison (normal pour dataset_test.csv).")
    else:
        for nom_cours, par_maison in tout.items():
            tailles = {m: len(v) for m, v in par_maison.items()}
            print(f"  {nom_cours:<30} {tailles}")

        # --------------------------------------------------------
        titre("5. Cohérence des deux fonctions")
        tout_ok = True
        for nom_cours in cours:
            a = get_column_by_house(colonnes, nom_cours)
            b = tout[nom_cours]
            if a != b:
                tout_ok = False
                print(f"  DIFFÉRENCE sur {nom_cours}")
        print("Résultat :", "OK, identiques" if tout_ok else "ERREUR")

    # ------------------------------------------------------------
    titre("6. Cas d'erreur")
    try:
        get_column_by_house(colonnes, "CoursQuiNExistePas")
        print("ERREUR : aucune exception levée")
    except KeyError as e:
        print("KeyError bien levée :", e)


if __name__ == "__main__":
    main()