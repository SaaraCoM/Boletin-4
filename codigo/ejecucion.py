from __future__ import annotations

import sys

from experto_futbol import ExpertoFutbol
from factoria_futbol import FactoriaFutbol


def ejecutar_tests() -> tuple[object, str]:
    ruta_excel = FactoriaFutbol.resolver_ruta_excel("Plantillas1D-2017-18.xls")
    experto = FactoriaFutbol.cargar_excel(ruta_excel)
    errores: list[str] = []

    def check(n: int, cond: bool, esperado: str, obtenido) -> None:
        if not cond:
            errores.append(f"❌ Ej{n:02d}: esperado '{esperado}', obtenido '{obtenido}'")
        else:
            print(f"✅ Ej{n:02d}: OK")

    r = {
        i: getattr(experto, f"ejercicio_{i:02d}")(ExpertoFutbol.get_default_k(i), False)
        for i in range(1, 34)
    }

    check(1,  "MESSI" in r[1][0] and "2011-12" in r[1][0] and "50" in r[1][0], "MESSI...2011-12...50", r[1][0])
    check(2,  "MESSI" in r[2][0] and "383" in r[2][0], "MESSI: 383 goles", r[2][0])
    check(3,  "ARANDA" in r[3][0] and "Numancia" in r[3][0], "ARANDA...Numancia", r[3][0])
    check(4,  "RAUL GONZALEZ" in r[4][0] and "550" in r[4][0], "RAUL GONZALEZ...550", r[4][0])
    check(5,  "ZUBIZARRETA" in r[5][0] and "55746" in r[5][0], "ZUBIZARRETA...55746", r[5][0])
    check(7,  any("GAINZA" in linea and "19" in linea for linea in r[7]), "GAINZA...19", r[7])
    check(8,  "GORRIZ" in r[8][0] and "76143" in r[8][0], "GORRIZ & LARRAÑAGA...76143", r[8][0])
    check(9,  "N'KONO" in r[9][0] and "241" in r[9][0], "N'KONO: 241", r[9][0])
    check(10, "Espanyol" in r[10][0] and "165" in r[10][0], "R.C.D. Espanyol...165", r[10][0])
    check(11, "MORATA" in r[11][0] and "97" in r[11][0], "MORATA...97", r[11][0])
    check(12, "CASTRO" in r[12][0] and "38" in r[12][0], "CASTRO...38", r[12][0])
    check(16, "LANGARA" in r[16][0] and "77.9" in r[16][0], "LANGARA...77.9", r[16][0])
    check(20, any("Real Betis" in linea and "11" in linea for linea in r[20]), "Real Betis...11 descensos", r[20])
    check(23, any("Athletic Club" in linea and "87" in linea for linea in r[23]), "Athletic Club...87", r[23])
    check(25, "Real Madrid" in r[25][0] and "5923" in r[25][0], "Real Madrid...5923", r[25][0])
    check(27, "1928-29" in r[27][0] and "4.20" in r[27][0], "1928-29...4.20", r[27][0])
    check(31, "RAFA GONZALEZ" in r[31][0] and "116.8" in r[31][0], "RAFA GONZALEZ...116.8", r[31][0])

    if errores:
        print("\n".join(errores))
        print("\n⚠️ Corrige los errores antes de lanzar la interfaz.")
        sys.exit(1)

    print("\n✅ Todos los tests pasaron. Lanzando interfaz...")
    return experto, ruta_excel


if __name__ == "__main__":
    experto, ruta_excel = ejecutar_tests()
    try:
        from interfaz import AppFutbol
    except ModuleNotFoundError as error:
        print(f"\nNo se pudo abrir la interfaz: {error}")
        print("Instala las dependencias necesarias, por ejemplo:")
        print("pip install customtkinter openpyxl xlrd pillow")
        sys.exit(1)

    app = AppFutbol(experto_inicial=experto, ruta_inicial=ruta_excel)
    app.mainloop()
