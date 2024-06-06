from pydantic import BaseModel


class WordCreate(BaseModel):
    main_language: str
    second_language: str
    transcription: str


class WordUpdate(BaseModel):
    main_language: str = None
    second_language: str = None
    transcription: str = None


class WordResponse(BaseModel):
    id: int
    main_language: str
    second_language: str
    transcription: str
