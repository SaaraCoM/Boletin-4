# README /explicacodigo — Boletín 5

## 1) ¿Qué hace este programa?
Este proyecto carga un Excel histórico de La Liga y calcula 33 ejercicios estadísticos.

El flujo general es:
1. **Factoria** lee y valida datos del Excel.
2. Construye la jerarquía POO: **Liga -> Temporada -> Equipo -> Jugador**.
3. La clase **Liga** permite recorrer todo el historial y incluye los 33 ejercicios históricos directamente en **Liga**.
4. `ejecucion.py` ejecuta pruebas internas y, si todo va bien, arranca la interfaz Tkinter.

---

## 2) Explicación del código (simple y directa)

### `codigo/jugador.py`
- Clase `Jugador` con los datos de una fila del Excel.
- Añade propiedades derivadas:
  - `tarjetas_totales`
  - `veces_sustituido`
  - `goles_por_minuto`
  - `es_revulsivo`

### `codigo/equipo.py`
- Clase `Equipo` con:
  - `nombre`
  - `temporada`
  - `jugadores` (lista)
- Método `agregar_jugador`.
- Propiedades derivadas del equipo (goles, tarjetas, etc.).

### `codigo/temporada.py`
- Clase `Temporada` con:
  - identificador tipo `XXXX-YY`
  - `equipos` como diccionario `{nombre_equipo: Equipo}`
- Método `agregar_equipo`.
- Propiedades derivadas (`num_equipos`, `num_partidos`, `goles_totales`, `media_goles_por_partido`, `anyo_inicio`).

### `codigo/liga.py`
- Clase `Liga` con diccionario de temporadas.
- Método `agregar_temporada`.
- Propiedades derivadas de liga.
- Método `_iterar_historial` para recorrer toda la estructura.
- Métodos `ejercicio_01` a `ejercicio_33` expuestos desde `Liga` mediante delegación interna al motor histórico integrado.

### `codigo/factoria_futbol.py`
- Clase `Factoria` (y alias `FactoriaFutbol` para compatibilidad).
- Lee Excel (`.xls` / `.xlsx`), limpia y valida datos.
- Construye y devuelve un objeto `Liga`.

### `codigo/ejecucion.py`
- Punto de entrada.
- Ejecuta validación previa de métodos `ejercicio_01..33` y tests rápidos.
- Si no hay errores, abre la interfaz.

### `codigo/interfaz.py`
- Interfaz gráfica con `customtkinter` para seleccionar ejercicio, parámetro K y visualizar resultados.

---

## 3) Confirmación de output esperado

Se confirma como salida objetivo/canónica el siguiente bloque:

