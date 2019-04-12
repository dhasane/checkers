


import sys
import time
import random as rand

BLANCO='-'
TOT=0
J1={
    'pieces':'xX',
    'adversary':'oO',
    'crown':7,
    'direction':{
        'x':[(1,1),(1,-1)],
        'X':[(1,1),(1,-1),(-1,1),(-1,-1)]
    }
}

J2={
    'pieces':'oO',
    'adversary':'xX',
    'crown':0,
    'direction':{
        'o':[(-1,1),(-1,-1)],
        'O':[(1,1),(1,-1),(-1,1),(-1,-1)]
    }
}

# crea un tablero de tamanio tam 
def crearTablero(tam):
    tab = [ [ BLANCO for j in range(tam) ] for i in range(tam)]
    P=['x','x','x',BLANCO,BLANCO,'o','o','o']
    for i in range(tam*tam):
        v=P[ int(i/tam) ]
        if i % 2 == int(i/tam)%2 :
            tab[int(i / tam)][i%tam] = v
    return tab

# imprime el tablero tab
def imprimirTablero(tab):
    imprimir(' |0|1|2|3|4|5|6|7|')
    for i in range(8):
        linea = ""
        for j in range(8):
            linea += "|" +tab[i][j]
        linea += "|"
        imprimir( i,linea )
    imprimir(" ")

def recmov(tablero,J,i,j):
    R=[]
    T=[]
    for dir in J['direction'][tablero[i][j]]:
        i_=i+2*dir[0]
        j_=j+2*dir[1]
        if i_ in range(8) and j_ in range(8) and tablero[i+dir[0]][j+dir[1]] in J['adversary'] and tablero[i_][j_]==BLANCO:
            T=recmov(makeMove(tablero,[(i,j),(i_,j_)],J),J,i_,j_)
            for k in range(len(T)):
                T[k]=[(i,j)]+T[k]
            R=R+T
    if len(R)==0:
        return [[(i,j)]]
    return R

def makeMove(tablero,m,J):
    E=[[tablero[i][j] for j in range(8)]for i in range(8)]
    if not (m is None):
        for i in range(1,len(m)):
            E[m[i][0]][m[i][1]]=E[m[i-1][0]][m[i-1][1]]
            E[m[i-1][0]][m[i-1][1]]=BLANCO
            if abs(m[i-1][0]-m[i][0])>1:
                x=int((m[i-1][0]+m[i][0])/2)
                y=int((m[i-1][1]+m[i][1])/2)
                E[x][y]=BLANCO
            if m[i][0]==J['crown']:
                E[m[i][0]][m[i][1]]=J['pieces'][1]
    
    return E

def moves(tablero,J):
    M=[]
    take=False
    for i in range(8):
        for j in range(8):
            if tablero[i][j] in J['pieces']:
                T=recmov(tablero,J,i,j)
                if len(T[0])>1:
                    take=True
                    M=M+T
    if not take:
        for i in range(8):
            for j in range(8):
                if tablero[i][j] in J['pieces']:
                    for dir in J['direction'][tablero[i][j]]:
                        if i+dir[0] in range(8) and j+dir[1] in range(8) and tablero[i+dir[0]][j+dir[1]]==BLANCO:
                            M=M+[[(i,j),(i+dir[0],j+dir[1])]]
    return M

# cuenta la cantidad de tableros viejos son exactamente iguales al tablero actual
# retorna el numero de coincidencias
def ciclos(T,Tv):
    coincidencias = 0 
    i = 0
    for tab in Tv :
        if tab == T:
           coincidencias += 1
    
    return coincidencias

# esta funcion sirve para definir si el jugador J ha perdido
# evalua si el jugador J tiene movimientos posibles
def lose( tablero, tam, J):
    if tam == 0 :
        return True
    for e in tablero:
        if J['pieces'][0] in e or J['pieces'][1] in e:
            return False 
    
    return True

# cuenta la cantidad de fichas de cada jugador y retorna el jugador con mayor cantidad de fichas
def contarJugadores(tablero):
    x = 0
    o = 0
    ganador = 0
    for i in range( len(tablero) ):
        for j in range( len ( tablero[i]) ):
            if   'x' == tablero[i][j] or 'X' == tablero[i][j]:
                x+=1
            elif 'o' == tablero[i][j] or 'O' == tablero[i][j]:
                o+=1
    if x > o:
        ganador = 1
    elif o > x:
        ganador = 2

    return ganador

# realiza el llamado al jugador f para decidir la siguiente jugada, teniendo en cuenta el tiempo 
# en caso de superar MaxTime, se retorna None, de lo contrario retorna el movimiento seleccionado
def race(f,MaxTime,*args):
    try:
        t1=time.time()
        R=f(*args)
        t2=time.time() - t1
        if t2 <=MaxTime:
            return R, t2
        return None, t2
    except:
        imprimir( "error en la ejecucion del jugador" )
        return None, 0

def imprimir(*args):
    imp = ''
    
    for i in args:
        imp +=str(i)
    print( imp )        #py3
    #print imp          #py2
    
