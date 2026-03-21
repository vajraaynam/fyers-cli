import typer
import auth
import account
import portfolio
import market
import orders

app = typer.Typer(
    help="FYERS CLI Trading Application",
    no_args_is_help=True
)

# Add subcommands
app.add_typer(auth.app, name="auth")
app.add_typer(account.app, name="account")
app.add_typer(portfolio.app, name="portfolio")
app.add_typer(market.app, name="market")
app.add_typer(orders.app, name="orders")

if __name__ == "__main__":
    app()
