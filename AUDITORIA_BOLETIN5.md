# Veredicto general
La implementación auditada **no cumple globalmente** el Boletín 5 en el formato exigido. El repositorio está organizado como una solución de **Boletín 4** centrada en `ExpertoFutbol`, no en la jerarquía `Liga -> Temporadas -> Equipos -> Jugadores` pedida para Boletín 5. Existen clases `Jugador`, `Equipo` y `Temporada`, pero son modelos mínimos sin los métodos y propiedades derivadas obligatorias. No existe clase `Liga`, no existe método generador `_iterar_historial`, y la factoría no devuelve un objeto `Liga` sino `ExpertoFutbol`. Además, `Temporada` y `Equipo` usan listas donde el enunciado exige diccionarios/listas específicas con nombres y métodos concretos. El programa principal sí existe, pero prueba la arquitectura de Boletín 4, no la de Boletín 5. Por tanto, el incumplimiento es tanto **funcional** (faltan piezas obligatorias) como de **formato estructural**.

# Resumen ejecutivo
| Requisito | Estado | Evidencia | Observación |
|---|---|---|---|
| A. Diseño general de clases | NO CUMPLE | `class Jugador`, `class Equipo`, `class Temporada`, `class FactoriaFutbol`, `class ExpertoFutbol`; ausencia de `class Liga`. | Falta `Liga` y se introduce `ExpertoFutbol` como núcleo, rompiendo el diseño obligatorio. |
| B. Clase Jugador | CUMPLE PARCIALMENTE | `Jugador` tiene campos de fila Excel; no hay propiedades derivadas. | Atributos base sí; faltan `tarjetas_totales`, `veces_sustituido`, `goles_por_minuto`, `es_revulsivo`. |
| C. Clase Equipo | NO CUMPLE | `Equipo(nombre, filas)` sin métodos ni propiedades derivadas. | Falta `temporada`, `agregar_jugador` y propiedades derivadas obligatorias. |
| D. Clase Temporada | NO CUMPLE | `Temporada(nombre, anyo_inicio, equipos: list[Equipo])`. | Se exige diccionario `equipos[nombre]=Equipo`, método `agregar_equipo` y derivadas; no existe. |
| E. Clase Liga | NO CUMPLE | No existe `class Liga`. | Falta atributo `temporadas` en diccionario, método `agregar_temporada` y derivadas. |
| F. Generador `_iterar_historial` | NO CUMPLE | No aparece `_iterar_historial` en el repositorio. | No existe iterador central que devuelva `(temporada, equipo, jugador)`. |
| G. Factoria y validaciones | NO CUMPLE | `FactoriaFutbol.cargar_excel` devuelve `ExpertoFutbol`; validación limitada a columnas y ajuste `PCOMPLETOS<=PJUGADOS`. | Lee Excel, pero no construye `Liga` ni implementa todas las validaciones obligatorias. |
| H. Métodos históricos Boletín 4 en Liga | NO VERIFICABLE | Hay referencia a “33 ejercicios del Boletín 4” en `README` y en `ExpertoFutbol`. | Sin listado oficial de métodos exigidos para Boletín 5 “en Liga”, no se puede auditar uno por uno con trazabilidad completa. |
| I. Programa principal | CUMPLE PARCIALMENTE | `codigo/ejecucion.py` ejecuta tests y lanza interfaz. | Sí existe entrada funcional, pero orientada al diseño `ExpertoFutbol`, no al modelo obligatorio de Boletín 5. |
| J. Criterio de mismo formato | NO CUMPLE | Múltiples desajustes estructurales en clases, contenedores y métodos obligatorios. | La arquitectura entregada no respeta el formato literal exigido por Boletín 5. |

# Comprobación detallada por bloques
## 1. Diseño general de clases
- **Estado: NO CUMPLE**.
- **Evidencia funcional**: existen `Jugador`, `Equipo`, `Temporada` y `FactoriaFutbol`. 
- **Evidencia de formato**: no existe `Liga`; el núcleo de dominio es `ExpertoFutbol`, clase no exigida para Boletín 5 y usada como agregado principal.
- **Impacto**: la arquitectura exigida no está implementada literalmente.

