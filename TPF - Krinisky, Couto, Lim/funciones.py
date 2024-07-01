#Para crear los equipos
import random 
#Para crear los graficos
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np 
from pokemon import TYPES,TYPES_COLORS
#Para la creacion de los Pokemon , Team y los combates
from team import Team
from pokemon import Pokemon
from move import Move
from combat import *
#Para el combate pokemon visual
import visualcombat as vc


def diccionarios_pokemones(archivo) -> list[dict[str:str]]:
    '''
    La funcion diccionarios_pokemones() recibe un archivo con dato de 
    entrada y devuelve una lista de diccionarios (pokemones_a_elegir) con todos los 
    pokemones que NO son legendarios, con sus respectivos datos cada uno 
    (id, nombre, tipos, hp, ataques, defensa, velocidad, altura, peso y movimientos) y devuelve
    un diccionario de diccionarios con los nombres de los pokemones como claves y como valores 
    otros diccionarios que tienen como clave caracteristicas(hp,type1,attack,moves,etc) y
    como valores las que le corresponden a cada pokemon \n
    
    Parametros:\n
        --> nombre del archivo CSV con todos los pokemones y sus caracteristicas \n 
    Retorna: \n
        --> pokemones_a_elegir (list[dict[str:str/list]]) 
    '''
    with open(archivo, 'r') as pokemones: # Abre el archivo.csv en modo lectura con el alias 'pokemones'
        pokemones_a_elegir = {} # Creacion de una lista vacia para colocar todos los pokemones NO legendarios
        puntero = 1 # Se agrega un puntero para empezar a recorrer las lineas del archivo
        for linea in pokemones: # Se inicializa un ciclo for para recorrer cada linea del archivo
            if puntero == 1: # Si el puntero es igual a 1, se le suma 1 y no hace nada. Esto sirve para evitar que se agregue el encabezado a la lista de pokemones
                puntero += 1
                continue
            elif puntero > 1: # Si el puntero es mayor a 1, se comienza a trabajar sobre la linea seleccionada
                linea = linea.rstrip('\n') # Se elimina los saltos de linea de la linea
                lista = linea.split(',') # Se crea una lista separando por comas los elementos de la lista
                if lista[-2] == '0': # si el anteultimo elemento (Que marca si es legendario o no) es 0, entonces puedo continuar al siguiente paso
                    pokemon = {} # Creo un diccionario vacio 'Pokemon' para que se vayan guardando todos los elementos de la lista de la linea
                    pokemon['pokedex_number'] = int(lista[0])
                    pokemon['type1'] = lista[2]
                    if lista[3]=="": # Este proceso se realiza ya que, si es que el pokemon no tiene un segundo tipo, seria muy poco util guardar en el diccionario un par cuyo valor sea un string vacio
                        pokemon['type2']=''
                    else:
                        pokemon['type2'] = lista[3] # En caso de que el pokemon si tenga un segundo tipo, se agrega el par al diccionario
                    pokemon['hp'] = int(lista[4])
                    pokemon['attack'] = int(lista[5])
                    pokemon['defense'] = int(lista[6])
                    pokemon['sp_attack'] = int(lista[7])
                    pokemon['sp_defense'] = int(lista[8])
                    pokemon['speed'] = int(lista[9])
                    if lista[11] == '':
                        pokemon['height_m'] = ''
                    else: 
                        pokemon['height_m'] = float(lista[11])
                    if lista[12] == '':
                        pokemon['weight_kg'] = ''
                    else:
                        pokemon['weight_kg'] = float(lista[12])
                    list_movimientos = lista[14].split(';') # Se separan los movimientos en una lista
                    pokemon['moves'] = list_movimientos
                    pokemones_a_elegir[lista[1]] = pokemon #  Se añade el diccionario del Pokémon a la lista de pokemones a elegir
                puntero += 1 # Al puntero se le suma 1 para seguir con la otra linea
        return pokemones_a_elegir # Esta funcion retorna el diccionario completo con todos los pokemones a elegir que NO sean legendarios
            
def dicc_efectividad(archivo:str) -> dict[str:float]:
    '''
    La funcion dicc_efectividad() recibe como parametro el nombre de un archivo.csv que indica que tan eficaz es\n 
    un tipo de movimiento pokemon con el restos de los tipos. Esta funcion se encarga de interpretar el archivo \n
    y crear un diccionario cuyas claves sean los tipos de pokemones, y los valores de cada uno son un diccionario\n
    que contiene como valores los tipos de pokemones y su efectividad con el tipo que es la clave del diccionario.\n

    Parametros:
        --> archivo: str del nombre del archvio con la efectividad
    Retorna:
        --> efective: un diccionario con cada tipo como clave y como valor otro diccionario 
        con claves del nombre del resto de tipos y como valores la efectividad del primer tipo al segundo
    '''
    with open(archivo,'r') as efectividad:
        efective = {}
        puntero = 1
        for linea in efectividad:
            if puntero == 1:
                puntero += 1
                continue
            else:
                linea = linea.rstrip('\n')
                lista = linea.split(',')
                efective[lista[0]] = {'normal':float(lista[1]), 'fire':float(lista[2]), 'water':float(lista[3]),'electric':float(lista[4]),'grass':float(lista[5]),'ice':float(lista[6]),'fighting':float(lista[7]),'poison':float(lista[8]),'ground':float(lista[9]),'flying':float(lista[10]),'psychic':float(lista[11]),'bug':float(lista[12]),'rock':float(lista[13]),'ghost':float(lista[14]),'dragon':float(lista[15]),'dark':float(lista[16]),'steel':float(lista[17]),'fairy':float(lista[18])}
                puntero += 1
        return efective
    
