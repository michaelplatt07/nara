import json
import logging
import re

from gpt4all import GPT4All
from llama_cpp import Llama

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
    n_ctx=2048,
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


# prompt = f"""
# You are a strict ingredient parser. Return ONLY a JSON array, nothing else. No headers, no explanation, no markdown.
#
# Rules:
# - Multiply compound quantities: "two 8-ounce cans" -> 16
# - Prefer parenthetical units: "2 pints (20 ounces)" -> 20 ounces
# - Strip packaging words: block, package, can, jar, container
# - Written numbers to digits: "one" -> 1
# - Vague seasoning amounts: set quantity to "to taste" and unit to ""
# - If a line contains multiple ingredients joined by "and", return one object per ingredient
# - A comma does NOT mean multiple ingredients - it introduces a preparation note or qualifier to strip
# - Split ingredients share the same quantity/unit if none is specified per ingredient
# - Words such as whole, clove, stalk used to describe ingredients that are not seasonings can be used in unit
# - If no unit can be derived simply make it a blank string ""
# - All keys in the JSON response MUST have a value
# - Strip preparation notes after a comma: minced, finely grated, chopped, drained, softened, and similar
# - Strip qualifier words after a comma: optional, to taste, if desired, as needed
# - Strip parenthetical notes like (see Cook's Note), (optional)
#
# Format: [{{"name":"string","quantity":"string","unit":"string"}}]
#
# Examples:
# Input: one 8-ounce block feta cheese, drained (see Cook's Note)
# Output: [{{"name":"feta cheese","quantity":"8","unit":"oz"}}]
# Input: 2 pints (20 ounces) cherry tomatoes
# Output: [{{"name":"cherry tomatoes","quantity":"20","unit":"oz"}}]
# Input: two 8-ounce cans tomato sauce
# Output: [{{"name":"tomato sauce","quantity":"16","unit":"oz"}}]
# Input: a dash of salt and pepper
# Output: [{{"name":"salt","quantity":"to taste","unit":""}},{{"name":"pepper","quantity":"to taste","unit":""}}]
# Input: salt and pepper to taste
# Output: [{{"name":"salt","quantity":"to taste","unit":""}},{{"name":"pepper","quantity":"to taste","unit":""}}]
# Input: 1 cup chicken stock and 2 tbsp butter
# Output: [{{"name":"chicken stock","quantity":"1","unit":"cup"}},{{"name":"butter","quantity":"2","unit":"tbsp"}}]
# Input: 1 clove garlic, finely grated
# Output: [{{"name":"garlic","quantity":"1","unit":"clove"}}]
# Input: 3 cloves garlic, minced
# Output: [{{"name":"garlic","quantity":"3","unit":"clove"}}]
# Input: Pinch crushed red pepper flakes, optional
# Output: [{{"name":"crushed red pepper flakes","quantity":"to taste","unit":""}}]
# Input: 2 stalks celery
# Output: [{{"name":"celery","quantity":"2","unit":"stalk"}}]
# Input: 1 whole onion
# Output: [{{"name":"onion","quantity":"1","unit":"whole"}}]
#
# Input: {text}
# Output:"""
# prompt = f"""
# You are a strict ingredient parser. Return ONLY a JSON array, nothing else. No headers, no explanation, no markdown.
# Rules:
# - Multiply compound quantities: "two 8-ounce cans" -> 16
# - Prefer parenthetical units: "2 pints (20 ounces)" -> 20 ounces
# - Strip packaging words: block, package, can, jar, container
# - Written numbers to digits: "one" -> 1
# - Vague seasoning amounts: set quantity to "to taste" and unit to ""
# - If a line contains multiple ingredients joined by "and", return one object per ingredient
# - A comma does NOT mean multiple ingredients - it introduces a preparation note or qualifier to strip
# - Split ingredients share the same quantity/unit if none is specified per ingredient
# - Words such as whole, clove, stalk used to describe ingredients that are not seasonings can be used in unit
# - If no unit can be derived simply make it a blank string ""
# - All keys in the JSON response MUST have a value
# - Preparation methods after a comma (minced, finely grated, chopped, drained, softened, diced, sliced, etc.) go into "notes", not the name
# - Preparation methods directly after the ingredient name with no comma (finely diced, roughly chopped, thinly sliced) also go into "notes"
# - Strip qualifier words: optional, to taste, if desired, as needed — these do NOT go in notes
# - Strip parenthetical notes like (see Cook's Note), (optional)
# - If there is no preparation note, "notes" must be an empty string ""
# Format: [{{"name":"string","quantity":"string","unit":"string","notes":"string"}}]
# Examples:
# Input: one 8-ounce block feta cheese, drained (see Cook's Note)
# Output: [{{"name":"feta cheese","quantity":"8","unit":"oz","notes":"drained"}}]
# Input: 2 pints (20 ounces) cherry tomatoes
# Output: [{{"name":"cherry tomatoes","quantity":"20","unit":"oz","notes":""}}]
# Input: two 8-ounce cans tomato sauce
# Output: [{{"name":"tomato sauce","quantity":"16","unit":"oz","notes":""}}]
# Input: a dash of salt and pepper
# Output: [{{"name":"salt","quantity":"to taste","unit":"","notes":""}},{{"name":"pepper","quantity":"to taste","unit":"","notes":""}}]
# Input: salt and pepper to taste
# Output: [{{"name":"salt","quantity":"to taste","unit":"","notes":""}},{{"name":"pepper","quantity":"to taste","unit":"","notes":""}}]
# Input: 1 cup chicken stock and 2 tbsp butter
# Output: [{{"name":"chicken stock","quantity":"1","unit":"cup","notes":""}},{{"name":"butter","quantity":"2","unit":"tbsp","notes":""}}]
# Input: 1 clove garlic, finely grated
# Output: [{{"name":"garlic","quantity":"1","unit":"clove","notes":"finely grated"}}]
# Input: 3 cloves garlic, minced
# Output: [{{"name":"garlic","quantity":"3","unit":"clove","notes":"minced"}}]
# Input: Pinch crushed red pepper flakes, optional
# Output: [{{"name":"crushed red pepper flakes","quantity":"to taste","unit":"","notes":""}}]
# Input: 2 stalks celery
# Output: [{{"name":"celery","quantity":"2","unit":"stalk","notes":""}}]
# Input: 1 whole onion
# Output: [{{"name":"onion","quantity":"1","unit":"whole","notes":""}}]
# Input: 3 cups mushrooms finely diced
# Output: [{{"name":"mushrooms","quantity":"3","unit":"cup","notes":"finely diced"}}]
# Input: 2 carrots, roughly chopped
# Output: [{{"name":"carrots","quantity":"2","unit":"","notes":"roughly chopped"}}]
# Input: {text}
# Output:
# """
def call_phi_model(text):
    prompt = f"""
You are a strict ingredient parser. Return ONLY a JSON array, nothing else. No headers, no explanation, no markdown.

Rules:
- Multiply compound quantities: "two 8-ounce cans" -> 16
- Prefer parenthetical units: "2 pints (20 ounces)" -> 20 ounces
- Strip packaging words: block, package, can, jar, container
- Written numbers to digits: "one" -> 1
- Keep fractions as-is: "2/3" -> "2/3", "1/4" -> "1/4"
- Vague or seasoning amounts (pinch, dash, to taste, optional): set quantity to "to taste" and unit to ""
- unit, quantity, and notes in the JSON response MUST ALWAYS at least have an empty string to be valid JSON
- If a line contains multiple ingredients joined by "and", return one object per ingredient
- If a line contains alternatives joined by "or", take the FIRST option only and ignore the rest
- A comma does NOT mean multiple ingredients - it introduces a preparation note or qualifier to strip
- Split ingredients share the same quantity/unit if none is specified per ingredient
- Words such as whole, clove, stalk used to describe ingredients that are not seasonings can be used as unit
- If no unit can be derived, make it a blank string ""
- All keys in the JSON response MUST have a value
- Do NOT convert units — preserve the unit as written, only normalize abbreviations (tablespoon -> tbsp, teaspoon -> tsp, ounce -> oz, pound -> lb)
- Preparation methods after a comma (minced, finely grated, chopped, drained, softened, diced, sliced, trimmed, halved, crushed, cut into X-inch pieces, etc.) go into "notes"
- Preparation methods directly after the ingredient name with no comma (finely diced, roughly chopped, thinly sliced) also go into "notes"
- Descriptor adjectives before the ingredient name (freshly, reduced-sodium, fresh, dried, coarsely, finely, boneless, skinless, ground, seasoned, all-purpose) should be stripped unless they are part of the ingredient's proper name
- Strip qualifier words: optional, to taste, if desired, as needed, divided — these do NOT go in notes
- Strip parenthetical notes like (see Cook's Note), (optional)
- If there is no preparation note, "notes" must be an empty string ""

Format: [{{"name":"string","quantity":"string","unit":"string","notes":"string"}}]

Examples:
Input: one 8-ounce block feta cheese, drained (see Cook's Note)
Output: [{{"name":"feta cheese","quantity":"8","unit":"oz","notes":"drained"}}]

Input: 2 pints (20 ounces) cherry tomatoes
Output: [{{"name":"cherry tomatoes","quantity":"20","unit":"oz","notes":""}}]

Input: two 8-ounce cans tomato sauce
Output: [{{"name":"tomato sauce","quantity":"16","unit":"oz","notes":""}}]

Input: a dash of salt and pepper
Output: [{{"name":"salt","quantity":"to taste","unit":"","notes":""}},{{"name":"pepper","quantity":"to taste","unit":"","notes":""}}]

Input: salt and pepper to taste
Output: [{{"name":"salt","quantity":"to taste","unit":"","notes":""}},{{"name":"pepper","quantity":"to taste","unit":"","notes":""}}]

Input: 1 cup chicken stock and 2 tbsp butter
Output: [{{"name":"chicken stock","quantity":"1","unit":"cup","notes":""}},{{"name":"butter","quantity":"2","unit":"tbsp","notes":""}}]

Input: 1 clove garlic, finely grated
Output: [{{"name":"garlic","quantity":"1","unit":"clove","notes":"finely grated"}}]

Input: 3 cloves garlic, minced
Output: [{{"name":"garlic","quantity":"3","unit":"clove","notes":"minced"}}]

Input: Pinch crushed red pepper flakes, optional
Output: [{{"name":"crushed red pepper flakes","quantity":"to taste","unit":"","notes":""}}]

Input: 2 stalks celery
Output: [{{"name":"celery","quantity":"2","unit":"stalk","notes":""}}]

Input: 1 whole onion
Output: [{{"name":"onion","quantity":"1","unit":"whole","notes":""}}]

Input: 3 cups mushrooms finely diced
Output: [{{"name":"mushrooms","quantity":"3","unit":"cup","notes":"finely diced"}}]

Input: 2 carrots, roughly chopped
Output: [{{"name":"carrots","quantity":"2","unit":"","notes":"roughly chopped"}}]

Input: 2 tablespoons olive oil, divided
Output: [{{"name":"olive oil","quantity":"2","unit":"tbsp","notes":""}}]

Input: 1 1/2 pounds skinless, boneless chicken breast cut into 1-inch pieces
Output: [{{"name":"chicken breast","quantity":"1 1/2","unit":"lb","notes":"cut into 1-inch pieces"}}]

Input: 3/4 teaspoon freshly ground black pepper, divided
Output: [{{"name":"black pepper","quantity":"3/4","unit":"tsp","notes":"ground"}}]

Input: 2/3 cup seasoned panko breadcrumbs
Output: [{{"name":"panko breadcrumbs","quantity":"2/3","unit":"cup","notes":""}}]

Input: 1 (8 ounce) package cream cheese, softened
Output: [{{"name":"cream cheese","quantity":"8","unit":"oz","notes":"softened"}}]

Input: 1 tablespoon chopped fresh basil or 1 teaspoon dried basil, crushed
Output: [{{"name":"basil","quantity":"1","unit":"tbsp","notes":"chopped fresh"}}]

Input: 1 cup grated Parmesan cheese, divided
Output: [{{"name":"Parmesan cheese","quantity":"1","unit":"cup","notes":"grated"}}]

Input: 1 pound asparagus, trimmed and coarsely chopped
Output: [{{"name":"asparagus","quantity":"1","unit":"lb","notes":"trimmed and coarsely chopped"}}]

Input: {text}
Output:
"""

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
        # Only break if we have a complete, valid JSON array
        stripped = response.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            break
    print("\n", end="", flush=True)
    return response


