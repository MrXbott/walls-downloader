import httpx
import typer

from downloader.enum import Month


def make_month_url(year: int, month:int) -> str:
    month_name = Month(month).name 
    if month == 1:
        return f'https://www.smashingmagazine.com/{year-1}/{12}/desktop-wallpaper-calendars-{month_name}-{year}/'
    else:
        return f'https://www.smashingmagazine.com/{year}/{month-1:02d}/desktop-wallpaper-calendars-{month_name}-{year}/'


async def fetch_html(url: str) -> str:
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            typer.echo(f'Month url: {url}')
            return resp.text
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                typer.echo(f'Url not found: {url} \nCheck selected month/year', err=True)
                raise typer.Exit(code=1)
            else:
                raise  

