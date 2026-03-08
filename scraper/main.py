from flask import Flask, request
from recipe_scrapers import scrape_me
import logging
from parser import parse_ingredient
from playwright.sync_api import sync_playwright

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


app = Flask(__name__)


@app.route("/health")
def hello_world():
    return "Healthy", 201


@app.route("/scrape")
def scrape():
    recipe_url = request.args.get("recipe_url")
    if not recipe_url:
        logging.info("No URL provided")
        return "No URL provided", 500

    if "facebook" in recipe_url:
        # TODO(map) Move this to a different method at some point
        title = ""
        ingredients = []
        instructions = []
        with sync_playwright() as p:
            browser = p.chromium.launch(
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            page = browser.new_page()
            page.goto(recipe_url)
            caption = page.locator('link[rel="alternate"][title]')
            recipe = caption.get_attribute("title")
            logging.info(f"Extracted data: {recipe}")
            for ingredient in recipe[
                recipe.lower().index("ingredients")
                + len("ingredients:") : recipe.lower().index("instructions")
            ].split("\n"):
                if ingredient:
                    ingredients.extend(parse_ingredient(ingredient))

        response = {
            "name": title,
            "ingredients": ingredients,
            "instructions": instructions,
        }
        logging.info(f"Cleaned response {response}")
    else:
        scraper = scrape_me(recipe_url)
        logging.info(f"Extracted data: {scraper.to_json()}")
        ingredients = []
        for ingredient in scraper.ingredients():
            ingredients.extend(parse_ingredient(ingredient))
        instructions = []
        for i, instruction in enumerate(scraper.instructions().split("\n")):
            instructions.append({"stepNumber": i, "instruction": instruction})
        response = {
            "name": scraper.title(),
            "ingredients": ingredients,
            "instructions": instructions,
        }
        logging.info(f"Cleaned response {response}")

    return response, 201
