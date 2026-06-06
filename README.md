# AI CV Tailorer CLI Tool

An automated AI-powered command-line tool designed to dynamically tailor a candidate's CV to match a specific target Job Description. Built with Python, using **Instructor** and **DeepSeek via OpenRouter** for structured data extraction and LLM-driven profile customization.

## 🚀 Features
- **Automated Parsing:** Converts standard PDF CVs into structured JSON profiles using LLMs.
- **Dynamic Contextual Tailoring:** Adapts the Professional Summary and Technical Skills sections dynamically to emphasize alignment with the target Job Description (JD) without changing factual history.
- **Cache-Busting PDF Generation:** Renders a newly tailored, production-ready PDF for every target role with automated local system preview.
- **Factual Integrity Guardrails:** Strict prompt engineering ensures zero hallucination regarding job titles, dates, or degrees.

## 🏗️ Project Structure
- `main.py`: The orchestrator and CLI interface that manages the input, pipelines, and execution flow.
- `parser_agent.py`: Handles the extraction and structuring of the original PDF resume.
- `tailor_agent.py`: Outlines the prompt logic and leverages OpenRouter/DeepSeek for structured rewriting.
- `models.py`: Defines strict Pydantic data schemas for data validation via the Instructor framework.
- `pdf_generator.py`: Generates the finalized, clean PDF output.

## 🛠️ Tech Stack
- **Language:** Python 3.12
- **LLM Integration:** Instructor, OpenAI SDK, OpenRouter (DeepSeek-Chat)
- **Data Validation:** Pydantic
- **Environment Management:** Python venv

## 💻 Getting Started

### Prerequisites
Make sure you have Python 3.10+ installed on your system.

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/rafahrafah1111/ai-cv-tailorer.git](https://github.com/rafahrafah1111/ai-cv-tailorer.git)
   cd ai-cv-tailorer