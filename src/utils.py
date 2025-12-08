import re
import typer
from datetime import datetime


def validate_year(year: int):
    current_year = datetime.now().year
    if year < 2010 or year > current_year:
        typer.echo(f'Error: year must be between 2010 and {current_year}')
        raise typer.Exit(code=1)
    
def validate_month(month: int):
    if month < 1 or month > 12:
        typer.echo('Error: month must be between 1 and 12')
        raise typer.Exit(code=1)

def validate_resolution(resolution: str) -> str:
    RESOLUTION_PATTERN = re.compile(r'^\d{3,4}x\d{3,4}$') 
    if resolution:
        reso_clean = resolution.replace(' ', '')
        if not RESOLUTION_PATTERN.match(reso_clean):
            typer.echo('Error: resolution must be WIDTHxHEIGHT, example 1920x1080')
            raise typer.Exit(code=1)
        return reso_clean
    return None