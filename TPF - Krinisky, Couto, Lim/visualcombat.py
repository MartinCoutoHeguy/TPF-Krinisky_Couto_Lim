from visualteam import Team


#

def __faint_change__(team1: Team, team2: Team, effectiveness: dict[str, dict[str, float]]) -> None:
    """
    Changes the current pokemon of the team that has a fainted pokemon. The other team can also switch its pokemon after
    the fainted team.

    Parameters:
    team1 (Team): One of the teams.
    team2 (Team): The other team.
    effectiveness (dict[str, dict[str, float]]): A dictionary that contains the effectiveness of each type against
    another.
    """
    if team1.get_current_pokemon().current_hp == 0:
        deadpok = team1.get_current_pokemon()
        print(f"{team1.get_current_pokemon().name} ha sido debilitado.")
        fainted_team = team1
        other_team = team2
    else:
        deadpok = team2.get_current_pokemon()
        print(f"{team2.get_current_pokemon().name} ha sido debilitado.")
        fainted_team = team2
        other_team = team1
    action_1, target_1 = fainted_team.get_next_action(other_team, effectiveness)
    fainted_team.do_action(action_1, target_1, other_team, effectiveness)
    if any(pokemon.current_hp > 0 for pokemon in fainted_team.pokemons):
        print(f"{fainted_team.name} cambia a su {deadpok.name} debilitado por {fainted_team.get_current_pokemon().name}")
    action_2, target_2 = other_team.get_next_action(fainted_team, effectiveness)
    if action_2 == 'switch':
        prevpok = other_team.get_current_pokemon().name
        other_team.do_action(action_2, target_2, fainted_team, effectiveness)
        print(f"{other_team.name} cambia a su {prevpok} por {other_team.get_current_pokemon().name}")

def __fight__(team1: Team, team2: Team, effectiveness: dict[str, dict[str, float]]) -> Team:
    """
    Simulates a fight between two teams. The fight ends when all the pokemons of one of the teams have fainted.

    Parameters:
    team1 (Team): One of the teams.
    team2 (Team): The other team.
    effectiveness (dict[str, dict[str, float]]): A dictionary that contains the effectiveness of each type against
    another.

    Returns:
    Team: The team that won the fight.
    """
    turn = 0
    print(f"Pokemones de {team1.name}:")
    for pk in team1.pokemons:
        print(f'{pk.name}')
    print('\n')
    print(f"Pokemones de {team2.name}:")
    for pk in team2.pokemons:
        print(f'{pk.name}')
    print('\nQue comience el combate!\n')

    print(f"{team1.name} comienza con su {team1.get_current_pokemon().name}")
    print(f"{team2.name} comienza con su {team2.get_current_pokemon().name}")

    while any(pokemon.current_hp > 0 for pokemon in team1.pokemons) and any(pokemon.current_hp > 0 for pokemon in team2.pokemons):
        print(f"\nTurno {turn+1} \n")            
        action_1, target_1 = team1.get_next_action(team2, effectiveness)
        action_2, target_2 = team2.get_next_action(team1, effectiveness)

        # Switching always happens first
        if action_1 == 'switch':
            first = team1
            second = team2
            print(f"{first.name} cambia a {first.get_current_pokemon().name} por {first.pokemons[target_1].name}")
        elif action_2 == 'switch':
            first = team2
            second = team1
            action_1, target_1, action_2, target_2 = action_2, target_2, action_1, target_1
            print(f"{first.name} cambia a {first.get_current_pokemon().name} por {first.pokemons[target_1].name}")
        # If nobody is switching, the fastest pokemon goes firsts
        elif team1.get_current_pokemon().speed > team2.get_current_pokemon().speed:
            first = team1
            second = team2
        else:
            first = team2
            second = team1
            action_1, target_1, action_2, target_2 = action_2, target_2, action_1, target_1
    
        first.do_action(action_1, target_1, second, effectiveness)
        if action_1 =='attack':
            print(f"El {first.get_current_pokemon().name} de {first.name} ha utilizado {target_1.name} al {second.get_current_pokemon().name} de {second.name}")
        # If any of the pokemons fainted, the turn ends, and both have the chance to switch
        if team1.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
            __faint_change__(team1, team2, effectiveness)
        else:
            if action_2 == 'attack' and target_2 is None:
                action_2, target_2 = second.get_next_action(first, effectiveness)
            if action_2 =='attack':
                print(f"El {second.get_current_pokemon().name} de {second.name} ha utilizado {target_2.name} al {first.get_current_pokemon().name} de {first.name}")
            second.do_action(action_2, target_2, first, effectiveness)

            if team1.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
                __faint_change__(team1, team2, effectiveness)

        turn += 1
    if any(pokemon.current_hp > 0 for pokemon in team1.pokemons):
        print(f"\n{team2.name} no tiene mas Pokemones que puedan luchar, por lo tanto, {team1.name} es el ganador!")
        return team1
    else:
        print(f"\n{team1.name} no tiene mas Pokemones que puedan luchar, por lo tanto, {team2.name} es el ganador!")
        return team2
    

def get_winner(team1: Team, team2: Team, effectiveness: dict[str, dict[str, float]]) -> Team:
    """
    Simulates a fight between two teams. The fight ends when all the pokemons of one of the teams have fainted. The
    pokemons of the teams are restored to their initial state after the fight.

    Parameters:
    team1 (Team): One of the teams.
    team2 (Team): The other team.
    effectiveness (dict[str, dict[str, float]]): A dictionary that contains the effectiveness of each type against
    another.

    Returns:
    Team: The team that won the fight.
    """
    team1_starter_pokemon = team1.current_pokemon_index
    team2_starter_pokemon = team2.current_pokemon_index
    
    winner = __fight__(team1, team2, effectiveness)
    
    # restore HP to max
    for pokemon in team1.pokemons:
        pokemon.current_hp = pokemon.max_hp
    for pokemon in team2.pokemons:
        pokemon.current_hp = pokemon.max_hp
    
    # restore current pokemon to starter
    team1.current_pokemon_index = team1_starter_pokemon
    team2.current_pokemon_index = team2_starter_pokemon
    
    return winner
