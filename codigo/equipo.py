from __future__ import annotations

from dataclasses import dataclass, field

from jugador import Jugador


@dataclass
class Equipo:
    nombre: str
    temporada: str
    jugadores: list[Jugador] = field(default_factory=list)

    def agregar_jugador(self, jugador: Jugador) -> None:
        self.jugadores.append(jugador)
        if not self.temporada:
            self.temporada = jugador.temporada

    @property
    def goles_marcados(self) -> int:
        return sum(jugador.goles for jugador in self.jugadores)

    @property
    def num_jugadores(self) -> int:
        return len(self.jugadores)

    @property
    def partidos_jugados(self) -> int:
        return sum(jugador.pjugados for jugador in self.jugadores)

    @property
    def total_tarjetas(self) -> int:
        return sum(jugador.tarjetas_totales for jugador in self.jugadores)

    @property
    def filas(self) -> list[Jugador]:
        return self.jugadores

    @filas.setter
    def filas(self, valor: list[Jugador]) -> None:
        self.jugadores = valor
