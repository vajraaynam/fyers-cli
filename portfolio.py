import typer
from rich.console import Console
from rich.table import Table
from auth import get_fyers_instance

app = typer.Typer(help="Commands for Holdings and Positions")
console = Console()

@app.command("holdings")
def holdings():
    """Display user's portfolio holdings."""
    fyers = get_fyers_instance()
    response = fyers.holdings()
    
    if response.get("s") == "ok":
        data = response.get("holdings", [])
        if not data:
            console.print("[yellow]No holdings found.[/yellow]")
            return
            
        table = Table(title="Holdings")
        table.add_column("Symbol", style="cyan")
        table.add_column("Quantity", justify="right")
        table.add_column("Avg Price", justify="right")
        table.add_column("LTP", justify="right")
        table.add_column("P&L", justify="right")
        
        for item in data:
            pnl = item.get("pl", 0)
            pnl_style = "green" if pnl >= 0 else "red"
            
            table.add_row(
                item.get("symbol"),
                str(item.get("quantity")),
                str(item.get("costPrice")),
                str(item.get("ltp")),
                f"[{pnl_style}]{pnl:.2f}[/{pnl_style}]"
            )
            
        console.print(table)
    else:
        console.print(f"[bold red]Failed to fetch holdings:[/bold red] {response.get('message')}")

@app.command("positions")
def positions():
    """Display user's current positions."""
    fyers = get_fyers_instance()
    response = fyers.positions()
    
    if response.get("s") == "ok":
        data = response.get("netPositions", [])
        if not data:
            console.print("[yellow]No open positions found.[/yellow]")
            return
            
        table = Table(title="Net Positions")
        table.add_column("Symbol", style="cyan")
        table.add_column("Side", justify="center")
        table.add_column("Net Qty", justify="right")
        table.add_column("Avg Price", justify="right")
        table.add_column("LTP", justify="right")
        table.add_column("P&L", justify="right")
        
        for item in data:
            pnl = item.get("pl", 0)
            pnl_style = "green" if pnl >= 0 else "red"
            qty = item.get("netQty")
            side = "BUY" if qty > 0 else "SELL" if qty < 0 else "CLOSED"
            side_style = "green" if qty > 0 else "red" if qty < 0 else "yellow"
            
            table.add_row(
                item.get("symbol"),
                f"[{side_style}]{side}[/{side_style}]",
                str(qty),
                str(item.get("buyAvg") if qty > 0 else item.get("sellAvg")),
                str(item.get("ltp")),
                f"[{pnl_style}]{pnl:.2f}[/{pnl_style}]"
            )
            
        console.print(table)
    else:
        console.print(f"[bold red]Failed to fetch positions:[/bold red] {response.get('message')}")
