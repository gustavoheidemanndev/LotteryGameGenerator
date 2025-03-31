import pandas as pd
import logging
from typing import List
from itertools import combinations
from app.config import Directories

logger = logging.getLogger(__name__)

def count_lists_with_exact_sequence_length(lists, sequence_length):
    def has_exact_sequence(lst, length):
        count = 1
        max_sequence_loop = 0
        found = False
        for i in range(1, len(lst)):
            if lst[i] == lst[i-1] + 1:
                count += 1
                if count > length:
                    return False
            else:
                if count > max_sequence_loop:
                    max_sequence_loop = count
                count = 1
        if count > max_sequence_loop:
            max_sequence_loop = count
        if max_sequence_loop == length: 
            found = True
        return found
    count = sum(1 for lst in lists if has_exact_sequence(lst, sequence_length))
    return f"{sequence_length}-{count}"

def extract_array_excel():
    excel_files = list(Directories.DATA.value.glob("loto_facil_asloterias_ate_concurso.xlsx"))
    if not excel_files:
        raise FileNotFoundError("File not found")
    excel_file = excel_files[0]
    logger.info(f"Reading Excel file: {excel_file}")
    df = pd.read_excel(excel_file)
    return df

def get_numbers_by_color(color_index: int) -> List[int]:
    logger.debug(f"Getting numbers for color index {color_index}")
    numbers = [n for n in range(1, 26) if n % 10 == color_index + 1 or (n % 10 == 0 and color_index == 9)]
    logger.debug(f"Numbers for color {color_index}: {numbers}")
    return numbers

def remove_lists_with_long_sequences(lists):
    def has_long_sequence(lst):
        count = 1
        for i in range(1, len(lst)):
            if lst[i] == lst[i-1] + 1:
                count += 1
                if count > 4:
                    return True
            else:
                count = 1
        return False
    filtered_lists = [lst for lst in lists if not has_long_sequence(lst)]
    return filtered_lists

def keep_lists_with_exacly_sequence(lists):
    def has_long_sequence(lst):
        count = 1
        max_sequence_loop = 0
        for i in range(1, len(lst)):
            if lst[i] == lst[i-1] + 1:
                count += 1
                if count > 4:
                    return True
            else:
                if count > max_sequence_loop:
                    max_sequence_loop = count
                count = 1
        if count > max_sequence_loop:
            max_sequence_loop = count        
        return max_sequence_loop != 4
    filtered_lists = [lst for lst in lists if not has_long_sequence(lst)]
    return filtered_lists

def get_last_set():
    df = extract_array_excel()
    return df.iloc[6][2:]

def gerar_combinacoes_complemento(array, repeated_numbers):
    resultado:list[list[int]] = []
    for combo in combinations(array, repeated_numbers):
        combo_set = set(combo)
        complementos = [num for num in array if num not in combo_set]
        lista_completa = list(combo) + complementos
        resultado.append(lista_completa)
    return resultado

def list_with_gaps(gaps, list):
    filtered_list = []
    filtered_list.append(list[0])
    for item in list:
        different = set(item) - set(filtered_list[-1])
        if len(different) == gaps:
            filtered_list.append(item)
    
    return filtered_list

def all_possible_combinations() :
    return [list(combinacao) for combinacao in combinations(range(1, 26), 15)]

def count_odd_even(numbers):
    odd_count = sum(1 for num in numbers if num % 2 != 0)
    even_count = len(numbers) - odd_count
    return odd_count, even_count

def should_keep_list(numbers):
    if len(numbers) != 15:
        return False
        
    if not all(1 <= num <= 25 for num in numbers):
        return False
        
    odd_count, even_count = count_odd_even(numbers)
    
    invalid_combinations = [
        (8, 7),
        (7, 8)
    ]
    
    return (odd_count, even_count) in invalid_combinations

def process_number_lists(list_of_lists):
    return [numbers for numbers in list_of_lists if should_keep_list(numbers)]

def special_selection(array_filter):
    df = extract_array_excel()
    dados = [
    row.iloc[2:].dropna().astype(int).tolist() 
    for index, row in df.iloc[6:].iterrows()]
    filtragem_resultado = []

    index = 0
    total_reg = len(array_filter)
    for game_generators in array_filter:
        conjuntos_acertadas_anteriormente = {}
        for resultados in dados:
            repetidos = len(set(game_generators).intersection(resultados))
            if repetidos > 10:
                conjuntos_acertadas_anteriormente[repetidos] = conjuntos_acertadas_anteriormente.get(repetidos, 0) + 1
        if conjuntos_acertadas_anteriormente.get(11, 0) > 300 and conjuntos_acertadas_anteriormente.get(13, 0) > 0:
            filtragem_resultado.append(game_generators)
        index += 1    
        print(f"{total_reg}-{index}")
    return filtragem_resultado

def initial_game_filter():
    filter = all_possible_combinations()
    filter = keep_lists_with_exacly_sequence(filter)
    filter = process_number_lists(filter)
    print(len(filter))
    filter = special_selection(filter)
    return filter