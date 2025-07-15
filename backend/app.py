from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from omegaconf import OmegaConf,DictConfig
from hydra import initialize, compose
import subprocess
import os
from backend.utils.utils_download import *
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Hydra config once at startup
with initialize(config_path="conf", version_base=None):
    cfg = compose(config_name="config")

@app.get("/variables")
def get_variables(dataset: str = Query(...)):
    if dataset not in cfg.mappings:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    dataset_cfg = cfg.mappings.get(dataset).variables
    return {"variables": list(dataset_cfg.keys())}

@app.get("/datasets")
def get_datasets():
    # Only return keys that contain a 'variables' section
    datasets = [k for k, v in cfg.mappings.items() if isinstance(v, DictConfig) and "variables" in v]
    return {"datasets": datasets}


@app.get("/download_csv")
def download_csv(
    lat: float = Query(...),
    lon: float = Query(...),
    dataset: str = Query(...),
    parameter: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    overrides = [
        f"location.lat={lat}",
        f"location.lon={lon}",
        f"dataset={dataset}",
        f"weather.parameter={parameter}",
        f"time_range.start_date={start_date}",
        f"time_range.end_date={end_date}",
    ]

    with initialize(config_path="conf", version_base=None):
        cfg = compose(config_name="config", overrides=overrides)

    # Run script
    subprocess.run([
        "python", "backend/download_location.py",
        *overrides
    ])

    filename = build_output_filename(cfg)
    print(filename)
    file_path = os.path.join("backend", "data", filename)

    if os.path.isfile(file_path):
        return FileResponse(path=file_path, filename=filename, media_type="text/csv")
    else:
        raise HTTPException(status_code=500, detail="Failed to generate CSV")


