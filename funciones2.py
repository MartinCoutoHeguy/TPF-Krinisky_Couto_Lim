import random
import matplotlib.pyplot as plt
import numpy as np
from team import Team
from pokemon import Pokemon
from move import Move
from combat import *
from pokemon import TYPES,TYPES_COLORS


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
                efective[lista[0]] = {'normal':float(lista[1]), 'fire':float(lista[2]), 'water':float(lista[3]),'electric':float(lista[4]),'grass':float(lista[5]),'ice':float(lista[6]),'fighting':float(lista[7]),'poison':float(lista[8]),'ground':float(lista[9]),'flying':float(lista[10]),'psychic':float(lista[11]),'bug':float(lista[12]),'rock':float(lista[13]),'ghost':float(lista[14]),'dragon':float(lista[15]),'dark':float(lista[16]),'steel':float(lista[17]),'fairy':float(lista[18])}
                puntero += 1
        return efective
    
def dic_movimientos(file: str):
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

    
def crear_equipos(cant_equipos,cant_pokemones):
    
    # print('crear equipos')
    equipos = []
    nombres = []
    pokemones_data = diccionarios_pokemones('pokemons.csv')
    # print('sali del dicctionario de pokemones')
    # print(f'Canti equipos : {cant_equipos}')
    # print(f'Canti pokemones : {cant_pokemones}')
    
    # Tomos todos los movimientos de todos los pokemones
    movimientos = dic_movimientos('moves.csv')
    # print('movimientos dic : ',type(movimientos))
    
    # Acá estoy tomando todos los nombres y datos de los pokemones
    for nombre,datos in pokemones_data.items():
        nombres.append(nombre)
        
    pokemon_ids = list(range(0, len(pokemones_data)-1))
    
    # Acá estoy generando todos los equipos
    while len(equipos) < cant_equipos:
        
        # inicializo un equipo vacio
        equipo = []
        
        # en lista equipo se tiene que llevar la clave entera del pokemon asi dentro de lista eq la modifica
        lista_eq = {} 
            
        #Para que no se repitan los pokemones en el equipo
        # Mientras el nombre del pokemon sea el mismo voy a generar otro pokemon.
        
        # genero una lista de numeros random de los pokemones -> Equipo
        lista_index = random.sample(pokemon_ids, k=6)
        # print('lista index : ', lista_index)
        
        # Aca estoy generando 1 equipo con 6 pokemones
        for index in lista_index:
        
            # Sacando los datos del diccionario de datos de pokemones
            NombrePokemon = nombres[index]
            pok_datos = pokemones_data[NombrePokemon]
            # Acá estoy agregando el pokemon al equipo 1
            lista_eq[NombrePokemon] = pok_datos

            for pk,info in lista_eq.items():
                # Si el pokemon no tiene movimentos (acá hay que verificar si es una lista vacia o una str vacia)
                if info['moves'] == '' or info['moves'] == []:
                    info['moves'] = []
                    
                # Ahora, si el pokemon tiene más movimientos, tomo solamente 4.
                elif len(info['moves']) > 4:
                    movimientos_4 = random.sample(info['moves'], k=4)
                    info['moves'] = movimientos_4
                # print("pk :", pk)
                # print('info moves : ', info['moves'])
                # print('lista equipos : ', lista_eq)
                # print('pokemones_data[pk] = ', pokemones_data[pk])
                # input()
                # print('movimientos : ', type(movimientos))
                # input()
                # print('movimientos : ', movimientos)
            
                pokemon = Pokemon
                moves_data = get_4_moves(pokemones_data[pk], movimientos)
                pok = Pokemon.from_dict(pk, info, moves_data)

                # Una vez generado el pokemon
                #pok = pokemon.from_dict(pk,pokemones_data[pk],moves) #MOVES TIENE QUE SER UNA LISTA DE class MOVE
                # print('pok.name = ', pok.pokedex_number)
                # print('pok.name = ', pok.type1)
                # print('pok.name = ', pok.type2)
                # print('pok.name = ', pok.attack)
                # print('pok.name = ', pok.defense)
                # print('pok.name = ', pok.sp_attack)
                # print('pok.name = ', pok.sp_defense)
                # print('pok.name = ', pok.speed)
                # print('pok.name = ', pok.height)
                # print('pok.name = ', pok.weight)
                #print('pok.name = ', pok.moves)
            equipo.append(pok)
        
        
        #print('Finalizado primer equipo')
        equipos.append(equipo)
        equiposfinal= []
        #print('len equipo: ', len(equipo))
    for i in range(len(equipos)):
        equiposfinal.append(Team(f"Equipo_{i+1}",equipos[i],0))
    #   equipo = Team(f"Equipo_{i+1}",equipos[i],0) #El i+1 es para que el primer team sea "Equipo_1" y no "Equipo_0"
        
    # print('fin de los equipos')
    # print('equipos : ', type(equiposfinal[0]))
    return equiposfinal

