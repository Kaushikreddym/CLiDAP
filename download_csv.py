import pandas as pd
from omegaconf import OmegaConf
import subprocess

cfg = OmegaConf.load("conf/config.yaml")  # adjust path if needed

locations_csv = "locations.csv"  # lat, lon columns
df = pd.read_csv(locations_csv)

dataset = cfg.dataset
start_date = cfg.time_range.start_date
end_date = cfg.time_range.end_date
parameter = cfg.weather.parameter

print(f"✔ Loaded base config: dataset={dataset}, start={start_date}, end={end_date}, parameter={parameter}")

for idx, row in df.iterrows():
    lat = row['lat']
    lon = row['lon']

    cmd = [
        "python", "download_location.py",
        f"dataset={dataset}",
        f"time_range.start_date={start_date}",
        f"time_range.end_date={end_date}",
        f"weather.parameter={parameter}",
        f"location.lat={lat}",
        f"location.lon={lon}"
    ]

    print(f"🚀 Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
