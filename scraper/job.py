from recipe_scrapers import scrape_me
from parser import parse_ingredient
from playwright.sync_api import sync_playwright
import threading

import logging

job_lock = threading.Lock()


def run_scrape_job(job_id: str, recipe_url: str, jobs: dict):
    with job_lock:
        try:
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
            jobs[job_id] = {"status": "success", "data": response}
        except Exception as err:
            logging.error(f"Job {job_id} failed: {str(err)}", exc_info=True)
            jobs[job_id] = {"status": "error", "message": str(err)}
