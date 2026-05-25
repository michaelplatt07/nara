import json
import logging
import threading
from parser import extract_info, parse_ingredient

from playwright.sync_api import sync_playwright
from recipe_scrapers import scrape_me

from db import Job, update_job

job_lock = threading.Lock()


def run_scrape_job(job_id: str, recipe_url: str, jobs: dict):
    with job_lock:
        try:
            if "facebook" in recipe_url:
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
                    # TODO(map) Does it make sense to store the original recipe text in the job?
                    logging.info(f"Extracted data: {recipe}")
                    update_job(Job(job_id=job_id, original_data=recipe))
                    recipe_info = extract_info(recipe)
                    ingredients = []
                    for ingredient in recipe_info["ingredients"]:
                        ingredients.extend(parse_ingredient(ingredient))
                    instructions = []
                    for i, instruction in enumerate(recipe_info["instructions"]):
                        instructions.append(
                            {"stepNumber": i, "instruction": instruction}
                        )
                response = {
                    "name": recipe_info["name"],
                    "url": recipe_url,
                    "ingredients": ingredients,
                    "instructions": instructions,
                }
                logging.info(f"Cleaned response {response}")
            else:
                scraper = scrape_me(recipe_url)
                logging.info(f"Extracted data: {scraper.to_json()}")
                update_job(
                    Job(
                        job_id=job_id,
                        original_data=json.dumps(scraper.to_json(), indent=2),
                    )
                )
                ingredients = []
                for ingredient in scraper.ingredients():
                    ingredients.extend(parse_ingredient(ingredient))
                instructions = []
                for i, instruction in enumerate(scraper.instructions().split("\n")):
                    instructions.append({"stepNumber": i, "instruction": instruction})
                response = {
                    "name": scraper.title(),
                    "url": recipe_url,
                    "ingredients": ingredients,
                    "instructions": instructions,
                }
                logging.info(f"Cleaned response {response}")
            update_job(Job(job_id=job_id, status="success", data=response))
            jobs[job_id] = {"status": "success", "data": response}

        except Exception as err:
            logging.error(f"Job {job_id} failed: {str(err)}", exc_info=True)
            update_job(Job(job_id=job_id, status="error", message=str(err)))
            jobs[job_id] = {"status": "error", "message": str(err)}
