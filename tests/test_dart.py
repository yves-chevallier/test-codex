"""Tests fonctionnels pour le programme ``dart``.

Ces tests utilisent ``pytest`` et fournissent des messages explicites en cas
 d'échec afin d'aider à comprendre quel comportement attendu n'est pas
 respecté.
"""

from __future__ import annotations

import os
import subprocess
from typing import Iterable, List

import pytest


EXECUTABLE = os.environ.get("EXEC", "./dart")


def run_dart(*args: str) -> subprocess.CompletedProcess[str]:
    """Exécute le programme ``dart`` avec les arguments donnés."""

    command: List[str] = [EXECUTABLE, *args]
    return subprocess.run(command, check=False, capture_output=True, text=True)


def assert_exit(result: subprocess.CompletedProcess[str], expected: int, message: str) -> None:
    """Vérifie le code de retour en fournissant un message clair."""

    assert (
        result.returncode == expected
    ), f"{message}\n  attendu : {expected}\n  obtenu  : {result.returncode}\n  stderr  : {result.stderr.strip()}"


@pytest.mark.parametrize(
    "args",
    [("1", "2"), ("0", "0"), ("0.5", "0.5"), ("-0.5", "-0.1")],
)
def test_programme_reussi(args: Iterable[str]) -> None:
    """Le programme doit terminer correctement lorsque deux coordonnées valides sont fournies."""

    result = run_dart(*args)
    assert_exit(result, 0, "Le programme devrait retourner 0 en cas de succès.")


def test_aucun_argument() -> None:
    """Le programme doit prévenir lorsqu'aucun argument n'est passé."""

    result = run_dart()
    assert_exit(
        result,
        1,
        "Sans arguments, le programme doit retourner 1 pour signaler un appel incorrect.",
    )


def test_un_seul_argument() -> None:
    """Avec un seul argument, l'erreur doit être la même que pour l'absence d'arguments."""

    result = run_dart("1")
    assert_exit(
        result,
        1,
        "Avec un seul argument, le programme doit retourner 1 pour signaler l'erreur.",
    )


@pytest.mark.parametrize("args", [("0", "foo"), ("foo", "0")])
def test_arguments_non_numeriques(args: Iterable[str]) -> None:
    """Les arguments non numériques doivent être détectés."""

    result = run_dart(*args)
    assert_exit(
        result,
        2,
        "Des arguments impossibles à convertir doivent faire retourner 2.",
    )


@pytest.mark.parametrize(
    "x, y, points",
    [
        ("0", "0", "100"),
        ("0.12", "0.5", "100"),
        ("1", "0", "100"),
        ("0", "1", "100"),
        ("0.707", "0.707", "100"),
    ],
)
def test_zone_a(x: str, y: str, points: str) -> None:
    result = run_dart(x, y)
    assert_exit(result, 0, "Les coordonnées dans la zone A doivent réussir.")
    assert (
        result.stdout.strip() == points
    ), f"Zone A : la sortie devrait être {points}, mais vaut {result.stdout.strip()!r}."


@pytest.mark.parametrize(
    "x, y",
    [
        ("0", "1.001"),
        ("0", "5"),
        ("1.001", "0"),
        ("5", "0"),
        ("1.1", "1.36"),
    ],
)
def test_zone_b(x: str, y: str) -> None:
    result = run_dart(x, y)
    assert_exit(result, 0, "Les coordonnées dans la zone B doivent réussir.")
    assert (
        result.stdout.strip() == "25"
    ), f"Zone B : la sortie devrait être 25, mais vaut {result.stdout.strip()!r}."


@pytest.mark.parametrize(
    "x, y",
    [
        ("0", "5.0001"),
        ("5.001", "0.001"),
        ("10.0", "0"),
        ("6.042", "7.968"),
    ],
)
def test_zone_c(x: str, y: str) -> None:
    result = run_dart(x, y)
    assert_exit(result, 0, "Les coordonnées dans la zone C doivent réussir.")
    assert (
        result.stdout.strip() == "5"
    ), f"Zone C : la sortie devrait être 5, mais vaut {result.stdout.strip()!r}."


