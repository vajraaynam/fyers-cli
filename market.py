import typer
from rich.console import Console
from rich.table import Table
from auth import get_fyers_instance

app = typer.Typer(help="Commands for Market Data (Quotes, Depth)")
console = Console()

@app.command("quote")
def quote(symbol: str = typer.Argument(..., help="Symbol (e.g., NSE:SBIN-EQ or NSE:NIFTY50-INDEX)")):
    """Get the latest quote for a symbol."""
    fyers = get_fyers_instance()
    data = {"symbols": symbol}
    response = fyers.quotes(data)
    
    if response.get("s") == "ok":
        quotes = response.get("d", [])
        if not quotes:
            console.print("[yellow]No data returned for symbol.[/yellow]")
            return
            
        quote_data = quotes[0].get("v", {})
        
        table = Table(title=f"Quote Info - {symbol}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", justify="right")
        
        table.add_row("LTP", str(quote_data.get("lp")))
        table.add_row("Change", str(quote_data.get("ch")))
        table.add_row("Change %", f"{quote_data.get('chp')}%")
        table.add_row("Open", str(quote_data.get("open_price")))
        table.add_row("High", str(quote_data.get("high_price")))
        table.add_row("Low", str(quote_data.get("low_price")))
        table.add_row("Prev Close", str(quote_data.get("prev_close_price")))
        table.add_row("Volume", str(quote_data.get("volume")))
        
        console.print(table)
    else:
        console.print(f"[bold red]Failed to fetch quote:[/bold red] {response.get('message')}")

@app.command("depth")
def depth(symbol: str = typer.Argument(..., help="Symbol (e.g., NSE:SBIN-EQ)")):
    """Get market depth (order book) for a symbol."""
    fyers = get_fyers_instance()
    data = {"symbol": symbol, "ohlcv_flag": "1"}
    response = fyers.depth(data)
    
    if response.get("s") == "ok":
        depth_data = response.get("d", {}).get(symbol, {})
        bids = depth_data.get("bids", [])
        asks = depth_data.get("ask", [])
        
        console.print(f"[bold cyan]Market Depth - {symbol}[/bold cyan]")
        
        table = Table()
        table.add_column("Bid Qty", justify="right", style="green")
        table.add_column("Bid Price", justify="right", style="green")
        table.add_column("Ask Price", justify="right", style="red")
        table.add_column("Ask Qty", justify="right", style="red")
        
        length = max(len(bids), len(asks))
        for i in range(length):
            bid = bids[i] if i < len(bids) else {}
            ask = asks[i] if i < len(asks) else {}
            
            table.add_row(
                str(bid.get("volume", "")),
                str(bid.get("price", "")),
                str(ask.get("price", "")),
                str(ask.get("volume", ""))
            )
            
        console.print(table)
    else:
        console.print(f"[bold red]Failed to fetch market depth:[/bold red] {response.get('message')}")
