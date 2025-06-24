import argparse
import re
# import yaml
import os
import io
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from datetime import datetime
import ipdb
import hydra
from omegaconf import DictConfig
import xarray as xr
import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
from datetime import datetime, timedelta
from utils.utils_download import *
import hydra
from omegaconf import DictConfig

def build_output_filename(cfg: DictConfig) -> str:
    """Generate output filename from pattern in config."""
    provider = cfg.dataset.lower()
    parameter = cfg.weather.parameter
    lat = cfg.location.lat
    lon = cfg.location.lon
    start = cfg.time_range.start_date
    end = cfg.time_range.end_date

    pattern = cfg.output.get("filename", "{provider}_{parameter}_{start}_{end}.csv")
    return pattern.format(
        provider=provider,
        parameter=parameter,
        lat=lat,
        lon=lon,
        start=start,
        end=end
    )
@hydra.main(config_path="conf", config_name="config", version_base="1.3")
def main(cfg: DictConfig):
    provider = cfg.dataset
    
    filename = build_output_filename(cfg)
    cfg.output.filename = filename

    print(f"📡 Fetching data for dataset: {provider.upper()}")
    print(f"📁 Output will be saved as: {filename}")

    if provider.lower() == "mswx":
        fetch_MSWX(cfg)
        extract_ts_MSWX(cfg)
    elif provider.lower() == "dwd_hyras":
        fetch_dwd(cfg)
        extract_ts_dwd(cfg)
    elif provider == "dwd": 
        fetch_dwd_loc(cfg)
    elif provider in ["gddp"]:
        fetch_ee_loc(cfg)
    elif provider == "era5-land":
        fetch_ee_loc_mod(cfg) 
    else:
        raise NotImplementedError(f"Provider '{provider}' is not yet supported in this script.")
    # print(f"Downloaded {len(downloaded)} new files for {var.name}")
if __name__ == '__main__':
    main()