# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from sympy import solve, symbols, Eq
from sympy.physics.units import kilo
from sympy.physics.units import convert_to
from sympy.physics.units import ohms, amperes, volts
import ltspice
import platform
import ahkab
import pylab as plt
from IPython import get_ipython

# %% [markdown]
#
#  # Objetivo del laboratorio
#  El objetivo de la presenta práctica es conocer el estándar de simulación de circuitos [SPICE](http://bwrcs.eecs.berkeley.edu/Classes/IcBook/SPICE) y realizar pequeñas simulaciones en corriente continua con el mismo. SPICE es una forma elegante y sencilla de codificar circuitos eléctricos de manera que puedan ser procesados por un ordenador. Mediante un sencillo lenguaje podemos definir resistencias, fuentes de alimentación, etc., las conexiones entre ellos y los resultados que deseamos obtener.
#
#  # El estándar SPICE
#  **SPICE** es una abreviabiación de *Simulation Program with Integrated Circtuit Emphasis*.
#  Se trata básicamente de un método estándar para describir circuitos usando texto plano en
#  lugar de una representación gráfica (o *esquemática*). A esta descripción en texto se
#  la llama también **netlist** y básicamente se corresponde con la *lista* de los componentes del circuito y cómo estos están conectados entre sí, es decir, de los nodos de unión.
#  Los ficheros netlist pueden tener extensiones `.cir`, `.net`, `.ckt`, ó `.sp` y es muy común encontrárselos con cualquiera de estas.
#
#  Existen en el mercado muchas variantes (intérpretes) de Spice, aunque el original fue descrito
#  en la Universidad de Berkeley. En la lista de intérpretes de Spice tenemos desde esfuerzos y proyectos comerciales hasta *open source* y regidos por distintas comunidades de usuarios y programadores.
#
# > **Pregunta:** Enumera todos los intérprete de Spice que puedas encontrar. Crea una tabla en Markdown con varias columnas (para el nombre, fabricante, versión actual, licencia y alguna característica sobresaliente). Aquí tienes un ejemplo del que puedes partir y seguir completando:
#
# | Intérprete | Licencia | Fabricante         | Características  |
# | ---------- | -------- | ------------------ | ---------------- |
# | Ahkab      | GPL      | Giuseppe Venturini | Basado en Python |
# |            |          |                    |                  |
# |            |          |                    |                  |
#
#
#  > **Pregunta:** ¿Qué comparación puedes efectuar entre C y Spice como estándares (lenguajes) y sus respectivas implementaciones en software? ¿Qué implementaciones reales (compiladores) del lenguaje C conoces?
#
#  ## Elementos de un netlist
#  Como acabamos de comentar, un netlist se corresponde con la codificación de los elementos electrónicos de un circuito y las uniones entre los mismos. Veamos con más concreción qué partes y secciones lo componen.
#
#  ## Comentarios
#
#  La primera línea de un netlist se corresponderá siempre con un comentario. A partir de esta línea se pueden introducir más comentarios pero tienen que ir siempre precedidos de un `*`. Ejemplo:
#
#  ```spice
#  Mi primer circuito
#  * Otro comentario
#  * más comentarios
#  *
#  ```
#
#  ## Dispositivos básicos de un circuito
#  Los elementos de un netlist son los mismos que encontramos en cualquier circuito eléctrico sencillo,
#  tales como resistencias, **condensadores**, **bobinas**, **interruptores**, **hilos** y **fuentes** de alimentación.
#  Para distinguir uno de otro, se reserva una letra característica: `V` para fuentes de alimentación, `R` para resistencias, `C` para condensadores y `L` para bobinas. También es posible usar estas letras en su versión en minúscula (`r`, `v`, `c`, `l`, etc.).
#  Después de esta letra característica se puede sufijar cualquier texto para diferenciar un elemento de otro (números, letras, palabras, etc.). Ejemplo:
#
#  ```
#  * Una resistencia
#  R1
#  *  Otra resistencia
#  R2
#  * Fuente de alimentación
#  V
#  * Un condensador
#  Cprincipal
#  ```
#
#  ## Conexiones
#  A continuación de indicar el elemento eléctrico, tenemos que informar a Spice cuáles
#  son los puntos de unión tanto a un lado como al otro del elemento.
#  Así es como Spice sabe qué está conectado a qué: porque comparten un **punto**
#  (o **nodo**, aunque este término se reserva sobretodo a uniones de más de dos elementos)
#  que hemos señalizado correctamente. Para nombrar nodos, lo mejor es emplear una
#  numeración secuencial: 0...n. **La enumeración de los puntos de unión es completamente
#  a nuestro criterio**.
#
#  ```
#  * Una resistencia
#  * entre cables 0 y 1
#  R1 0 1
#  ```
#
#  **Sólo es necesario seguir un criterio**: en el caso de una
#  fuente de alimentación, el nodo que pondremos primero será
#  aquel que está más cerca del *borne* positivo. Ejemplo:
#
#  ```spice
#  * Para una fuente indicamos primeramente conexión a nodo positivo.
#  v 2 3 type=vdc vdc=1
#  ```
#
# En el *caso de LTspice* no es necesario indicar los parámetros `type=vdc` y `vdc=X`, sino que si no se especifica nada, se supone que el último valor es el del voltaje a corriente continua:
#
# ```spice
# * Especificación de una fuente de alimentación de 10 V en corrient continua en el caso de LTspice
# v 0 1 10
# ```
#
# Aquí tienes un ejemplo gráfico de los componentes comentados justo arriba (resistencia y voltaje):
#
# ![](https://raw.githubusercontent.com/pammacdotnet/spicelab/master/resistencia%20y%20pila%20con%20nodos.svg?sanitize=true)
#
#  ## Unidades en SPICE
#
#  Las unidades de las magnitudes características del circuito son siempre [unidades
#  del Sistema Internacional](https://en.wikipedia.org/wiki/SI_electromagnetism_units) y no es necesario indicarlo explícitamente en el netlist.
#
#  La forma de especificar múltiplos de estas cantidades es añadiendo una letra.
#  Básicamente las que nos interesan y las que suelen aparecer mayoritariamente son `k` para "kilo-," `m` para "mili?" y `u` para "micro?".
#
#  > **Pregunta:** Crea una tabla en Markdown con todos los prefijos de múltiplos que puedas, su abreviatura y su equivalencia numérica.
#
#  En el caso de las fuentes de alimentación hemos de especificar si se trata de corriente contínua (`vdc`) o alterna (`ac`).
#
#  ```
#  * Una resistencia de 5 Ohmios
#  R2 1 0 5
#  * Una pila de 10 Voltios (continua)
#  V1 1 0 type=vdc vdc=10
#  * Una resistencia de 5 kΩ
#  RX 2 4 5k
#  ```
#
#  > **Pregunta**: ¿qué unidades del Sistema Internacional relacionadas con la asignatura –y los circuitos en general– conoces? Responde aquí mismo en una celda de Markdown con una tabla.
#
#  ## Valores iniciales
#
#  Aparecen justo al final de la definición del componente (`ic`). Suelen aplicarse principalmente con condensadores.
#
#  ```
#  * Una condensador inicialmente no cargado
#  c 1 0 1u ic=0
#  ```
#
#  ## Fin del circuito
#
#  El fin de la descripción de un netlist se especifica mediante el
#  comando `.end`.
#
#  ```spice
#  * Mi primer circuito
#  V 1 0 vdc=10 type=vdc
#  R 1 0 5
#  * Fin del circuito
#  .end
#  ```
#
#
#  ## Comandos SPICE para circuitos en corriente continua
#
#  Además de la descripción del circuito, hemos de indicar al intérprete de Spice qué
#  tipo de análisis queremos realizar en sobre el mismo y cómo queremos presentar
#  la salida de la simulación. Los comandos en Spice empiezan por un `.` y suelen
#  escribirse justo al final del circuito, pero antes del comando `.end`.
#
#  ```
#   Mi primer circuito
#  * Aquí van los componentes
#  R 1 0 6k
#  ...
#  * Comandos
#  .op
#  ...
#  * Fin del circuito
#  .end
#  ```
#
#  > **Pregunta**: Hasta lo que has visto del lenguaje Spice, ¿dentro de qué tipo o conjunto de lenguajes encajaría? ¿Funcionales? ¿Específicos de dominio? ¿Procedurales? ¿Estructurados? ¿Orientado a Objetos ¿Funcionales? Justifica tu respuesta.
#
#  Veamos los principales comandos de simulación:
#
#  - `.op` es el comando más sencillo que podemos emplear en. Devuelve el voltaje e intensidad en cada ramal y componente del circuito. Este comando no necesita parámetros.
#  - `.dc` es uy parecido al comando `.op` pero nos permite cambiar el valor del voltaje de una fuente de alimentación en pasos consecutivos entre el valor A y el valor B.
#  En el caso de que la fuente tuviera asignada ya un valor para su voltaje, este sería ignorado. Ejemplo:
#
#
#  ```spice
#  * Variamos el valor del voltaje
#  * de la fuente "v" de 1 a 1000
#  * en pasos de 5 voltios
#  v 1 0 type=vdc vdc=10
#  .dc v 1 start=1 stop=1000 step=20
#  v2a 2 4 type=vdc vdc=9
#  * Igual para v2a. Se ignora su voltaje de 9V
#  .dc v2a start=0 stop=10 step=2
#  ```
#
#  - El comando `.tran` realiza un análisis en el tiempo de los parámetros del
#  circuito. Si no se emplea la directiva `uic` (*use initial conditions*) o esta es igual a cero, este análisis se realiza desde el punto estable de funcionamiento del circuito hasta un tiempo `tfinal`.
#  y en intervalos `tstep`. Si empleamos un varlor distinto para parámetro `uic`,
#  entonces se hará uso de las condiciones iniciales definidas para cada componente
#   (típicamente `ic=X` en el caso de los condensadores, que da cuenta de la carga incial que estos pudieran tener).
#
#
#  ```
#  * Hacemos avanzar el tiempo entre
#  * tinicial y tfinal en pasos tstep
#  .tran tstart=X tstop=Y tstep=Z uic=0/1/2/3
#  ```
#
#  `X`, `Y` y `Z` tienen, evidentemente unidades de tiempo en el S.I. (segundos).
#
#  > **Pregunta**: El parámetro `uic` puede tener varios valores y cada uno significa una cosa. Detállalo usando un celda Markdown y consultando la [documentación de Ahkab](https://buildmedia.readthedocs.org/media/pdf/ahkab/latest/ahkab.pdf).
#
#  ## Intérprete SPICE que vamos a usar: Ahkab
#  Tras un estándar siempre hay una o varias implementaciones. Ahkab no deja de ser una implmentación más en Python del estándar Spice.
#  > **Pregunta:** Comenta las distintas implementaciones de lenguajes y estándares que conozcas. Hazlo usando una tabla en Markdown. [Aquí](https://www.markdownguide.org/extended-syntax/#tables) tienes un poco de ayuda (aunque antes ya se ha puesto el ejemplo de una tabla).
#
#  > **Pregunta:** Describe brevemente este software (creador, objetivos, versiones, licencia, características principales, dependencias, etc.).
#
#  # Trabajo práctico
#  Muy bien, ahora toca definir circuitos y ejecutar simulaciones sobre los mismos gracias a Ahkab.
#  ## Instalación de bibliotecas necesarias
#  Si estás utilizando Anaconda, asegúrate de tener su entorno activado:
#
#  ```cmd
#  C:\> conda activate base (en el caso de Windows)
#  ```
#  ó
#
#  ```bash
#  $ source /usr/local/Caskroom/miniconda/base/bin/activate (en el caso de macOS)
#  ```
#
# En el caso de Windows tienes que tener en el PATH el directorio donde se encuentre el comando `conda` (visita la sección de [Environment Variables](https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10) del [Panel de Control](https://www.digitalcitizen.life/8-ways-start-control-panel-windows-10)). Si has instalado Anaconda con [esta opción](https://docs.anaconda.com/_images/win-install-options.png) marcada, ya no tienes que preocuparte por ello.
#
# En el caso de usar Visual Studio Code, este puede encontrar automáticamente la distintas distribuciones de Python que tengamos instaladas y si abrimos un terminal, este se adaptará automáticamente al entorno Python que hayamos seleccionado. La configuración de Python en VS Code está bien explicada su [documentación](https://code.visualstudio.com/docs/python/python-tutorial).
#
# ![](https://raw.githubusercontent.com/microsoft/vscode-python/main/images/InterpreterSelectionZoom.gif)
#
# Ahora ya puedes instalar Ahkab:
#
#  ```
#  (base) $ pip install ahkab
#  ```
# %% [markdown]
# También puedes instalar Ahkab directamente desde este mismo notebook:

