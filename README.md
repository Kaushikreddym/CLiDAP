# 📡 Weather Data Downloader

This project automates the fetching and extraction of weather data from multiple sources — such as **MSWX**, **DWD HYRAS**, **ERA5-Land**, **GDDP**, and more — for a given location and time range.

It supports:
✅ Automatic file download (e.g., from Google Drive or online servers)  
✅ Flexible configuration via `config.yaml`  
✅ Time series extraction for a user-specified latitude/longitude  
✅ Batch processing for many locations from a CSV file

---

## ⚙️ **Key Features**

- **Supports multiple weather data providers**
- **Uses `xarray` for robust gridded data extraction**
- **Handles curvilinear and rectilinear grids**
- **Uses a Google Drive Service Account for secure downloads**
- **Easily reproducible runs using Hydra**

---
## 📡 Google Drive API Setup

This project uses the **Google Drive API** with a **Service Account** to securely download weather data files from a shared Google Drive folder.

Follow these steps to set it up correctly:

---

### ✅ 1. Create a Google Cloud Project

- Go to [Google Cloud Console](https://console.cloud.google.com/).
- Click **“Select Project”** → **“New Project”**.
- Enter a project name (e.g. `WeatherDataDownloader`).
- Click **“Create”**.

---

### ✅ 2. Enable the Google Drive API

- In the left sidebar, go to **APIs & Services → Library**.
- Search for **“Google Drive API”**.
- Click it, then click **“Enable”**.

---

### ✅ 3. Create a Service Account

- Go to **IAM & Admin → Service Accounts**.
- Click **“Create Service Account”**.
- Enter a name (e.g. `weather-downloader-sa`).
- Click **“Create and Continue”**. You can skip assigning roles for read-only Drive access.
- Click **“Done”** to finish.

---

### ✅ 4. Create and Download a JSON Key

- After creating the Service Account, click on its email address to open its details.
- Go to the **“Keys”** tab.
- Click **“Add Key” → “Create new key”** → choose **`JSON`** → click **“Create”**.
- A `.json` key file will download automatically. **Store it securely!**

### ✅ 5. Store the JSON Key Securely

- Place the downloaded `.json` key in the conf folder with the name service.json. 


## Setup Instructions fro ERA5 api

### 1. CDS API Key Setup

1. Create a free account on the
[Copernicus Climate Data Store](https://cds.climate.copernicus.eu/user/register)
2. Once logged in, go to your [user profile](https://cds.climate.copernicus.eu/user)
3. Click on the "Show API key" button
4. Create the file `~/.cdsapirc` with the following content:

   ```bash
   url: https://cds.climate.copernicus.eu/api/v2
   key: <your-api-key-here>
   ```

5. Make sure the file has the correct permissions: `chmod 600 ~/.cdsapirc`