def call_phi_model_extract_ingredients_and_instructions(text):
    prompt = f"""
You are a recipe parser. Extract data from raw recipe text.

Given the text below, extract:
1. **name** - the name of the recipe as listed in the caption
2. **ingredients** - every ingredient mentioned, as a simple plain-text string per item
3. **instructions** - each step, as a simple plain-text string per item

Rules:
- Do not infer, add, or modify any information not present in the text
- Include quantities and descriptors as part of the ingredient string (e.g. "2 cups flour")
- Discard section headers, notes, tips, serving suggestions, and nutrition info
- If either section cannot be found, return an empty list

Respond ONLY with valid JSON, no explanation or preamble:
{{
  "name": "bang bang salmon bites",
  "ingredients": ["2 skinless boneless salmon fillets cubed (~240g)", "1 tsp paprika"],
  "instructions": ["Add the salmon cubes to a bowl with all the seasonings.", "Toss well."]
}}

Input: {text}
Output:
"""
    logging.info(
        "Attempting to extract ingredients and instructions from Facebook recipe"
    )
    response = ""
    for chunk in model(
        prompt,
        max_tokens=1024,
        temperature=0.0,
        stream=True,
    ):
        token = chunk["choices"][0]["text"]
        print(token, end="", flush=True)  # live token output
        response += token
        # Only break if we have a complete, valid JSON array
        stripped = response.strip()
        if stripped.startswith("{") and stripped.endswith("}"):
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
    logging.info(f"Model response: {response}")
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError:
        pass
    matches = [
        re.sub(r",\s*([}\]])", r"\1", res)
        for res in re.findall(r"\{.*?\}", response, re.DOTALL)
    ]
    if matches:
        try:
            logging.info(f"Matches: {matches}")
            results = []
            for match in matches:
                try:
                    results.append(json.loads(match))
                except json.JSONDecodeError:
                    logging.warning(f"Skipping malformed match: {match}")
                    continue
                if results:
                    return results
        except:
            raise Exception("Couldn't match")

    raise Exception("Couldn't extract data")


def extract_info(text):
    response = call_phi_model_extract_ingredients_and_instructions(text)
    logging.info(f"Model response: {response}")
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError:
        pass
    matches = [
        re.sub(r",\s*([}\]])", r"\1", res)
        for res in re.findall(r"\{.*?\}", response, re.DOTALL)
    ]
    if matches:
        try:
            logging.info(f"Matches: {matches}")
            results = []
            for match in matches:
                try:
                    results.append(json.loads(match))
                except json.JSONDecodeError:
                    logging.warning(f"Skipping malformed match: {match}")
                    continue
                if results:
                    return results
        except:
            raise Exception("Couldn't match")

    raise Exception("Couldn't extract data")