# %%
get_ipython().system('pip install ahkab')

# %% [markdown]
#
#  Como siempre, una vez instalado cualquier framework para Python, ya lo podemos utilizar, tanto desde el [REPL](https://en.wikipedia.org/wiki/Read–eval–print_loop) como desde un entorno Jupyter (Jupyter, [Jupyterlab](http://jupyterlab.readthedocs.io/en/stable/), VS Code o nteract). Recuerda que para usar el kernel Python (que viene con Anaconda) desde nteract debes seguir las instrucciones que se indican en su [documentación oficial](https://nteract.io/kernels).
# %% [markdown]
# Como vamos a pintar algunas gráficas, necesitamos instlar [matplotlib](https://matplotlib.org). Al igual que con Ahkab, esto lo podemos hacer directamente desde este mismo notebook. Si hemos usado Anaconda:

# %%
get_ipython().system('conda install -y -c conda-forge matplotlib')


# %%

# %% [markdown]
#  > **Pregunta:** ¿Qué es y para qué sirve PyLab?
#
#  ## Circuitos sencillos para trabjar con la ley de Ohm:
#
#  La *mal llamada* ley de Ohm reza que el voltaje (la *energía por unidad de carga*) que se disipa en un tramo de un circuito eléctrico es equivalente a la intensidad ($I$) de la corriente (es decir, cuántos electrones circulan por unidad de tiempo) por la resistencia del material ($R$) en el que está desplazándose dicha corriente. Matemáticamente:
#
#  $$
#  V = I\cdot R
#  $$
#
#  > **Pregunta:** comprueba que la ecuación anterior está ajustada a nivel dimensional, es decir, que la naturaleza de lo que está a ambos lados del signo igual es la misma. Realiza este ejercicio con LaTeX en una celda Markdown.
#
#  Comencemos con el circuito más sencillo posible de todos:
#
#  ![](https://raw.githubusercontent.com/pammacdotnet/spicelab/master/primer%20circuito.svg?sanitize=true)
#
#  Vamos a escribir su contenido (componentes o *netlist*) en disco con el nombre `circuito sencillo.sp`. Esto lo podemos lograr directamente y en tiempo real desde una celda de Jupyter gracias a los *comandos mágicos* de este entorno de programación literaria. En concreto vamos a utilizar `%%writefile` que guarda los contenidos de una celda como un fichero.

