import os
from pathlib import Path

def make_month_dir(save_to: Path, year: int, month: int) -> str:
    month_dir = os.path.join(save_to, str(year), f'{month:02d}')
    os.makedirs(month_dir, exist_ok=True)
    return month_dir