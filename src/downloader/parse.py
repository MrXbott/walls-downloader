import typer
from bs4 import BeautifulSoup


def prepare_soup_from_html(html: str) -> BeautifulSoup:
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_wallpapers_links(soup: BeautifulSoup, resolution: str) -> list[str]:
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'wallpaper' in href and (not resolution or resolution in href):
            links.append(href)
            typer.echo(f'Wall url found: {href}')
    return links