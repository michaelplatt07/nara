from gpt4all import GPT4All
from llama_cpp import Llama

import re
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# "orca-mini-3b-gguf2-q4_0.gguf",
# "mistral-7b-instruct-v0.1.Q4_K_M.gguf",
# model = GPT4All(
#     "Phi-3-mini-4k-instruct-q4.gguf",
#     model_path="/home/app/models",
#     allow_download=False,
#     device="cpu",
#     n_threads=4,
# )
model = Llama(
    model_path="/home/app/models/Phi-3-mini-4k-instruct-q4.gguf",
    n_ctx=1024,
    n_threads=4,
    verbose=False,
)


# Warm up for GPTAll
# logging.info("Warming up model...")
# model.generate("Hello", max_tokens=5, temp=0)
# logging.info("Finished warmup...")

# Warm up for Lallam
logging.info("Warming up model...")
model(
    "Hello",
    max_tokens=5,
    temperature=0.0,
)
logging.info("Finished warmup...")


def call_phi_model(text):
    prompt = f"""
    You are a strict ingredient parser. Return ONLY a JSON array, nothing else. No headers, no explanation, no markdown.

    Rules:
    - Multiply compound quantities: "two 8-ounce cans" -> 16
    - Prefer parenthetical units: "2 pints (20 ounces)" -> 20 ounces
    - Strip packaging words: block, package, can, jar, container
    - Written numbers to digits: "one" -> 1
    - Vague seasoning amounts: set quantity to "to taste" and unit to ""
    - If a line contains multiple ingredients joined by "and", return one object per ingredient
    - A comma does NOT mean multiple ingredients - it introduces a preparation note or qualifier to strip
    - Split ingredients share the same quantity/unit if none is specified per ingredient
    - Words such as whole, clove, stalk used to describe ingredients that are not seasonings can be used in unit
    - If no unit can be derived simply make it a blank string ""
    - All keys in the JSON response MUST have a value
    - Strip preparation notes after a comma: minced, finely grated, chopped, drained, softened, and similar
    - Strip qualifier words after a comma: optional, to taste, if desired, as needed
    - Strip parenthetical notes like (see Cook's Note), (optional)

    Format: [{{"name":"string","quantity":"string","unit":"string"}}]

    Examples:
    Input: one 8-ounce block feta cheese, drained (see Cook's Note)
    Output: [{{"name":"feta cheese","quantity":"8","unit":"oz"}}]
    Input: 2 pints (20 ounces) cherry tomatoes
    Output: [{{"name":"cherry tomatoes","quantity":"20","unit":"oz"}}]
    Input: two 8-ounce cans tomato sauce
    Output: [{{"name":"tomato sauce","quantity":"16","unit":"oz"}}]
    Input: a dash of salt and pepper
    Output: [{{"name":"salt","quantity":"to taste","unit":""}},{{"name":"pepper","quantity":"to taste","unit":""}}]
    Input: salt and pepper to taste
    Output: [{{"name":"salt","quantity":"to taste","unit":""}},{{"name":"pepper","quantity":"to taste","unit":""}}]
    Input: 1 cup chicken stock and 2 tbsp butter
    Output: [{{"name":"chicken stock","quantity":"1","unit":"cup"}},{{"name":"butter","quantity":"2","unit":"tbsp"}}]
    Input: 1 clove garlic, finely grated
    Output: [{{"name":"garlic","quantity":"1","unit":"clove"}}]
    Input: 3 cloves garlic, minced
    Output: [{{"name":"garlic","quantity":"3","unit":"clove"}}]
    Input: Pinch crushed red pepper flakes, optional
    Output: [{{"name":"crushed red pepper flakes","quantity":"to taste","unit":""}}]
    Input: 2 stalks celery
    Output: [{{"name":"celery","quantity":"2","unit":"stalk"}}]
    Input: 1 whole onion
    Output: [{{"name":"onion","quantity":"1","unit":"whole"}}]

    Input: {text}
    Output:"""
    logging.info(f"Attempting to generate response for ingredient {text}")
    response = ""
    for chunk in model(
        prompt,
        max_tokens=100,
        temperature=0.0,
        stream=True,
    ):
        token = chunk["choices"][0]["text"]
        print(token, end="", flush=True)  # live token output
        response += token
        if "]" in response:
            break
    print("\n", end="", flush=True)
    return response


def call_mistral_model(text):
    prompt = f"""You are a strict ingredient parser. Return ONLY a JSON array, nothing else.

    Rules:
    - Multiply compound quantities: "two 8-ounce cans" -> 16
    - Prefer parenthetical units: "2 pints (20 ounces)" -> 20 ounces
    - Strip packaging words: block, package, can, jar, container
    - Written numbers to digits: "one" -> 1
    - Vague seasoning amounts: set quantity to "to taste" and unit to ""
    - If a line contains multiple ingredients joined by "and" or ",", return one object per ingredient
    - Split ingredients share the same quantity/unit if none is specified per ingredient
    - Words such as whole, clove, stalks used to describe ingredients taht are not seasonings can be used in unit
    - If no unit can be derived simply make it a blank string ""
    - All keys in the JSON response MUST have a value

    Format: [{{"name":"string","quantity":"string","unit":"string"}}]

    Examples:
    Input: one 8-ounce block feta cheese
    Output: [{{"name":"feta cheese","quantity":"8","unit":"oz"}}]
    Input: 2 pints (20 ounces) cherry tomatoes
    Output: [{{"name":"cherry tomatoes","quantity":"20","unit":"oz"}}]
    Input: two 8-ounce cans tomato sauce
    Output: [{{"name":"tomato sauce","quantity":"16","unit":"oz"}}]
    Input: a dash of salt and pepper
    Output: [{{"name":"salt","quantity":"to taste","unit":""}},{{"name":"pepper","quantity":"to taste","unit":""}}]
    Input: salt and pepper to taste
    Output: [{{"name":"salt","quantity":"to taste","unit":""}},{{"name":"pepper","quantity":"to taste","unit":""}}]
    Input: 1 cup chicken stock and 2 tbsp butter
    Output: [{{"name":"chicken stock","quantity":"1","unit":"cup"}},{{"name":"butter","quantity":"2","unit":"tbsp"}}]

    Input: {text}
    Output:"""
    logging.info(f"Attempting to generate response for ingredient {text}")
    response = ""
    # response = model.generate(prompt, max_tokens=50, temp=0)
    for token in model.generate(
        prompt,
        max_tokens=400,
        temp=0,
        streaming=True,
    ):
        print(token, end="", flush=True)  # live token output
        response += token

    return response


def parse_ingredient(text: str) -> list:
    response = call_phi_model(text)
    logging.info(f"Response: {response}")
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError:
        pass
    matches = re.findall(r"\{.*?\}", response, re.DOTALL)
    if matches:
        try:
            return [json.loads(match) for match in matches]
            return response
        except:
            raise Exception("Couldn't match")

    raise Exception("Couldn't extract data")
