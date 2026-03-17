from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from equipo import Equipo
from jugador import Jugador
from temporada import Temporada


@dataclass
class Liga:
    temporadas: dict[str, Temporada] = field(default_factory=dict)

    def agregar_temporada(self, temporada: Temporada) -> None:
        self.temporadas[temporada.identificador] = temporada

    @property
    def num_temporadas(self) -> int:
        return len(self.temporadas)

    @property
    def num_temporadas_no_jugadas(self) -> int:
        return sum(1 for temporada in self.temporadas.values() if temporada.num_partidos == 0)

    def _iterar_historial(self) -> Iterator[tuple[Temporada, Equipo, Jugador]]:
        """
        Itera sobre toda la base de datos y devuelve una tupla con el contexto:
        (Objeto Temporada, Objeto Equipo, Objeto Jugador)
        """
        for temporada in self.temporadas.values():
            for equipo in temporada.equipos.values():
                for jugador in equipo.jugadores:
                    yield temporada, equipo, jugador

    def _construir_experto(self):
        from experto_futbol import ExpertoFutbol

        temporadas = list(self.temporadas.values())
        filas: list[Jugador] = [jugador for _, _, jugador in self._iterar_historial()]
        return ExpertoFutbol(temporadas=temporadas, filas=filas)

    @staticmethod
    def get_default_k(numero: int) -> int:
        from experto_futbol import ExpertoFutbol

        return ExpertoFutbol.get_default_k(numero)



def _crear_wrapper(indice: int):
    def _wrapper(self: Liga, k: int, ascendente: bool):
        experto = self._construir_experto()
        return getattr(experto, f"ejercicio_{indice:02d}")(k, ascendente)

    _wrapper.__name__ = f"ejercicio_{indice:02d}"
    return _wrapper


for _i in range(1, 34):
    setattr(Liga, f"ejercicio_{_i:02d}", _crear_wrapper(_i))
