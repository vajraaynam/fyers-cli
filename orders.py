import typer
from rich.console import Console
from rich.table import Table
from auth import get_fyers_instance

app = typer.Typer(help="Commands for placing and managing orders")
console = Console()

@app.command("book")
def book():
    """Display today's order book."""
    fyers = get_fyers_instance()
    response = fyers.orderbook()
    
    if response.get("s") == "ok":
        orders = response.get("orderBook", [])
        if not orders:
            console.print("[yellow]No orders found for today.[/yellow]")
            return
            
        table = Table(title="Order Book")
        table.add_column("ID", style="dim")
        table.add_column("Symbol", style="cyan")
        table.add_column("Side", justify="center")
        table.add_column("Qty", justify="right")
        table.add_column("Type", justify="center")
        table.add_column("Price", justify="right")
        table.add_column("Status", justify="center")
        
        for order in orders:
            side = "BUY" if order.get("side") == 1 else "SELL"
            side_style = "green" if side == "BUY" else "red"
            
            # 1=>Limit, 2=>Market, 3=>Stop(Loss), 4=>StopLimit
            order_type = order.get("type", 0)
            order_type_str = {1: "LIMIT", 2: "MARKET", 3: "STOP", 4: "STOP-LIMIT"}.get(order_type, "UNKNOWN")
            
            status = order.get("status", 0)
            status_str = {
                1: "Canceled", 2: "Traded/Filled", 3: "For future use",
                4: "Transit", 5: "Rejected", 6: "Pending"
            }.get(status, "UNKNOWN")
            
            status_style = "green" if status == 2 else "red" if status in [1, 5] else "yellow"
            
            table.add_row(
                order.get("id", "")[-6:], # Last 6 chars of ID for brevity
                order.get("symbol"),
                f"[{side_style}]{side}[/{side_style}]",
                str(order.get("qty")),
                order_type_str,
                str(order.get("limitPrice") if order_type in [1, 4] else "MKT"),
                f"[{status_style}]{status_str}[/{status_style}]"
            )
            
        console.print(table)
    else:
        console.print(f"[bold red]Failed to fetch orderbook:[/bold red] {response.get('message')}")

@app.command("place")
def place(
    symbol: str = typer.Argument(..., help="Symbol (e.g. NSE:SBIN-EQ)"),
    qty: int = typer.Option(..., help="Quantity to buy/sell"),
    side: str = typer.Option(..., help="BUY or SELL"),
    type: str = typer.Option("MARKET", help="Order type: MARKET or LIMIT"),
    price: float = typer.Option(0.0, help="Limit price (required if type=LIMIT)"),
    productType: str = typer.Option("CNC", help="Product type: CNC, INTRADAY, MARGIN, BO, CO")
):
    """Place a new order."""
    fyers = get_fyers_instance()
    
    side_val = 1 if side.upper() == "BUY" else -1 if side.upper() == "SELL" else 0
    if side_val == 0:
        console.print("[bold red]Invalid side. Use BUY or SELL.[/bold red]")
        raise typer.Exit(1)
        
    type_val = 2 if type.upper() == "MARKET" else 1 if type.upper() == "LIMIT" else 0
    if type_val == 0:
        console.print("[bold red]Invalid type. Use MARKET or LIMIT.[/bold red]")
        raise typer.Exit(1)
        
    if type_val == 1 and price <= 0:
        console.print("[bold red]Limit price must be > 0 for LIMIT orders.[/bold red]")
        raise typer.Exit(1)
        
    data = {
        "symbol": symbol,
        "qty": qty,
        "type": type_val,
        "side": side_val,
        "productType": productType,
        "limitPrice": price,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
    }
    
    response = fyers.place_order(data)
    
    if response.get("s") == "ok":
        console.print(f"[bold green]Order placed successfully![/bold green] Order ID: {response.get('id')}")
    else:
        console.print(f"[bold red]Failed to place order:[/bold red] {response.get('message')}")

@app.command("cancel")
def cancel(order_id: str = typer.Argument(..., help="The Order ID to cancel")):
    """Cancel a pending order."""
    fyers = get_fyers_instance()
    data = {"id": order_id}
    
    response = fyers.cancel_order(data)
    
    if response.get("s") == "ok":
        console.print(f"[bold green]Order cancelled successfully![/bold green]")
    else:
        console.print(f"[bold red]Failed to cancel order:[/bold red] {response.get('message')}")
