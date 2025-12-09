import os
import asyncio
import httpx
import typer
import aiofiles
from pathlib import Path

from downloader.html import make_month_url, fetch_html
from downloader.parse import prepare_soup_from_html, extract_wallpapers_links
from downloader.filesystem import make_month_dir


async def download_image(client: httpx.AsyncClient, url: str, save_path: str):
    try:
        typer.echo(f'Start downloading: {url}')
        resp = await client.get(url)
        resp.raise_for_status()
        typer.echo(f'Downloaded: {url}')

        async with aiofiles.open(save_path, 'wb') as f:
            await f.write(resp.content)
            typer.echo(f'Saved: {save_path}')
    except httpx.HTTPStatusError as e:
        typer.echo(f'Error {e.response.status_code} while downloading {url}', err=True)
    except Exception as e:
        typer.echo(f'Some error while downloading {url} - {str(e)}', err=True)
        

async def download_wallpapers_for_month(year: int, month: int, resolution: str , save_to: Path):
    url = make_month_url(year, month)
    html = await fetch_html(url)
    soup = prepare_soup_from_html(html)
    links = extract_wallpapers_links(soup, resolution)
    
    if not links:
        typer.echo(f'No wallpapers found for {month:02d}.{year} with resolution "{resolution}".', err=True)
        return 

    month_dir_path = make_month_dir(save_to, year, month)

    async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
        tasks = [download_image(client, link, os.path.join(month_dir_path, os.path.basename(link))) for link in links]
        await asyncio.gather(*tasks)


async def download_wallpapers_for_year(year: int, resolution: str, save_to: Path):
    for month in range(1, 13):
        try:
            await download_wallpapers_for_month(year, month, resolution, save_to)
        except typer.Exit:
            typer.echo(f'Error: page not found for {month}/{year} ', err=True)
