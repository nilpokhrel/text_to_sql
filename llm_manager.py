
from openai import OpenAI
# import openai
# import os
import config
from google import genai
from google.genai import types


# get api keys
from dotenv import load_dotenv
load_dotenv()

openai_api_key = config.OPENAI_API_KEY #
client_openai = OpenAI(api_key=openai_api_key)

# Set up API Key
gemini_api_key = config.GEMINI_API_KEY
client_gemini = genai.Client(api_key=gemini_api_key)
## AGENT BASE

llm_model = config.LLM_MODEL

class LLMManager:
    """ Text Processing Using AI
    """
    def __init__(self):
        """Text Processing on Given Document or Prompt

        Args:
            gpt_model (str): Versions of LLM model
            user_question_query (str): Query on embedded documents/texts for semantic search/text extraction
            system_response_query (str, optional): How AI should answer. Defaults to None.
            temperature (int, optional): Tunning Parameter on creativity of AI. Defaults to 0.
            debug (bool, optional): To display information of Input/Output. Defaults to False.
        """
            
    def open_ai_llm_engine(self, user_question_query, system_response_query=None, temperature=0, max_out_tokens=1024):
        
        
        params = {
                    "model": llm_model,
                    "messages": [
                                    {'role': 'system', 'content': system_response_query},
                                    {'role': 'user', 'content': user_question_query}
                                ],
                    'temperature':temperature
                    }
        # control output tokens 

        params["max_tokens"] = max_out_tokens
            
        try:
            response = client_openai.chat.completions.create(**params)
            response = response.choices[0].message.content
        except  Exception as err:
            raise err('LLM server error: {err}')
    
    def gemini_ai_llm_engine(self, user_question, system_prompt=None, temperature=0, max_output_tokens=8192):
        
        try:
            response = client_gemini.models.generate_content(
                        model=llm_model,
                        config=types.GenerateContentConfig(
                                system_instruction=system_prompt,
                                max_output_tokens=max_output_tokens,
                                temperature=temperature),
                        contents=[user_question],
 
                        )
            return response.text  # Gemini returns `.text` instead of `.choices[0].message.content`
        except Exception as err:
            raise Exception(f"LLM server error: {err}")
        

    def query_engine(self, user_question_query, system_response_query=None, max_out_tokens=1024, T=0, engine=None, show_response=False):
        
            """
            Accepts user query and request gpt api to return json answer response.
            Args:
                user_question_query (str, optional): Accepts user query string. Defaults to None.
                system_response_query (str, optional): String query for system. Defaults to None.
                temperature (int, optional): ranges from 0-10 where 0 means factual and 10 means imaginative. Defaults to 0.

            Raises:
                ValueError: User query is mandatory for any request to gpt api.

            Returns:
                json: LLM Model generated Output
            """
            if engine is None:
                engine = config.LLM_PROVIDER
            
            response = '************************LLM Response not available*****************************'
            
            if not user_question_query:
                raise ValueError('User query cannot have empty string or Null value.')

            if not system_response_query:
                system_response_query = 'You follow the given query.'
                
            # call llm engine
            if engine == 'gemini':
                response = self.gemini_ai_llm_engine(user_question_query, system_prompt=system_response_query, temperature=T, max_output_tokens=max_out_tokens)
            elif engine == 'openai':
                response = self.open_ai_llm_engine(user_question_query, system_response_query=system_response_query, temperature=T, max_out_tokens=max_out_tokens)
            else:
                ValueError('Select correct LLM model engine name')
                      
            if show_response:
                print('LLM response for user query: ')
                print(response)
            return response
        
    

if __name__ == '__main__':
    # SAMPLE TEST 
    llm_agent = LLMManager()
    
    usry = """explain ai."""
   
    task = llm_agent.query_engine(usry, system_response_query='Act as a Ontologist.',show_response=False)
    print(task)

        