@pytest.mark.parametrize(
    "x, y",
    [
        ("100", "100"),
        ("0", "100"),
        ("100", "0"),
        ("100000000000", "1234567891234567"),
    ],
)
def test_zone_d(x: str, y: str) -> None:
    result = run_dart(x, y)
    assert_exit(result, 0, "Les coordonnées dans la zone D doivent réussir.")
    assert (
        result.stdout.strip() == "0"
    ), f"Zone D : la sortie devrait être 0, mais vaut {result.stdout.strip()!r}."


def test_points_personnalises_zone_a() -> None:
    result = run_dart("0", "0", "42")
    assert_exit(result, 0, "Le programme doit accepter un score personnalisé pour la zone A.")
    assert (
        result.stdout.strip() == "42"
    ), "Zone A personnalisée : la sortie doit correspondre aux points fournis."

    result_b = run_dart("0", "1.001", "42")
    assert_exit(result_b, 0, "Les autres zones doivent conserver les valeurs par défaut.")
    assert (
        result_b.stdout.strip() == "25"
    ), "Zone B personnalisée : sans valeur fournie, le score doit rester à 25."

    result_c = run_dart("0", "5.0001", "42")
    assert_exit(result_c, 0, "Les zones sans personnalisation doivent garder les valeurs par défaut.")
    assert (
        result_c.stdout.strip() == "5"
    ), "Zone C personnalisée : sans valeur fournie, le score doit rester à 5."


def test_points_personnalises_zone_ab() -> None:
    result = run_dart("0", "1.001", "32", "42")
    assert_exit(result, 0, "Le programme doit accepter les scores personnalisés des zones A et B.")
    assert (
        result.stdout.strip() == "42"
    ), "Zone B personnalisée : la sortie doit correspondre aux points fournis."

    result_a = run_dart("0", "0", "32", "42")
    assert_exit(result_a, 0, "Les zones personnalisées doivent être utilisées pour le calcul du score.")
    assert (
        result_a.stdout.strip() == "32"
    ), "Zone A personnalisée : la sortie doit correspondre aux points fournis."

    result_c = run_dart("6.042", "7.968", "32", "42")
    assert_exit(result_c, 0, "Les zones sans personnalisation doivent garder les valeurs par défaut.")
    assert (
        result_c.stdout.strip() == "5"
    ), "Zone C doit conserver sa valeur par défaut lorsqu'elle n'est pas fournie."


def test_points_personnalises_zone_abc() -> None:
    result = run_dart("0", "5.0001", "1", "2", "3")
    assert_exit(result, 0, "Le programme doit accepter les scores personnalisés pour A, B et C.")
    assert (
        result.stdout.strip() == "3"
    ), "Zone C personnalisée : la sortie doit correspondre aux points fournis."

    result_a = run_dart("1", "0", "1", "2", "3")
    assert_exit(result_a, 0, "La zone A personnalisée doit utiliser le score fourni.")
    assert result_a.stdout.strip() == "1", "Zone A personnalisée : résultat attendu 1."

    result_b = run_dart("0", "5", "1", "2", "3")
    assert_exit(result_b, 0, "La zone B personnalisée doit utiliser le score fourni.")
    assert result_b.stdout.strip() == "2", "Zone B personnalisée : résultat attendu 2."

    result_d = run_dart("100", "100", "1", "2", "3")
    assert_exit(result_d, 0, "Les zones non personnalisées doivent rester à 0.")
    assert result_d.stdout.strip() == "0", "Zone D : résultat attendu 0."


def test_points_personnalises_zone_abcd() -> None:
    result = run_dart("100", "100", "9", "8", "7", "6")
    assert_exit(result, 0, "Les quatre zones personnalisées doivent être prises en compte.")
    assert (
        result.stdout.strip() == "6"
    ), "Zone D personnalisée : la sortie doit correspondre aux points fournis."

    result_a = run_dart("1", "0", "9", "8", "7", "6")
    assert_exit(result_a, 0, "La zone A personnalisée doit utiliser le score fourni.")
    assert result_a.stdout.strip() == "9", "Zone A personnalisée : résultat attendu 9."


def test_option_version() -> None:
    result = run_dart("-v")
    assert_exit(result, 0, "L'option -v doit terminer correctement.")
    sortie = result.stdout
    assert "ersion" in sortie, "La sortie de -v doit contenir le mot 'version'."
    assert "@" in sortie, "La sortie de -v doit contenir une adresse e-mail."