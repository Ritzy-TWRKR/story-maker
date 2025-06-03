from pydantic import BaseModel, field_validator, model_validator, ValidationError
from validators import sanitize_string

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

    @field_validator('imageNeeded')
    @classmethod
    def validate_image_needed(cls, v):
        if not isinstance(v, bool):
            raise ValueError("Bad input: imageNeeded must be a boolean.")
        return v

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

    @model_validator(mode="after")
    def adjust_experiment_boundary(self):
        if self.experimentBoundary > 0:
            object.__setattr__(self, "experimentBoundary", self.experimentBoundary / 10)
        return self
    

class DevelopStoryRequest(StoryRequest):
    summary: str


class ModelStatistics(BaseModel):
    tokensUsedCount: int | None = None
    timeTakenToProcessPrompt: float | None = None


class StoryResponse(BaseModel):
    story: str | None = None
    storySummary: str | None = None
    image: str | None = None
    error: str | None = None
    modelStatistics: ModelStatistics | None = None

