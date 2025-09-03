from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from omegaconf import OmegaConf, DictConfig
from hydra import initialize, compose
import subprocess
import os
from backend.utils.utils_download import *
import intake
import xarray as xr
import tempfile
import json

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


col = intake.open_esm_datastore("https://storage.googleapis.com/cmip6/pangeo-cmip6.json")
df = col.df.dropna(subset=["source_id", "variable_id", "experiment_id"])  # Clean NaNs

@app.get("/cmip6/options")
def get_cmip6_options(
    dataset: str = Query("CMIP6"),  # Ignored since only CMIP6 here
    variable_id: str = Query("tasmax"),
    experiment_id: str = Query("historical"),
    stage: str = Query("init")  # "init", "experiment", or "source"
):
    try:
        filtered = df.copy()

        if variable_id:
            filtered = filtered[filtered["variable_id"] == variable_id]

        if experiment_id:
            filtered = filtered[filtered["experiment_id"] == experiment_id]

        if stage == "experiment":
            return JSONResponse({"experiment_ids": sorted(filtered["experiment_id"].unique().tolist())})

        if stage == "source":
            return JSONResponse({"source_ids": sorted(filtered["source_id"].unique().tolist())})

        return JSONResponse({
            "variable_ids": sorted(df["variable_id"].unique().tolist())
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/cmip6_download")
async def cmip6_download(request: Request):
    params = await request.json()
    experiment_id = [params['experiment_id']]
    source_id = params['source_id']
    variable_id = params['variable_id']
    lat = float(params['lat'])
    lon = float(params['lon'])
    start_time = params['start_time']
    end_time = params['end_time']

    # Open catalog and search
    col = intake.open_esm_datastore("https://storage.googleapis.com/cmip6/pangeo-cmip6.json")
    query = dict(
        experiment_id=experiment_id,
        source_id=source_id,
        variable_id=variable_id,
        table_id='day'
    )
    col_subset = col.search(require_all_on=["source_id"], **query)
    if len(col_subset.df) == 0:
        return {"error": "No matching dataset found."}
    zstore_path = col_subset.df.zstore.values[0].replace('gs:/',"https://storage.googleapis.com")
    df = xr.open_zarr(zstore_path)
    df = df.sel(lat=lat, lon=lon, method="nearest").sel(time=slice(start_time, end_time))[[variable_id]]

    # Save to temporary NetCDF file
    with tempfile.NamedTemporaryFile(suffix='.nc', delete=False) as tmp:
        df.to_netcdf(tmp.name)
        tmp.seek(0)
        filename = os.path.basename(tmp.name)
        def iterfile():
            with open(tmp.name, mode="rb") as file_like:
                yield from file_like
            os.remove(tmp.name)
        return StreamingResponse(iterfile(), media_type="application/x-netcdf", headers={
            "Content-Disposition": f"attachment; filename={filename}"
        })