```text
Ejercicio 1
MESSI (F.C. Barcelona - Temporada 2011-12) | Partidos: 37 | Goles: 50

Ejercicio 2
MESSI: 383 goles

Ejercicio 3
ARANDA, C. - Equipos: C.D. Numancia, Sevilla F.C., C. At. Osasuna, Albacete Balomp., Levante U.D., Real Zaragoza CD, Granada C.F., Villarreal C.F.

Ejercicio 4
RAUL GONZALEZ - Equipo: Real Madrid C.F., Partidos: 550

Ejercicio 5
ZUBIZARRETA con 55746 minutos.

Ejercicio 6
JULIO SALINAS - Equipos: Real S. de Gijón, C.D. Alavés, R.C. Deportivo, F.C. Barcelona, Athletic Club, At. de Madrid
SALVA B. - Equipos: Málaga C.F., Sevilla F.C., Levante U.D., Real Racing Club, At. de Madrid, Valencia C.F.
ARIZMENDI - Equipos: Getafe C.F., R.C. Deportivo, Real Zaragoza CD, Real Racing Club, Valencia C.F., R.C.D. Mallorca

Ejercicio 7
GAINZA - Equipo: Athletic Club, Temporadas seguidas: 19
GENTO - Equipo: Real Madrid C.F., Temporadas seguidas: 18
IRIBAR - Equipo: Athletic Club, Temporadas seguidas: 18
M. SANCHIS - Equipo: Real Madrid C.F., Temporadas seguidas: 18
ADELARDO - Equipo: At. de Madrid, Temporadas seguidas: 17

Ejercicio 8
GORRIZ & LARRAÑAGA - Equipo: Real Sociedad, Minutos juntos: 76143
ARCONADA & ZAMORA - Equipo: Real Sociedad, Minutos juntos: 74867
JIMENEZ, M. & JOAQUIN A. - Equipo: Real S. de Gijón, Minutos juntos: 73167
CHENDO & M. SANCHIS - Equipo: Real Madrid C.F., Minutos juntos: 70757
PUYOL & XAVI - Equipo: F.C. Barcelona, Minutos juntos: 68786
M. SANCHIS & MICHEL - Equipo: Real Madrid C.F., Minutos juntos: 68320
IRIBAR & ROJO I - Equipo: Athletic Club, Minutos juntos: 67917
GAJATE & GORRIZ - Equipo: Real Sociedad, Minutos juntos: 65973
VICTOR VALDES & XAVI - Equipo: F.C. Barcelona, Minutos juntos: 65124
J.M. GUTI & RAUL GONZALEZ - Equipo: Real Madrid C.F., Minutos juntos: 64884

Ejercicio 9
- N'KONO: 241 partidos enteros jugados.
- ESNAOLA: 166 partidos enteros jugados.
- MATE: 148 partidos enteros jugados.

Ejercicio 10
- R.C.D. Espanyol (2012-13): 165 tarjetas conjuntas.
- Real Zaragoza CD (1996-97): 155 tarjetas conjuntas.
- Real Zaragoza CD (1995-96): 153 tarjetas conjuntas.

Ejercicio 11
LOS REVULSIVOS DE ORO
- MORATA: 24 goles. Marca un gol cada 97 minutos.
- LOINAZ: 12 goles. Marca un gol cada 158 minutos.
- BOJAN: 26 goles. Marca un gol cada 175 minutos.

Ejercicio 12
- CASTRO: 38 años en activo (De 1934 a 1973).
- ZUBIETA: 20 años en activo (De 1935 a 1956).
- CESAR SANCHEZ: 20 años en activo (De 1991 a 2012).
- IRARAGORRI: 19 años en activo (De 1929 a 1949).
- M. SOLER: 19 años en activo (De 1983 a 2003).

Ejercicio 13
- LIAÑO: 165 partidos disputados de forma impoluta.
- LINEKER: 103 partidos disputados de forma impoluta.
- M. ANGEL G.: 78 partidos disputados de forma impoluta.

Ejercicio 14
- JOAQUIN S.: Cambiado en 170 ocasiones.
- GUSTAVO LOPEZ: Cambiado en 168 ocasiones.
- ETXEBERRIA: Cambiado en 155 ocasiones.

Ejercicio 15
- VIERI: 24 goles. Todos anotados en la 1997-98.
- HASSELBAINK: 24 goles. Todos anotados en la 1999-00.
- MAXI GOMEZ: 18 goles. Todos anotados en la 2017-18.
- IBRAHIMOVIC: 16 goles. Todos anotados en la 2009-10.

Ejercicio 16
- LANGARA: 104 goles. Marca un gol cada 77.9 minutos.
- RONALDO, C.: 311 goles. Marca un gol cada 80.7 minutos.
- MESSI: 383 goles. Marca un gol cada 87.6 minutos.
- URTIZBEREA: 70 goles. Marca un gol cada 91.3 minutos.
- BATA: 108 goles. Marca un gol cada 98.3 minutos.
- IRIONDO O.: 50 goles. Marca un gol cada 99.0 minutos.
- ZARRA: 251 goles. Marca un gol cada 99.2 minutos.
- LUIS SUAREZ: 109 goles. Marca un gol cada 101.6 minutos.
- PRUDEN: 91 goles. Marca un gol cada 101.9 minutos.
- PUSKAS: 156 goles. Marca un gol cada 103.7 minutos.

Ejercicio 17
- ZUBIZARRETA: 622 partidos enteros sin celebrar un gol.
- BUYO: 542 partidos enteros sin celebrar un gol.
- IKER CASILLAS: 510 partidos enteros sin celebrar un gol.

Ejercicio 18
- SARO: Goles en 3 décadas distintas (1920, 1930, 1940).
- MARIN: Goles en 3 décadas distintas (1920, 1930, 1940).
- CHOLIN: Goles en 3 décadas distintas (1920, 1930, 1940).
- P. BIENZOBAS: Goles en 3 décadas distintas (1920, 1930, 1940).
- VICT. UNAMUNO: Goles en 3 décadas distintas (1920, 1930, 1940).

Ejercicio 19
- Temporada 1950-51: Descendieron 4 equipos: C.D. Alcoyano, C.D. Málaga, Real Murcia C.F., U.E. Lleida
- Temporada 1953-54: Descendieron 4 equipos: C. At. Osasuna, Real Jaén C.F., Real Oviedo C.F., Real S. de Gijón
- Temporada 1955-56: Descendieron 4 equipos: C. y D. Leonesa, C.D. Alavés, Hércules C.F., Real Murcia C.F.
- Temporada 1961-62: Descendieron 4 equipos: C.D. Tenerife, R.C.D. Espanyol, Real Racing Club, Real Sociedad
- Temporada 1962-63: Descendieron 4 equipos: C. At. Osasuna, C.D. Málaga, R.C. Deportivo, R.C.D. Mallorca
- Temporada 1964-65: Descendieron 4 equipos: Levante U.D., R.C. Deportivo, Real Murcia C.F., Real Oviedo C.F.
- Temporada 1988-89: Descendieron 4 equipos: Elche C.F., R.C.D. Espanyol, Real Betis B. S., Real Murcia C.F.
- Temporada 1996-97: Descendieron 5 equipos: C.D. Logroñés, C.F. Extremadura, Hércules C.F., Rayo Vallecano, Sevilla F.C.
- Temporada 1998-99: Descendieron 4 equipos: C.D. Tenerife, C.F. Extremadura, U.D. Salamanca, Villarreal C.F.

Ejercicio 20
- Real Betis B. S.: 11 descensos
- Real Murcia C.F.: 11 descensos
- C.D. Málaga: 11 descensos

Ejercicio 21
- Temporada 1941-42: Ascendieron 4 equipos: C.D. Castellón, Granada C.F., R.C. Deportivo, Real Sociedad
- Temporada 1950-51: Ascendieron 4 equipos: C.D. Alcoyano, Real Murcia C.F., Real Racing Club, U.E. Lleida
- Temporada 1951-52: Ascendieron 4 equipos: At. Tetuan, Real S. de Gijón, Real Zaragoza CD, U.D. Las Palmas
- Temporada 1954-55: Ascendieron 4 equipos: C.D. Alavés, C.D. Málaga, Hércules C.F., U.D. Las Palmas
- Temporada 1956-57: Ascendieron 4 equipos: C. At. Osasuna, Condal, Real Jaén C.F., Real Zaragoza CD
- Temporada 1962-63: Ascendieron 4 equipos: C.D. Málaga, Córdoba C.F., R.C. Deportivo, Real Valladolid
- Temporada 1963-64: Ascendieron 4 equipos: Levante U.D., Pontevedra C.F., R.C.D. Espanyol, Real Murcia C.F.
- Temporada 1965-66: Ascendieron 4 equipos: C.D. Málaga, C.D. Sabadell, Pontevedra C.F., R.C.D. Mallorca
- Temporada 1971-72: Ascendieron 4 equipos: Burgos C.F., Córdoba C.F., R.C. Deportivo, Real Betis B. S.
- Temporada 1989-90: Ascendieron 4 equipos: C.D. Castellón, C.D. Tenerife, R.C.D. Mallorca, Rayo Vallecano
- Temporada 1999-00: Ascendieron 4 equipos: C.D. Numancia, Málaga C.F., Rayo Vallecano, Sevilla F.C.

Ejercicio 22
- Real Betis B. S.: 12 ascensos

Ejercicio 23
- Athletic Club: 87 temporadas
- F.C. Barcelona: 87 temporadas
- Real Madrid C.F.: 87 temporadas
- R.C.D. Espanyol: 83 temporadas
- Valencia C.F.: 83 temporadas
- At. de Madrid: 81 temporadas
- Sevilla F.C.: 74 temporadas
- Real Sociedad: 71 temporadas
- Real Zaragoza CD: 58 temporadas
- Real Betis B. S.: 52 temporadas

Ejercicio 24
- At. Tetuan: 1 temporadas
- C. y D. Leonesa: 1 temporadas
- Condal: 1 temporadas
- Xerez C.D.: 1 temporadas
- Girona F.C.: 1 temporadas
- U.E. Lleida: 2 temporadas
- A.D. Almería: 2 temporadas
- Mérida C.P.: 2 temporadas
- C.F. Extremadura: 2 temporadas
- C.D. Leganés: 2 temporadas

Ejercicio 25
- Real Madrid C.F.: 5923 goles
- F.C. Barcelona: 5864 goles
- Athletic Club: 4572 goles
- At. de Madrid: 4499 goles
- Valencia C.F.: 4387 goles
- Sevilla F.C.: 3645 goles
- R.C.D. Espanyol: 3578 goles
- Real Sociedad: 3215 goles
- Real Zaragoza CD: 2619 goles
- RC Celta de Vigo: 2292 goles

Ejercicio 26
- U.E. Lleida: 70 goles
- A.D. Almería: 70 goles
- Mérida C.P.: 68 goles
- C.D. Leganés: 68 goles
- C.F. Extremadura: 61 goles
- At. Tetuan: 50 goles
- Girona F.C.: 50 goles
- Xerez C.D.: 37 goles
- Condal: 36 goles
- C. y D. Leonesa: 33 goles

Ejercicio 27
- Temporada 1928-29: 378 goles en 90 partidos. Media: 4.20 goles/partido.
- Temporada 1929-30: 410 goles en 90 partidos. Media: 4.56 goles/partido.
- Temporada 1930-31: 377 goles en 90 partidos. Media: 4.19 goles/partido.
- Temporada 1932-33: 398 goles en 90 partidos. Media: 4.42 goles/partido.
- Temporada 1933-34: 373 goles en 90 partidos. Media: 4.14 goles/partido.
- Temporada 1934-35: 533 goles en 132 partidos. Media: 4.04 goles/partido.
- Temporada 1940-41: 560 goles en 132 partidos. Media: 4.24 goles/partido.
- Temporada 1941-42: 732 goles en 182 partidos. Media: 4.02 goles/partido.
- Temporada 1948-49: 728 goles en 182 partidos. Media: 4.00 goles/partido.
- Temporada 1949-50: 758 goles en 182 partidos. Media: 4.16 goles/partido.
- Temporada 1950-51: 1021 goles en 240 partidos. Media: 4.25 goles/partido.
- Temporada 1951-52: 972 goles en 240 partidos. Media: 4.05 goles/partido.

Ejercicio 28
- Temporada 1928-29: Máximo goleador fue Real Sociedad, C.D. Europa
- Temporada 1953-54: Máximo goleador fue F.C. Barcelona, Real Madrid C.F.
- Temporada 1967-68: Máximo goleador fue U.D. Las Palmas, Real Madrid C.F.
- Temporada 1972-73: Máximo goleador fue At. de Madrid, R.C.D. Espanyol
- Temporada 1980-81: Máximo goleador fue Real Madrid C.F., F.C. Barcelona
- Temporada 1995-96: Máximo goleador fue Valencia C.F., Real Madrid C.F.

Ejercicio 29
- Real Madrid C.F.: Racha de 5 temporadas consecutivas siendo el máximo goleador.
- Athletic Club: Racha de 5 temporadas consecutivas siendo el máximo goleador.
- F.C. Barcelona: Racha de 4 temporadas consecutivas siendo el máximo goleador.

Ejercicio 30
- Sevilla F.C. vs Real Betis B. S.: 9 jugadores. Ejemplos: ANTUNEZ, CARVAJAL, DIEGO R., JOSE MARI, MATEOS ...

Ejercicio 31
- RAFA GONZALEZ: Promedio de 116.8 minutos por temporada (Total: 934 minutos en 8 temporadas).
- LESTON: Promedio de 351.0 minutos por temporada (Total: 2808 minutos en 8 temporadas).
- IZPIZUA: Promedio de 448.2 minutos por temporada (Total: 3586 minutos en 8 temporadas).
- CELDRAN: Promedio de 462.6 minutos por temporada (Total: 3701 minutos en 8 temporadas).
- NEBOT C.: Promedio de 546.0 minutos por temporada (Total: 4368 minutos en 8 temporadas).

Ejercicio 32
- UNZUE - Equipo: C. At. Osasuna, Años fuera: 14.
- A. PRATS - Equipo: R.C.D. Mallorca, Años fuera: 14.
- CAPDEVILA - Equipo: R.C.D. Espanyol, Años fuera: 14.
- ANGEL D. - Equipo: U.D. Las Palmas, Años fuera: 14.
- DEL SOL - Equipo: Real Betis B. S., Años fuera: 13.

Ejercicio 33
- ELDUAYEN: Racha de 8 temporadas consecutivas.
- ITURRINO: Racha de 7 temporadas consecutivas.
- P. LLORENTE: Racha de 7 temporadas consecutivas.
```

