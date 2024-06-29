import random
from team import Team
from combat import *


def diccionarios_pokemones(archivo) -> list[dict[str:str]]:
    '''
    La funcion diccionarios_pokemones() recibe un archivo con dato de 
    entrada y devuelve una lista de diccionarios (pokemones_a_elegir)con todos los 
    pokemones que NO son legendarios, con sus respectivos datos cada uno 
    (id, nombre, tipos, hp, ataques, defensa, velocidad, altura, peso y movimientos)
    
    Entrada:
        --> archivo CSV
        
    Salida:
        --> pokemones_a_elegir (list[dict[str:str/list]])
    '''
    with open(archivo, 'r') as pokemones: # Abre el archivo.csv en modo lectura con el alias 'pokemones'
        pokemones_a_elegir = [] # Creacion de una lista vacia para colocar todos los pokemones NO legendarios
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
                    pokemon['id'] = lista[0]
                    pokemon['name'] = lista[1]
                    pokemon['tipo 1'] = lista[2]
                    if lista[3]=="": # Este proceso se realiza ya que, si es que el pokemon no tiene un segundo tipo, seria muy poco util guardar en el diccionario un par cuyo valor sea un string vacio
                        continue
                    else:
                        pokemon['tipo 2'] = lista[3] # En caso de que el pokemon si tenga un segundo tipo, se agrega el par al diccionario
                    pokemon['hp'] = lista[4]
                    pokemon['attack'] = lista[5]
                    pokemon['defense'] = lista[6]
                    pokemon['sp_attack'] = lista[7]
                    pokemon['sp_defense'] = lista[8]
                    pokemon['speed'] = lista[9]
                    pokemon['height'] = lista[11]
                    pokemon['weight'] = lista[12]
                    movimientos = [] # Se crea una lista vacia para guardar todos los movimientos del pokemon
                    list_movimientos = lista[14].split(';') # Se separan los movimientos en una lista  
                    for elemento in list_movimientos:
                        movimientos.append(elemento) # Por cada elemento en list_movimientos, se agrega ese elemento a la lista vacia de movimientos
                    pokemon['movimientos'] = movimientos # Se asigna la lista de movimientos al diccionario del Pokémon
                    pokemones_a_elegir.append(pokemon) #  Se añade el diccionario del Pokémon a la lista de pokemones a elegir
                puntero += 1 # Al puntero se le suma 1 para seguir con la otra linea
        return pokemones_a_elegir # Esta funcion retorna el diccionario completo con todos los pokemones a elegir que NO sean legendarios
            

def dicc_efectividad(archivo):
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
                efective[lista[0]] = {'Normal':lista[1], 'Fire':lista[2], 'water':lista[3],'electric':lista[4],'grass':lista[5],'ice':lista[6],'fighting':lista[7],'poison':lista[8],'ground':lista[9],'flying':lista[10],'psychic':lista[11],'bug':lista[12],'rock':lista[13],'ghost':lista[14],'dragon':lista[15],'dark':lista[16],'steel':lista[17],'fairy':lista[18]}
                puntero += 1
        return efective
    
def algoritmo_genetico():
    equipos = poblacion_inicial(5,6)
    print(aptitud(equipos))
    
def poblacion_inicial(cant_equipos:int, cant_pokemon_equipo:int) -> list[dict,dict,dict,dict,dict,dict]:
    '''
    La funcion crear_equipos() recibe como argumento de entrada la cantidad de equipos pokemon 
    que se quieren crear y cuantos pokemones se quiere que haya en cada equipo. Luego, 
    se generan x equipos con x cantidad de pokemones distintos por equipo y con cuatro movimientos 
    aleatorios por cada pokemon.
    
    Argumentos de entrada:
        --> cant_equipos (int)
        --> cant_pokemon_equipo (int)
        
    Argumentos de salida: 
        --> equipos (list[dict,dict,dict,dict,dict,dict])
    '''
    pokemons = diccionarios_pokemones('pokemons.csv')
    equipos = []
    while len(equipos) < cant_equipos:
        equipo = []
        while len(equipo) < cant_pokemon_equipo:
            generar_pos = random.randint(1,len(pokemons))
            for pokemon in pokemons:
                if pokemons.index(pokemon) == generar_pos:
                    if pokemon['name'] in equipo:
                        continue
                    else:
                        num1 = random.randint(0,len(pokemon['movimientos'])-1)
                        num2 = random.randint(0,len(pokemon['movimientos'])-1)
                        while num2 == num1:
                            num2 = random.randint(0,len(pokemon['movimientos'])-1)
                        num3 = random.randint(0,len(pokemon['movimientos'])-1)
                        while num3 == num2 or num3 == num1:
                            num3 = random.randint(0,len(pokemon['movimientos'])-1)
                        num4 = random.randint(0,len(pokemon['movimientos'])-1)
                        while num4 == num3 or num4 == num2 or num4 == num1:
                            num4 = random.randint(0,len(pokemon['movimientos'])-1)
                        pokemon['movimientos'] = [pokemon['movimientos'][num1],pokemon['movimientos'][num2],pokemon['movimientos'][num3],pokemon['movimientos'][num4]]
                        equipo.append(pokemon)
        equipos.append(equipo)
    return equipos

def aptitud(equipos:list):
    cant_batallas = 0
    cant_batallas_ganadas = 0
    equipos_aleatorios = poblacion_inicial(3,6)
    efectividad = dicc_efectividad('effectiveness_chart.csv')
    for equipo in equipos:
        for equipo_random in equipos_aleatorios:
            equipo_ganador = get_winner(equipo,equipo_random,efectividad)
            cant_batallas += 1
            if equipo_ganador == equipo:
                cant_batallas_ganadas += 1
        equipo.append(cant_batallas_ganadas)
    return equipos
               
    
'''
DUDAS REURISON
2- inicialización de combate
3- Como comparar equipos cuando hagamos los 400 combates

'''