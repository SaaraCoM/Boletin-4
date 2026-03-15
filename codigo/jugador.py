from dataclasses import dataclass


@dataclass
class Jugador:
    jugador_id: str
    nombre: str
    equipo: str
    temporada: str
    anyo_inicio: int
    pjugados: int
    pcompletos: int
    ptitular: int
    psuplente: int
    minutos: int
    lesiones: int
    tarjetas: int
    expulsiones: int
    goles: int
    pen_fallados: int
