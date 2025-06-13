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

import hydra
from omegaconf import DictConfig

def load_config(config_path):
    """Load the YAML config file"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

# Google Drive functions
def download_google_drive_files(service, folder_id, varname, output_dir):
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

    os.makedirs(output_dir, exist_ok=True)
    downloaded_files = []

    for file in files:
        filename = f"{file['name']}"
        filepath = os.path.join(output_dir,varname, filename)

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

# DWD functions
# def get_dwd_links(base_url, file_extension):
#     """Get download links from DWD server"""
#     response = requests.get(base_url)
#     soup = BeautifulSoup(response.content, "html.parser")
#     return [base_url + link.get("href") for link in soup.find_all("a", href=True) 
#             if link.get("href").endswith(file_extension)]

# def download_dwd_file(url, output_dir):
#     """Download a single file from DWD server"""
#     os.makedirs(output_dir, exist_ok=True)
#     filename = os.path.join(output_dir, url.split("/")[-1])
    
#     try:
#         response = requests.get(url, stream=True)
#         response.raise_for_status()
#         with open(filename, "wb") as file:
#             for chunk in response.iter_content(chunk_size=1024):
#                 if chunk:
#                     file.write(chunk)
#         print(f"Downloaded: {filename}")
#         return True
#     except Exception as e:
#         print(f"Failed to download {url}: {str(e)}")
#         return False

# def download_dwd_files_parallel(urls, output_dir, max_workers=5):
#     """Download multiple DWD files in parallel"""
#     with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = [executor.submit(download_dwd_file, url, output_dir) for url in urls]
#         return [f.result() for f in futures]

@hydra.main(config_path="conf", config_name="config_download", version_base="1.3")
def main(cfg: DictConfig):
    # Parse command line arguments
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    creds = service_account.Credentials.from_service_account_file(
        cfg.google_service_account, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)

    mswx = cfg.datasets.MSWX
    output_dir = mswx.output_dir

    for var in mswx.variables:
        print(f"\nProcessing variable: {var.name}")
        downloaded = download_google_drive_files(
            service=service,
            folder_id=var.folder_id,
            varname=var.name,
            output_dir=output_dir
        )
        print(f"Downloaded {len(downloaded)} new files for {var.name}")
if __name__ == '__main__':
    main()