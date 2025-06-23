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

# Google Drive functions
def fetch_MSWX(var_cfg: DictConfig):
    param_mapping = var_cfg.mappings
    provider = var_cfg.dataset.lower()
    parameter_key = var_cfg.weather.parameter
    # Validate provider and parameter
    # ipdb.set_trace()
    param_info = param_mapping[provider]['variables'][parameter_key]
    folder_id = param_info["folder_id"]
    
    start_date = var_cfg.time_range.start_date
    end_date = var_cfg.time_range.end_date

    # Parse dates & extract unique years
    start_year = datetime.fromisoformat(start_date).year
    end_year = datetime.fromisoformat(end_date).year
    years = list(range(start_year, end_year + 1))

    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    creds = service_account.Credentials.from_service_account_file(
        param_mapping[provider].params.google_service_account, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)

    """Download all files from the folder if not already present"""
    files = []
    page_token = None

    while True:
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="files(id, name), nextPageToken",
            pageToken=page_token
        ).execute()
        files.extend(results.get("files", []))
        page_token = results.get("nextPageToken", None)
        if not page_token:
            break
    files_to_download = [
    f for f in files
    if f['name'][:4].isdigit() and int(f['name'][:4]) in years
    ]
    
    output_dir = './'
    os.makedirs(output_dir, exist_ok=True)
    downloaded_files = []
    # ipdb.set_trace()
    for file in files_to_download:
        filename = f"{file['name']}"
        filepath = os.path.join(output_dir,parameter_key, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if os.path.exists(filepath):
            print(f"Skipping {filename} (already exists)")
            continue

        print(f"Downloading {filename}...")
        request = service.files().get_media(fileId=file["id"])
        fh = io.FileIO(filepath, 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}% complete")

        downloaded_files.append(filename)

    return downloaded_files

def fetch_dwd(var_cfg):
    """Download HYRAS data for one variable and a list of years."""
    param_mapping = var_cfg.mappings
    provider = var_cfg.dataset.lower()
    parameter_key = var_cfg.weather.parameter
    # Validate provider and parameter
    # ipdb.set_trace()
    param_info = param_mapping[provider]['variables'][parameter_key]
    base_url = param_info["base_url"]
    prefix = param_info["prefix"]
    version = param_info["version"]

    start_date = var_cfg.time_range.start_date
    end_date = var_cfg.time_range.end_date

    # Parse dates & extract unique years
    start_year = datetime.fromisoformat(start_date).year
    end_year = datetime.fromisoformat(end_date).year
    years = list(range(start_year, end_year + 1))

    # output_file = cfg.output.filename
    os.makedirs(parameter_key, exist_ok=True)

    for year in years:
        file_name = f"{prefix}_{year}_{version}_de.nc"
        file_url = f"{base_url}{file_name}"
        local_path = os.path.join(parameter_key, file_name)

        print(f"⬇️  Checking: {file_url}")

        # Check if file exists on server first (HEAD request)
        head = requests.head(file_url)
        if head.status_code != 200:
            raise FileNotFoundError(f"❌ Not found on server: {file_url} (HTTP {head.status_code})")

        if os.path.exists(local_path):
            print(f"✔️  Exists locally: {local_path}")
            continue

        print(f"⬇️  Downloading: {file_url}")
        try:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ Saved: {local_path}")
        except requests.HTTPError as e:
            raise RuntimeError(f"❌ Failed download: {file_url} — {e}")

@hydra.main(config_path="conf", config_name="config", version_base="1.3")
def main(cfg: DictConfig):
    provider = cfg.dataset
    # print(f"\nProcessing variable: {var.name}")
    if provider.lower() == "mswx":
        fetch_MSWX(cfg)
    elif provider.lower() == "dwd_hyras":
        fetch_dwd(cfg)
    # print(f"Downloaded {len(downloaded)} new files for {var.name}")
if __name__ == '__main__':
    main()