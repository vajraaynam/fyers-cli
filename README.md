# FYERS CLI Trading Application

A powerful command-line interface (CLI) for the FYERS Securities API built with Python, [Typer](https://typer.tiangolo.com/), and [Rich](https://rich.readthedocs.io/).

This application provides continuous terminal-based access to your FYERS trading account. You can log in, view your market depth, fetch quotes, monitor your portfolio and positions, and place or cancel orders directly from the command line.

## Prerequisites

- Python 3.8+
- A FYERS trading account
- FYERS API access enabled (App ID, Secret Key, and Redirect URL). Create an app on the [FYERS API Dashboard](https://myapi.fyers.in/) if you don't have one.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd fyers-cli
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and configure your FYERS API credentials:
   ```env
   # Your FYERS API App ID (e.g. XXXX-100)
   FYERS_APP_ID="YOUR_APP_ID"

   # Your FYERS API Secret Key (e.g. YYYYZZZZ)
   FYERS_SECRET_KEY="YOUR_SECRET_KEY"

   # Your FYERS Redirect URL used in your App
   FYERS_REDIRECT_URL="https://127.0.0.1:8080/login"
   ```

## Usage

You can run the application through the main entry point:
```bash
python main.py
```

To see all available commands, run:
```bash
python main.py --help
```

### 1. Authentication

Before running any account or market commands, you must authenticate.

*   **Generate Login URL:**
    ```bash
    python main.py auth login
    ```
    This will print a URL. Open it in your browser and log in to FYERS. After successful login, you will be redirected to your `FYERS_REDIRECT_URL`. The URL will contain an `auth_code` parameter.

*   **Verify Auth Code:**
    Copy the `auth_code` from the redirect URL and verify it:
    ```bash
    python main.py auth verify <your_auth_code>
    ```
    *This securely saves your access token to `~/.fyers_access_token`.*

---

### 2. Account & Funds

*   **View Profile:**
    ```bash
    python main.py account profile
    ```
    Displays your User Profile including Client ID, Name, Email, and Mobile.

*   **View Funds:**
    ```bash
    python main.py account funds
    ```
    Displays available funds and margin limits.

---

### 3. Portfolio & Positions

*   **View Holdings:**
    ```bash
    python main.py portfolio holdings
    ```
    Displays a table of your current equity holdings, average price, LTP, and P&L.

*   **View Open Positions:**
    ```bash
    python main.py portfolio positions
    ```
    Shows today's net positions with quantity, average price, LTP, and real-time P&L.

---

### 4. Market Data

*   **Get Quote:**
    ```bash
    python main.py market quote "NSE:SBIN-EQ"
    ```
    Fetches the latest snapshot for the provided symbol (LTP, Open, High, Low, Prev Close, etc.).

*   **Get Market Depth (Order Book):**
    ```bash
    python main.py market depth "NSE:SBIN-EQ"
    ```
    Shows the bid/ask market depth for the specified symbol.

---

### 5. Orders

*   **View Order Book:**
    ```bash
    python main.py orders book
    ```
    Lists all orders (Pending, Filled, Cancelled, Rejected) for the day.

*   **Place an Order:**
    ```bash
    python main.py orders place "NSE:SBIN-EQ" --qty 1 --side BUY --type MARKET --producttype CNC
    ```
    Place a new market or limit order.
    *   `--side`: `BUY` or `SELL`
    *   `--type`: `MARKET` or `LIMIT`
    *   `--price`: Required if `--type` is `LIMIT`
    *   `--producttype`: `CNC` (Delivery), `INTRADAY` (MIS), `MARGIN`, `BO`, or `CO`

*   **Cancel an Order:**
    ```bash
    python main.py orders cancel <order_id>
    ```
    Cancels a pending order matching the specified ID.

## Architecture & Configuration

*   **`config.py`**: Manages environment variables and token storage. Uses `python-dotenv` to load `.env` variables and stores the final access token in `~/.fyers_access_token`.
*   **`auth.py`**: Handles API login flow via `fyers_apiv3`.
*   **`account.py`, `portfolio.py`, `market.py`, `orders.py`**: Separate Typer subcommands for logical modules.
*   **`main.py`**: The CLI entry point that binds all Typer commands together.

Logs for the FYERS API are generated in the project directory (`fyersApi.log`, `fyersRequests.log`).

## Technologies Used
*   [Typer](https://typer.tiangolo.com/): CLI application framework
*   [Rich](https://rich.readthedocs.io/): Terminal formatting and tables
*   [fyers-apiv3](https://myapi.fyers.in/docs): Official FYERS API SDK
*   python-dotenv: Environment variable management

## Disclaimer
This project is an unofficial tool. Use it at your own risk. The developers are not responsible for any financial losses or unexpected trades triggered by this application. Always review your orders carefully before placing them.