## 2. Clase Jugador
- **Estado: CUMPLE PARCIALMENTE**.
- **Cumple (funcional)**:
  - La clase existe.
  - Contiene atributos de la fila del Excel (`TEMPORADA`, `EQUIPO`, `PJUGADOS`, `GOLES`, etc.) mapeados a campos del dataclass.
- **No cumple (formato)**:
  - No hay propiedades derivadas obligatorias: `tarjetas_totales`, `veces_sustituido`, `goles_por_minuto`, `es_revulsivo`.
  - No hay implementación explícita del criterio “más suplente que titular” para `es_revulsivo`.

## 3. Clase Equipo
- **Estado: NO CUMPLE**.
- **Cumple (parcial funcional)**:
  - La clase existe y contiene `nombre`.
- **No cumple (funcional y formato)**:
  - El contenedor de jugadores se llama `filas` (lista), pero no se define explícitamente como “lista de jugadores” con la semántica pedida en Boletín 5.
  - Falta atributo `temporada`.
  - Falta método `agregar_jugador`.
  - Faltan propiedades derivadas `goles_marcados`, `num_jugadores`, `partidos_jugados`, `total_tarjetas`.

## 4. Clase Temporada
- **Estado: NO CUMPLE**.
- **Cumple (parcial funcional)**:
  - La clase existe con identificador (`nombre`) y `anyo_inicio`.
- **No cumple (formato)**:
  - `equipos` es `list[Equipo]`; se exige diccionario `dict[str, Equipo]` con clave = nombre del equipo.
  - Falta `agregar_equipo`.
  - Faltan propiedades derivadas `num_equipos`, `num_partidos`, `goles_totales`, `media_goles_por_partido`, `año_inicio` (como derivada especificada).
  - No hay validación explícita del formato `XXXX-YY` del identificador.

## 5. Clase Liga
- **Estado: NO CUMPLE**.
- **Evidencia**:
  - No existe símbolo/clase `Liga`.
  - Tampoco existe una clase alternativa con el mismo contrato (diccionario temporadas, `agregar_temporada`, derivadas).
- **Conclusión**:
  - No se implementa la jerarquía exigida `Liga -> Temporadas -> Equipos -> Jugadores` con los tipos y contenedores pedidos.

## 6. Generador _iterar_historial
- **Estado: NO CUMPLE**.
- **Evidencia**:
  - No existe método `_iterar_historial` ni equivalente en `Liga` (porque `Liga` no existe).
  - La lógica se apoya en índices internos de `ExpertoFutbol` y bucles distribuidos por ejercicios, no en un generador común de contexto `(temporada, equipo, jugador)`.

## 7. Clase Factoria y validaciones
- **Estado: NO CUMPLE**.
- **Cumple (funcional parcial)**:
  - Lee Excel `.xls/.xlsx` y valida columnas.
- **No cumple (funcional y formato)**:
  - La factoría devuelve `ExpertoFutbol`, no `Liga`.
  - Falta clase con nombre exacto `Factoria` (solo `FactoriaFutbol`; equivalente no justificable porque el contrato de salida tampoco coincide).
  - Validaciones obligatorias ausentes o incompletas:
    - coherencia de temporadas consecutivas,
    - positividad estricta de cantidades,
    - `PJUGADOS == PSUPLENTE + PTITULAR`,
    - `MINUTOS <= PJUGADOS*90`,
    - `PJUGADOS <= partidos de la temporada`.
  - Solo se observa corrección de `PCOMPLETOS` truncándolo a `PJUGADOS`, lo cual además modifica dato en lugar de rechazar inconsistencia.

## 8. Métodos históricos del Boletín 4
- **Estado: NO VERIFICABLE**.
- **Evidencia**:
  - Sí hay 33 ejercicios implementados en `ExpertoFutbol` y descritos en README.
  - No se dispone en el repositorio del enunciado/listado formal de “métodos históricos de Boletín 4” que Boletín 5 exige portar a `Liga`.
