# 🤖 GitHub AI Assistant with RAG and LangChain 💀
This repository contains a GitHub AI assistant implemented in Python, leveraging Retrieval-Augmented Generation (RAG) and LangChain. This agent is designed to help users interact with GitHub repositories by retrieving and summarizing information such as issues, pull requests, and more.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Example](#example)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

## Features
- **GitHub Repository Interaction:** Select a GitHub repository and retrieve information such as open issues, pull requests, or file contents.
- **Issue Summarization:** Summarizes issues for better understanding and quicker decision-making.
- **Retrieval-Augmented Generation (RAG):** Combines information retrieval with generative AI for precise and context-aware responses.
- **LangChain and Hugging Face Integration:** Uses LangChain for efficient chaining of multiple language model queries and Hugging Face models for generative responses.
- **Poetry Dependency Management:** Simplifies dependency management and project setup.

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- Python 3.8 or higher
- Poetry (for dependency management)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sakhileln/GitHub-Agent.git
   cd GitHub-Agent/
   ```
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Usage
1. Ensure you have access to the GitHub repository you wish to analyze and have a GitHub personal access token (PAT) with appropriate permissions.

2. Configure your environment by adding the GitHub token:
   ```bash
   export GITHUB_TOKEN=your_personal_access_token
   ```

3. Run the AI assistant:
   ```bash
   python main.py
   ```

4. Select a repository and interact with the AI agent to retrieve and summarize data.

Example commands:
- "Summarize the open issues in this repository."
- "List the pull requests and their statuses."

## Project Structure

- `main.py`: The entry point of the application.
- `retriever.py`: Handles interactions with the GitHub API and retrieves repository data.
- `summarizer.py`: Uses LangChain and Hugging Face models to generate summaries from retrieved data.
- `pyproject.toml`: Poetry configuration file for dependencies.
- `README.md`: Documentation for the project.

## Example
To get a quick sense of how it works, try the following after running the script:
1. Select a GitHub repository.
2. Ask the assistant to summarize open issues.

Example Query:
```plaintext
Summarize the open issues in this repository.
```

Example Response:
```plaintext
There are 5 open issues:
1. Bug in the login flow causing 500 errors (critical).
2. Feature request: Add dark mode support.
...
```
## Contributing
Contributions are welcome! If you'd like to contribute. See the [CONTRIBUTING](CONTRIBUTING.md) file for details.
1. Fork the repository.
2. Create a new branch for your feature/bug fix:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Make your changes and test thoroughly.
4. Submit a pull request explaining your changes.

## License
This project is licensed under the GPL v3.0 License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [LangChain](https://www.langchain.com/): For providing robust tools to handle language model operations.
- [Hugging Face](https://huggingface.co/): For providing versatile and high-quality machine learning models.
- GitHub: For offering a robust platform for collaboration and version control.

## Contact
- Sakhile III  
- [LinkedIn Profile](https://www.linkedin.com/in/sakhile-ndlazi)
- [GitHub Profile](https://github.com/sakhileln)
