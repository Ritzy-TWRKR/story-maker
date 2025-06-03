from fastapi import FastAPI, Body, Query
from pydantic import BaseModel, field_validator
import html
from fastapi.middleware.cors import CORSMiddleware
from story_writer import StoryWriter
from validators import sanitize_string

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:3000"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StoryRequest(BaseModel):
    plot: str
    imageNeeded: bool
    genre: str
    experimentBoundary: float = 0
    totalStoryCharacters: int = 1
    totalParagraphs: int = 1
    totalWords: int = 100

    @field_validator('plot', 'genre')
    @classmethod
    def sanitize_strings(cls, v):
        return sanitize_string(v)

    @field_validator('totalStoryCharacters')
    @classmethod
    def validate_total_story_characters(cls, v):
        if not (1 <= v <= 10):
            raise ValueError('totalStoryCharacters must be between 1 and 10')
        return v

    @field_validator('totalParagraphs')
    @classmethod
    def validate_total_paragraphs(cls, v):
        if not (1 <= v <= 5):
            raise ValueError('totalParagraphs must be between 1 and 5')
        return v

    @field_validator('totalWords')
    @classmethod
    def validate_total_words(cls, v):
        if not (100 <= v <= 400):
            raise ValueError('totalWords must be between 100 and 400')
        return v

@app.post("/story")
def create_story(request: StoryRequest = Body(...)):
    result = StoryWriter.new_story(
        plot=request.plot,
        image_needed=request.imageNeeded,
        genre=request.genre,
        temperature=request.experimentBoundary,
        totalStoryCharacters=request.totalStoryCharacters,
        totalParagraphs=request.totalParagraphs,
        totalWords=request.totalWords
    )
    return result

class DevelopStoryRequest(StoryRequest):
    summary: str

@app.post("/develop-story")
def develop_story(request: DevelopStoryRequest = Body(...)):
    result = StoryWriter.develop_story(
        summary=request.summary,
        genre=request.genre,
        image_needed=request.imageNeeded,
        developmentPlot=request.plot,
        temperature=request.experimentBoundary,
        totalStoryCharacters=request.totalStoryCharacters,
        totalParagraphs=request.totalParagraphs,
        totalWords=request.totalWords
    )
    return result