# %%
get_ipython().run_cell_magic('writefile', '"circuito sencillo.sp"',
                             '* Este es un circuito sencillo\nr1 1 0 10\nv1 0 1 type=vdc vdc=9\n.op\n.dc v1 start=0 stop=9 step=1\n.end')

# %% [markdown]
# Ahora vamos a leer su descripción con Ahkab, interpretar y ejecutar las simulaciones que en él estén descritas.

# %%
circuito_y_análisis = ahkab.netlist_parser.parse_circuit(
    'circuito sencillo.sp')

# %% [markdown]
#  Separamos la información del netlist (componentes) de los análisis (uno de tipo `op` y otro de tipo `dc`):

# %%
circuito = circuito_y_análisis[0]
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(
    circuito, análisis_en_netlist)
print(lista_de_análisis)

# %% [markdown]
# > **Pregunta:** ¿qué tipo de estructura de Python es `lista_de_análisis`?
#
#  Las simulaciones que implican listas de datos (`.dc`, `.tran`, etc.) necesitan de un fichero temporal (`outfile`)
#  donde almacenar los resultados. Para ello tenemos que definir la propiedad `outfile`.

# %%
lista_de_análisis[1]['outfile'] = "simulación dc.tsv"

# %% [markdown]
#  > **Pregunta:** escribe el código Python necesario para identificar qué análisis de `lista_de_análisis`
#  son de tipo `dc` ó `tran` y sólo añadir la propiedad `outfile` en estos casos.
# Aquí tenéis un post de Stackoverflow con algo de [ayuda](https://stackoverflow.com/questions/49194107/how-to-find-index-of-a-dictionary-key-value-within-a-list-python).
#  Un poco más de ayuda: el siguiente código (sí, una única línea) devuelve el índice de la simulación que es de tipo `dc`. Para simplificar un poco el ejercicio, suponed que, como máximo, habrá un análisis de tipo `tran` y/o `dc`.