- **Conclusión estricta**:
  - No se puede verificar uno por uno si están todos los obligatorios, ni su equivalencia exacta en nombre/firma respecto al enunciado original.
  - Independientemente de ello, **sí** puede afirmarse que no están añadidos a `Liga` porque `Liga` no existe.

## 9. Programa principal
- **Estado: CUMPLE PARCIALMENTE**.
- **Cumple (funcional)**:
  - Existe un punto de entrada claro en `if __name__ == "__main__":`.
  - Carga datos, ejecuta comprobaciones y lanza interfaz.
- **No cumple (formato Boletín 5)**:
  - El flujo prueba `FactoriaFutbol -> ExpertoFutbol`, no `Factoria -> Liga` con la jerarquía exigida.

## 10. Cumplimiento del mismo formato exigido
- **Estado: NO CUMPLE**.
- **Evaluación explícita**:
  - Nombres de clases: faltan `Liga` y `Factoria` exacta.
  - Organización jerárquica: no existe `Liga` como raíz.
  - Lista de jugadores en `Equipo`: existe lista (`filas`) pero sin el contrato completo exigido.
  - Diccionarios en `Temporada` y `Liga`: no implementado.
  - Propiedades derivadas: faltan en `Jugador`, `Equipo`, `Temporada`, `Liga`.
  - Métodos `agregar_jugador`, `agregar_equipo`, `agregar_temporada`: no implementados.
  - Generador `_iterar_historial`: no implementado.
  - Clase `Factoria` que devuelva `Liga`: no implementado.
  - Programa principal de prueba: existe, pero para arquitectura distinta.

# Incumplimientos concretos
1. **Falta la clase `Liga`**.
   - Dónde: repositorio `codigo/*.py`.
   - Por qué: no existe símbolo ni implementación equivalente con su contrato.
   - Gravedad: **alta**.

2. **La factoría no devuelve `Liga`**.
   - Dónde: `FactoriaFutbol.cargar_excel`.
   - Por qué: retorna `ExpertoFutbol`.
   - Gravedad: **alta**.

3. **No existe `_iterar_historial` en `Liga`**.
   - Dónde: ausencia total del método/símbolo.
   - Por qué: no hay clase `Liga` ni generador equivalente central.
   - Gravedad: **alta**.

4. **`Equipo` no tiene contrato obligatorio** (`temporada`, `agregar_jugador`, derivadas).
   - Dónde: `codigo/equipo.py`.
   - Por qué: solo `nombre` y `filas`.
   - Gravedad: **alta**.

5. **`Temporada` no usa diccionario de equipos ni método `agregar_equipo`**.
   - Dónde: `codigo/temporada.py` y construcción en factoría.
   - Por qué: usa lista de `Equipo`.
   - Gravedad: **alta**.

6. **`Jugador` carece de propiedades derivadas obligatorias**.
   - Dónde: `codigo/jugador.py`.
   - Por qué: solo campos base del dataclass.
   - Gravedad: **media**.

7. **No se implementan validaciones de negocio obligatorias del Boletín 5**.
   - Dónde: `codigo/factoria_futbol.py`.
   - Por qué: solo validación de columnas y ajuste puntual `PCOMPLETOS<=PJUGADOS`.
   - Gravedad: **alta**.

8. **Desviación de arquitectura (“ExpertoFutbol” como eje)** frente al formato exigido.
   - Dónde: `codigo/experto_futbol.py`, `codigo/ejecucion.py`, `README_TXT.txt`.
   - Por qué: diseño orientado a resolver Boletín 4, no la estructura literal de Boletín 5.
   - Gravedad: **alta**.

9. **Programa principal no demuestra la solución en el formato requerido**.
   - Dónde: `codigo/ejecucion.py`.
   - Por qué: prueba y arranque sobre modelo distinto.
   - Gravedad: **media**.

# Elementos no verificables
1. **Listado exacto de métodos históricos de Boletín 4 exigidos en Boletín 5**.
   - Razón: no aparece el enunciado oficial de Boletín 4 ni un inventario formal de métodos obligatorios a portar en este repositorio.

# Veredicto final
NO CUMPLE
