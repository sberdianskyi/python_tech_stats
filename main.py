import logging
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from parser.parse import set_driver, get_all_python_vacancies
from data_analysis.data_analyzer import analyze_data_from_csv

PROJECT_ROOT = Path(__file__).parent

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)8s]: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)


def main():
    """Main program function"""
    try:
        # Check if CSV file already exists
        csv_path = PROJECT_ROOT / "python_vacancies.csv"
        if csv_path.exists():
            logging.info("CSV file with data already exists. Program will exit.")
            return

        options = Options()
        options.add_argument("--headless")

        # Parse vacancies
        logging.info("Starting vacancy parsing...")
        try:
            with webdriver.Chrome(options=options) as driver:
                set_driver(driver)
                get_all_python_vacancies()
        except Exception as e:
            logging.error(f"Error during vacancy parsing: {str(e)}")

        # Analyze data and create chart
        logging.info("Starting data analysis...")
        try:
            csv_path = PROJECT_ROOT / "python_vacancies.csv"
            analyze_data_from_csv(csv_path)
        except Exception as e:
            logging.error(f"Error during data analysis: {str(e)}")

        logging.info("Process completed successfully!")

    except Exception as e:
        logging.error(f"Critical error in main function: {str(e)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Program interrupted by user")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