# %%
[i for i, d in enumerate(lista_de_análisis) if "dc" in d.values()][0]

# %% [markdown]
# Una vez que ya hemos separado netlists de simulaciones, ahora ejecutamos las segundas (¡todas a la vez!) gracias al método `.run` de Ahkab:

# %%
resultados = ahkab.run(circuito, lista_de_análisis)

# %% [markdown]
# ### Resultados de la simulación `.dc`
# Imprimimos información sobre la simulación de tipo `.dc`:

# %%
print(resultados['dc'])

# %% [markdown]
#  Veamos qué variables podemos dibujar para el caso del análisis `dc`.

# %%
print(resultados['dc'].keys())

# %% [markdown]
# Y ahora graficamos el resultado del análisis anterior. Concretamente vamos a representar el voltaje en el borne 1 (`V1`) con respecto a la intensidad del circuito (`I(V1)`).

# %%
figura = plt.figure()
plt.title("Prueba DC")
plt.plot(resultados['dc']['V1'], resultados['dc']
         ['I(V1)'], label="Voltaje (V1)")

# %% [markdown]
# > **Pregunta:** comenta la gráfica anterior… ¿qué estamos viendo exactamente? Etiqueta los ejes de la misma convenientemente. Así como ningún número puede *viajar* solo sin hacer referencia a su naturaleza, ninguna gráfica puede estar sin sus ejes convenientemente etiquetados. Algo de [ayuda](https://matplotlib.org/3.1.0/gallery/pyplots/fig_axes_labels_simple.html). ¿Qué biblioteca estamos usando para graficar? Una [pista](https://matplotlib.org).
# %% [markdown]
#  ### Resultados de la simulación `.op`
#  El método `.results` nos devuelve un diccionario con los resultados de la simulación.

