import csv
import logging
import random
import sys
import time
import asyncio

from dataclasses import fields, astuple
from datetime import datetime
from pathlib import Path

from selenium.common import (
    ElementNotInteractableException,
    ElementClickInterceptedException,
    NoSuchElementException,
)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options

from parser.parsing_item import Vacancy
from parser.technologies import ALL_TECHNOLOGIES


PROJECT_ROOT = Path(__file__).parent.parent

BASE_URL = "https://jobs.dou.ua/"
CATEGORY = "Python"

_driver: WebDriver | None = None


def get_driver() -> WebDriver:
    return _driver


def set_driver(new_driver: WebDriver) -> None:
    global _driver
    _driver = new_driver


VACANCY_FIELDS = [field.name for field in fields(Vacancy)]


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)8s]: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)


async def get_vacancy_details(
    link: str, semaphore: asyncio.Semaphore
) -> Vacancy | None:
    async with semaphore:
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            return await loop.run_in_executor(executor, get_vacancy_details_sync, link)


def get_vacancy_details_sync(link: str) -> Vacancy | None:
    driver = None
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)

        time.sleep(random.uniform(2, 4))
        driver.get(link)

        title = driver.find_element(By.CLASS_NAME, "g-h2").text
        company = driver.find_element(By.CSS_SELECTOR, "div.l-n a").text
        vacancy_description = driver.find_element(By.CLASS_NAME, "l-vacancy").text
        tech_list = list(
            set([tech for tech in ALL_TECHNOLOGIES if tech in vacancy_description])
        )
        location = driver.find_element(By.CLASS_NAME, "place").text
        salary = "Not specified"
        if driver.find_elements(By.CLASS_NAME, "salary"):
            salary = driver.find_element(By.CLASS_NAME, "salary").text

        logging.info(f"Got {title} details")

        return Vacancy(
            title=title,
            company=company,
            technologies=tech_list,
            location=location,
            salary=salary,
            link=driver.current_url,
        )

    except Exception as e:
        logging.error(f"Failed to get details for {link}: {str(e)}")
        return None

    finally:
        if driver:
            driver.quit()


async def parsing_page() -> list[Vacancy] | None:
    try:
        url = f"{BASE_URL}vacancies/?category={CATEGORY}"
        driver = get_driver()
        driver.get(url)

        while True:
            try:
                logging.info("Clicking 'More' button")
                more_button = driver.find_element(By.CLASS_NAME, "more-btn")
                if more_button.is_displayed():
                    more_button.click()
                else:
                    break
            except (
                NoSuchElementException,
                ElementNotInteractableException,
                ElementClickInterceptedException,
            ):
                logging.info("'More' button is not displayed")
                break

        page_vacancies = driver.find_elements(By.CLASS_NAME, "l-vacancy")
        vacancy_links = [
            vacancy.find_element(By.CLASS_NAME, "vt").get_attribute("href")
            for vacancy in page_vacancies
        ]

        semaphore = asyncio.Semaphore(5)
        tasks = [get_vacancy_details(link, semaphore) for link in vacancy_links]
        all_vacancies = await asyncio.gather(*tasks)
        vacancies = [
            vacancy for vacancy in all_vacancies if isinstance(vacancy, Vacancy)
        ]
        logging.info(f"Ended parsing page. Got {len(vacancies)} vacancies")

        return vacancies

    except Exception as e:
        logging.error(f"Error during page parsing: {str(e)}")
        return []


def write_vacancies_to_csv_file(vacancies: list[Vacancy], root: Path) -> None:
    try:
        logging.info("Started writing to CSV file")
        with open(root, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(VACANCY_FIELDS)
            writer.writerows([astuple(vacancy) for vacancy in vacancies])

    except Exception as e:
        logging.error(f"Error writing to CSV file: {str(e)}")


def generate_csv_filename() -> Path:
    """Generate CSV filename with current date and time"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return PROJECT_ROOT / f"python_vacancies_{timestamp}.csv"


async def get_all_python_vacancies() -> Path | None:
    try:
        csv_path = generate_csv_filename()
        vacancies = await parsing_page()
        write_vacancies_to_csv_file(vacancies, csv_path)
        logging.info("Finished writing to CSV file")
        return csv_path

    except Exception as e:
        logging.error(f"Error in get_all_python_vacancies: {str(e)}")