def get_4_moves(pokemon:dict,moves:dict):
    moves_pok = {}
    for movimiento,lista in moves.items():
        if movimiento in pokemon['moves']:
            moves_pok[movimiento] = lista
    return moves_pok

def aptitud(equipos:list):
    # print("Comienza")
    # print('tipo:',equipos[0].pokemons[0].type2)
    efectividad = dicc_efectividad('effectiveness_chart.csv')
    # print('efectividad : ', efectividad)
    tuple_aptitud = []
    lista_contadores=[]
    tupla = []
    print("Comienza aptitud!")
    # print("equipos: ",type(equipos))
    equipos_a_pelear = crear_equipos(200,6)
    for equipo in equipos:
        # print("Equipo:", type(equipo))
        contador = 0
        for equipo_pelea in equipos_a_pelear:
            ganador = get_winner(equipo,equipo_pelea,efectividad)
            if ganador == equipo:
                contador += 1
        lista_contadores.append(contador)
    print("Fin de combates")
    for i in range(0,len(equipos)):
        tupla = [equipos[i].name,lista_contadores[i]]
        tuple_aptitud.append(tupla)
    print("Termino la lista de tuplas")
    return equipos,tuple_aptitud


def contar_diversidad(epoca: int, equipos: list)->str:
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
    mejores_equipos=bubble_sort(aptitudes)
    mejores_equipos = mejores_equipos[:5]
    listafinal =[]
    # equipo1 = buscar_equipo_por_nombre(mejores_equipos[0],equipos)
    # equipo2 = buscar_equipo_por_nombre(mejores_equipos[1],equipos)
    # equipo3 = buscar_equipo_por_nombre(mejores_equipos[2],equipos)
    # equipo4 = buscar_equipo_por_nombre(mejores_equipos[3],equipos)
    # equipo5 = buscar_equipo_por_nombre(mejores_equipos[4],equipos)
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

def buscar_equipo_por_nombre(nombre: str,equipos:list[Team]):
    for equipo in equipos:
        if equipo.name == nombre:
            return equipo






def bubble_sort(lista): # para mejores equipos de mayor a peor
    n = len(lista)

    for i in range(n):

        for j in range(0, n-i-1):

            if lista[j][1] < lista[j+1][1]:

                lista[j], lista[j+1] = lista[j+1], lista[j]
    
    return lista


def main():
    # creo los dos archivos al principio asi no hay que eliminarlos cada vez que se ejecuta el codigo
    with open("epochs1.csv", "w") as epocas:
        epocas.close()
    with open("best_teams1.csv", "w") as besteams:
        besteams.close()
    teams = crear_equipos(50,6)
    epoca = 0
    for i in range(50):
        teams, epoca = algoritmo_genetico(teams,epoca)
        epoca = i + 1