# %%
print(resultados['op'].results)

# %% [markdown]
#  > **Pregunta:** justifica el sencillo resultado anterior (análisis `op`). Repite el cálculo con Sympy, atendiendo con mimo a las unidades y al formateo de los resultados (tal y como hemos visto en muchos otros notebooks en clase).
# %% [markdown]
# ## Resolución del mismo circuito pero con LTspice
# ¿Cómo? ¿Es esto posible? ¿Desde Jupyter? Sí!!! Pero primero, por comodidad, deberíamos crear un alias del comando que apunte a nuestro ejecutable. Además, con un poco de inteligencia, podemos adelantarnos al hecho de si estamos en Windows o macOS:

# %%
get_ipython().run_line_magic(
    'alias', 'lts /Applications/LTspice.app/Contents/MacOS/LTspice -ascii -b')
if platform.system() == "Windows":
    get_ipython().run_line_magic(
        'alias', 'lts C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe -ascii -b')

# %% [markdown]
# **Pregunta**: ¿Qué significan las opciones `-b` y `-ascii`? Algo de ayuda [aquí](http://ltwiki.org/LTspiceHelp/LTspiceHelp/Command_Line_Switches.htm).
# %% [markdown]
# También tenemos que cambiar ligeramente la sintaxis. Ejecuta esta línea para que se escriba el fichero siguiente. Para LTspice, vamos a reservar la extensión `.net`:

# %%
get_ipython().run_cell_magic('writefile', '"circuito sencillo.net"',
                             '* Este es un circuito sencillo adaptado para LTspice\nr1 1 0 100\nv1 0 1 9\n.op\n* Comentamos el análisis .dc para centrarnos primero en el .op\n* .dc v1 1 10 \n.end')

# %% [markdown]
# Ejecutamos LTspice con el circuito (de la misma manera que antes habíamos hecho con Ahkab).

# %%
lts "circuito sencillo.net"

# %% [markdown]
# Veamos el contenido de la simulación.

# %%
get_ipython().run_line_magic('pycat', 'circuito sencillo.log')

# %% [markdown]
# Ahora repitamos lo mismo para el análisis `.dc`:

# %%
get_ipython().run_cell_magic('writefile', '"circuito sencillo.net"',
                             '* Este es un circuito sencillo adaptado para LTspice\nr1 1 0 100\nv1 0 1 9\n* Ahora obviamos el análisis .op\n* .op\n.dc v1 1 10 \n.end')


# %%
lts "circuito sencillo.net"

# %% [markdown]
# Al ejecutar esta simulación, se genera un fichero `.raw` con los resultados. Es muy parecido al `outfile` que hemos empleado antes con Ahkab. Para leer este fichero, tenemos que usar el paquete [ltspice de Python](https://github.com/DongHoonPark/ltspice_pytool), el cual podéis instalar directamente desde Jupyter:

# %%
get_ipython().system('pip install ltspice')

# %% [markdown]
# Ahora ya podemos leer este fichero `.raw` y pintar una recta de voltaje muy parecida a la que obtuvimos anteriormente con Ahkab:

# %%
l = ltspice.Ltspice("circuito sencillo.raw")
l.parse()
tiempo = l.get_time()
voltaje = l.get_data('V(1)')
corriente = l.get_data('I(V1)')
# Podemos pintar la corrente en función del tiempo
# plt.plot(tiempo, corriente)
# O el voltaje
plt.plot(tiempo, voltaje)

