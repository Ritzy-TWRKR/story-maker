# Story Maker FastAPI Project

This is a FastAPI project for generating and developing stories using LLMs.
Note: Enter API_KEY in the story_maker.py 

## Getting Started

1. **Create and activate the virtual environment** (already done):
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies** (already done):
   ```sh
   pip install fastapi uvicorn
   ```

3. **Run the FastAPI server:**
   ```sh
   uvicorn main:app --reload
   ```
4. Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000) to see the API.


## API Endpoints
- `POST /story` — Receives a JSON body with:
  - `plot` (string): The story plot.
  - `imageNeeded` (boolean): Whether to generate an image.
  - `genre` (string): The genre of the story.
  - `experimentBoundary` (float, optional): LLM temperature (default 0).
  - `totalStoryCharacters` (int, default 1, min 1, max 10): Number of main characters.
  - `totalParagraphs` (int, default 1, min 1, max 5): Number of paragraphs.
  - `totalWords` (int, default 100, min 100, max 400): Target word count.

- `POST /develop-story` — Receives a JSON body with:
  - `plot` (string): The new plot or development direction for the story.
  - `imageNeeded` (boolean): Whether to generate an image for the developed story.
  - `genre` (string): The genre of the story.
  - `experimentBoundary` (float, optional): LLM temperature (default 0).
  - `totalStoryCharacters` (int, default 1, min 1, max 10): Number of main characters in the developed story.
  - `totalParagraphs` (int, default 1, min 1, max 5): Number of paragraphs in the developed story.
  - `totalWords` (int, default 100, min 100, max 400): Target word count for the developed story.
  - `summary` (string): The summary to develop into a full story.

  **Example request body:**
  ```json
  {
    "plot": "A hero faces a new challenge.",
    "imageNeeded": true,
    "genre": "Drama",
    "experimentBoundary": 0.5,
    "totalStoryCharacters": 2,
    "totalParagraphs": 3,
    "totalWords": 250,
    "summary": "A hero saved the world but now must find peace."
  }
  ```

## Development
- Edit `main.py` and `story_writer.py` to add or modify endpoints and logic.
- API docs available at `/docs` when the server is running.
- Run tests with `pytest test_main.py`.
