# checkers
Arbitro damas

# Reglas
Las reglas del juego se encuentran descritas en el archivo pdf "ReglasDamas.pdf"

# Manual
El programa se debe ejecutar con el siguiente comando:
<pre><code>python checkers.py archivo1 archivo2 [time]</code></pre>

## archivo ##
-Puede ser un archivo .py .jar o un ejecutable el cual describe el comportamiento del jugador
## [time] ##
Es el tiempo maximo del que dispone un jugador antes de que se considere como derrotado

# Entregable
Los siguientes son los requerimientos de los archivos que recibe el comando descrito anteriormente
## Para archivos .py ##
El archivo debe definir una funcion __play(E,J)__ donde E es el estado del tablero representado por una matriz de caracteres con dimensiones de 8x8 (char[8][8]) dicha representacion se realiza de la siguiente manera:
1. 'x':representa fichas blancas normales.
2. 'X':representa fichas blancas coronadas.
3. 'o':representa fichas negras normales.
4. 'O':representa fichas negras coronadas.
5. '-':representa espacios vacios.
  
y J es un caracter que representa el jugador por el cual se esta jugando y puede tomar los valores 'X' y 'O'. Y debe retornar una jugada descrita por un vector de posiciones(donde una posicion es una tupla de enteros) ej:
<pre><code>[(0,0),(2,2),(4,4)]</code></pre>

## Para archivos .jar y ejecutables ##
En este caso el archivo en cuestion correra sobre un proceso aparte y se comunicara con el arbtitro checkers por medio de dos archivos FIFO:
1. pipe\<nombre del archivo\>T: Este archivo lo usara el arbitro para enviarle al jugador el estado del tablero. Este archivo es de solo escritura para el arbitro y de solo lectura para el jugador. ej: Si la entrada es el archivo playDummie(un ejecutable) el nombre del pipe seria pipeplayDummieT.
2. pipe\<nombre del archivo\>M: Este archivo lo usara el jugador para enviarle al arbitro la jugada que ha decidido. Este archivo es de solo escritura para el jugador y de solo lectura para el arbitro. ej: Si la entrada es el archivo playDummie(un ejecutable) el nombre del pipe seria pipeplayDummieM.

### Sintaxix en los pipes ###
#### pipe\<nombre del archivo\>T ####
Por este pipe se enviaran los caracteres que representan el tablero ('x','X','o','O','-') sin incluir las casillas donde no pueden haber fichas (las casillas cuyas coordenadas X + Y sean un numero par). Seguido del estado del tablero se envia el caracter ':' y un caracter que representa las fichas con las que juega el jugador. ej:
<pre><code>
tablero=[
['x','-','x','-','x','-','x','-'],
['-','x','-','x','-','x','-','x'],
['x','-','x','-','x','-','x','-'],
['-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-'],
['-','o','-','o','-','o','-','o'],
['o','-','o','-','o','-','o','-'],
['-','o','-','o','-','o','-','o']
]
Jugador='X'
mensaje='xxxxxxxxxxxx--------oooooooooooo:X'
</code></pre>

#### pipe\<nombre del archivo\>T ####
Por este pipe se enviaran las jugadas que decida realizar el jugador, representadas por las posiciones que toma la pieza en la jugada separadas por ';', donde una posicion esta representada por dos coordenadas separadas por ',' y representadas por numeros o letras
<pre><code>
Jugada=[(0,0),(2,2),(4,4)]
#significa que la ficha en (0,0) se mueve a (2,2) y luego a (4,4) tomando dos piezas
mensaje='0,0;2,2;4,4'
</code></pre>

### Interaccion ###
Las interacciones seran las siguientes:
1. El arbitro envia el estado del tablero al jugador y espera a su respuesta.
2. El jugador envia la jugada decidida.
3. El proceso se repite hasta que haya un ganador.