def dic_movimientos(file: str) -> dict:
    '''
    La funcion dic_movimientos() recibe como parametro un archivo.csv que contiene los\n
    datos especificos de cada movimiento, para luego crear un diccionario cuyas claves sean\n
    el nombre de cada movimiento y sus valores sean diccionarios que contengan los datos especificos\n
    del movimiento.

    Parametros:
        --> file:str con el nombre del archivo CSV con los movimientos y sus datos
    Retorna:
        --> diccionariomovs: un diccionario con los nombres de los movimientos como claves, y
        diccionarios como valores que dentro de estos las claves son las caracteristicas(power,accuracy,PP,etc)
        y sus valores son la cantidad de cada tipo de estos
    '''
    with open(file) as movs:
        diccionariomovs = {}
        puntero = 1
        for linea in movs: # Se inicializa un ciclo for para recorrer cada linea del archivo
            if puntero == 1: # Si el puntero es igual a 1, se le suma 1 y no hace nada. Esto sirve para evitar que se agregue el encabezado a la lista de pokemones
                puntero += 1
                continue
            elif puntero > 1: # Si el puntero es mayor a 1, se comienza a trabajar sobre la linea seleccionada
                linea = linea.rstrip('\n') # Se elimina los saltos de linea de la linea
                lista = linea.split(',') # Se crea una lista separando por comas los elementos de la lista
                nombrePokemon = lista[0]
                movimiento = {} # Creo un diccionario vacio 'Pokemon' para que se vayan guardando todos los elementos de la lista de la linea
                movimiento['type'] = (lista[1])
                movimiento['category'] = (lista[2])
                movimiento['pp'] = int(lista[3])
                movimiento['power'] = int(lista[4])
                movimiento['accuracy'] = int(lista[5])
                diccionariomovs[nombrePokemon] = movimiento
                puntero += 1
    move = Move
    dicc_final = []
    for nombre,movimiento in diccionariomovs.items():
        dicc_final.append(move.from_dict(nombre,movimiento))
    return diccionariomovs

def crear_equipos(cant_equipos: int) -> list[Team]:
    '''
    La funcion crear_equipos genera una lista de equipos con Pokemones aleatorios en clase
    Team a partir de la info obtenida en ambos csv (moves y pokemon).

    Parámetros:
        --> cant_equipos: Cantidad de equipos que quieren ser creados (int).

    Retorna:
        --> Lista de objetos clase Team de la cantidad de equipos pedida (list[Team]).
    '''
    
    equipos = []
    poknames = []
    pokemones_data = diccionarios_pokemones('pokemons.csv')
    movimientos = dic_movimientos('moves.csv')
    nrodeequipo = 1
    for name in pokemones_data.keys():
        poknames.append(name)
    #Hasta aca cree las tres variables con info necesarias pokemonesdata(diccionario de pokemones y su info), movimientos(diccionario de los movimientos de los pokemones y su info) y poknames(Lista con el nombre de todos los pokemones)
    while len(equipos) < cant_equipos:
        equipo = []
        nombres = random.sample(poknames,6) # Elije 6 nombres de pokemones random
        for pkname in nombres:
            pokemon = Pokemon.from_dict(pkname,pokemones_data[pkname],movimientos) # Crea al pokemon
            equipo.append(pokemon) # Lo agrega al equipo 
        team = Team(f"Equipo_{nrodeequipo}",equipo)# Pasa a la lista de pokemones a clase Team y le pone un nombre
        nrodeequipo += 1
        equipos.append(team)
    return equipos

def aptitud(equipos:list) -> list[list]:
    '''
    La funcion aptitud() recibe una lista de equipos Pokemon y evaluá el rendimiento de 
    cada equipo mediante simulaciones de combate contra 400 equipos generados aleatoriamente.
    Utiliza un diccionario de efectividad para determinar los ganadores de cada combate y
    cuenta las victorias de cada equipo. Por ultimo, devuelve una lista de los equipos
    originales y una lista de tuplas con el nombre de cada equipo y su respectivo conteo
    de victorias.

    Parametros:
        -> equipos: Lista de Team con los equipos que se estan probando

    Retorna:
        -> equipos: la misma Lista de Team que se introdujo
        -> tuple_aptitud: lista de listas con dos items cada una estilo tupla,
        el primero el nombre del equipo y el segundo la cantidad de combates que gano
    '''
    efectividad = dicc_efectividad('effectiveness_chart.csv')
    tuple_aptitud = []
    lista_contadores=[]
    tupla = []
    # print("equipos: ",type(equipos))
    equipos_a_pelear = crear_equipos(400)
    for equipo in equipos:
        # print("Equipo:", type(equipo))
        contador = 0
        for equipo_pelea in equipos_a_pelear:
            ganador = get_winner(equipo,equipo_pelea,efectividad)
            if ganador == equipo:
                contador += 1
        lista_contadores.append(contador)
    for i in range(0,len(equipos)):
        tupla = [equipos[i].name,lista_contadores[i]]
        tuple_aptitud.append(tupla)
    return equipos,tuple_aptitud


