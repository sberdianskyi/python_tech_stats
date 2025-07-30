"""
List of technologies to track in job listings.
This file contains categorized lists of technologies commonly mentioned in Python job listings.
"""

# Core Python technologies and frameworks
PYTHON_TECHNOLOGIES = [
    "Python",
    "Django",
    "Flask",
    "FastAPI",
    "Pyramid",
    "Tornado",
    "Bottle",
    "CherryPy",
    "aiohttp",
    "asyncio",
    "uvicorn",
    "gunicorn",
    "WSGI",
    "ASGI",
]

# Data processing and analysis
DATA_TECHNOLOGIES = [
    "Pandas",
    "NumPy",
    "SciPy",
    "Matplotlib",
    "Seaborn",
    "Plotly",
    "Jupyter",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Keras",
    "NLTK",
    "SpaCy",
    "Dask",
    "PySpark",
    "Apache Spark",
    "Hadoop",
]

# Database technologies
DATABASE_TECHNOLOGIES = [
    "SQL",
    "PostgreSQL",
    "MySQL",
    "SQLite",
    "MongoDB",
    "Redis",
    "Elasticsearch",
    "Cassandra",
    "DynamoDB",
    "SQLAlchemy",
    "Alembic",
    "Django ORM",
    "Prisma",
]

# Web technologies
WEB_TECHNOLOGIES = [
    "HTML",
    "CSS",
    "JavaScript",
    "TypeScript",
    "React",
    "Vue",
    "Angular",
    "jQuery",
    "Bootstrap",
    "Tailwind",
    "REST",
    "RESTful",
    "GraphQL",
    "API",
]

# DevOps and infrastructure
DEVOPS_TECHNOLOGIES = [
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "Terraform",
    "Ansible",
    "Jenkins",
    "CI/CD",
    "Git",
    "GitHub",
    "GitLab",
    "Bitbucket",
    "Linux",
    "Nginx",
    "Apache",
]

# Testing frameworks
TESTING_TECHNOLOGIES = [
    "Pytest",
    "Unittest",
    "Selenium",
    "Cypress",
    "Playwright",
    "Behave",
    "Robot Framework",
    "Mock",
    "TDD",
]

# Messaging and async systems
MESSAGING_TECHNOLOGIES = [
    "RabbitMQ",
    "Kafka",
    "Celery",
    "Redis Queue",
    "ZeroMQ",
    "gRPC",
    "WebSockets",
]

# All technologies combined
ALL_TECHNOLOGIES = (
    PYTHON_TECHNOLOGIES
    + DATA_TECHNOLOGIES
    + DATABASE_TECHNOLOGIES
    + WEB_TECHNOLOGIES
    + DEVOPS_TECHNOLOGIES
    + TESTING_TECHNOLOGIES
    + MESSAGING_TECHNOLOGIES
)

# Technology categories for visualization grouping
TECHNOLOGY_CATEGORIES = {
    "Python": PYTHON_TECHNOLOGIES,
    "Data": DATA_TECHNOLOGIES,
    "Database": DATABASE_TECHNOLOGIES,
    "Web": WEB_TECHNOLOGIES,
    "DevOps": DEVOPS_TECHNOLOGIES,
    "Testing": TESTING_TECHNOLOGIES,
    "Messaging": MESSAGING_TECHNOLOGIES,
}