# %% [markdown]
# ** En resumen: ** hemos usado dos *compiladores* Spice distintos para hacer el mismo ejercicio. De igual manera podríamos haber usado [Ngspice](http://ngspice.sourceforge.net) u otro. De hecho, podíamos haber usado Ahkab en modo comando. Si tenemos correctamente instalado este framework, en princpio podemos invocarlo [directamente desde línea de comandos](https://ahkab.readthedocs.io/en/latest/help/Command-Line-Help.html):

# %%
get_ipython().system('ahkab "circuito sencillo.sp"')

# %% [markdown]
# **Ejercicio premium**: Graficar los datos anteriores con [Gnuplot](http://www.gnuplot.info).
# %% [markdown]
#  ## Análisis de circuito con resistencias en serie
# %% [markdown]
# Vamos a resolver (en punto de operación) el siguiente circuito:
#
# ![](https://raw.githubusercontent.com/pammacdotnet/spicelab/master/resistencias%20en%20serie.svg?sanitize=true)
#
# Al igual que antes, grabamos el netlist en disco desde Jupyter gracias a la *palabra mágica* [`%writefile`](https://ipython.readthedocs.io/en/stable/interactive/magics.html#cellmagic-writefile). Más info [aquí](https://ipython.readthedocs.io/en/stable/interactive/magics.html#cellmagic-writefile).

# %%
get_ipython().run_cell_magic('writefile', '"resistencias en serie.net"',
                             '* circuito con tres resistencias en serie\nv1 1 0 type=vdc vdc=9\nR1 0 2 3k\nR2 2 3 10k  \nR3 3 1 5k\n* análisis del circuito\n.op\n.end')


# %%
circuito_y_análisis = ahkab.netlist_parser.parse_circuit(
    'resistencias en serie.net')
circuito = circuito_y_análisis[0]
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(
    circuito, análisis_en_netlist)
resultados = ahkab.run(circuito, lista_de_análisis)

# %% [markdown]
# Imprimos los resultados del análisis `.op`:

# %%
print(resultados['op'])

# %% [markdown]
# Los cantidades `V1`, `V2` y `V3` hacen referencia a los distintos valores del potencial que se ha perdido en cada uno de los bornes que has elegido para describir el netlist (`1`, `2`, etc.). Por ejemplo, podemos calcular el *potencial consumido* por la resistencia `R1` y verás que coincide con el del punto `V2` devuelto por Ahkab. **Ejercicio**: compruébalo tú mismo y refléjalo por escrito.
# %% [markdown]
# Cargamos primero todo lo relacionado con Sympy:

# %%


# %%
r1 = 3E3*ohms
intensidad_ahkab = resultados['op']['I(V1)'][0][0]*amperes
v2 = convert_to(intensidad_ahkab*r1, [volts])
v2

# %% [markdown]
#  > **Pregunta**: reproduce el resto de los valores anteriores de manera *manual* mediante Sympy (es decir, aplicando la ley de Ohm, pero con un *toque computacional*). Te pongo aquí un ejemplo del que puedes partir… En él sólo calculo la corriente que circula por el circuito (sí, justo la que antes Ahkab ha devuelto de manera automática). Para ello necesito previamente computar la resistencia total (`r_total`). Faltarían el resto de resultados y convertirlos a unidades más *vistosas* (mediante la orden `convert_to` y `.n()`).

# %%
v1 = 9*volts
r1 = 3*kilo*ohms
r2 = 10*kilo*ohms
r3 = 5*kilo*ohms
r_total = r1 + r2 + r3
intensidad = symbols('i')
ley_ohm = Eq(v1, intensidad*r_total)
solucion_para_intensidad = solve(ley_ohm, intensidad)
convert_to(solucion_para_intensidad[0], [amperes]).n(2)

