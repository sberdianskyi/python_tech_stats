from dataclasses import dataclass


@dataclass
class Vacancy:
    title: str
    company: str
    technologies: list[str]
    location: str
    salary: str
    link: str