def contar_diversidad(epoca: int, equipos: list[Team])-> str|int|dict[str:int]:
    '''
    La funcion contar_diversidad() recibe la epoca en la que se encuentra y 
    una lista de Team y devuelve la epoca, la cantidad de pokemon distintos que hay en todos
    los teams y la cantidad de cada pokemon que hay en todos los equipos para poder ser escrito en el csv de epochs.

    Parametros:
    --> epoca: la epoca en la que se encuentra
    --> equipos: list[Team] que quieren ser censados

    Retorna:
    --> epoca: epoca
    --> diversidad: cantidad de pokemon distintos que hay en todos los teams
    --> dic_diversidad: diccionario que sus claves son nombres de pokemones y 
    sus valores la cantidad de veces que aparecen en la totalidaad de los equipos
    '''
    todos_los_pokemones=[]
    for equipo in equipos:
        for pk in equipo.pokemons:
            todos_los_pokemones.append(pk.name)
    dic_diversidad ={}
    for pk in todos_los_pokemones:
        if pk in dic_diversidad:
            dic_diversidad[pk] += 1
        else:
            dic_diversidad [pk] = 1


    diversidad = len(dic_diversidad.keys())


    return epoca,diversidad,dic_diversidad

def contar_mejores_equipos(epoca,equipos,aptitudes): # Mejores 5 equipos por epoca
    '''
    La funcion contar_mejores_equipos() recibe la epoca, los equipos y sus aptitudes 
    y devuelve una lista con los mejores 5 equipos pokemon y sus aptitudes para poder
    ser escritos en el csv de best_teams

    Parametros:
        --> epoca: epoca de la iteracion
        --> equipos: list[Team] con todos los equipos de la epoca
        --> aptitudes: lista de listas con primer valor el nombre del equipo y del segundo
        valor la aptitud de la epoca del equipo

    Retorna:
        --> listafinal: lista con la epoca,
    '''
    mejores_equipos=bubble_sort(aptitudes)
    mejores_equipos = mejores_equipos[:5]
    listafinal =[]
    for equipo in mejores_equipos:
        listainfo = [] #lista con la info (epoca,aptitud, nombre, starter,pokemones)
        listainfo.append(epoca)
        equipoactual=buscar_equipo_por_nombre(equipo[0],equipos)
        listainfo.append(equipo[1])
        listainfo.append(equipoactual.name)
        listainfo.append('0')
        for pokemon in equipoactual.pokemons:
            listainfo.append(pokemon.name)
        listafinal.append(listainfo)
    return listafinal

def buscar_equipo_por_nombre(nombre: str,equipos:list[Team])-> Team:
    '''
    La funcion buscar_equipo_por_nombre() recibe el nombre de un equipo y una 
    lista con objetos clase Team y busca en la lista de Team el Team que tiene
    ese nombre y lo retorna.

    Parametros:
        --> nombre: str del nombre del equipo que se busca
        --> equipos: list[Team] con el equipo que se busca
    
    Retorna:
        --> equipo: El equipo al que le pertenece el nombre
    '''
    for equipo in equipos:
        if equipo.name == nombre:
            return equipo


def bubble_sort(lista): # para mejores equipos de mayor a peor
    '''
    La funcion bubble_sort() es un bubble sort normal con la unica
    diferencia que compara elementos en una lista de listas comparando 
    el segundo elemento de la lista dentro de la lista ordenando la lista de mayor a menor y es utilizada para
    el csv de best_teams.

    Parametros:
        --> lista: la lista de listas que se quiere ordenar

    Retorna:
        --> lista: la lista ya ordenada
    
    '''
    n = len(lista)

    for i in range(n):

        for j in range(0, n-i-1):

            if lista[j][1] < lista[j+1][1]:

                lista[j], lista[j+1] = lista[j+1], lista[j]
    
    return lista

def getbestteam(besteam: str):
    '''
    La funcion getbesteam() toma de parametro el nombre del
    archivo csv de best_teams y accede a el para buscar el
    mejor equipo de la ultima epoca, luego crea y retorna
    un Team con los pokemones de este.

    Parametros:
        --> besteam: el nombre del csv al que se quiere acceder

    Retorna:
        --> objeto clase Team con el nombre y los pokemones del
        mejor equipo de la ultima epoca de best_teams
 

    '''
    with open(besteam) as besteam:
        contador = 0
        for linea in besteam:
            contador +=1
            if contador == 247: # Linea donde se encuentra el mejor equipo de la ultima epoca
                linea = linea.strip()
                linea = linea.split(',')
                break
        best_team = linea[4:]
        best_team_name = linea[2]
    return crearequipoespecifico(best_team_name,best_team)


        
        