def algoritmo_genetico(equipos,epoch):
    print("Preaptitud")
    equipos, aptitudes = aptitud(equipos)
    print("Postaptitud")
    # ahora escribo en los archivos los datos de esta epoca
    with open("epochs1.csv",'a') as epocas:
        epoch,diversidad,dicdiversidad = contar_diversidad(epoch,equipos)
        epocas.write(f"{epoch},{diversidad}")
        for nombre,cantidad in dicdiversidad.items():
            epocas.write(f",{nombre},{cantidad}")
        epocas.write('\n')
    with open("best_teams1.csv",'a') as besteams:
        datosequipos = contar_mejores_equipos(epoch,equipos,aptitudes)
        besteams.write('epoch,aptitude,team_name,starter,pokemon_1,pokemon_2,pokemon_3,pokemon_4,pokemon_5,pokemon_6\n')
        for equipo in datosequipos:
            besteams.write(f"{equipo[0]},{equipo[1]},{equipo[2]},{equipo[3]},{equipo[4]},{equipo[5]},{equipo[6]},{equipo[7]},{equipo[8]},{equipo[9]}\n")
    
    
    for equipo in aptitudes:
        contador = 0
        if equipo[1] >=75:
            contador +=1
            if equipo[1] >= 125:
                contador +=1
                if equipo[1] >= 175:
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
    # print(contador1)
    # print(contador2)
    # print(contador3)
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
    print (aptitudes)
    #Ahora que tengo una lista de listas[equipo,cantidad de equipos que tienen que cambiar
    cambios3= contador3//2
    cambios2= contador2//2
    cambios1= contador1//2
    print('cambios(1,2,3):',cambios1,cambios2,cambios3)
    print('contador(1,2,3):',contador1,contador2,contador3)

    
    #Cambio de pokemones
    print("pokemones:",equipos[0].pokemons)
    #Los peores equipos se cambian
    for equipo,apt in aptitudes:
        if apt == 0:
            newteam = crear_equipos(1,6)
            newteam = newteam[0] #Porque la funcion crear equipos devuelve una lista de equipos
            equipoparareemplazar = buscar_equipo_por_nombre(equipo,equipos) #busco el objeto a partir de su nombre
            index= equipos.index(equipoparareemplazar) # busco el indice del equipo en la lista de equipos
            newteam.name = equipo # le pongo el mismo nombre para evitar problemas
            equipos[index] = newteam   
    
    
    
    if cambios3>=1:
        
        for i in range(cambios3):
            print("cambios 3 =",cambios3)
            print(aptitudes)
            nombreacambiar =[] #nombreacambiar es el nombre de los equipos a cambiar
            for equipo,contador in aptitudes:
                print(equipo,':',contador)
                if len(nombreacambiar) == 2: break
                elif contador == 3:
                    nombreacambiar.append(equipo)
                    contador = 0
            print(nombreacambiar)
            equipoacambiar=[]
            for nombre in nombreacambiar:
                equipoacambiar.append(buscar_equipo_por_nombre(nombre,equipos))
            #elijo 3 numeros para cada equipo
            opciones=[0,1,2,3,4,5]
            num1 = random.sample(opciones,k=3)
            num2 = random.sample(opciones,k=3)

            indice1=equipos.index(equipoacambiar[0])
            indice2=equipos.index(equipoacambiar[1])
            print(num1)
            print(num2)
            print(equipoacambiar[0].pokemons[num1[0]].name)
            print(equipoacambiar[0].pokemons[num1[1]].name)
            print(equipoacambiar[0].pokemons[num1[2]].name)


            print(equipoacambiar[1].pokemons[num1[0]].name)
            print(equipoacambiar[1].pokemons[num1[1]].name)
            print(equipoacambiar[1].pokemons[num1[2]].name)
            pokemon1a= equipoacambiar[0].pokemons[num1[0]]
            pokemon1b= equipoacambiar[0].pokemons[num1[1]]
            pokemon1c= equipoacambiar[0].pokemons[num1[2]]
            pokemon2a= equipoacambiar[1].pokemons[num2[0]]
            pokemon2b= equipoacambiar[1].pokemons[num1[1]]
            pokemon2c= equipoacambiar[1].pokemons[num1[2]]
            print("Antes del while")
            # print(pokemon1a,pokemon1b,pokemon1c,pokemon2a,pokemon2b,pokemon2c)
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

            for pk in equipoacambiar[0].pokemons:
                print(pk.name)
            print('\n')
            for pk in equipoacambiar[1].pokemons:
                print(pk.name)
            print('\n')
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



            for pk in equipoacambiar[0].pokemons:
                print(pk.name)
            print('\n')
            for pk in equipoacambiar[1].pokemons:
                print(pk.name)
            # print(pokemon1a,pokemon1b,pokemon1c,pokemon2a,pokemon2b,pokemon2c)
    
    
    if cambios2>=1:
        for i in range(cambios2):
            print("cambios 2 =",cambios2)
            print(aptitudes)
            nombreacambiar =[] #nombreacambiar es el nombre de los equipos a cambiar
            for equipo,contador in aptitudes:
                if len(nombreacambiar) == 2: break
                elif contador == 2:
                    nombreacambiar.append(equipo)
                    contador = 0
            print("nombre a cambiar: ",nombreacambiar)
            equipoacambiar=[]
            for nombre in nombreacambiar:
                equipoacambiar.append(buscar_equipo_por_nombre(nombre,equipos))
            #elijo 2 numeros para cada equipo
            opciones=[0,1,2,3,4,5]
            num1 = random.sample(opciones,k=2)
            num2 = random.sample(opciones,k=2)
            indice1=equipos.index(equipoacambiar[0])
            indice2=equipos.index(equipoacambiar[1])
            print(num1)
            print(num2)
            print(equipoacambiar[0].pokemons[num1[0]].name)
            print(equipoacambiar[0].pokemons[num1[1]].name)



            print(equipoacambiar[1].pokemons[num2[0]].name)
            print(equipoacambiar[1].pokemons[num2[1]].name)

            pokemon1a= equipoacambiar[0].pokemons[num1[0]]
            pokemon1b= equipoacambiar[0].pokemons[num1[1]]
            pokemon2a= equipoacambiar[1].pokemons[num2[0]]
            pokemon2b= equipoacambiar[1].pokemons[num1[1]]
            print("Antes del while")
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

            print("cambio de 2 pokemones: equipo previo: \n")
            for pk in equipoacambiar[0].pokemons:
                print(pk.name)
            print('\n')
            for pk in equipoacambiar[1].pokemons:
                print(pk.name)
            print('\n nuevos equipo:')
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




            for pk in equipoacambiar[0].pokemons:
                print(pk.name)
            print('\n')
            for pk in equipoacambiar[1].pokemons:
                print(pk.name)
            # print(pokemon1a,pokemon1b,pokemon1c,pokemon2a,pokemon2b,pokemon2c)
    if cambios1>=1:
        for i in range(cambios1):
            print("cambios 1 =",cambios1)
            print(aptitudes)
            nombreacambiar =[] #nombreacambiar es el nombre de los equipos a cambiar
            for equipo,contador in aptitudes:
                if len(nombreacambiar) == 2: break
                elif contador == 1:
                    nombreacambiar.append(equipo)
                    contador = 0
            print("nombre a cambiar: ",nombreacambiar)
            equipoacambiar=[]
            for nombre in nombreacambiar:
                equipoacambiar.append(buscar_equipo_por_nombre(nombre,equipos))
            #elijo 2 numeros para cada equipo
            opciones=[0,1,2,3,4,5]
            num1 = random.sample(opciones,k=1)
            num2 = random.sample(opciones,k=1)
            indice1=equipos.index(equipoacambiar[0])
            indice2=equipos.index(equipoacambiar[1])
            print(num1)
            print(num2)
            print(equipoacambiar[0].pokemons[num1[0]].name)



            print(equipoacambiar[1].pokemons[num2[0]].name)

            pokemon1a= equipoacambiar[0].pokemons[num1[0]]
            pokemon2a= equipoacambiar[1].pokemons[num2[0]]
            print("Antes del while")
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
    
            print('defino poks')

            print("cambio de 2 pokemones: equipo previo: \n")
            for pk in equipoacambiar[0].pokemons:
                print(pk.name)
            print('\n')
            for pk in equipoacambiar[1].pokemons:
                print(pk.name)
            print('\n nuevos equipo:')
            #cambio en el primer equipo
            if intentos >3: 
                    continue
            equipoacambiar[0].pokemons[num1[0]] = pokemon2a
            #cambio en el segundo equipo
            equipoacambiar[1].pokemons[num2[0]] = pokemon1a

            equipos[indice1] = equipoacambiar[0]
            equipos[indice2] = equipoacambiar[1]



            for pk in equipoacambiar[0].pokemons:
                print(pk.name)
            print('\n')
            for pk in equipoacambiar[1].pokemons:
                print(pk.name)
    
    print("Termino el algoritmo")
    
    return equipos,epoch



