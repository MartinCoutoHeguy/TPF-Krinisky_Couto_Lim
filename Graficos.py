def graficos(archivo1,archivo2):
    
    #No llegue a:
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




