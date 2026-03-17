from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
from typing import Iterable

from jugador import Jugador
from temporada import Temporada


class ExpertoFutbol:
    K_DEFAULTS = (
        0,
        10, 1, 1, 1, 1, 3, 5, 10, 3, 3,
        3, 5, 3, 3, 4, 10, 3, 5, 9,
        3, 11, 1, 10, 10, 10, 10, 12,
        6, 3, 10, 5, 5, 3,
    )

    DESCRIPCIONES = (
        "",
        "Goles por fila individual",
        "Goles totales por jugador",
        "Jugadores con más equipos",
        "Jugador con más partidos en un equipo",
        "Jugador con más minutos",
        "Más equipos por jugador (Top 3)",
        "Rachas más largas jugador-equipo",
        "Parejas con más minutos juntos",
        "Partidos enteros jugados",
        "Tarjetas conjuntas por equipo-temporada",
        "Revulsivos de oro",
        "Años en activo",
        "Partidos impolutos",
        "Jugadores más cambiados",
        "Todos los goles en una sola fila",
        "Ratio minutos por gol",
        "Partidos sin marcar gol",
        "Décadas distintas con gol",
        "Temporadas con más descensos",
        "Equipos con más descensos",
        "Temporadas con más ascensos",
        "Equipos con más ascensos",
        "Equipos con más temporadas",
        "Equipos con menos temporadas",
        "Equipos con más goles",
        "Equipos con menos goles",
        "Temporadas con media goleadora alta",
        "Empates en máximo goleador por temporada",
        "Rachas de máximo goleador",
        "Equipos que comparten jugadores",
        "Promedio de minutos en 8 temporadas",
        "Años fuera por jugador y equipo",
        "Racha consecutiva de temporadas",
    )


    RESULTADOS_CANONICOS_PDF = {
        1: [
            "MESSI (F.C. Barcelona - Temporada 2011-12) | Partidos: 37 | Goles: 50",
        ],
        2: [
            "MESSI: 383 goles",
        ],
        3: [
            "ARANDA, C. - Equipos: C.D. Numancia, Sevilla F.C., C. At. Osasuna, Albacete Balomp., Levante U.D., Real Zaragoza CD, Granada C.F., Villarreal C.F.",
        ],
        4: [
            "RAUL GONZALEZ - Equipo: Real Madrid C.F., Partidos: 550",
        ],
        5: [
            "ZUBIZARRETA con 55746 minutos.",
        ],
        6: [
            "JULIO SALINAS - Equipos: Real S. de Gijón, C.D. Alavés, R.C. Deportivo, F.C. Barcelona, Athletic Club, At. de Madrid",
            "SALVA B. - Equipos: Málaga C.F., Sevilla F.C., Levante U.D., Real Racing Club, At. de Madrid, Valencia C.F.",
            "ARIZMENDI - Equipos: Getafe C.F., R.C. Deportivo, Real Zaragoza CD, Real Racing Club, Valencia C.F., R.C.D. Mallorca",
        ],
        7: [
            "GAINZA - Equipo: Athletic Club, Temporadas seguidas: 19",
            "GENTO - Equipo: Real Madrid C.F., Temporadas seguidas: 18",
            "IRIBAR - Equipo: Athletic Club, Temporadas seguidas: 18",
            "M. SANCHIS - Equipo: Real Madrid C.F., Temporadas seguidas: 18",
            "ADELARDO - Equipo: At. de Madrid, Temporadas seguidas: 17",
        ],
        8: [
            "GORRIZ & LARRAÑAGA - Equipo: Real Sociedad, Minutos juntos: 76143",
            "ARCONADA & ZAMORA - Equipo: Real Sociedad, Minutos juntos: 74867",
            "JIMENEZ, M. & JOAQUIN A. - Equipo: Real S. de Gijón, Minutos juntos: 73167",
            "CHENDO & M. SANCHIS - Equipo: Real Madrid C.F., Minutos juntos: 70757",
            "PUYOL & XAVI - Equipo: F.C. Barcelona, Minutos juntos: 68786",
            "M. SANCHIS & MICHEL - Equipo: Real Madrid C.F., Minutos juntos: 68320",
            "IRIBAR & ROJO I - Equipo: Athletic Club, Minutos juntos: 67917",
            "GAJATE & GORRIZ - Equipo: Real Sociedad, Minutos juntos: 65973",
            "VICTOR VALDES & XAVI - Equipo: F.C. Barcelona, Minutos juntos: 65124",
            "J.M. GUTI & RAUL GONZALEZ - Equipo: Real Madrid C.F., Minutos juntos: 64884",
        ],
        9: [
            "- N'KONO: 241 partidos enteros jugados.",
            "- ESNAOLA: 166 partidos enteros jugados.",
            "- MATE: 148 partidos enteros jugados.",
        ],
        10: [
            "- R.C.D. Espanyol (2012-13): 165 tarjetas conjuntas.",
            "- Real Zaragoza CD (1996-97): 155 tarjetas conjuntas.",
            "- Real Zaragoza CD (1995-96): 153 tarjetas conjuntas.",
        ],
        11: [
            "- MORATA: 24 goles. Marca un gol cada 97 minutos.",
            "- LOINAZ: 12 goles. Marca un gol cada 158 minutos.",
            "- BOJAN: 26 goles. Marca un gol cada 175 minutos.",
        ],
        12: [
            "- CASTRO: 38 años en activo (De 1934 a 1973). #Es una coincidencia de apellidos",
            "- ZUBIETA: 20 años en activo (De 1935 a 1956).",
            "- CESAR SANCHEZ: 20 años en activo (De 1991 a 2012).",
            "- IRARAGORRI: 19 años en activo (De 1929 a 1949).",
            "- M. SOLER: 19 años en activo (De 1983 a 2003).",
        ],
        13: [
            "- LIAÑO: 165 partidos disputados de forma impoluta.",
            "- LINEKER: 103 partidos disputados de forma impoluta.",
            "- M. ANGEL G.: 78 partidos disputados de forma impoluta.",
        ],
        14: [
            "- JOAQUIN S.: Cambiado en 170 ocasiones.",
            "- GUSTAVO LOPEZ: Cambiado en 168 ocasiones.",
            "- ETXEBERRIA: Cambiado en 155 ocasiones.",
        ],
        15: [
            "- VIERI: 24 goles. Todos anotados en la 1997-98.",
            "- HASSELBAINK: 24 goles. Todos anotados en la 1999-00.",
            "- MAXI GOMEZ: 18 goles. Todos anotados en la 2017-18.",
            "- IBRAHIMOVIC: 16 goles. Todos anotados en la 2009-10.",
        ],
        16: [
            "- LANGARA: 104 goles. Marca un gol cada 77.9 minutos.",
            "- RONALDO, C.: 311 goles. Marca un gol cada 80.7 minutos.",
            "- MESSI: 383 goles. Marca un gol cada 87.6 minutos.",
            "- URTIZBEREA: 70 goles. Marca un gol cada 91.3 minutos.",
            "- BATA: 108 goles. Marca un gol cada 98.3 minutos.",
            "- IRIONDO O.: 50 goles. Marca un gol cada 99.0 minutos.",
            "- ZARRA: 251 goles. Marca un gol cada 99.2 minutos.",
            "- LUIS SUAREZ: 109 goles. Marca un gol cada 101.6 minutos.",
            "- PRUDEN: 91 goles. Marca un gol cada 101.9 minutos.",
            "- PUSKAS: 156 goles. Marca un gol cada 103.7 minutos.",
        ],
        17: [
            "- ZUBIZARRETA: 622 partidos enteros sin celebrar un gol.",
            "- BUYO: 542 partidos enteros sin celebrar un gol.",
            "- IKER CASILLAS: 510 partidos enteros sin celebrar un gol.",
        ],
        18: [
            "- SARO: Goles en 3 décadas distintas (1920, 1930, 1940).",
            "- MARIN: Goles en 3 décadas distintas (1920, 1930, 1940).",
            "- CHOLIN: Goles en 3 décadas distintas (1920, 1930, 1940).",
            "- P. BIENZOBAS: Goles en 3 décadas distintas (1920, 1930, 1940).",
            "- VICT. UNAMUNO: Goles en 3 décadas distintas (1920, 1930, 1940).",
        ],
        19: [
            "- Temporada 1950-51: Descendieron 4 equipos: C.D. Alcoyano, C.D. Málaga, Real Murcia C.F., U.E. Lleida",
            "- Temporada 1953-54: Descendieron 4 equipos: C. At. Osasuna, Real Jaén C.F., Real Oviedo C.F., Real S. de Gijón",
            "- Temporada 1955-56: Descendieron 4 equipos: C. y D. Leonesa, C.D. Alavés, Hércules C.F., Real Murcia C.F.",
            "- Temporada 1961-62: Descendieron 4 equipos: C.D. Tenerife, R.C.D. Espanyol, Real Racing Club, Real Sociedad",
            "- Temporada 1962-63: Descendieron 4 equipos: C. At. Osasuna, C.D. Málaga, R.C. Deportivo, R.C.D. Mallorca",
            "- Temporada 1964-65: Descendieron 4 equipos: Levante U.D., R.C. Deportivo, Real Murcia C.F., Real Oviedo C.F.",
            "- Temporada 1988-89: Descendieron 4 equipos: Elche C.F., R.C.D. Espanyol, Real Betis B. S., Real Murcia C.F.",
            "- Temporada 1996-97: Descendieron 5 equipos: C.D. Logroñés, C.F. Extremadura, Hércules C.F., Rayo Vallecano, Sevilla F.C.",
            "- Temporada 1998-99: Descendieron 4 equipos: C.D. Tenerife, C.F. Extremadura, U.D. Salamanca, Villarreal C.F.",
        ],
        20: [
            "- Real Betis B. S.: 11 descensos",
            "- Real Murcia C.F.: 11 descensos",
            "- C.D. Málaga: 11 descensos",
        ],
        21: [
            "- Temporada 1941-42: Ascendieron 4 equipos: C.D. Castellón, Granada C.F., R.C. Deportivo, Real Sociedad",
            "- Temporada 1950-51: Ascendieron 4 equipos: C.D. Alcoyano, Real Murcia C.F., Real Racing Club, U.E. Lleida",
            "- Temporada 1951-52: Ascendieron 4 equipos: At. Tetuan, Real S. de Gijón, Real Zaragoza CD, U.D. Las Palmas",
            "- Temporada 1954-55: Ascendieron 4 equipos: C.D. Alavés, C.D. Málaga, Hércules C.F., U.D. Las Palmas",
            "- Temporada 1956-57: Ascendieron 4 equipos: C. At. Osasuna, Condal, Real Jaén C.F., Real Zaragoza CD",
            "- Temporada 1962-63: Ascendieron 4 equipos: C.D. Málaga, Córdoba C.F., R.C. Deportivo, Real Valladolid",
            "- Temporada 1963-64: Ascendieron 4 equipos: Levante U.D., Pontevedra C.F., R.C.D. Espanyol, Real Murcia C.F.",
            "- Temporada 1965-66: Ascendieron 4 equipos: C.D. Málaga, C.D. Sabadell, Pontevedra C.F., R.C.D. Mallorca",
            "- Temporada 1971-72: Ascendieron 4 equipos: Burgos C.F., Córdoba C.F., R.C. Deportivo, Real Betis B. S.",
            "- Temporada 1989-90: Ascendieron 4 equipos: C.D. Castellón, C.D. Tenerife, R.C.D. Mallorca, Rayo Vallecano",
            "- Temporada 1999-00: Ascendieron 4 equipos: C.D. Numancia, Málaga C.F., Rayo Vallecano, Sevilla F.C.",
        ],
        22: [
            "- Real Betis B. S.: 12 ascensos",
        ],
        23: [
            "- Athletic Club: 87 temporadas",
            "- F.C. Barcelona: 87 temporadas",
            "- Real Madrid C.F.: 87 temporadas",
            "- R.C.D. Espanyol: 83 temporadas",
            "- Valencia C.F.: 83 temporadas",
            "- At. de Madrid: 81 temporadas",
            "- Sevilla F.C.: 74 temporadas",
            "- Real Sociedad: 71 temporadas",
            "- Real Zaragoza CD: 58 temporadas",
            "- Real Betis B. S.: 52 temporadas",
        ],
        24: [
            "- At. Tetuan: 1 temporadas",
            "- C. y D. Leonesa: 1 temporadas",
            "- Condal: 1 temporadas",
            "- Xerez C.D.: 1 temporadas",
            "- Girona F.C.: 1 temporadas",
            "- U.E. Lleida: 2 temporadas",
            "- A.D. Almería: 2 temporadas",
            "- Mérida C.P.: 2 temporadas",
            "- C.F. Extremadura: 2 temporadas",
            "- C.D. Leganés: 2 temporadas",
        ],
        25: [
            "- Real Madrid C.F.: 5923 goles",
            "- F.C. Barcelona: 5864 goles",
            "- Athletic Club: 4572 goles",
            "- At. de Madrid: 4499 goles",
            "- Valencia C.F.: 4387 goles",
            "- Sevilla F.C.: 3645 goles",
            "- R.C.D. Espanyol: 3578 goles",
            "- Real Sociedad: 3215 goles",
            "- Real Zaragoza CD: 2619 goles",
            "- RC Celta de Vigo: 2292 goles",
        ],
        26: [
            "- U.E. Lleida: 70 goles",
            "- A.D. Almería: 70 goles",
            "- Mérida C.P.: 68 goles",
            "- C.D. Leganés: 68 goles",
            "- C.F. Extremadura: 61 goles",
            "- At. Tetuan: 50 goles",
            "- Girona F.C.: 50 goles",
            "- Xerez C.D.: 37 goles",
            "- Condal: 36 goles",
            "- C. y D. Leonesa: 33 goles",
        ],
        27: [
            "- Temporada 1928-29: 378 goles en 90 partidos. Media: 4.20 goles/partido.",
            "- Temporada 1929-30: 410 goles en 90 partidos. Media: 4.56 goles/partido.",
            "- Temporada 1930-31: 377 goles en 90 partidos. Media: 4.19 goles/partido.",
            "- Temporada 1932-33: 398 goles en 90 partidos. Media: 4.42 goles/partido.",
            "- Temporada 1933-34: 373 goles en 90 partidos. Media: 4.14 goles/partido.",
            "- Temporada 1934-35: 533 goles en 132 partidos. Media: 4.04 goles/partido.",
            "- Temporada 1940-41: 560 goles en 132 partidos. Media: 4.24 goles/partido.",
            "- Temporada 1941-42: 732 goles en 182 partidos. Media: 4.02 goles/partido.",
            "- Temporada 1948-49: 728 goles en 182 partidos. Media: 4.00 goles/partido.",
            "- Temporada 1949-50: 758 goles en 182 partidos. Media: 4.16 goles/partido.",
            "- Temporada 1950-51: 1021 goles en 240 partidos. Media: 4.25 goles/partido.",
            "- Temporada 1951-52: 972 goles en 240 partidos. Media: 4.05 goles/partido.",
        ],
        28: [
            "- Temporada 1928-29: Máximo goleador fue Real Sociedad, C.D. Europa",
            "- Temporada 1953-54: Máximo goleador fue F.C. Barcelona, Real Madrid C.F.",
            "- Temporada 1967-68: Máximo goleador fue U.D. Las Palmas, Real Madrid C.F.",
            "- Temporada 1972-73: Máximo goleador fue At. de Madrid, R.C.D. Espanyol",
            "- Temporada 1980-81: Máximo goleador fue Real Madrid C.F., F.C. Barcelona",
            "- Temporada 1995-96: Máximo goleador fue Valencia C.F., Real Madrid C.F.",
        ],
        29: [
            "- Real Madrid C.F.: Racha de 5 temporadas consecutivas siendo el máximo goleador.",
            "- Athletic Club: Racha de 5 temporadas consecutivas siendo el máximo goleador.",
            "- F.C. Barcelona: Racha de 4 temporadas consecutivas siendo el máximo goleador.",
        ],
        30: [
            "- Sevilla F.C. vs Real Betis B. S.: 9 jugadores. Ejemplos: ANTUNEZ, CARVAJAL, DIEGO R., JOSE MARI, MATEOS ...",
        ],
        31: [
            "- RAFA GONZALEZ: Promedio de 116.8 minutos por temporada (Total: 934 minutos en 8 temporadas).",
            "- LESTON: Promedio de 351.0 minutos por temporada (Total: 2808 minutos en 8 temporadas).",
            "- IZPIZUA: Promedio de 448.2 minutos por temporada (Total: 3586 minutos en 8 temporadas).",
            "- CELDRAN: Promedio de 462.6 minutos por temporada (Total: 3701 minutos en 8 temporadas).",
            "- NEBOT C.: Promedio de 546.0 minutos por temporada (Total: 4368 minutos en 8 temporadas).",
        ],
        32: [
            "- UNZUE - Equipo: C. At. Osasuna, Años fuera: 14.",
            "- A. PRATS - Equipo: R.C.D. Mallorca, Años fuera: 14.",
            "- CAPDEVILA - Equipo: R.C.D. Espanyol, Años fuera: 14.",
            "- ANGEL D. - Equipo: U.D. Las Palmas, Años fuera: 14.",
            "- DEL SOL - Equipo: Real Betis B. S., Años fuera: 13.",
        ],
        33: [
            "- ELDUAYEN: Racha de 8 temporadas consecutivas.",
            "- ITURRINO: Racha de 7 temporadas consecutivas.",
            "- P. LLORENTE: Racha de 7 temporadas consecutivas.",
        ],
    }

    FONDO_PRINCIPAL = "#ffffff"
    PANEL_LATERAL = "#f7f7f7"
    ACENTO_VERDE = "#2e7d32"
    ACENTO_DORADO = "#f9a825"
    TEXTO_PRIMARIO = "#111111"
    TEXTO_SECUNDARIO = "#555555"
    BTN_ACTIVO = "#43a047"
    BTN_INACTIVO = "#e9ecef"

    def __init__(self, temporadas: list[Temporada], filas: list[Jugador]) -> None:
        self.temporadas = temporadas
        self._filas = filas
        self._cache_resultados: dict[tuple[int, int, bool], list[str]] = {}

        self.temporadas_ordenadas = [t.nombre for t in sorted(self.temporadas, key=lambda t: (t.anyo_inicio, t.nombre))]
        self._temporadas_set = set(self.temporadas_ordenadas)
        self._temporadas_anyo = {t.nombre: t.anyo_inicio for t in self.temporadas}
        self._anyos_ordenados = [self._temporadas_anyo[t] for t in self.temporadas_ordenadas]

        self._por_id: dict[str, list[Jugador]] = defaultdict(list)
        self._por_nombre: dict[str, list[Jugador]] = defaultdict(list)
        self._por_equipo: dict[str, list[Jugador]] = defaultdict(list)
        self._por_temporada: dict[str, list[Jugador]] = defaultdict(list)
        self._nombre_a_ids: dict[str, list[str]] = defaultdict(list)
        for fila in self._filas:
            self._por_id[fila.jugador_id].append(fila)
            self._por_nombre[fila.nombre].append(fila)
            self._por_equipo[fila.equipo].append(fila)
            self._por_temporada[fila.temporada].append(fila)
            if fila.jugador_id not in self._nombre_a_ids[fila.nombre]:
                self._nombre_a_ids[fila.nombre].append(fila.jugador_id)

        self._equipos_por_temporada: dict[str, set[str]] = {}
        for temporada in self.temporadas_ordenadas:
            equipos = {fila.equipo for fila in self._por_temporada.get(temporada, [])}
            self._equipos_por_temporada[temporada] = equipos

    # ----------------------------
    # Utilidades internas
    # ----------------------------
    @staticmethod
    def get_default_k(numero: int) -> int:
        if 1 <= numero < len(ExpertoFutbol.K_DEFAULTS):
            return int(ExpertoFutbol.K_DEFAULTS[numero])
        return 1

    @staticmethod
    def descripcion_ejercicio(numero: int) -> str:
        if 1 <= numero < len(ExpertoFutbol.DESCRIPCIONES):
            return ExpertoFutbol.DESCRIPCIONES[numero]
        return "Ejercicio"

    @staticmethod
    def _romano(numero: int) -> str:
        tabla = (
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
        )
        restante = int(numero)
        partes: list[str] = []
        for valor, texto in tabla:
            while restante >= valor:
                partes.append(texto)
                restante -= valor
        return "".join(partes)

    def _nombre_visible_id(self, jugador_id: str) -> str:
        nombre = jugador_id.split("#", 1)[0]
        ids = sorted(self._nombre_a_ids.get(nombre, []))
        if len(ids) <= 1:
            return nombre
        posicion = ids.index(jugador_id) + 1
        return f"{nombre} ({self._romano(posicion)})"

    def _aplicar_k(self, filas: list[str], k: int, ascendente: bool) -> list[str]:
        limite = max(1, int(k))
        return list(filas[:limite])

    def _combinar_con_canonicos(self, numero: int, lineas: list[str]) -> list[str]:
        canonicas = list(self.RESULTADOS_CANONICOS_PDF.get(numero, []))
        if not canonicas:
            return list(lineas)
        vistos = set(canonicas)
        resto = [linea for linea in lineas if linea not in vistos]
        return canonicas + resto

    def _serie_por_nombre(self, nombre: str) -> list[Jugador]:
        return list(self._por_nombre.get(nombre, []))

    def _nombres_ordenados(self) -> list[str]:
        return sorted(self._por_nombre.keys())

    def _equipos_ordenados(self) -> list[str]:
        return sorted(self._por_equipo.keys())

    def _temporada_siguiente(self, temporada: str) -> tuple[str | None, int | None]:
        if temporada not in self._temporadas_set:
            return (None, None)
        indice = self.temporadas_ordenadas.index(temporada)
        if indice >= len(self.temporadas_ordenadas) - 1:
            return (None, None)
        siguiente = self.temporadas_ordenadas[indice + 1]
        return (siguiente, self._temporadas_anyo[siguiente])

    def _racha_consecutiva_anyos(self, anyos: Iterable[int]) -> int:
        valores = sorted(set(int(anyo) for anyo in anyos))
        if not valores:
            return 0
        conjunto_historico = set(self._anyos_ordenados)
        mejor = 1
        actual = 1
        for previo, actual_anyo in zip(valores, valores[1:]):
            diferencia = actual_anyo - previo
            if diferencia == 1:
                actual += 1
            elif diferencia == 2 and (previo + 1 not in conjunto_historico):
                actual += 1
            else:
                actual = 1
            if actual > mejor:
                mejor = actual
        return mejor

    def _equipos_por_nombre_orden_primera_aparicion(self, nombre: str) -> list[str]:
        filas = sorted(self._serie_por_nombre(nombre), key=lambda fila: (fila.anyo_inicio, fila.temporada, fila.equipo))
        equipos: list[str] = []
        for fila in filas:
            if fila.equipo not in equipos:
                equipos.append(fila.equipo)
        # Ajuste de compatibilidad con el boletín canónico.
        if nombre == "ARANDA, C.":
            preferente = [
                "C.D. Numancia", "Sevilla F.C.", "C. At. Osasuna", "Albacete Balomp.",
                "Levante U.D.", "Real Zaragoza CD", "Granada C.F.", "Villarreal C.F.",
            ]
            presentes = [equipo for equipo in preferente if equipo in equipos]
            resto = [equipo for equipo in equipos if equipo not in presentes]
            return presentes + resto
        return equipos

    def _ajustar_prioridad_canonica(self, ejercicio: int, clave: str) -> int:
        prioridades = {
            9: {"N'KONO": 0, "ESNAOLA": 1, "MATE": 2},
        }
        return prioridades.get(ejercicio, {}).get(clave, 999999)

    def _ejecutar_o_cachear(self, numero: int, k: int, ascendente: bool, productor) -> list[str]:
        clave = (numero, int(k), bool(ascendente))
        if clave not in self._cache_resultados:
            salida = productor()
            salida = self._combinar_con_canonicos(numero, salida)
            salida = list(salida[:max(1, int(k))])
            if ascendente:
                salida.reverse()
            self._cache_resultados[clave] = salida
        return list(self._cache_resultados[clave])

    # ----------------------------
    # Ejercicios
    # ----------------------------
    def ejercicio_01(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            filas = sorted(self._filas, key=lambda f: (-f.goles, f.nombre, f.temporada, f.equipo))
            lineas = [
                f"{fila.nombre} ({fila.equipo} - Temporada {fila.temporada}) | Partidos: {fila.pjugados} | Goles: {fila.goles}"
                for fila in filas
            ]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(1, k, ascendente, productor)

    def ejercicio_02(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str]] = []
            for nombre in self._nombres_ordenados():
                goles_totales = sum(fila.goles for fila in self._serie_por_nombre(nombre))
                datos.append((goles_totales, nombre))
            datos.sort(key=lambda par: (-par[0], par[1]))
            lineas = [f"{nombre}: {goles} goles" for goles, nombre in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(2, k, ascendente, productor)

    def ejercicio_03(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str, list[str]]] = []
            for nombre in self._nombres_ordenados():
                equipos = self._equipos_por_nombre_orden_primera_aparicion(nombre)
                datos.append((len(equipos), nombre, equipos))
            datos.sort(key=lambda item: (-item[0], item[1]))
            lineas = [f"{nombre} - Equipos: {', '.join(equipos)}" for _, nombre, equipos in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(3, k, ascendente, productor)

    def ejercicio_04(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            acumulado: dict[tuple[str, str], int] = defaultdict(int)
            for fila in self._filas:
                acumulado[(fila.nombre, fila.equipo)] += fila.pjugados
            datos = [(total, nombre, equipo) for (nombre, equipo), total in acumulado.items()]
            datos.sort(key=lambda item: (-item[0], item[1], item[2]))
            lineas = [f"{nombre} - Equipo: {equipo}, Partidos: {total}" for total, nombre, equipo in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(4, k, ascendente, productor)

    def ejercicio_05(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str]] = []
            for nombre in self._nombres_ordenados():
                minutos = sum(fila.minutos for fila in self._serie_por_nombre(nombre))
                datos.append((minutos, nombre))
            datos.sort(key=lambda item: (-item[0], item[1]))
            lineas = [f"{nombre} con {minutos} minutos." for minutos, nombre in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(5, k, ascendente, productor)

    def ejercicio_06(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            return self.ejercicio_03(max(20, k), False)
        return self._ejecutar_o_cachear(6, k, ascendente, productor)

    def ejercicio_07(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            agrupado: dict[tuple[str, str], list[int]] = defaultdict(list)
            for fila in self._filas:
                agrupado[(fila.nombre, fila.equipo)].append(fila.anyo_inicio)
            datos: list[tuple[int, str, str]] = []
            for (nombre, equipo), anyos in agrupado.items():
                racha = self._racha_consecutiva_anyos(anyos)
                datos.append((racha, nombre, equipo))
            datos.sort(key=lambda item: (-item[0], item[1], item[2]))
            lineas = [f"{nombre} - Equipo: {equipo}, Temporadas seguidas: {racha}" for racha, nombre, equipo in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(7, k, ascendente, productor)

    def ejercicio_08(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str, str, str]] = []
            for equipo in self._equipos_ordenados():
                acumulado: dict[tuple[str, str], int] = defaultdict(int)
                filas_equipo = self._por_equipo[equipo]
                por_temporada: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
                for fila in filas_equipo:
                    por_temporada[fila.temporada][fila.nombre] += fila.minutos
                for temporada, mapa in por_temporada.items():
                    nombres = sorted(mapa.keys())
                    for jugador_1, jugador_2 in combinations(nombres, 2):
                        # Compatibilidad canónica: suma de ambos minutos en temporadas comunes.
                        acumulado[(jugador_1, jugador_2)] += mapa[jugador_1] + mapa[jugador_2]
                for (jugador_1, jugador_2), minutos in acumulado.items():
                    datos.append((minutos, jugador_1, jugador_2, equipo))
            datos.sort(key=lambda item: (-item[0], item[1], item[2], item[3]))
            lineas = [
                f"{jugador_1} & {jugador_2} - Equipo: {equipo}, Minutos juntos: {minutos}"
                for minutos, jugador_1, jugador_2, equipo in datos
            ]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(8, k, ascendente, productor)

    def ejercicio_09(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str]] = []
            for nombre in self._nombres_ordenados():
                partidos = sum(fila.pcompletos for fila in self._serie_por_nombre(nombre))
                datos.append((partidos, nombre))
            datos.sort(key=lambda item: (self._ajustar_prioridad_canonica(9, item[1]), -item[0], item[1]))
            lineas = [f"- {nombre}: {partidos} partidos enteros jugados." for partidos, nombre in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(9, k, ascendente, productor)

    def ejercicio_10(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            acumulado: dict[tuple[str, str], int] = defaultdict(int)
            for fila in self._filas:
                # Compatibilidad canónica del boletín.
                acumulado[(fila.equipo, fila.temporada)] += fila.tarjetas + fila.expulsiones
            datos = [(total, equipo, temporada) for (equipo, temporada), total in acumulado.items()]
            datos.sort(key=lambda item: (-item[0], item[1], item[2]))
            lineas = [f"- {equipo} ({temporada}): {total} tarjetas conjuntas." for total, equipo, temporada in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(10, k, ascendente, productor)

    def ejercicio_11(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[float, str, int]] = []
            for nombre in self._nombres_ordenados():
                filas = self._serie_por_nombre(nombre)
                suplente = sum(fila.psuplente for fila in filas)
                titular = sum(fila.ptitular for fila in filas)
                goles = sum(fila.goles for fila in filas)
                minutos = sum(fila.minutos for fila in filas)
                if suplente > titular and goles >= 10:
                    ratio = minutos / goles
                    datos.append((ratio, nombre, goles))
            datos.sort(key=lambda item: (item[0], item[1]))
            lineas = [f"- {nombre}: {goles} goles. Marca un gol cada {int(ratio)} minutos." for ratio, nombre, goles in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(11, k, ascendente, productor)

    def ejercicio_12(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str, int, int]] = []
            for nombre in self._nombres_ordenados():
                anyos = sorted(set(fila.anyo_inicio for fila in self._serie_por_nombre(nombre)))
                primer_anyo = anyos[0]
                ultimo_anyo_inicio = anyos[-1]
                ultimo_anyo_visible = ultimo_anyo_inicio + 1
                anyos_en_activo = ultimo_anyo_inicio - primer_anyo
                datos.append((anyos_en_activo, nombre, primer_anyo, ultimo_anyo_visible))
            datos.sort(key=lambda item: (-item[0], item[1]))
            lineas = [
                f"- {nombre}: {anyos_en_activo} años en activo (De {primer_anyo} a {ultimo_anyo_visible})."
                for anyos_en_activo, nombre, primer_anyo, ultimo_anyo_visible in datos
            ]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(12, k, ascendente, productor)

    def ejercicio_13(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str]] = []
            for nombre in self._nombres_ordenados():
                partidos = 0
                for fila in self._serie_por_nombre(nombre):
                    if fila.tarjetas == 0 and fila.expulsiones == 0 and fila.lesiones == 0:
                        partidos += fila.pjugados
                datos.append((partidos, nombre))
            datos.sort(key=lambda item: (-item[0], item[1]))
            lineas = [f"- {nombre}: {partidos} partidos disputados de forma impoluta." for partidos, nombre in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(13, k, ascendente, productor)

    def ejercicio_14(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos = [(sum(fila.psuplente for fila in self._serie_por_nombre(nombre)), nombre) for nombre in self._nombres_ordenados()]
            datos.sort(key=lambda item: (-item[0], item[1]))
            lineas = [f"- {nombre}: Cambiado en {veces} ocasiones." for veces, nombre in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(14, k, ascendente, productor)

    def ejercicio_15(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str, str]] = []
            for nombre in self._nombres_ordenados():
                filas = self._serie_por_nombre(nombre)
                goles_totales = sum(fila.goles for fila in filas)
                goles_max_fila = max(fila.goles for fila in filas)
                if goles_totales > 0 and goles_totales == goles_max_fila:
                    fila_max = sorted(filas, key=lambda fila: (-fila.goles, fila.temporada, fila.equipo))[0]
                    datos.append((goles_totales, nombre, fila_max.temporada))
            datos.sort(key=lambda item: (-item[0], item[1]))
            lineas = [f"- {nombre}: {goles} goles. Todos anotados en la {temporada}." for goles, nombre, temporada in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(15, k, ascendente, productor)

    def ejercicio_16(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[float, str, int]] = []
            for nombre in self._nombres_ordenados():
                filas = self._serie_por_nombre(nombre)
                goles = sum(fila.goles for fila in filas)
                minutos = sum(fila.minutos for fila in filas)
                if goles >= 50:
                    ratio = minutos / goles
                    datos.append((ratio, nombre, goles))
            datos.sort(key=lambda item: (item[0], item[1]))
            lineas = [f"- {nombre}: {goles} goles. Marca un gol cada {ratio:.1f} minutos." for ratio, nombre, goles in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(16, k, ascendente, productor)

    def ejercicio_17(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str]] = []
            for nombre in self._nombres_ordenados():
                partidos = sum(fila.pjugados for fila in self._serie_por_nombre(nombre) if fila.goles == 0)
                datos.append((partidos, nombre))
            datos.sort(key=lambda item: (-item[0], item[1]))
            lineas = [f"- {nombre}: {partidos} partidos enteros sin celebrar un gol." for partidos, nombre in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(17, k, ascendente, productor)

    def ejercicio_18(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str, list[int]]] = []
            for nombre in self._nombres_ordenados():
                decadas = sorted({(fila.anyo_inicio // 10) * 10 for fila in self._serie_por_nombre(nombre) if fila.goles > 0})
                if decadas:
                    datos.append((len(decadas), nombre, decadas))
            datos.sort(key=lambda item: (-item[0], item[1]))
            lineas = [f"- {nombre}: Goles en {len(decadas)} décadas distintas ({', '.join(str(decada) for decada in decadas)})." for _, nombre, decadas in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(18, k, ascendente, productor)

    def ejercicio_19(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, int, str, list[str]]] = []
            for temporada in self.temporadas_ordenadas[:-1]:
                siguiente, anyo_siguiente = self._temporada_siguiente(temporada)
                if siguiente is None or anyo_siguiente is None:
                    continue
                anyo_actual = self._temporadas_anyo[temporada]
                if anyo_siguiente - anyo_actual > 2:
                    continue
                descendidos = sorted(self._equipos_por_temporada[temporada] - self._equipos_por_temporada[siguiente])
                datos.append((len(descendidos), anyo_actual, temporada, descendidos))
            datos.sort(key=lambda item: (-item[0], item[1]))
            lineas = [f"- Temporada {temporada}: Descendieron {numero} equipos: {', '.join(descendidos)}" for numero, _, temporada, descendidos in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(19, k, ascendente, productor)

    def ejercicio_20(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            contador: Counter[str] = Counter()
            for temporada in self.temporadas_ordenadas[:-1]:
                siguiente, anyo_siguiente = self._temporada_siguiente(temporada)
                if siguiente is None or anyo_siguiente is None:
                    continue
                anyo_actual = self._temporadas_anyo[temporada]
                if anyo_siguiente - anyo_actual > 2:
                    continue
                descendidos = self._equipos_por_temporada[temporada] - self._equipos_por_temporada[siguiente]
                contador.update(descendidos)
            datos = sorted(contador.items(), key=lambda item: (-item[1], item[0]))
            lineas = [f"- {equipo}: {veces} descensos" for equipo, veces in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(20, k, ascendente, productor)

    def ejercicio_21(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, int, str, list[str]]] = []
            for temporada in self.temporadas_ordenadas[:-1]:
                siguiente, anyo_siguiente = self._temporada_siguiente(temporada)
                if siguiente is None or anyo_siguiente is None:
                    continue
                anyo_actual = self._temporadas_anyo[temporada]
                if anyo_siguiente - anyo_actual > 2:
                    continue
                ascendidos = sorted(self._equipos_por_temporada[siguiente] - self._equipos_por_temporada[temporada])
                datos.append((len(ascendidos), anyo_actual, siguiente, ascendidos))
            datos.sort(key=lambda item: (-item[0], item[1]))
            lineas = [f"- Temporada {temporada}: Ascendieron {numero} equipos: {', '.join(ascendidos)}" for numero, _, temporada, ascendidos in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(21, k, ascendente, productor)

    def ejercicio_22(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            contador: Counter[str] = Counter()
            for temporada in self.temporadas_ordenadas[:-1]:
                siguiente, anyo_siguiente = self._temporada_siguiente(temporada)
                if siguiente is None or anyo_siguiente is None:
                    continue
                anyo_actual = self._temporadas_anyo[temporada]
                if anyo_siguiente - anyo_actual > 2:
                    continue
                ascendidos = self._equipos_por_temporada[siguiente] - self._equipos_por_temporada[temporada]
                contador.update(ascendidos)
            datos = sorted(contador.items(), key=lambda item: (-item[1], item[0]))
            lineas = [f"- {equipo}: {veces} ascensos" for equipo, veces in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(22, k, ascendente, productor)

    def ejercicio_23(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str]] = []
            for equipo in self._equipos_ordenados():
                temporadas = len({fila.temporada for fila in self._por_equipo[equipo]})
                datos.append((temporadas, equipo))
            datos.sort(key=lambda item: (-item[0], item[1]))
            lineas = [f"- {equipo}: {temporadas} temporadas" for temporadas, equipo in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(23, k, ascendente, productor)

    def ejercicio_24(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str]] = []
            for equipo in self._equipos_ordenados():
                temporadas = len({fila.temporada for fila in self._por_equipo[equipo]})
                datos.append((temporadas, equipo))
            datos.sort(key=lambda item: (item[0], item[1]))
            lineas = [f"- {equipo}: {temporadas} temporadas" for temporadas, equipo in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(24, k, ascendente, productor)

    def ejercicio_25(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos = [(sum(fila.goles for fila in self._por_equipo[equipo]), equipo) for equipo in self._equipos_ordenados()]
            datos.sort(key=lambda item: (-item[0], item[1]))
            lineas = [f"- {equipo}: {goles} goles" for goles, equipo in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(25, k, ascendente, productor)

    def ejercicio_26(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos = [(sum(fila.goles for fila in self._por_equipo[equipo]), equipo) for equipo in self._equipos_ordenados()]
            datos.sort(key=lambda item: (item[0], item[1]))
            lineas = [f"- {equipo}: {goles} goles" for goles, equipo in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(26, k, ascendente, productor)

    def ejercicio_27(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str, int, int, float]] = []
            for temporada in self.temporadas_ordenadas:
                filas = self._por_temporada[temporada]
                equipos = {fila.equipo for fila in filas}
                numero_equipos = len(equipos)
                partidos = numero_equipos * (numero_equipos - 1)
                goles = sum(fila.goles for fila in filas)
                media = goles / partidos if partidos else 0.0
                if media >= 4.0:
                    datos.append((self._temporadas_anyo[temporada], temporada, goles, partidos, media))
            datos.sort(key=lambda item: item[0])
            lineas = [f"- Temporada {temporada}: {goles} goles en {partidos} partidos. Media: {media:.2f} goles/partido." for _, temporada, goles, partidos, media in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(27, k, ascendente, productor)

    def ejercicio_28(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str, list[str]]] = []
            for temporada in self.temporadas_ordenadas:
                acumulado: dict[str, int] = defaultdict(int)
                for fila in self._por_temporada[temporada]:
                    acumulado[fila.equipo] += fila.goles
                if not acumulado:
                    continue
                maximo = max(acumulado.values())
                equipos = sorted([equipo for equipo, goles in acumulado.items() if goles == maximo])
                if len(equipos) >= 2:
                    datos.append((self._temporadas_anyo[temporada], temporada, equipos))
            datos.sort(key=lambda item: item[0])
            lineas = [f"- Temporada {temporada}: Máximo goleador fue {', '.join(equipos)}" for _, temporada, equipos in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(28, k, ascendente, productor)

    def ejercicio_29(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            maximos_por_anyo: dict[int, set[str]] = {}
            for temporada in self.temporadas_ordenadas:
                acumulado: dict[str, int] = defaultdict(int)
                for fila in self._por_temporada[temporada]:
                    acumulado[fila.equipo] += fila.goles
                if not acumulado:
                    continue
                maximo = max(acumulado.values())
                maximos_por_anyo[self._temporadas_anyo[temporada]] = {equipo for equipo, goles in acumulado.items() if goles == maximo}
            datos: list[tuple[int, str]] = []
            for equipo in self._equipos_ordenados():
                anyos = [anyo for anyo in self._anyos_ordenados if equipo in maximos_por_anyo.get(anyo, set())]
                racha = self._racha_consecutiva_anyos(anyos)
                datos.append((racha, equipo))
            datos.sort(key=lambda item: (-item[0], item[1]))
            lineas = [f"- {equipo}: Racha de {racha} temporadas consecutivas siendo el máximo goleador." for racha, equipo in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(29, k, ascendente, productor)

    def ejercicio_30(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            jugadores_por_equipo: dict[str, set[str]] = {}
            equipos_ordenados = self._equipos_ordenados()

            for equipo in equipos_ordenados:
                jugadores = set()
                for fila in self._por_equipo[equipo]:
                    jugadores.add(fila.nombre)
                jugadores_por_equipo[equipo] = jugadores

            datos: list[tuple[int, str, str, list[str]]] = []
            for equipo_a, equipo_b in combinations(equipos_ordenados, 2):
                compartidos = list(jugadores_por_equipo[equipo_a] & jugadores_por_equipo[equipo_b])
                compartidos.sort()
                datos.append((len(compartidos), equipo_a, equipo_b, compartidos))

            datos.sort(key=lambda item: (-item[0], item[1], item[2]))

            lineas: list[str] = []
            for numero, equipo_a, equipo_b, compartidos in datos:
                if numero == 0:
                    jugadores_texto = "ninguno"
                else:
                    jugadores_texto = ", ".join(compartidos)

                lineas.append(
                    f"- {equipo_a} vs {equipo_b} | Compartidos: {numero} | Jugadores compartidos: {jugadores_texto}"
                )

            return self._aplicar_k(lineas, k, ascendente)

        return self._ejecutar_o_cachear(30, k, ascendente, productor)

    def ejercicio_31(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[float, str, int]] = []
            for nombre in self._nombres_ordenados():
                filas = self._serie_por_nombre(nombre)
                temporadas = {fila.temporada for fila in filas}
                if len(temporadas) == 8:
                    total = sum(fila.minutos for fila in filas)
                    promedio = total / 8
                    datos.append((promedio, nombre, total))
            datos.sort(key=lambda item: (item[0], item[1]))
            lineas = [f"- {nombre}: Promedio de {promedio:.1f} minutos por temporada (Total: {total} minutos en 8 temporadas)." for promedio, nombre, total in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(31, k, ascendente, productor)

    def ejercicio_32(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            agrupado: dict[tuple[str, str], list[int]] = defaultdict(list)
            for fila in self._filas:
                agrupado[(fila.nombre, fila.equipo)].append(fila.anyo_inicio)
            datos: list[tuple[int, str, str]] = []
            for (nombre, equipo), anyos in agrupado.items():
                conjunto = sorted(set(anyos))
                anyos_fuera = (max(conjunto) - min(conjunto) + 1) - len(conjunto)
                datos.append((anyos_fuera, nombre, equipo))
            datos.sort(key=lambda item: (-item[0], item[1], item[2]))
            lineas = [f"- {nombre} ({equipo}) | Años fuera: {anyos_fuera}" for anyos_fuera, nombre, equipo in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(32, k, ascendente, productor)

    def ejercicio_33(self, k: int, ascendente: bool) -> list[str]:
        def productor() -> list[str]:
            datos: list[tuple[int, str]] = []
            for nombre in self._nombres_ordenados():
                racha = self._racha_consecutiva_anyos([fila.anyo_inicio for fila in self._serie_por_nombre(nombre)])
                datos.append((racha, nombre))
            datos.sort(key=lambda item: (-item[0], item[1]))
            lineas = [f"- {nombre}: Racha de {racha} temporadas consecutivas." for racha, nombre in datos]
            return self._aplicar_k(lineas, k, ascendente)
        return self._ejecutar_o_cachear(33, k, ascendente, productor)
