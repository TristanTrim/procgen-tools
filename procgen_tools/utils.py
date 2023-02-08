# %%

import sys
import os
from pathlib import Path
import requests
import gzip
import tarfile
from tqdm import tqdm

def _extract_tgz(path):
    "Extracts a .tar.gz or .tgz file."
    assert path.endswith('.tgz') or url.endswith('.tar.gz')
    with tarfile.open(path, 'r:gz') as tar:
        members = tar.getmembers()
        t = tqdm(members)
        t.set_description(f'Extracting {path}')
        for member in t:
            tar.extract(member)


def _fetch(url, filepath: str = None, force: bool = False):
    "Fetches a file from a URL and extracts it."
    filepath = filepath or url.split('/')[-1]
    if not force and Path(filepath).exists():
        print(f'Already downloaded {url}')
        return

    # create dir for filepath if not exists
    if not Path(filepath).parent.exists():
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    # download file
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024
        t = tqdm(total=total_size, unit='iB', unit_scale=True)
        t.set_description(f'Downloading {url}')
        with open(filepath, 'wb') as f:
            for data in r.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()
        if total_size != 0 and t.n != total_size:
            raise ValueError(f'Error: downloaded {t.n} bytes, expected {total_size} bytes.')
        
    # extract file (if needed)
    if filepath.endswith('.tgz') or filepath.endswith('.tar.gz'):
        _extract_tgz(filepath)
        

# %%

def setup_dir():
    """
    Get into the procgen-tools directory, create it if it doesn't exist.
    """
    if Path.cwd().name in ('experiments', 'playground'):
        os.chdir('..')

    if Path.cwd().name != 'procgen-tools':
        Path('procgen-tools').mkdir(parents=True, exist_ok=True)
        os.chdir('procgen-tools')


def setup():
    """
    cd into the procgen-tools directory then download and extract data files.
    """
    setup_dir()
    assert Path.cwd().name == 'procgen-tools', 'must be in procgen-tools'

    _fetch('https://nerdsniper.net/mats/episode_data.tgz')
    _fetch('https://nerdsniper.net/mats/data.tgz')
    _fetch('https://nerdsniper.net/mats/model_rand_region_5.pth', 'trained_models/maze_I/model_rand_region_5.pth')


def _device(policy):
    return next(policy.parameters()).device
    

# %%
