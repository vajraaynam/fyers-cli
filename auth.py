import typer
from rich.console import Console
from fyers_apiv3 import fyersModel
import config

app = typer.Typer(help="Authentication commands for FYERS API")
console = Console()

@app.command("login")
def login():
    """Generate the FYERS login URL to authorize the app."""
    config.load_config()
    app_id = config.get_app_id()
    secret_key = config.get_secret_key()
    redirect_url = config.get_redirect_url()

    if not all([app_id, secret_key, redirect_url]):
        console.print("[bold red]Error:[/bold red] Missing `FYERS_APP_ID`, `FYERS_SECRET_KEY`, or `FYERS_REDIRECT_URL` in .env")
        raise typer.Exit(1)

    client_id = app_id if app_id.endswith("-100") else f"{app_id}-100"
    
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_url,
        response_type="code",
        grant_type="authorization_code"
    )

    auth_link = session.generate_authcode()
    console.print()
    console.print(f"[bold green]Please visit the following URL to log in to FYERS:[/bold green]")
    console.print()
    console.print(f"[cyan]{auth_link}[/cyan]")
    console.print()
    console.print("After logging in, you will be redirected to your redirect_url.")
    console.print("Copy the `auth_code` from the URL parameters and use `fyers auth verify <code>`")

@app.command("verify")
def verify(auth_code: str = typer.Argument(..., help="The auth_code from the redirect URL")):
    """Verify the auth code and generate the access token."""
    config.load_config()
    app_id = config.get_app_id()
    client_id = app_id if app_id.endswith("-100") else f"{app_id}-100"
    
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=config.get_secret_key(),
        redirect_uri=config.get_redirect_url(),
        response_type="code",
        grant_type="authorization_code"
    )

    session.set_token(auth_code)
    try:
        response = session.generate_token()
        if response.get("s") == "ok":
            access_token = response.get("access_token")
            config.save_access_token(access_token)
            console.print("[bold green]Successfully authenticated! Access token saved.[/bold green]")
        else:
            console.print(f"[bold red]Authentication failed:[/bold red] {response.get('message', response)}")
            raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Exception during verification:[/bold red] {str(e)}")
        raise typer.Exit(1)

def get_fyers_instance():
    """Helper function to get a configured fyersModel instance."""
    config.load_config()
    access_token = config.get_access_token()
    if not access_token:
        console.print("[bold red]Access token not found. Please log in first using `fyers auth login`.[/bold red]")
        raise typer.Exit(1)
        
    app_id = config.get_app_id()
    client_id = app_id if app_id.endswith("-100") else f"{app_id}-100"
    fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
    return fyers
