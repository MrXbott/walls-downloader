import os
import asyncio
import httpx
import typer
from bs4 import BeautifulSoup
from enum import Enum
import aiofiles
from pathlib import Path

class Month(Enum):
    january = 1
    february = 2
    march = 3
    april = 4
    may = 5
    june = 6
    july = 7
    august = 8
    september = 9
    october = 10
    november = 11
    december = 12


def make_url(year: int, month:int) -> str:
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

async def download_image(client: httpx.AsyncClient, url: str, save_path: str):
    try:
        typer.echo(f'Start downloading: {url}')
        resp = await client.get(url)
        resp.raise_for_status()
        typer.echo(f'Downloaded: {url}')
        
        # ----- optional -----
        #       uncomment this code if you want to save both files
        #       when a file with the same name already exists
        
        # base, ext = os.path.splitext(save_path)
        # counter = 1
        # while os.path.exists(save_path):
        #     save_path = f'{base}_{counter}{ext}'
        #     counter += 1

        # ----- optional end ----

        async with aiofiles.open(save_path, 'wb') as f:
            await f.write(resp.content)
            typer.echo(f'Saved: {save_path}')
    except httpx.HTTPStatusError as e:
        typer.echo(f'Error {e.response.status_code} while downloading {url}', err=True)
    except Exception as e:
        typer.echo(f'Some error while downloading {url} - {str(e)}', err=True)
        

async def download_wallpapers_for_month(year: int, month: int, resolution: str , save_to: Path):
    url = make_url(year, month)

    html = await fetch_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    # find links for wallpapers with selected resolution
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'wallpaper' in href and (not resolution or resolution in href):
            links.append(href)
            typer.echo(f'Wall url found: {href}')

    # make dir based on month
    month_dir = os.path.join(save_to, str(year), f'{month:02d}')
    os.makedirs(month_dir, exist_ok=True)

    async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
        tasks = [download_image(client, link, os.path.join(month_dir, os.path.basename(link))) for link in links]
        await asyncio.gather(*tasks)

async def download_wallpapers_for_year(year: int, resolution: str, save_to: Path):
    for month in range(1, 13):
        try:
            await download_wallpapers_for_month(year, month, resolution, save_to)
        except typer.Exit:
            typer.echo(f'Error: page not found for {month}/{year} ', err=True)
