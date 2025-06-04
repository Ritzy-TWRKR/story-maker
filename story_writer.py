import openai
import logging
import time
import httpx

from schemas import DevelopStoryRequest, StoryRequest, StoryResponse, ModelStatistics

API_KEY = ""#Enter API KEy here
MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"
BASE_URL = "https://api.deepinfra.com/v1/openai"

openai_client = openai.OpenAI(api_key=API_KEY, 
                              base_url=BASE_URL, 
                              http_client=httpx.Client(timeout=60))


class StoryWriter:


    @staticmethod

    @staticmethod
    def develop_story(request:DevelopStoryRequest) -> StoryResponse:
        try:
            start_time = time.time()
            story, tokens_used_story = StoryWriter.develop_story_from_summary(request)
            story_summary, tokens_used_summary = StoryWriter.generate_summary(story, request.genre, request.experimentBoundary)
            image_url = None
            if request.imageNeeded:
                image_url = StoryWriter.generate_image(request.plot, request.genre)
            time_taken = time.time() - start_time
            total_tokens = (tokens_used_story or 0) + (tokens_used_summary or 0)
            return StoryResponse(
                story=story,
                storySummary=story_summary,
                image=image_url,
                modelStatistics=ModelStatistics(tokensUsedCount=total_tokens, timeTakenToProcessPrompt=time_taken)
            )
        except Exception as e:
            logging.exception("Error in developing a story")
            return StoryResponse(error=str(e))


    @staticmethod
    def new_story(request:StoryRequest) -> StoryResponse:
        try:
            start_time = time.time()
            story, tokens_used_story = StoryWriter.generate_story(request.plot, request.genre, request.experimentBoundary, request.totalStoryCharacters, request.totalParagraphs, request.totalWords)
            story_summary, tokens_used_summary = StoryWriter.generate_summary(story, request.genre, request.experimentBoundary)
            image_url = None
            if request.imageNeeded:
                image_url = StoryWriter.generate_image(request.plot, request.genre)
            time_taken = time.time() - start_time
            total_tokens = (tokens_used_story or 0) + (tokens_used_summary or 0)
            return StoryResponse(
                story=story,
                storySummary=story_summary,
                image=image_url,
                modelStatistics=ModelStatistics(tokensUsedCount=total_tokens, timeTakenToProcessPrompt=time_taken)
            )
        except Exception as e:
            logging.exception("Error in generrating a new story")
            return StoryResponse(error=str(e))

    def develop_story_from_summary(request:DevelopStoryRequest):
        prompt = (
            f"Use the following summary of the story: {request.summary} of type {request.genre} and"
            f"use the {request.plot} to develop the story further. "
            f"Include {request.totalStoryCharacters} main character(s), {request.totalParagraphs} paragraph(s),"
             f" and aim for about {request.totalWords} words."
        )
        response = openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=request.experimentBoundary
        )
        story = response.choices[0].message.content.strip()
        tokens_used = None
        if hasattr(response, 'usage') and response.usage and hasattr(response.usage, 'total_tokens'):
            tokens_used = response.usage.total_tokens
        return story, tokens_used
    

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
