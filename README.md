# 🚀 AI CV Tailorer & RenderCV Generator

An advanced, production-ready **AI-powered CV Tailoring Pipeline** designed to automate the process of optimizing resumes for specific job descriptions. The application extracts content from an original PDF resume, leverages a Large Language Model (LLM) agent to dynamically realign experience and skills, and compiles a beautifully formatted, ATS-compliant PDF using a modern typesetting engine.

---

## 🏗️ System Architecture & Workflow

The application is engineered as an End-to-End (E2E) asynchronous pipeline where different components handle text processing, structured AI generation, data sanitization, and CLI-based document rendering:

[ Upload PDF ] ➡️ [ PyPDF Text Extraction ] ➡️ [ LLM Agent + Pydantic Validation ]
⬇️
[ Download PDF ] ⬅️ [ RenderCV (Typst Engine) ] ⬅️ [ PyYAML Sanitization & Dump ]


1. **Upload & Parse:** The user uploads their original CV (PDF) and pastes the target Job Description (JD) into the Streamlit UI. Text is extracted programmatically using `pypdf`.
2. **Semantic Realignment (AI Agent):** The raw text and JD are passed to a DeepSeek/OpenRouter LLM. Instead of returning raw conversational text, the agent is strictly constrained using **Pydantic Models** to enforce a structured JSON schema output, ensuring bullet points, summaries, and skills are perfectly tailored to the JD.
3. **Data Sanitization & Structuring:** The output is sanitized (handling dates, durations, and nesting) and dumped into a standardized `tailored_cv.yaml` file using `PyYAML`.
4. **CLI Rendering:** The application triggers a background system process via `subprocess` to invoke the **RenderCV** CLI compiler, which utilizes the ultra-fast **Typst** engine to render an ATS-optimized PDF resume.

---

## 🛠️ Tech Stack & Dependencies

* **Frontend / UI:** [Streamlit](https://streamlit.io/) - For building a clean, dynamic, and interactive user interface.
* **Text Extraction:** [PyPDF](https://pypi.org/project/pypdf/) - For parsing and extracting raw text from uploaded PDF resumes.
* **Orchestration & AI Agent:** [DeepSeek API](https://www.deepseek.com/) / OpenRouter - Powering the contextual reasoning and automated CV tailoring.
* **Data Validation:** [Pydantic](https://docs.pydantic.dev/) - Guarantees strict type safety and enforces structured JSON outputs from the LLM.
* **Serialization:** [PyYAML](https://pyyaml.org/) - Handles formatting, cleaning, and dumping data into the exact schema required by the rendering engine.
* **Typesetting & PDF Compilation:** [RenderCV](https://github.com/sinaatalay/rendercv) & [Typst](https://typst.app/) - The modern, blazing-fast alternative to LaTeX, generating professional, publication-quality resumes.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/rafahrafah1111/ai-cv-tailorer.git](https://github.com/rafahrafah1111/ai-cv-tailorer.git)
cd ai-cv-tailorer
2. Set Up a Virtual Environment & Install Dependencies
Bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. Run the Application
Bash
streamlit run app.py
⚙️ Configuration & Usage
Open the application in your browser (usually http://localhost:8501).

Input your DeepSeek/OpenRouter API Key in the sidebar.

Upload your original resume in PDF format.

Paste the targeted Job Description in the input text area.

Click Generate Tailored CV and download your ATS-ready resume instantly! 🎈


git push origin main
