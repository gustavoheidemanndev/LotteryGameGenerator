from fastapi import APIRouter, HTTPException
from fastapi import Response
from app.game_generator import generate_quantity_sequences, find_most_eleven_ocurrencies, generate_color_combinations, read_colors_past_games, generate_games_by_best_results, get_amount_occurence_numbers_last_draw, correct_numbers_winning_draws
from app.tests_game_generator import test_generator_games
from typing import List, Dict
import logging
from app.exceptions import ValidationError
from app.validators import validate_color_quantities
from app.game_generator_utils import initial_game_filter
from app.utils import generate_pdf


router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Game Generator API"}

@router.post("/generate-color-combinations")
async def get_color_combinations(color_quantities: List[int]) -> Dict:
    try:
        logger.info(f"Generating combinations for quantities: {color_quantities}")
        validate_color_quantities(color_quantities)
        games= generate_color_combinations(color_quantities)
        total_combinations = len(games)
        return {
            "total": total_combinations,
            "combinations": games
        }
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)

@router.post("/generate-color-combinations-pdf")
def gerar_pdf(color_quantities: List[int]) -> Response:
    try:
        logger.info(f"Generating combinations for quantities: {color_quantities}")
        validate_color_quantities(color_quantities)
        games= generate_color_combinations(color_quantities)
        buffer = generate_pdf(games)
        return Response(content=buffer.read(), media_type="application/pdf")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)

@router.get("/read-excel")
async def read_excel_file() -> list:
    try:
        return read_colors_past_games()
    except Exception as e:
        logger.error(f"Error reading Excel file: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error reading Excel file: {str(e)}")
    

@router.get("/get-quantity-sequences")
async def find_quantity_sequences() -> list:
    try:
        return generate_quantity_sequences()
    except Exception as e:
        logger.error(f"Error reading Excel file: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error reading Excel file: {str(e)}")


@router.post("/game-generator-1")
async def find_games_by_best_results():
    games = generate_games_by_best_results()
    buffer = generate_pdf(games)
    return Response(content=buffer.read(), media_type="application/pdf")


@router.get("/game-generator-test")
async def advanced_filter():
    filter = initial_game_filter()
    total_combinations = len(filter)   
    return {
        "total": total_combinations,
        "combinations": filter
    }

@router.get("/most_eleven_ocurrencies")
async def most_eleven_ocurrencies():
    return find_most_eleven_ocurrencies()

@router.get("/jogos-vencidos-quantidade-acertos-anterior")
async def numero_de_jogos_numeros_repetidos():
    return correct_numbers_winning_draws()

@router.get("/count-ocurrency-last-draw")
async def count_ocurrency_numbers_last_draw() -> list:
    return get_amount_occurence_numbers_last_draw()


@router.get("/test-game-generator-past-games")
async def get_test_game_generator_past_games() -> list:
    return test_generator_games()