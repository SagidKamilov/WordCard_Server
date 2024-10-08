from typing import List

from fastapi import APIRouter, HTTPException, status

from src.controller.dependencies import word_container
from src.dto.word import WordCreate, WordUpdate, WordResponse
from src.error.word.word_errors import WordNotExists
from src.error.base_error import internal_server_message


router = APIRouter(prefix="", tags=["Действия над словами"])


@router.post(path="/word/{category_id}", status_code=status.HTTP_201_CREATED, response_model=WordResponse)
async def create_word(category_id: int, word_create: WordCreate):
    try:
        category = await word_container().create_word(category_id=category_id, word_create=word_create)

        return category
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=internal_server_message)


@router.get(path="/word/{word_id}", status_code=status.HTTP_200_OK, response_model=WordResponse)
async def get_word(word_id: int):
    try:
        word = await word_container().get_word(word_id=word_id)

        return word
    except WordNotExists as wrong:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=wrong.message)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=internal_server_message)


@router.get(path="/{category_id}/words", status_code=status.HTTP_200_OK, response_model=List[WordResponse])
async def get_words(category_id: int):
    try:
        words = await word_container().get_words(category_id=category_id)

        return words
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=internal_server_message)


@router.put(path="/word/{word_id}", status_code=status.HTTP_200_OK, response_model=WordResponse)
async def update_word(word_id: int, word_update: WordUpdate):
    try:
        word = await word_container().update_word(word_id=word_id, word_update=word_update)

        return word
    except WordNotExists as wrong:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=wrong.message)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=internal_server_message)


@router.delete(path="/word/{word_id}", status_code=status.HTTP_200_OK, response_model=int)
async def delete_word(word_id: int):
    try:
        result: int = await word_container().delete_word(word_id=word_id)

        return result
    except WordNotExists as wrong:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=wrong.message)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=internal_server_message)
