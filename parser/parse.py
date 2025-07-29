import csv
import logging
import random
import sys
import time

from dataclasses import fields, astuple
from pathlib import Path

from selenium import webdriver
from selenium.common import (
    ElementNotInteractableException,
    ElementClickInterceptedException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

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


def get_vacancy_details(driver: WebDriver, link: str) -> Vacancy:
    try:
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


def parsing_page() -> list[Vacancy]:
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

        all_vacancies = [get_vacancy_details(driver, link) for link in vacancy_links]
        all_vacancies = [v for v in all_vacancies if v is not None]
        logging.info("Ended parsing page")

        return all_vacancies

    except Exception as e:
        logging.error(f"Error during page parsing: {str(e)}")


def write_vacancies_to_csv_file(vacancies: list[Vacancy], root: str) -> None:
    try:
        logging.info("Started writing to CSV file")
        with open(root, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(VACANCY_FIELDS)
            writer.writerows([astuple(vacancy) for vacancy in vacancies])

    except Exception as e:
        logging.error(f"Error writing to CSV file: {str(e)}")


def get_all_python_vacancies() -> None:
    try:
        csv_path = PROJECT_ROOT / "python_vacancies.csv"
        write_vacancies_to_csv_file(parsing_page(), csv_path)
        logging.info("Finished writing to CSV file")

    except Exception as e:
        logging.error(f"Error in get_all_python_vacancies: {str(e)}")
