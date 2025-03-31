from app.game_generator_utils import extract_array_excel, count_lists_with_exact_sequence_length, get_numbers_by_color, all_possible_combinations, initial_game_filter, keep_lists_with_exacly_sequence, process_number_lists, special_selection, get_last_set, gerar_combinacoes_complemento, list_with_gaps
from itertools import combinations
from typing import List
import logging

logger = logging.getLogger(__name__)

def generate_color_combinations(color_quantities: List[int]): 
    color_numbers = []
    for color_index in range(10):
        if color_quantities[color_index] > 0:
            numbers = get_numbers_by_color(color_index)
            color_numbers.extend(list(combinations(numbers, color_quantities[color_index])))

    result = []
    from itertools import product
    
    color_combinations = []
    for qty in color_quantities:
        if qty > 0:
            numbers = get_numbers_by_color(len(color_combinations))
            color_combinations.append(list(combinations(numbers, qty)))
        else:
            color_combinations.append([()])
    
    for combination in product(*color_combinations):
        numbers = []
        for group in combination:
            numbers.extend(group)
        if len(numbers) == 15 and len(set(numbers)) == 15:
            result.append(sorted(numbers))

    total_combinations = len(result)
    logger.info(f"Generated {total_combinations} valid combinations")
    
    return result

def generate_quantity_sequences() -> list:
    df = extract_array_excel()
    array_set_numbers = []

    for index, row in df.iloc[6:].iterrows():
        array_set_numbers.append(row.iloc[2:].dropna().astype(int).tolist())

    resultados = []
    for i in range(1, 16):
        resultado = count_lists_with_exact_sequence_length(array_set_numbers, i)
        resultados.append(resultado)
    return resultados
        
def extract_colors_from_excel():
    df = extract_array_excel()
    color_mapping = {
        "vermelho": {1, 11, 21},
        "amarelo": {2, 12, 22},
        "verde": {3, 13, 23},
        "marrom": {4, 14, 24},
        "azul": {5, 15, 25},
        "rosa": {6, 16},
        "preto": {7, 17},
        "cinza": {8, 18},
        "laranja": {9, 19},
        "branco": {10, 20}
    }
    color_with_qty = {}
    array_colors = []
    for index, row in df.iloc[6:].iterrows():
        numbers = row.iloc[2:].dropna().astype(int).tolist()
        for label, values in color_mapping.items():
            count = sum(1 for n in numbers if n in values)
            color_with_qty[label] = count
        key_str = f"{row.iloc[0]}-{row.iloc[1]}"
        array_colors.append({key_str: color_with_qty.copy()})
    return array_colors

def find_most_eleven_ocurrencies():
    df = extract_array_excel()
    dados = [
    row.iloc[2:].dropna().astype(int).tolist() 
    for index, row in df.iloc[6:].iterrows()]
    titulos = [
    row.iloc[0]
    for index, row in df.iloc[6:].iterrows()]
    concursos = []
    bigger = 0
    title_game_chosen = 0
    for i in range(0, len(dados)):
        conjuntos_acertadas_anteriormente = {}
        for j in  range(i+1, len(dados)):
            repetidos = len(set(dados[i]).intersection(dados[j]))
            if repetidos > 10:
                conjuntos_acertadas_anteriormente[repetidos] = conjuntos_acertadas_anteriormente.get(repetidos, 0) + 1
        if conjuntos_acertadas_anteriormente.get(14, 0) > bigger:
            bigger = conjuntos_acertadas_anteriormente.get(14, 0)
            title_game_chosen = titulos[i]
    return {
        "concurso_vencedor": title_game_chosen,
        "record": bigger
    }


def read_colors_past_games():
        df = extract_array_excel()
        
        color_mapping = {
            "vermelho": {1, 11, 21},
            "amarelo": {2, 12, 22},
            "verde": {3, 13, 23},
            "marrom": {4, 14, 24},
            "azul": {5, 15, 25},
            "rosa": {6, 16},
            "preto": {7, 17},
            "cinza": {8, 18},
            "laranja": {9, 19},
            "branco": {10, 20}
        }
    
        color_with_qty = {}

        colors_past_games = []

        for index, row in df.iloc[6:].iterrows():
            numbers = row.iloc[2:].dropna().astype(int).tolist()
            for label, values in color_mapping.items():
                count = sum(1 for n in numbers if n in values)
                color_with_qty[label] = count
            key_str = f"{row.iloc[0]}-{row.iloc[1]}"
            colors_past_games.append({key_str: color_with_qty.copy()})

        return colors_past_games


def generate_games_by_best_results():
    list = initial_game_filter()
    last_combination = get_last_set()
    combinations_last_prize = gerar_combinacoes_complemento(last_combination, 10)
    total_reg = len(combinations_last_prize)
    listFinal = []
    index = 0
    for item in combinations_last_prize:
        filtered_list = [numbers for numbers in list 
                         if all(n in numbers for n in item[:10]) 
                         and all(n not in numbers for n in item[10:])]
        if filtered_list:
            listFinal.extend(filtered_list)
        index += 1
        print(f"{total_reg}-{index}")
    return list_with_gaps(5, listFinal)


def get_amount_occurence_numbers_last_draw():
    df = extract_array_excel()
    list = [
    row.iloc[2:].dropna().astype(int).tolist() 
    for index, row in df.iloc[6:].iterrows()]
    listas_invertidas = list[::-1]
    contagens = [0] * 16
    for i in range(1, len(listas_invertidas)):
        lista_atual = listas_invertidas[i]
        lista_anterior = listas_invertidas[i - 1]
        repetidos = len(set(lista_atual).intersection(lista_anterior))
        if repetidos < 16:
            contagens[repetidos] += 1
    return contagens

def correct_numbers_winning_draws():
    df = extract_array_excel()
    dados = [
    row.iloc[2:].dropna().astype(int).tolist() 
    for index, row in df.iloc[6:].iterrows()]
    titulos = [
    row.iloc[0]
    for index, row in df.iloc[6:].iterrows()]
    concursos = []
    for i in range(0, len(dados)):
        conjuntos_acertadas_anteriormente = {}
        for j in  range(i+1, len(dados)):
            repetidos = len(set(dados[i]).intersection(dados[j]))
            if repetidos > 10:
                conjuntos_acertadas_anteriormente[repetidos] = conjuntos_acertadas_anteriormente.get(repetidos, 0) + 1
        concursos.append({titulos[i]: conjuntos_acertadas_anteriormente.copy()})
    return concursos