def notinteam(equipo,listapokemon):
    for pk in equipo.pokemons:
        for nombre in listapokemon:
            if pk.name == nombre.name:
                return False
    else: return True


def obtenervalor(clave: str):
    return clave[1]

    
def graficos(archivo1,archivo2):
    
    
    # 5. Distribución de Tipos de Pokémon en los Equipos por Época
    # 7. Mejor equipo encontrado


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
    # 1. Diversidad de Pokémon en los Equipos por Época 

    # print("epocas:" ,epocas,'\n')
    # print('diversidad: ',diversidad,'\n')

    # Crear el gráfico de dispersión
    
    plt.plot(epocas, diversidad)  # Graficar épocas vs diversidad
    plt.xlabel('Épocas')  # Etiqueta del eje x
    plt.ylabel('Diversidad')  # Etiqueta del eje y
    plt.title('Diversidad de Pokemones en los equipos por época')  # Título del gráfico
    plt.grid(False)  # Activar cuadrícula
    plt.tight_layout()  # Ajustar el diseño
    plt.savefig('Epocas')
    plt.show()  # Mostrar el gráfico   
    plt.close()
    ######

    pokemones = []
    contadores = []
    cuantosva = 0 # Solo pone los 25 pokemones mas aparecidos
    for pok,cont in pok_ultima_epoch.items():
        if cuantosva == 25: break
        cuantosva +=1
        pokemones.append(pok)
        contadores.append(cont)
    # 3. Distribución de Pokémon en los Equipos en la última Época

    # Crear el gráfico de barras horizontal
    
    plt.barh(pokemones,contadores)
    plt.xlabel('Count')
    plt.ylabel('Pokemones')
    plt.title('Pokemon count in best teams')
    plt.savefig('Contadores_pok')
    plt.show()
    plt.close()

    
    # 2. Evolución de la Aptitud a lo largo de las Épocas
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
    print(epocas)
    print(aptitud)
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
    print(variedad_tipo)
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

    pokemon_stats = {}
    with open(archivo2) as besteams:
        for linea in besteams:
            linea=linea.strip()
            linea=linea.split(',')
        bestteam=linea
    contador = 0
    for item in  bestteam:
        contador+=1
        if contador > 4:
            pokemon_stats[item]= []
    for pk in pokemon_stats.keys():
        pokemon_stats[pk]=pokemones_data[pk]['hp'],pokemones_data[pk]['attack'],pokemones_data[pk]['defense'],pokemones_data[pk]['sp_attack'],pokemones_data[pk]['sp_defense'],pokemones_data[pk]['speed']

    
            


    # 6. Estadísticas del mejor equipo encontrado
    radar_chart(pokemon_stats, ['hp','attack','defense','sp_attack','sp_defense','speed'])
    plt.savefig("BestStats")
    plt.show()
    plt.close()

 


def radar_chart(pokemon_stats, labels):
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
        ax.plot(angles, stats, linewidth=1, linestyle='solid', label=pokemon)
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