def main()->None:
    '''
    La funcion main() ejecuta el programa principal del Trabajo Practico. Primero crea los dos archivos csv,
    luego crea los equipos y itera las 50 epocas del algortimo genetico, escribiendo el avance en los csv para
    finalmente crear los graficos con los datos finales y probar si el mejor equipo de la ultima epoca es apto 
    para ser campeon de la liga de Kanto.
    '''
    # creo los dos archivos al principio asi no hay que eliminarlos cada vez que se ejecuta el codigo
    with open("epochs1.csv", "w") as epocas:
        epocas.close()
    with open("best_teams1.csv", "w") as besteams:
        besteams.write('epoch,aptitude,team_name,starter,pokemon_1,pokemon_2,pokemon_3,pokemon_4,pokemon_5,pokemon_6\n')
        besteams.close()
    #Creo los primeros 50 equipos
    teams = crear_equipos(50)
    epoca = 0
    #Hago las 50 epocas de algoritmo genetico
    for i in range(50):
        teams, epoca = algoritmo_genetico(teams,epoca)
        epoca = i + 1
    #Una vez finalizadas las epocas creo los graficos
    graficos('epochs1.csv','best_teams1.csv')
    #Obtengo el mejor equipo de las 50 epocas
    mejorequipo = getbestteam("best_teams1.csv")
    #Lo hago luchar contra la Elite 4 y el Campeon de Kanto para ver si es digno de convertirse en campeon
    combatonterminal(mejorequipo)


# def buscarsublista(nombre,aptitudes):
#     for 

