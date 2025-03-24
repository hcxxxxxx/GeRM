# AI Hedge Fund

An AI-powered hedge fund project that utilizes multiple agents to make trading decisions. This project serves as a proof of concept to explore the application of artificial intelligence in financial trading. This project is intended for **educational** purposes only and is not designed for real trading or investment.

## Features

- **Multiple Trading Agents**: The system employs various agents, each specializing in different investment strategies:
  - **Ben Graham Agent**: Focuses on value investing with a margin of safety.
  - **Bill Ackman Agent**: An activist investor who takes bold positions.
  - **Cathie Wood Agent**: Advocates for growth investing and innovation.
  - **Charlie Munger Agent**: Invests in wonderful businesses at fair prices.
  - **Phil Fisher Agent**: Master of scuttlebutt analysis for growth investing.
  - **Stanley Druckenmiller Agent**: Targets asymmetric opportunities.
  - **Warren Buffett Agent**: Seeks excellent companies at fair valuations.
  - **Valuation Agent**: Calculates intrinsic value and generates trading signals.
  - **Sentiment Agent**: Analyzes market sentiment to inform trading decisions.
  - **Fundamentals Agent**: Evaluates fundamental data for trading signals.
  - **Technicals Agent**: Uses technical indicators to inform trading decisions.
  - **Risk Manager**: Assesses risk metrics and establishes position limits.
  - **Portfolio Manager**: Makes final trading decisions and generates orders.

![AI Hedge Fund](https://github.com/user-attachments/assets/cbae3dcf-b571-490d-b0ad-3f0f035ac0d4)

**Note**: The system simulates trading decisions and does not conduct actual trades.

[![Twitter Follow](https://img.shields.io/twitter/follow/virattt?style=social)](https://twitter.com/virattt)

## Disclaimer

This project is for **educational and research purposes only**. It is not intended for real trading or investment. No warranties or guarantees are provided, and past performance does not indicate future results. Creator assumes no liability for financial losses. Always consult a financial advisor for investment decisions.

By using this software, you agree to use it solely for learning purposes.

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
  - [Running the Hedge Fund](#running-the-hedge-fund)
  - [Running the Backtester](#running-the-backtester)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Feature Requests](#feature-requests)
- [License](#license)

## Setup

Clone the repository:

```bash
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund
```

1. Install Poetry (if not already installed):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:

```bash
poetry install
```

3. Set up your environment variables:

```bash
# Create .env file for your API keys
cp .env.example .env
```

4. Set your API keys:

```bash
# For running LLMs hosted by OpenAI (gpt-4o, etc.)
OPENAI_API_KEY=your-openai-api-key

# For running LLMs with Groq
GROQ_API_KEY=your-groq-api-key

# For financial data access
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key
```

**Important**: You must set `OPENAI_API_KEY`, `GROQ_API_KEY`, `ANTHROPIC_API_KEY`, or `DEEPSEEK_API_KEY` for the hedge fund to function. If you wish to use LLMs from all providers, set all API keys. 

Financial data for AAPL, GOOGL, MSFT, NVDA, and TSLA is free and does not require an API key.

## Usage

### Running the Hedge Fund

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

**Example Output**:
![Example Output](https://github.com/user-attachments/assets/e8ca04bf-9989-4a7d-a8b4-34e04666663b)

You can specify a `--show-reasoning` flag to print the reasoning of each agent to the console.

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --show-reasoning
```

You can also specify the start and end dates to make decisions for a specific time period.

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01
```

### Running the Backtester

```bash
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA
```

**Example Output**:
![Backtester Output](https://github.com/user-attachments/assets/00e794ea-8628-44e6-9a84-8f8a31ad3b47)

You can specify the start and end dates to backtest over a specific time period.

```bash
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01
```

## Project Structure

```
ai-hedge-fund/
├── src/
│   ├── agents/                   # Agent definitions and workflow
│   │   ├── bill_ackman.py        # Bill Ackman agent
│   │   ├── fundamentals.py       # Fundamental analysis agent
│   │   ├── portfolio_manager.py  # Portfolio management agent
│   │   ├── risk_manager.py       # Risk management agent
│   │   ├── sentiment.py          # Sentiment analysis agent
│   │   ├── technicals.py         # Technical analysis agent
│   │   ├── valuation.py          # Valuation analysis agent
│   │   ├── warren_buffett.py     # Warren Buffett agent
│   ├── tools/                    # Agent tools
│   │   ├── api.py                # API tools
│   ├── backtester.py             # Backtesting tools
│   ├── main.py                   # Main entry point
├── pyproject.toml
├── ...
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

**Important**: Please keep your pull requests small and focused for easier review and merging.

## Feature Requests

If you have a feature request, please open an [issue](https://github.com/virattt/ai-hedge-fund/issues) and ensure it is tagged with `enhancement`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.