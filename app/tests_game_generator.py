from app.game_generator_utils import extract_array_excel, gerar_combinacoes_complemento_com_restante_combinacoes, get_numbers_by_color, all_possible_combinations, initial_game_filter, remove_lists_with_long_sequences, process_number_lists, gerar_combinacoes_complemento, list_with_gaps


def test_generator_games():
    print("inicio...")

    df = extract_array_excel()
    list = [
    row.iloc[2:].dropna().astype(int).tolist() 
    for index, row in df.iloc[6:].iterrows()]
    array_past_games = list[::-1]
    titles = [
    row.iloc[0]
    for index, row in df.iloc[6:].iterrows()]
    titles_sort = titles[::-1]
    list_return = []
    for i in range(2000, len(array_past_games)):
        last_combination = array_past_games[i-1]
        filter = gerar_combinacoes_complemento_com_restante_combinacoes(last_combination, 10)
        print(f"first!-{len(filter)}")
        filter = process_number_lists(filter)
        filter = remove_lists_with_long_sequences(filter)
        print(f"{len(filter)} -- 1")
        filter = special_selection(filter, array_past_games[:i])
        print(f"{len(filter)} -- 2")
        list_win = [numbers for numbers in filter 
                            if all(n in numbers for n in array_past_games[i])]
        print(f"{titles_sort[i]}-{len(list_win)}- tamanho list final:{len(filter)}")
        if list_win:
            list_return.append(list_win)
        print(f"Vitórias até o momento:{len(list_return)}")
    return list_return



def special_selection(array_filter, array_past_games):
    filtragem_resultado = []

    index = 0
    total_reg = len(array_filter)
    total_array_past = len(array_past_games)
    eith_percent = int(total_array_past*0.07)
    five_percent = int(total_array_past*0.001)
    print(f"{int(five_percent)} -- 1")
    print(f"{int(eith_percent)} -- 2")
    for game_generators in array_filter:
        conjuntos_acertadas_anteriormente = {}
        for resultados in array_past_games:
            repetidos = len(set(game_generators).intersection(resultados))
            if repetidos > 10:
                conjuntos_acertadas_anteriormente[repetidos] = conjuntos_acertadas_anteriormente.get(repetidos, 0) + 1
        if conjuntos_acertadas_anteriormente.get(11, 0) > int(eith_percent) and conjuntos_acertadas_anteriormente.get(13, 0) > int(five_percent):
            filtragem_resultado.append(game_generators)
        index += 1    
        
    print(f"{total_reg}-{len(array_past_games)}")
    return filtragem_resultado



