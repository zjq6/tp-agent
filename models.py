import os
import openai
import backoff
import google.generativeai as genai
from retry import retry  
from google.api_core.exceptions import GoogleAPIError

completion_tokens = prompt_tokens = 0

openai.api_key = "Your OPENAI_KEY"

# api_key = os.getenv("OPENAI_API_KEY", "")
# if api_key != "":
#     openai.api_key = api_key
# else:
#     print("Warning: OPENAI_API_KEY is not set")
    
api_base = os.getenv("OPENAI_API_BASE", "")
if api_base != "":
    print("Warning: OPENAI_API_BASE is set to {}".format(api_base))
    openai.api_base = api_base

@backoff.on_exception(backoff.expo, openai.error.OpenAIError)
def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

def gpt(prompt, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list: # easy 1000 tokens
    #messages = [{"role": "user", "content": prompt}]
    return chatgpt(prompt, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)
    
def chatgpt(messages, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    global completion_tokens, prompt_tokens
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        #change to google
        res = google_completions_with_backoff(messages=messages,n=cnt)
        #print(res)
        #res为列表，outputs接上res的内容        
        outputs.extend(res)
        # log completion tokens
        #completion_tokens += res["usage"]["completion_tokens"]
        #prompt_tokens += res["usage"]["prompt_tokens"]
    return outputs
    
def gpt_usage(backend="gpt-4"):
    global completion_tokens, prompt_tokens
    if backend == "gpt-4":
        cost = completion_tokens / 1000 * 0.06 + prompt_tokens / 1000 * 0.03
    elif backend in ["gpt-3.5-turbo", 'gpt-3.5-turbo-16k']:
        cost = (completion_tokens + prompt_tokens) / 1000 * 0.0002
    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens, "cost": cost}







def retry_gemini_call():
    def wrapper(func):
        @retry(tries=3, delay=2, on_exception=lambda e: isinstance(e, GoogleAPIError))
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapped
    return wrapper

@retry(tries=3, delay=2, exceptions=GoogleAPIError)
def google_completions_with_backoff(messages,n, model="gemini-pro", generation_config=None):
    #从message中取出prompt:messages = [{"role": "user", "content": prompt}]
    prompt=messages
    response_list=[]

    api_key = os.getenv("", "AIzaSyA2hiBKfimyF5ckq-Ui3-FtimJZJo6bH-c")
    genai.configure(api_key=api_key, transport='rest')
    if generation_config is None:
        generation_config = {
            "temperature": 0.1,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 1000,
        }
    model = genai.GenerativeModel(model_name=model, generation_config=generation_config)
    try:
        for _ in range(n):
            response = model.generate_content(prompt)
            #print("prompt:\n"+prompt+"\nprompt_end\n")
            #print(response.text)
            #response.text为str,将其加入到response_list中
            response_list.append(response.text)

        return response_list
    except GoogleAPIError as e:
        # 处理异常或重试逻辑
        raise e


def test_google_completions_with_backoff():
    prompt = """
    Make a writing plan for a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: It isn't difficult to do a handstand if you just stand on your hands. It caught him off guard that space smelled of seared steak. When she didn鈥檛 like a guy who was trying to pick her up, she started using sign language. Each person who knows you has a different perception of who you are.


The plan contains a one-setence description on each paragraph. Your output should be of the following format:

Plan:
Your plan here.

Following this plan: Plan:
 to write a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: It isn't difficult to do a handstand if you just stand on your hands. It caught him off guard that space smelled of seared steak. When she didn鈥檛 like a guy who was trying to pick her up, she started using sign language. Each person who knows you has a different perception of who you are.


Your output should be of the following format:

Passage:
Your passage here.

Analyze the following passage, then at the last line conclude "Thus the coherency score is {s}", where s is an integer from 1 to 10.
    """
    response = google_completions_with_backoff(prompt)
    print(response)

#test_google_completions_with_backoff()








