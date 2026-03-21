import typer
from rich.console import Console
from rich.table import Table
from auth import get_fyers_instance

app = typer.Typer(help="Commands for account profile and funds")
console = Console()

@app.command("profile")
def profile():
    """Display user profile details."""
    fyers = get_fyers_instance()
    response = fyers.get_profile()
    
    if response.get("s") == "ok":
        data = response.get("data", {})
        console.print("[bold cyan]User Profile[/bold cyan]")
        console.print(f"Name: [bold]{data.get('name')}[/bold]")
        console.print(f"Client ID: {data.get('fy_id')}")
        console.print(f"Email: {data.get('email_id')}")
        console.print(f"Mobile: {data.get('mobile_number')}")
    else:
        console.print(f"[bold red]Failed to get profile:[/bold red] {response.get('message')}")

@app.command("funds")
def funds():
    """Display available funds and margins."""
    fyers = get_fyers_instance()
    response = fyers.funds()
    
    if response.get("s") == "ok":
        fund_limit = response.get("fund_limit", [])
        
        table = Table(title="Account Funds")
        table.add_column("Category", style="cyan")
        table.add_column("Value", style="magenta", justify="right")
        
        for item in fund_limit:
            table.add_row(item.get("title"), str(item.get("equityAmount")))
            
        console.print(table)
    else:
        console.print(f"[bold red]Failed to fetch funds:[/bold red] {response.get('message')}")
