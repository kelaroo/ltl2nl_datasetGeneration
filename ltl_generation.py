'''
    Module to call LLM and generate LTL from NLP
'''

from google import genai
import time

PROMPT_LTL2NLP = "Given this the following sentance in natural language, describing a command for a mobile robot: <nlp>, generate a LTL(linear temporal logic) formula equivalent to the given command. Don't add any whitespace, only use the following operators and only in the format given before the '=' sign: &&=AND, ||=OR, F=eventually, G=globally"

MAX_NR_RETRIES = 6

def generate_nlp2ltl(aiClient, nlpSentence: str) -> str:
    prompt = PROMPT_LTL2NLP.replace("<nlp>", nlpSentence)

    retries = 0
    
    while retries < MAX_NR_RETRIES:
        try:
            response = aiClient.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': str,
                },
            )
            return response.text
        
        except genai.errors.APIError as e:
            # Usage limit hit: back off and retry
            print(f"[Rate limit hit] Retrying in 10 seconds...")
            print(e)
            time.sleep(10)
            retries += 1
        except Exception as e:
            # Catch all other exceptions
            raise RuntimeError(f"Request failed: {e}") from e

    return "[ERROR] Max retries reached"