'''
T=[
['x','-','-','-','-','-','-','-'],
['-','x','-','-','-','-','-','x'],
['-','-','x','-','x','-','x','-'],
['-','-','-','-','-','x','-','x'],
['o','-','-','-','o','-','o','-'],
['-','-','-','o','-','-','-','o'],
['o','-','-','-','-','-','-','-'],
['-','o','-','o','-','-','-','-']
]'''

try:
    L=[sys.argv[1][:len(sys.argv[1])-3],sys.argv[2][:len(sys.argv[2])-3]]
    rand.shuffle(L)
    imprimir( L[0]," juega como X" )
    imprimir( L[1]," juega como O" )
    exec("import "+L[0]+" as LP1")
    exec("import "+L[1]+" as LP2")
    P1=LP1.player
    P2=LP2.player
    if len(sys.argv)>3:
        MaxTime=float(sys.argv[3])
    else:
        MaxTime=float("inf")
except:
    imprimir( "uso:python checkers.py <lib1.py> <lib2.py> [maxtime(segundos)]" )
    exit()

memoria = 20    # cantidad de tableros guardados para revisar ciclos
Tv = []         # tableros viejos

ganador = 0     # | 0 : empate | 1 : jugador 1 | 2 : jugador 2 |

tablero=crearTablero(8)
imprimir("tablero inicial :")
imprimirTablero(tablero)
fin=False
k=0             # contador de turnos en la partida
M  = []         # lista de movimientos posibles

tiempo = 0

tiempoTotal = time.time()
tiempoj1 = 0 
tiempoj2 = 0
while not fin:

    # jugadas posibles jugador 1
    
    M=moves(tablero,J1)
    fin=lose(tablero,len(M),J1)

    if not fin:
        # turno jugador 1
        m, tiempo = race(P1,MaxTime,tablero,M,'X')
        tablero=makeMove(tablero,m,J1)

        imprimir("-----------")
        imprimir("turno : ",J1["pieces"]," (",L[0],")")
        imprimirTablero(tablero)

        coincidencias = ciclos(tablero, Tv)
        imprimir("coincidencias : ",coincidencias,"\ttiempo jugada : ",tiempo)
        tiempoj1 += tiempo
        # fin turno jugador 1
        
        # verificacion jugador 1 
        if not(m in M):
            imprimir("jugada invalida por : ", J1["pieces"])
            fin = True
            ganador = 2
        elif tiempo > MaxTime:
            imprimir("jugador ", J1["pieces"], " ha excedido el tiempo")
            fin = True
            ganador = 2
        elif coincidencias >= 5:
            ganador =  contarJugadores(tablero)
            fin = True
        else: # no tiene sentido revisar si es viable, si el jugador ya incumplio una de las condiciones
            # jugadas posibles jugador 2
            M=moves(tablero,J2)
            fin=lose(tablero,len(M),J2)
            if fin:
                ganador = 1
        # fin verificacion 1

        Tv += [tablero] # tablero de repeticiones
        if len(Tv) > memoria:
            Tv.pop(0)
        
        if not fin:
            # turno jugador 2 
            m, tiempo = race(P2,MaxTime,tablero,M,'O')
            tablero=makeMove(tablero,m,J2)

            imprimir("-----------")
            imprimir("turno : ",J2["pieces"]," (",L[1],")")
            imprimirTablero(tablero)

            coincidencias = ciclos(tablero, Tv)
            imprimir("coincidencias : ",coincidencias,"\ttiempo jugada : ",tiempo)
            tiempoj2 += tiempo
            # fin turno jugador 2

            # verificacion jugador 2 
            if not(m in M):
                imprimir("jugada invalida por : ", J2["pieces"])
                fin = True
                ganador = 1
            elif tiempo > MaxTime:
                imprimir("jugador ", J2["pieces"], " ha excedido el tiempo")
                fin = True
                ganador = 1
            elif coincidencias >= 5:
                ganador =  contarJugadores(tablero)
                fin = True
            
            # aqui no es necesario tener un else adicional, ya que en este caso el while actua de forma equivalente
            # fin verificacion 2

            Tv += [tablero] # tablero de repeticiones
            if len(Tv) > memoria:
                Tv.pop(0)

    else: # aqui se usa el else, ya que en el otro caso, hay mas situacioens de fin, aqui solo hay 1
        ganador = 2   

    k+=1

tiempoTotal = time.time() - tiempoTotal

imprimir("\n")
if ganador == 1:
    imprimir( "gana jugador : ", J1['pieces'],"(",L[0],")")
elif ganador == 2:
    imprimir( "gana jugador : ", J2['pieces'],"(",L[1],")")
else:
    imprimir("empate")


imprimir( "\npartida terminada en ", k, " turnos\t tiempo total : ",tiempoTotal )
imprimir("tiempo total ",J1['pieces']," ",L[0], ": ", tiempoj1)
imprimir("tiempo total ",J2['pieces']," ",L[1], ": ", tiempoj2)