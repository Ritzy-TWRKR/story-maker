from fastapi import FastAPI, Body
from schemas import DevelopStoryRequest ,StoryRequest
from fastapi.middleware.cors import CORSMiddleware
from story_writer import StoryWriter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:3000"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/story")
def create_story(request: StoryRequest = Body(...)):
    result = StoryWriter.new_story(request)
    return result


@app.post("/develop-story")
def develop_story(request: DevelopStoryRequest = Body(...)):
    result = StoryWriter.develop_story(request)
    return result
