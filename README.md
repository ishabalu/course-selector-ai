# IU Course Chat Assistant 🎓

An AI-powered chat assistant for Indiana University students to get instant answers about courses, prerequisites, and eligibility rules.

## Features

- 💬 Interactive chat interface for course-related queries
- 📚 Access to course information and prerequisites
- 🎯 Personalized course recommendations
- 🔍 Quick answers to eligibility questions
- 🎨 IU-themed interface

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd course-selector-ai
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up your secrets:
   - Create a `.streamlit` folder in the project root
   - Create a `secrets.toml` file inside the `.streamlit` folder
   - Add your API keys and other secrets to the file

## Running the Application

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Usage

1. Type your questions in the chat input box
2. Example questions:
   - "Can I take CSCI-A 110 as a grad student?"
   - "What are the prerequisites for INFO-I 101?"
   - "Show me all courses in the Computer Science department"

## Project Structure

```
course-selector-ai/
├── app.py              # Main Streamlit application
├── chat_engine.py      # Chat processing logic
├── data_handler.py     # Data loading and processing
├── data/               # Data files
│   ├── courses.csv
│   └── CourseHistory.csv
├── .streamlit/         # Streamlit configuration
│   └── secrets.toml    # API keys and secrets
└── requirements.txt    # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a Pull Request



## Contact

Isha Saikumar (isaikuma@iu.edu)
Nitin Chowdary K (nkoduru@iu.edu)