def algoritmo_genetico(equipos:list[Team],epoch:int)->list[Team]|int:
    '''
    La funcion algoritmo_genetico() se encarga de primero recibir en que epoca se encuentra y
    una lista de Teamy escribir como van los equipos y su diversidad en epochs y en best_teams,
    luego empieza con el algoritmo genetico. EN este, dependiendo de la aptitud de cada equipo 
    les pone cuantos pokemones del equipo se van a reproducir. Por ejemplo, si dos equipos tienen
    +350 de aptitud van a tener un 3 , es decir, que se van a intercambiar 3 pokemones de un equipo
    por 3 pokemones del otro. Luego, se va a repetir el proceso para todos los equipos. Los equipos 
    que no llegaron a la cantidad minima de aptitud para reproducirse van a ser intercambiados por 
    equipos generados aleatoriamente de nuevo para probar nuevas combinaciones.

    Parametros:
        --> equipos: lista de objetos clase Team.
        --> epoch: la epoca en la que se enuentra el programa
    
    Retorna:
        --> equipos: la lista de Team ya modificada por el algoritmo genetico
        --> epoch: la epoca en la que se enuentra el programa
    '''

    equipos, aptitudes = aptitud(equipos)

    # ahora escribo en los archivos los datos de esta epoca
    with open("epochs1.csv",'a') as epocas:
        epoch,diversidad,dicdiversidad = contar_diversidad(epoch,equipos)
        epocas.write(f"{epoch},{diversidad}")
        for nombre,cantidad in dicdiversidad.items():
            epocas.write(f",{nombre},{cantidad}")
        epocas.write('\n')
    with open("best_teams1.csv",'a') as besteams:
        datosequipos = contar_mejores_equipos(epoch,equipos,aptitudes)
        for equipo in datosequipos:
            besteams.write(f"{equipo[0]},{equipo[1]},{equipo[2]},{equipo[3]},{equipo[4]},{equipo[5]},{equipo[6]},{equipo[7]},{equipo[8]},{equipo[9]}\n")
    
    
    for equipo in aptitudes:
        contador = 0
        if equipo[1] >=150:
            contador +=1
            if equipo[1] >= 250:
                contador +=1
                if equipo[1] >= 350:
                    contador += 1
        equipo[1]=contador # El valor de la aptitud pasa a ser la cantidad de pokemones del equipo que van a mutar
    #Ahora se fija que haya cantidad par para la mutacion y si hay impar se busca algun pokemon y se le retira un contador asi hay parejas para todas las mutaciones
    contador1=0
    contador2=0
    contador3=0
    for equipo in aptitudes:
        if equipo[1] == 1:
            contador1 +=1
        if equipo[1] == 2:
            contador2 +=1
        if equipo[1] == 3:
            contador3 +=1
    if contador3 % 2 != 0:
        for equipo in aptitudes:
            if equipo[1] == 3:
                equipo[1] -=1
                contador2+=1
                contador3-=1
                break
    if contador2 % 2 != 0:
        for equipo in aptitudes:
            if equipo[1] == 2:
                equipo[1] -=1
                contador1+=1
                contador2-=1
                break
    if contador1 % 2 != 0:
        for equipo in aptitudes:
            if equipo[1] == 1:
                equipo[1] -=1
                contador1 -=1
                break

    #Ahora que tengo una lista de listas[equipo,cantidad de equipos que tienen que cambiar
    cambios3= contador3//2
    cambios2= contador2//2
    cambios1= contador1//2

    #Cambio de pokemones

    #Los peores equipos se cambian
    for equipo,apt in aptitudes:
        if apt == 0:
            newteam = crear_equipos(1)
            newteam = newteam[0] #Porque la funcion crear equipos devuelve una lista de equipos
            equipoparareemplazar = buscar_equipo_por_nombre(equipo,equipos) #busco el objeto a partir de su nombre
            index= equipos.index(equipoparareemplazar) # busco el indice del equipo en la lista de equipos
            newteam.name = equipo # le pongo el mismo nombre para evitar problemas
            equipos[index] = newteam   
    
    
    
    if cambios3>=1:
        
        for i in range(cambios3):

            nombreacambiar =[] #nombreacambiar es el nombre de los equipos a cambiar
            for equipo,contador in aptitudes:
                if len(nombreacambiar) == 2: break
                elif contador == 3:
                    nombreacambiar.append(equipo)
                    aptitudes[aptitudes.index([equipo,contador])][1] = 0
                    

            equipoacambiar=[]
            for nombre in nombreacambiar:
                equipoacambiar.append(buscar_equipo_por_nombre(nombre,equipos))
            #elijo 3 numeros para cada equipo
            opciones=[0,1,2,3,4,5]
            num1 = random.sample(opciones,k=3)
            num2 = random.sample(opciones,k=3)

            indice1=equipos.index(equipoacambiar[0])
            indice2=equipos.index(equipoacambiar[1])

            pokemon1a= equipoacambiar[0].pokemons[num1[0]]
            pokemon1b= equipoacambiar[0].pokemons[num1[1]]
            pokemon1c= equipoacambiar[0].pokemons[num1[2]]
            pokemon2a= equipoacambiar[1].pokemons[num2[0]]
            pokemon2b= equipoacambiar[1].pokemons[num1[1]]
            pokemon2c= equipoacambiar[1].pokemons[num1[2]]

            #que el pok no sea el mismo(compara los nombres de los pokemones que se van a intercambiar)
            intentos = 0
            while (notinteam(equipoacambiar[0],[pokemon2a,pokemon2b,pokemon2c]) == False) or (notinteam(equipoacambiar[1],[pokemon1a,pokemon1b,pokemon1c]) == False):
                num1 = random.sample(opciones,k=3)
                num2 = random.sample(opciones,k=3) 
            # print('defino poks')
                pokemon1a= equipoacambiar[0].pokemons[num1[0]]
                pokemon1b= equipoacambiar[0].pokemons[num1[1]]
                pokemon1c= equipoacambiar[0].pokemons[num1[2]]
                pokemon2a= equipoacambiar[1].pokemons[num2[0]]
                pokemon2b= equipoacambiar[1].pokemons[num1[1]]
                pokemon2c= equipoacambiar[1].pokemons[num1[2]]
                if intentos >3: 
                    break
                intentos +=1

            #cambio en el primer equipo
            if intentos > 3:
                continue
            equipoacambiar[0].pokemons[num1[0]] = pokemon2a
            equipoacambiar[0].pokemons[num1[1]] = pokemon2b
            equipoacambiar[0].pokemons[num1[2]] = pokemon2c
            #cambio en el segundo equipo
            equipoacambiar[1].pokemons[num2[0]] = pokemon1a
            equipoacambiar[1].pokemons[num2[1]] = pokemon1b
            equipoacambiar[1].pokemons[num2[2]] = pokemon1c

            equipos[indice1] = equipoacambiar[0]
            equipos[indice2] = equipoacambiar[1]




    
    if cambios2>=1:
        for i in range(cambios2):
            nombreacambiar =[] #nombreacambiar es el nombre de los equipos a cambiar
            for equipo,contador in aptitudes:
                if len(nombreacambiar) == 2: break
                elif contador == 2:
                    nombreacambiar.append(equipo)
                    aptitudes[aptitudes.index([equipo,contador])][1] = 0
                    
            equipoacambiar=[]
            for nombre in nombreacambiar:
                equipoacambiar.append(buscar_equipo_por_nombre(nombre,equipos))
            #elijo 2 numeros para cada equipo
            opciones=[0,1,2,3,4,5]
            num1 = random.sample(opciones,k=2)
            num2 = random.sample(opciones,k=2)
            indice1=equipos.index(equipoacambiar[0])
            indice2=equipos.index(equipoacambiar[1])

            pokemon1a= equipoacambiar[0].pokemons[num1[0]]
            pokemon1b= equipoacambiar[0].pokemons[num1[1]]
            pokemon2a= equipoacambiar[1].pokemons[num2[0]]
            pokemon2b= equipoacambiar[1].pokemons[num1[1]]
            intentos = 0
            #que el pok no sea el mismo(compara los nombres de los pokemones que se van a intercambiar)
            while (notinteam(equipoacambiar[0],[pokemon2a,pokemon2b]) == False) or (notinteam(equipoacambiar[1],[pokemon1a,pokemon1b]) == False):
                num1 = random.sample(opciones,k=2)
                num2 = random.sample(opciones,k=2) 
                pokemon1a= equipoacambiar[0].pokemons[num1[0]]
                pokemon1b= equipoacambiar[0].pokemons[num1[1]]
                pokemon2a= equipoacambiar[1].pokemons[num2[0]]
                pokemon2b= equipoacambiar[1].pokemons[num1[1]]
                if intentos >3: 
                    break
                intentos+=1

            #cambio en el primer equipo
            if intentos >3: 
                    continue
            equipoacambiar[0].pokemons[num1[0]] = pokemon2a
            equipoacambiar[0].pokemons[num1[1]] = pokemon2b
            #cambio en el segundo equipo
            equipoacambiar[1].pokemons[num2[0]] = pokemon1a
            equipoacambiar[1].pokemons[num2[1]] = pokemon1b



            equipos[indice1] = equipoacambiar[0]
            equipos[indice2] = equipoacambiar[1]


    if cambios1>=1:
        for i in range(cambios1):
            nombreacambiar =[] #nombreacambiar es el nombre de los equipos a cambiar
            for equipo,contador in aptitudes:
                if len(nombreacambiar) == 2: break
                elif contador == 1:
                    nombreacambiar.append(equipo)
                    aptitudes[aptitudes.index([equipo,contador])][1] = 0

            equipoacambiar=[]
            for nombre in nombreacambiar:
                equipoacambiar.append(buscar_equipo_por_nombre(nombre,equipos))
            #elijo 2 numeros para cada equipo
            opciones=[0,1,2,3,4,5]
            num1 = random.sample(opciones,k=1)
            num2 = random.sample(opciones,k=1)
            indice1=equipos.index(equipoacambiar[0])
            indice2=equipos.index(equipoacambiar[1])

            pokemon1a= equipoacambiar[0].pokemons[num1[0]]
            pokemon2a= equipoacambiar[1].pokemons[num2[0]]
            intentos = 0
            #que el pok no sea el mismo(compara los nombres de los pokemones que se van a intercambiar)
            while ((notinteam(equipoacambiar[0],[pokemon2a]) == False) or (notinteam(equipoacambiar[1],[pokemon1a]) == False)):
                num1 = random.sample(opciones,k=1)
                num2 = random.sample(opciones,k=1) 
                pokemon1a= equipoacambiar[0].pokemons[num1[0]]
                pokemon2a= equipoacambiar[1].pokemons[num2[0]]
                if intentos >3: 
                    break
                intentos+=1
            #cambio en el primer equipo
            if intentos >3: 
                    continue
            equipoacambiar[0].pokemons[num1[0]] = pokemon2a
            #cambio en el segundo equipo
            equipoacambiar[1].pokemons[num2[0]] = pokemon1a

            equipos[indice1] = equipoacambiar[0]
            equipos[indice2] = equipoacambiar[1]

    
    return equipos,epoch



