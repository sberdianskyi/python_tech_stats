# Python Tech Stats 📊

A project for analyzing technology requirements in Python job vacancies on DOU.ua. Automatically collects job data, analyzes the most in-demand technologies, and creates visualization of results.

## 🎯 Project Description

Python Tech Stats is a tool for monitoring trends in Python development in the Ukrainian IT market. The project scrapes job vacancies from DOU.ua, extracts information about required technologies, and creates detailed statistics with visualization.

## ✨ Features

- 🔍 Automatic parsing of Python vacancies from DOU.ua
- 📊 Analysis of 100+ different technologies
- 📈 Creating charts with top-15 most demanded technologies
- 💾 Saving data in CSV format for further analysis
- 🚀 Asynchronous processing for fast data collection
- 📱 Headless browser mode support

## 🛠 Technologies

### Core Tools:
- **Python 3.12+** - main programming language
- **Selenium** - for web scraping
- **Matplotlib** - for chart creation
- **Asyncio** - for asynchronous processing
- **CSV** - for data storage

### Tracked Technology Categories:
- 🐍 **Python Frameworks**: Django, Flask, FastAPI, Tornado
- 📊 **Data Science**: Pandas, NumPy, TensorFlow, PyTorch
- 🗄️ **Databases**: PostgreSQL, MongoDB, Redis, Elasticsearch
- 🌐 **Web Technologies**: React, Vue, Angular, TypeScript
- ☁️ **DevOps**: Docker, Kubernetes, AWS, Azure, GCP
- 🧪 **Testing**: Pytest, Selenium, Unittest

## 📋 Requirements

- Python 3.12 or higher
- Chrome browser
- ChromeDriver (managed automatically via Selenium)

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/sberdianskyi/python_tech_stats.git
cd python_tech_stats
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Basic Run
```bash
python main.py
```

The program automatically:
1. Starts parsing vacancies from DOU.ua
2. Saves data to CSV file with timestamp
3. Analyzes technologies
4. Creates chart with top-15 technologies
5. Saves chart to PNG file

### Project Structure
```
python_tech_stats/
├── main.py                    # Main launcher file
├── README.md                  # Documentation
├── requirements.txt           # Dependencies
├── parser/
│   ├── parse.py              # Parsing logic
│   ├── parsing_item.py       # Vacancy data model
│   └── technologies.py       # List of tracked technologies
├── data_analysis/
│   └── data_analyzer.py      # Data analysis and chart creation
└── *.csv                     # Vacancy data files
└── *.png                     # Generated charts
```

## 📊 Example Results

### Top-15 Technologies Chart
![Technologies Chart](technologies_chart_20250730_131633.png)

*Chart shows the most demanded technologies in Python vacancies as of analysis date*

### CSV Data Example

Each vacancy is saved with the following fields:

| Field | Description | Example |
|-------|-------------|---------|
| title | Position name | "Senior Python Developer" |
| company | Company | "EPAM Systems" |
| technologies | Technology list | ['Python', 'Django', 'PostgreSQL'] |
| location | Location | "Київ, віддалено" |
| salary | Salary | "$3000–5000" or "Not specified" |
| link | Vacancy link | "https://jobs.dou.ua/..." |

## 🔧 Configuration

### Setting Up Technologies to Track

Edit the `parser/technologies.py` file to add new technologies:

```python
# Add new technologies to the appropriate category
PYTHON_TECHNOLOGIES = [
    "Python",
    "Django",
    "FastAPI",
    # Your new technology
]
```

### Parser Settings

In `parser/parse.py` file you can modify:
- Number of concurrent connections
- Delays between requests
- Target vacancy category

## 🔬 Advanced Features

### Analyzing Saved Data Only
```python
from data_analysis.data_analyzer import analyze_data_from_csv
from pathlib import Path

# Analyze specific file
csv_path = Path("python_vacancies_20250730_130917.csv")
analyze_data_from_csv(csv_path)
```

### Creating Custom Charts
```python
from data_analysis.data_analyzer import create_technology_chart

# Chart with top-20 technologies
tech_data = {...}  # Your data
create_technology_chart(tech_data, top_n=20)
```

## ⚠️ Important Notes

- The project is intended for educational purposes only
- Please respect robots.txt and DOU.ua terms of use
- Use reasonable delays between requests
- Don't run the parser too frequently to avoid server overload