# %% [markdown]
# > **Pregunta**: Demuestra que se cumple la Ley de Kirchhoff de la energía en un circuito, es decir, que la suma de la energía suministrada por las fuentes (pilas) es igual a la consumida por las resistencias. Realiza la operación con Sympy.
#
# $$
# \sum_i^N V_{\text{fuentes}} = \sum_j^M V_{\text{consumido en resistencias}}
# $$
#
# Ten en cuenta que en este caso sólo hay una fuente.
# %% [markdown]
# ## Análisis `.op` de circuitos con resistencias en paralelo
#
# Vamos a complicar un poco el trabajo añadiendo elementos en paralelo.
#
#  > **Pregunta**: realiza los análisis `.op` de los siguientes circuitos.
#  Para ello crea un netlist separado para cada uno donde queden correctamente descritos
#  junto con la simulación (`.op`). Comenta los resultados que devuelve Ahkab (no imprimas los resultados de las simulaciones *sin más*).
#
#  ![](https://raw.githubusercontent.com/pammacdotnet/spicelab/master/resistencias%20en%20paralelo.svg?sanitize=true)
#
#  Aquí tienes el análisis del primer circuito, para que sirva de ejemplo:

# %%
get_ipython().run_cell_magic('writefile', '"resistencias en paralelo 1.cir"',
                             '* resistencias en paralelo\nvdd 0 1 vdc=12 type=vdc\nr2 1 2 1k\nr3 2 3 220\nr4 3 0 1.5k\nr5 2 0 470\n.op\n.end')


# %%
circuito_y_análisis = ahkab.netlist_parser.parse_circuit(
    'resistencias en paralelo 1.cir')
circuito = circuito_y_análisis[0]
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(
    circuito, análisis_en_netlist)
resultados = ahkab.run(circuito, lista_de_análisis)

# %% [markdown]
# Imprimimos los resultados del análisis `.op`. Como puedes comprobar, Ahkab sólo reporta la intensidad de corriente en las ramas en las que hay una pila (en este caso, la rama donde está la pila `VDD`).

# %%
print(resultados['op'])

# %% [markdown]
# > **Pregunta:** inserta dos *pilas virtuales* de 0 voltios en el resto de ramas del circuito (`Vdummy1` en la rama donde está `R5` y `Vdummy2` en la rama donde está `R3` y `R4`) para que Ahkab nos imprima también la corriente en las mismas. Es muy parecido al tercer circuito que tienes que resolver, donde `V1`, `V2` y `V3` tienen cero voltios. Estas *pilas nulas* son, a todos los efectos, *simples cables*. Una vez que ya tienes las corrientes en todas las ramas, comprueba que se cumple la Ley de Kirchhoff para las corrientes:
#
# $$
# I_{\text{entrante}} = \sum_i^{N} I_{\text{salientes}}
# $$
#
# Repite lo mismo para los otros dos circuitos. Realiza además los cálculos con Sympy (recalcula los mismos voltajes que devuelve Ahkab a partir de la corriente que sí te devuelve la simulación) y cuidando de no olvidar las unidades. Recuerda que el objeto `resultados` alberga toda la información que necesitas de manera indexada. Ya han aparecido un ejemplo más arriba. Es decir: no *copies* los números *a mano*, trabaja de manera informáticamente elegante (usando la variable `resultados`).
# %% [markdown]
#  # Circuitos en DC que evolucionan con el tiempo
# %% [markdown]
#  ## Carga de un condensador
#  Vamos a ver qué le pasa a un circuito de corriente continua cuando tiene un condensador
#  en serie.
#
#  ![](https://raw.githubusercontent.com/pammacdotnet/spicelab/master/condensador%20en%20continua.svg?sanitize=true)
#
#  Al igual que antes, primero guardamos el circuito en un netlist externo:

# %%
get_ipython().run_cell_magic('writefile', '"condensador en continua.ckt"',
                             '* Carga condensador\nv1 0 1 type=vdc vdc=6\nr1 1 2 1k\nc1 2 0 1m ic=0\n.op\n.tran tstep=0.1 tstop=8 uic=0\n.end')

# %% [markdown]
# > **Pregunta:** ¿qué significa el parámetro `ic=0`? ¿qué perseguimos con un análisis de tipo `.tran`?
#
# Leamos el circuito:

# %%
circuito_y_análisis = ahkab.netlist_parser.parse_circuit(
    "condensador en continua.ckt")

# %% [markdown]
#  Separamos el netlist de los análisis y asignamos un fichero de almacenamiento de datos (`outfile`):

# %%
circuito = circuito_y_análisis[0]
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(
    circuito, análisis_en_netlist)
lista_de_análisis[1]['outfile'] = "simulación tran.tsv"

# %% [markdown]
#  Ejecutamos la simulación:

# %%
resultados = ahkab.run(circuito, lista_de_análisis)
print(resultados['op'])
# print(resultados['tran'].keys())

# %% [markdown]
#  Dibujamos la gráfica de carga del condensador con el tiempo, centrándonos en la intensidad que circula por la pila.

