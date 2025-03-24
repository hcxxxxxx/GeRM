# AI Hedge Fund

An AI-powered hedge fund that utilizes multiple agents to make informed trading decisions based on various investment principles.

## Features

- **Multi-Agent System**: Implements various investment strategies based on renowned investors' principles.
- **Backtesting Framework**: Simulates and evaluates trading strategies to assess performance.
- **Data Analysis**: Analyzes financial metrics, market conditions, and sentiment to guide trading decisions.
- **User-Friendly Interface**: Allows users to input stock tickers and relevant dates for analysis.
- **Visualization Tools**: Provides visual representations of data for better understanding.

## Installation

To install the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/repo.git
   cd repo
   ```

2. Install Poetry if you haven't already:
   ```bash
   pip install poetry
   ```

3. Install the dependencies:
   ```bash
   poetry install
   ```

4. Create a `.env` file based on the `.env.example` provided and set your environment variables.

## Usage

To run the main application, execute:
```bash
poetry run python src/main.py
```

### Example Commands
- Input stock tickers (e.g., "AAPL", "GOOGL") and specify the analysis dates to receive trading signals.
- You can toggle options like showing reasoning behind decisions or displaying agent graphs.

## Architecture

This project is structured into several key components:

- **src/**: Contains the source code for the hedge fund system.
  - **agents/**: Implements various investment signal generators based on different investors' strategies (e.g., Charlie Munger, Stanley Druckenmiller).
  - **data/**: Manages data retrieval and caching mechanisms.
  - **graph/**: Handles state management for agent decision processes.
  - **llm/**: Interfaces with language models for decision-making assistance.
  - **utils/**: Contains utility functions and helpers for various tasks.
  - **main.py**: Entry point for the application, orchestrating the overall workflow.
  
## Technology Stack

- **Programming Language**: Python
- **Dependencies**:
  - `langchain`
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `python-dotenv`
  - `questionary`

## Contribution

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

For any questions or suggestions, feel free to open an issue on the repository.