def notinteam(equipo:Team,listapokemon:list[Pokemon])-> bool:
    '''
    La funcion notinteam() toma a un equipo pokemon(Team) y
    una lista con nombres de pokemon y comprueba si los nombres
    de los pokemon en listapokemon no estan en el Team.\n
    Parametros:
        --> equipo: Team al que se quiere comprobar si los pokemons de listapokemon se encunetran ahi.
        --> listapokemon: lista de nombres de pokemon que se van a probar si estan en el Team.
    Retorna:
        --> bool: True or False dependiendo si hay un pokemon de listapokemon en equipo o no.
    '''
    for pk in equipo.pokemons:
        for nombre in listapokemon:
            if pk.name == nombre.name:
                return False
    else: return True


    
def graficos(archivo1:str,archivo2:str)-> None:
    '''
    La funcion graficos() se encarga de crear,mostrar y guardar 6 graficos sobre los csv finales de epocas y mejores equipos del programa de seleccion natural de Pokemon.
    los graficos son:\n
    1. Diversidad de Pokémon en los Equipos por Época\n
    2. Distribución de Pokémon en los Equipos en la última Época \n
    3. Evolución de la Aptitud a lo largo de las Épocas\n
    4. Distribución de Tipos de Pokémon en los Equipos en la última Época\n
    5. Estadísticas del mejor equipo encontrado\n
    6. Distribución de Tipos de Pokémon en los Equipos por Época\n
    Parametros:\n
        --> archivo1: str del nombre del archivo de epochs\n
        --> archivo2: str del nombre del archivo de best_teams\n
    
    '''
    # 1. Diversidad de Pokémon en los Equipos por Época 
    with open(archivo1,'r') as epochs:
        epocas = []
        diversidad = []
        cant_apariciones_pok = {}
        pok_ultima_epoch = {}
        for linea in epochs:
            linea = linea.rstrip()
            lista = linea.split(',')
            epocas.append(int(lista[0]))
            diversidad.append(int(lista[1]))
            for i in range(2,len(lista)-1,2):
                cant_apariciones_pok[lista[i]] = lista[i + 1]
                if lista[0] == '49':
                    pok_ultima_epoch[lista[i]] = lista[i + 1]

    plt.plot(epocas, diversidad)  
    plt.xlabel('Épocas')
    plt.ylabel('Diversidad') 
    plt.title('Diversidad de Pokemones en los equipos por época') 
    plt.grid(False) 
    plt.tight_layout() 
    plt.savefig('Epocas')
    plt.show() 
    plt.close()
    
    # 2. Distribución de Pokémon en los Equipos en la última Época
    pokemones = []
    contadores = []
    cuantosva = 0 # Solo pone los 25 pokemones mas aparecidos
    for pok,cont in pok_ultima_epoch.items():
        if cuantosva == 25: break
        cuantosva +=1
        pokemones.append(pok)
        contadores.append(cont)
    
    sorted_indices = np.argsort(contadores) # ordeno los indices de una lista asi puedo ordenar las listas cada una
    pok_ord = []
    for i in sorted_indices:
        pok_ord.append(pokemones[i])
    contadores_ord = []
    for i in sorted_indices:
        contadores_ord.append(contadores[i])


    plt.barh(pok_ord,contadores_ord)
    plt.xlabel('Count')
    plt.ylabel('Pokemones')
    plt.title('Pokemon count in best teams')
    plt.savefig('Contadores_pok')
    plt.show()
    plt.close()

    # 3. Evolución de la Aptitud a lo largo de las Épocas
    with open(archivo2,'r') as best:
        aptitud=[]
        epocasusadas=[]
        puntero=1
        for linea in best:
            if puntero==1:
                puntero+=1
                continue
            linea=linea.strip()
            linea=linea.split(',')
            
            if int(linea[0]) in epocasusadas:
                continue
            else:
                aptitud.append(int(linea[1]))
                epocasusadas.append(int(linea[0]))
    plt.figure()
    plt.plot(epocas,aptitud)
    plt.xlabel('Épocas')
    plt.ylabel('Aptitud')
    plt.title('Aptitud a través del tiempo')
    plt.savefig('Aptitud')
    plt.show()
    plt.close()
    

    # 4. Distribución de Tipos de Pokémon en los Equipos en la última Época
    pokemones_data = diccionarios_pokemones('pokemons.csv')
    variedad_tipo = {}
    for pokemon,cant in pok_ultima_epoch.items():
        if pokemones_data[pokemon]["type1"] not in variedad_tipo:
            variedad_tipo[pokemones_data[pokemon]["type1"]] = int(1 * cant)
        else: variedad_tipo[pokemones_data[pokemon]["type1"]] += int(1 * cant)
        if pokemones_data[pokemon]["type2"] not in variedad_tipo and not None:
            variedad_tipo[pokemones_data[pokemon]["type2"]] = int(1 * cant)
        elif pokemones_data[pokemon]["type2"] in variedad_tipo and not None:
            variedad_tipo[pokemones_data[pokemon]["type2"]] += int(1 * cant)
    variedad_tipo.pop('')
    tipos=[]
    cantidadportipo=[]
    for tipo,cant in variedad_tipo.items():
        tipos.append(tipo)
        cantidadportipo.append(cant)
    
    TYPES_COLORS_DICT = {
    'normal': '#A8A77A',
    'fire': '#EE8130',
    'water': '#6390F0',
    'electric': '#F7D02C',
    'grass': '#7AC74C',
    'ice': '#96D9D6',
    'fighting': '#C22E28',
    'poison': '#A33EA1',
    'ground': '#E2BF65',
    'flying': '#A98FF3',
    'psychic': '#F95587',
    'bug': '#A6B91A',
    'rock': '#B6A136',
    'ghost': '#735797',
    'dragon': '#6F35FC',
    'dark': '#705746',
    'steel': '#B7B7CE',
    'fairy': '#D685AD'
    }
    listacoloresordenados=[]
    for tp in tipos:
        if tp in TYPES_COLORS_DICT:
            listacoloresordenados.append(TYPES_COLORS_DICT[tp])


    plt.barh(tipos, cantidadportipo,color=listacoloresordenados) 
    plt.xlabel('Cantidad')  
    plt.ylabel('Tipo')  
    plt.title('Distribución de Tipos de Pokémon en los Equipos en la última Época')  
    plt.grid(False)  
    plt.tight_layout()  
    plt.savefig('DivTipos')
    plt.show() 
    plt.close()


    # 5. Estadísticas del mejor equipo encontrado
    pokemon_stats = {}
    with open(archivo2, 'r') as besteams:
        contador = 0
        for linea in besteams:
            contador+=1
            if contador == 247:
                linea=linea.strip()
                linea=linea.split(',')
                break
        bestteam=linea
    contador = 0
    for item in  bestteam:
        contador+=1
        if contador > 4:
            pokemon_stats[item]= []
    for pk in pokemon_stats.keys():
        pokemon_stats[pk]=pokemones_data[pk]['hp'],pokemones_data[pk]['attack'],pokemones_data[pk]['defense'],pokemones_data[pk]['sp_attack'],pokemones_data[pk]['sp_defense'],pokemones_data[pk]['speed']
    radar_chart(pokemon_stats)
    plt.savefig("BestStats")
    plt.show()
    plt.close()

    
    # 6. Distribución de Tipos de Pokémon en los Equipos por Época
    with open (archivo1,'r') as diversidad:
        pokemonesxepoca=[]
        for epoca in diversidad:
            epocadic={}
            epoca=epoca.strip()
            epoca=epoca.split(',')
            for i in range(2,len(epoca)-1,2):
                epocadic[epoca[i]] = epoca[i+1]
            pokemonesxepoca.append(epocadic)
    tiposporepoca = []
    for epoca in pokemonesxepoca:
        tiposdic={}
        for pok,cant in epoca.items():
            tipo1 = pokemones_data[pok]['type1']
            tipo2 = pokemones_data[pok]['type2']

            if tipo1 not in tiposdic.keys():
                tiposdic[tipo1]= int(cant)
            else: tiposdic[tipo1] += int(cant)

            if tipo2 not in tiposdic.keys():
                tiposdic[tipo2]= int(cant)
            else: tiposdic[tipo2] += int(cant)
        tiposporepoca.append(tiposdic)
    
    for epoca in tiposporepoca:
            epoca.pop('')
    

    df = pd.DataFrame(tiposporepoca)
    df = df.fillna(0) 


    df.plot(kind='area', stacked=True)
    plt.xlabel('Época')
    plt.ylabel('Cantidad')
    plt.title('Distribución de Tipos de Pokémon en los Equipos por Época')
    plt.savefig("TiposPorEpoca") 
    plt.show() 
    plt.close()



