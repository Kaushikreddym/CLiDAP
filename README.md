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