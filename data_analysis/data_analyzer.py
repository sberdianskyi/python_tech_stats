import csv
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path
from typing import List, Dict
import logging

from parser.parsing_item import Vacancy

PROJECT_ROOT = Path(__file__).parent.parent


def read_vacancies_from_csv(csv_path: Path) -> List[Vacancy]:
    """Reads vacancies from CSV file"""
    vacancies = []
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Parse technologies list from string
            technologies = eval(row["technologies"]) if row["technologies"] else []
            vacancy = Vacancy(
                title=row["title"],
                company=row["company"],
                technologies=technologies,
                location=row["location"],
                salary=row["salary"],
                link=row["link"],
            )
            vacancies.append(vacancy)
    return vacancies


def analyze_technologies(vacancies: List[Vacancy]) -> Dict[str, int]:
    """Analyzes technologies from all vacancies and returns their frequency"""
    all_technologies = []
    for vacancy in vacancies:
        all_technologies.extend(vacancy.technologies)

    tech_counter = Counter(all_technologies)
    logging.info(f"Found {len(tech_counter)} unique technologies")
    return dict(tech_counter)


def create_technology_chart(tech_data: Dict[str, int], top_n: int = 15) -> None:
    """Creates chart of top technologies"""
    # Get top N technologies
    top_technologies = dict(
        sorted(tech_data.items(), key=lambda x: x[1], reverse=True)[:top_n]
    )

    if not top_technologies:
        logging.warning("No technologies data to display")
        return

    technologies = list(top_technologies.keys())
    counts = list(top_technologies.values())

    plt.figure(figsize=(12, 8))
    bars = plt.bar(technologies, counts, color="skyblue")
    plt.ylabel("Number of Vacancies")
    plt.xlabel("Technologies")
    plt.title(f"Top {top_n} Required Technologies for Python Vacancies")

    # Add values on bars
    for bar, count in zip(bars, counts):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            str(count),
            ha="center",
            va="bottom",
        )

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    chart_path = PROJECT_ROOT / "technologies_chart.png"
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.show()

    logging.info(f"Chart saved to {chart_path}")


def analyze_data_from_csv(csv_path: Path = None) -> None:
    """Main function for analyzing data from CSV"""
    if csv_path is None:
        csv_path = PROJECT_ROOT / "python_vacancies.csv"

    if not csv_path.exists():
        logging.error(f"CSV file not found: {csv_path}")
        return

    logging.info("Reading vacancies from CSV...")
    vacancies = read_vacancies_from_csv(csv_path)
    logging.info(f"Loaded {len(vacancies)} vacancies")

    # Analyze technologies
    tech_data = analyze_technologies(vacancies)

    # Create chart
    create_technology_chart(tech_data)
