import openai
import logging
import time
from pydantic import BaseModel,field_validator
import httpx

API_KEY = "Sjm8mDzDUj5X2qLSV2jZPDMUUpKfZxbr"
MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"
BASE_URL = "https://api.deepinfra.com/v1/openai"

openai_client = openai.OpenAI(api_key=API_KEY, 
                              base_url=BASE_URL, 
                              http_client=httpx.Client(timeout=60))


class ModelStatistics(BaseModel):
    tokensUsedCount: int | None = None
    timeTakenToProcessPrompt: float | None = None


class StoryResponse(BaseModel):
    story: str | None = None
    storySummary: str | None = None
    image: str | None = None
    error: str | None = None
    modelStatistics: ModelStatistics | None = None


class StoryWriter:

    @staticmethod
    def generate_story(plot: str, genre: str, temperature: float = 0, totalStoryCharacters: int = 1, totalParagraphs: int = 1, totalWords: int = 100):
        prompt = (
            f"Write a {genre} story based on the following plot: {plot}. "
            f"Include {totalStoryCharacters} main character(s), "
            f"{totalParagraphs} paragraph(s), and aim for about {totalWords} words. "
        )
        print(f"Prompt for a new story : {prompt}")
       
        response = openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
    
        story = response.choices[0].message.content.strip()
    
        tokens_used = None
        if hasattr(response, 'usage') and response.usage and hasattr(response.usage, 'total_tokens'):
            tokens_used = response.usage.total_tokens
        return story, tokens_used


    @staticmethod
    def develop_story_from_summary(summary: str, genre: str, developmentPlot: str, temperature: float = 0, totalStoryCharacters: int = 1, totalParagraphs: int = 1, totalWords: int = 100):
        prompt = (
            f"Use the following summary of the story: {summary} of type {genre} and use the {developmentPlot} to develop the story further. "
            f"Include {totalStoryCharacters} main character(s), {totalParagraphs} paragraph(s), and aim for about {totalWords} words."
        )
        response = openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        story = response.choices[0].message.content.strip()
        tokens_used = None
        if hasattr(response, 'usage') and response.usage and hasattr(response.usage, 'total_tokens'):
            tokens_used = response.usage.total_tokens
        return story, tokens_used
    

    @staticmethod
    def generate_summary(story: str, genre: str, temperature: float = 0):
        summary_prompt = f"Summarize the following {genre} story in 3-4 sentences: {story}"
        summary_response = openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": summary_prompt}],
            temperature=temperature,
        )
        story_summary = summary_response.choices[0].message.content.strip()
        tokens_used = None
        if hasattr(summary_response, 'usage') and summary_response.usage and hasattr(summary_response.usage, 'total_tokens'):
            tokens_used = summary_response.usage.total_tokens
        return story_summary, tokens_used
    

    @staticmethod
    def generate_image(plot: str, genre: str) -> str | None:
        image_prompt = f"Generate an illustration for this {genre} story: {plot}"
        image_response = openai_client.images.generate(
            model="dall-e-3", 
            quality="standard",  
            prompt=image_prompt,
            n=1, size="1024x1024"
        )
        base64Data = image_response.data[0].b64_json;
        return image_response.data[0].url if image_response.data else None


    @staticmethod
    def develop_story(summary: str, genre: str, image_needed: bool, developmentPlot: str, temperature: float = 0, totalStoryCharacters: int = 1, totalParagraphs: int = 1, totalWords: int = 100) -> StoryResponse:
        try:
            start_time = time.time()
            story, tokens_used_story = StoryWriter.develop_story_from_summary(summary, genre, developmentPlot, temperature, totalStoryCharacters, totalParagraphs, totalWords)
            story_summary, tokens_used_summary = StoryWriter.generate_summary(story, genre, temperature)
            image_url = None
            if image_needed:
                image_url = StoryWriter.generate_image(developmentPlot, genre)
            time_taken = time.time() - start_time
            total_tokens = (tokens_used_story or 0) + (tokens_used_summary or 0)
            return StoryResponse(
                story=story,
                storySummary=story_summary,
                image=image_url,
                modelStatistics=ModelStatistics(tokensUsedCount=total_tokens, timeTakenToProcessPrompt=time_taken)
            )
        except Exception as e:
            logging.exception("Error in StoryWriter.develop_story")
            return StoryResponse(error=str(e))


    @staticmethod
    def new_story(plot: str, image_needed: bool, genre: str, temperature: float = 0, totalStoryCharacters: int = 1, totalParagraphs: int = 1, totalWords: int = 100) -> StoryResponse:
        try:
            start_time = time.time()
            story, tokens_used_story = StoryWriter.generate_story(plot, genre, temperature, totalStoryCharacters, totalParagraphs, totalWords)
            story_summary, tokens_used_summary = StoryWriter.generate_summary(story, genre, temperature)
            image_url = None
            if image_needed:
                image_url = StoryWriter.generate_image(plot, genre)
            time_taken = time.time() - start_time
            total_tokens = (tokens_used_story or 0) + (tokens_used_summary or 0)
            return StoryResponse(
                story=story,
                storySummary=story_summary,
                image=image_url,
                modelStatistics=ModelStatistics(tokensUsedCount=total_tokens, timeTakenToProcessPrompt=time_taken)
            )
        except Exception as e:
            logging.exception("Error in StoryWriter.new_story")
            return StoryResponse(error=str(e))