# %%
figura = plt.figure()
plt.title("Carga de un condensador")
plt.plot(resultados['tran']['T'], resultados['tran']
         ['I(V1)'], label="Una etiqueta")

# %% [markdown]
# > **Pregunta:** Etiqueta los ejes convenientemente y comenta la gráfica. Dibuja otra gráfica con el voltaje en el borne `V1`. ¿Por qué son *opuestas*? ¿Qué le ocurre al voltaje a medida que evoluciona el circuito en el tiempo? Dibuja las gráficas en un formato estándar de representación vectorial (SVG, por ejemplo). Algo de ayuda [aquí](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#IPython.display.set_matplotlib_formats). ¿Qué valores devuelve el análisis de tipo `.op`? Justifícalo.
# %% [markdown]
# ## Carrera de condensadores
#
# Ahora tenemos un circuito con dos condensadores en paralelo:
#
# ![](https://raw.githubusercontent.com/pammacdotnet/spicelab/master/condensadores%20en%20paralelo.svg?sanitize=true)
#
# > **Pregunta:** Crea el netlist de este circuito e identifica qué condensador se satura primero. Dibuja la evolución de la intensidad en ambas ramas de manera simultánea. [Aquí](https://matplotlib.org/gallery/api/two_scales.html) tienes un ejemplo de cómo se hace esto en Matplotlib. Recuerda que para que Ahkab nos devuelva la corriente en una rama, debe de estar presente una pila. Si es necesario, inserta pilas virtuales de valor nulo (cero voltios), tal y como hemos comentado antes. Grafica también los voltajes (en otra gráfica, pero que aparezcan juntos).

# %%
get_ipython().run_cell_magic('writefile', '"carrera en condensadores.ckt"',
                             '* Carga condensador\nv0 0 1 type=vdc vdc=10\nr1 0 2 3k\nc1 2 3 47u ic=0\nv1dummy 3 1 type=vdc vdc=0\nc2 2 4 22u ic=0\nv2dummy 4 1 type=vdc vdc=0\n.tran tstep=0.01 tstart=6.5 tstop=7.5 uic=0\n.end')


# %%
circuito_y_análisis = ahkab.netlist_parser.parse_circuit(
    "carrera en condensadores.ckt")
circuito = circuito_y_análisis[0]
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(
    circuito, análisis_en_netlist)
lista_de_análisis[0]['outfile'] = "simulación tran carrera condensadores.tsv"
resultados = ahkab.run(circuito, lista_de_análisis)


# %%
figura = plt.figure()
plt.title("Carrera de condensadores")
plt.xlim(6.65, 7.5)
plt.ylim(0.0, 0.0005)
plt.grid()
plt.plot(resultados['tran']['T'], resultados['tran']
         ['I(V1DUMMY)'], label="Intensidad en C1")
plt.plot(resultados['tran']['T'], resultados['tran']
         ['I(V2DUMMY)'], label="Intensidad en C2")

# %% [markdown]
# **Ejercicio premium:** Repite la simulación con LTspice (invocándolo como comando externo, leyendo los datos de un fichero `.raw` y volviendo a graficar con Matplotlib.
# %% [markdown]
# ## Circuitos en corriente alterna
#
# ** Ejercicio:** Simula este circuito con LTspice y representa el voltaje y la intensidad en función del tiempo. Traduce este ejercicio a la versión Spice de Akhab y haz la misma representación. Ahkab utiliza otra sintaxis para expresar la corriente alterna. Esta está descrita en la [documentación](https://ahkab.readthedocs.io/en/latest/help/Netlist-Syntax.html#id24).

# %%
get_ipython().run_cell_magic('writefile', '"corriente alterna.net"',
                             '* Circuito en corriente alterna\nv1 1 0 sin(0 120 60 0 0)\nr1 0 1 10k\n.tran 1\n.end')


# %%
lts "corriente alterna.net"

# %% [markdown]
# # Resumen de lo que se pide
# Volved a realizar todos los ejercicios y demos en vuestro propio notebook, explicando con vuestras palabras cada paso, cada gráfica y respondiendo a cada pregunta. Cuidad la belleza, coherencia, narración, explicaciones y gráficas. Todas las gráficas se han pintado con Matplotlib, que es una biblioteca extendidísima en ciencia y tecnología. Es muuuuy bueno que la conozcáis. [Aquí](https://matplotlib.org/tutorials/introductory/pyplot.html) tenéis muchos ejemplos.
