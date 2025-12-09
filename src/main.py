import asyncio
import typer
from pathlib import Path

from downloader.validate import validate_month, validate_year, validate_resolution
from downloader.download import download_wallpapers_for_month, download_wallpapers_for_year


app = typer.Typer()

@app.command()
def download(year: int = typer.Option(None, help='The year for which you need to download wallpapers.'), 
             month: int = typer.Option(None, help='The month for which to download wallpapers. If a month is not specified, wallpapers for the entire year will be downloaded.'), 
             resolution: str = typer.Option('1920x1080', help='The resolution for wallpapers. Example: 1920x1080'),
             save_to: Path = typer.Option('./wallpapers', 
                                          '--save-to', 
                                          help='Path to directory where images will be saved.',
                                          exists=False,
                                          file_okay=False,
                                          dir_okay=True,
                                          writable=True
                                          )
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
        asyncio.run(download_wallpapers_for_month(year, month, resolution, save_to))
    else:
        asyncio.run(download_wallpapers_for_year(year, resolution, save_to))

if __name__ == '__main__':
    app()