def combatonterminal(besteam:Team)-> None:
    '''
    La funcion combatonterminal() se encarga de crear los equipos de la Elite 4 y el
    campeon de Kalos y hacer combatir al equipo introducido como parametro contra ellos, mostrando
    el combate por la terminal de Python, teniendo que tocar ENTER para avanzar en 
    cada combate, si el equipo gana los 5 combates sera coronado nuevo campeon de 
    la liga Pokemon de Kalos. Esta funcion utiliza  getwinner del archvio visualcombat.py ya que aqui
    cada vez que se ejecuta un combate se puede ver como fue por la terminal

    Parametros:
        --> besteam: El equipo que se quiere hacer pelear(se utiliza en main() con el mejor equipo de la ultima epoca del algoritmo genetico)
    '''
    
    efectividad = dicc_efectividad('effectiveness_chart.csv')

    will=crearequipoespecifico("Elite Four Member #1 - Will",['Bronzong', 'Jynx', 'Grumpig', 'Slowbro', 'Gardevoir', 'Xatu'])
    koga = crearequipoespecifico("Elite Four Member #2 - Koga",['Skuntank', 'Toxicroak', 'Swalot', 'Venomoth', 'Muk', 'Crobat'])
    bruno = crearequipoespecifico("Elite Four Member #3 - Bruno",['Hitmontop','Hitmonlee','Hariyama','Machamp','Lucario','Hitmonchan'])
    karen = crearequipoespecifico("Elite Four Member #4 - Karen",['Weavile', 'Spiritomb', 'Honchkrow', 'Umbreon', 'Houndoom', 'Absol'])
    lance=crearequipoespecifico("Champion - Lance",['Salamence', 'Garchomp', 'Dragonite', 'Charizard', 'Altaria', 'Gyarados'])
    ganador = vc.get_winner(besteam,will,efectividad)
    if ganador == besteam:
        input("Presione ENTER para continuar: ")
        ganador = vc.get_winner(besteam,koga,efectividad)
        if ganador == besteam:
            input("Presione ENTER para continuar: ")
            ganador = vc.get_winner(besteam,bruno,efectividad)
            if ganador == besteam:
                input("Presione ENTER para continuar: ")
                ganador = vc.get_winner(besteam,karen,efectividad)
                if ganador == besteam:
                    input("Presione ENTER para continuar: ")
                    ganador = vc.get_winner(besteam,lance,efectividad)
                    if ganador == besteam:
                        print(f"Felicidades {besteam.name}, eres el nuevo campeón de la región de Kanto")


        