---

## 4) Cambios respecto a la primera versión

1. **Arquitectura POO Boletín 5**
   - Se consolidó toda la lógica en `Liga`, manteniendo la jerarquía `Liga` -> `Temporada` -> `Equipo` -> `Jugador`.

2. **Factoría de carga**
   - `Factoria` ahora construye `Liga` y no solo un objeto experto directo.
   - Se añadieron validaciones de integridad de datos durante la carga.

3. **Propiedades derivadas y métodos `agregar_*`**
   - Se añadieron propiedades derivadas en `Jugador`, `Equipo`, `Temporada` y `Liga`.
   - Se añadieron métodos de construcción incremental (`agregar_jugador`, `agregar_equipo`, `agregar_temporada`).

4. **Iteración histórica centralizada**
   - Se añadió `_iterar_historial` en `Liga` para recorrer temporadas/equipos/jugadores de forma uniforme.

5. **Compatibilidad con ejercicios históricos**
   - Los 33 ejercicios históricos quedaron integrados dentro de `Liga`, eliminando el módulo `experto_futbol.py`.

6. **Interfaz y ejecución**
   - `ejecucion.py` y `interfaz.py` se adaptaron para trabajar con `Liga` como objeto raíz.
   - Se añadieron comprobaciones previas en la ejecución para validar disponibilidad de ejercicios.

