import asyncio
import typer

from utils import validate_month, validate_year, validate_resolution
from downloader import download_wallpapers_for_month, download_wallpapers_for_year


app = typer.Typer()

@app.command()
def download(year: int = typer.Option(None, help='The year for which you need to download wallpapers.'), 
             month: int = typer.Option(None, help='The month for which to download wallpapers. If a month is not specified, wallpapers for the entire year will be downloaded.'), 
             resolution: str = typer.Option(None, help='The resolution for wallpapers. Example: 1920x1080')
             ):
    
    if not year:
        typer.echo('Error: You must specify the year with --year')
        raise typer.Exit(code=1)
    
    validate_year(year)

    if month is not None:
        validate_month(month)

    if resolution is not None:
        resolution = validate_resolution(resolution)
    
    if month:
        asyncio.run(download_wallpapers_for_month(year, month, resolution))
    else:
        asyncio.run(download_wallpapers_for_year(year, resolution))

if __name__ == '__main__':
    app()