def crearequipoespecifico(nombre:str,nombrepokemones: list[str])-> Team:
    '''
    la funcion crearequipoespecifico() crea un equipo Team(Pokemon) a partir de los parametros dados.

    Parametros:
        --> nombre: str con el nombre del equipo.
        --> nombrepokemones: list[str] de los nombres de los Pokemones que quieren ser añadidos al equipo.

    Retorna:
        --> team: Equipo clase Team(Pokemon)
        
    '''
    pokemones_data = diccionarios_pokemones('pokemons.csv')
    pokemones_moves = dic_movimientos("moves.csv")
    equipo=[]
    for pkname in nombrepokemones:
        pokemon = Pokemon.from_dict(pkname,pokemones_data[pkname],pokemones_moves)
        equipo.append(pokemon)
    team = Team(nombre,equipo)

    return team


def radar_chart(pokemon_stats: dict[str:list[int]])-> None:
    '''
    La funcion radar_chart() se encarga de a partir de las stats
    de un equipo pokemon crear mostrar y guardar un radar chart
    con las estadisticas de cada pokemon de ese equipo.

    Parametros:
        --> pokemon_stats: diccionario de diccionarios de las estadisticas del mejor equipo en el formato dic[pokemon:list[stats]]
    '''
    labels = ['hp','attack','defense','sp_attack','sp_defense','speed']
    angles = np.linspace(0, 2 * np.pi, 6, endpoint=False).tolist()
    angles += angles[:1] 
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 160)

    for pokemon, stats in pokemon_stats.items():
        stats += stats[:1]  
        ax.plot(angles, stats, label=pokemon)
        ax.fill(angles, stats, alpha=0.25)

    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))

    for i in range(len(labels)):
        angle_rad = angles[i]
        angle_deg = angle_rad * 180 / np.pi
        ha = 'left'
        if angle_deg > 180:
            ha = 'right'
        ax.annotate(f'{labels[i]}', xy=(angle_rad, 160), xytext=(angle_rad, 170), textcoords='polar', ha=ha, fontsize=10)

    return fig, ax




