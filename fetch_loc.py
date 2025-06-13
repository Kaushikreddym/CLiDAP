import pandas as pd
from wetterdienst import Settings
from wetterdienst.provider.dwd.observation import DwdObservationRequest
import hydra
from omegaconf import DictConfig
import os
import yaml
import geemap
import ee
import ipdb 
import geopandas as gpd

def fetch_dwd_loc(cfg: DictConfig):
    
    param_mapping = cfg.mappings
    provider = cfg.dataset.lower()
    parameter_key = cfg.weather.parameter
    # Validate provider and parameter
    
    if provider not in param_mapping:
        raise ValueError(f"Provider '{provider}' not found in parameter map.")
    if parameter_key not in param_mapping[provider]['variables']:
        raise ValueError(f"Parameter '{parameter_key}' not defined for provider '{provider}'.")

    param_info = param_mapping[provider]['variables'][parameter_key]
    resolution = param_info["resolution"]
    dataset = param_info["dataset"]
    variable_name = param_info["name"]

    lat = cfg.location.lat
    lon = cfg.location.lon
    distance = cfg.location.buffer_km
    start_date = cfg.time_range.start_date
    end_date = cfg.time_range.end_date
    output_file = cfg.output.filename
    # ipdb.set_trace()
    settings = Settings(
        ts_shape="long",
        ts_humanize=True,
        # ts_si_units=False
        )

    request = DwdObservationRequest(
        parameters=(resolution, dataset, variable_name),
        start_date=start_date,
        end_date=end_date,
        settings=settings
    ).filter_by_distance(
        latlon=(lat, lon),
        distance=distance,
        unit="km"
    )

    df = request.values.all().df.to_pandas()
    
    df['date'] = pd.to_datetime(df['date'])
    df = df.groupby(['station_id', 'date']).agg({
        'value': 'mean',
        'resolution': lambda x: x.mode().iloc[0] if not x.mode().empty else None,
        'dataset': lambda x: x.mode().iloc[0] if not x.mode().empty else None,
        'parameter': lambda x: x.mode().iloc[0] if not x.mode().empty else None,
        'quality': lambda x: x.mode().iloc[0] if not x.mode().empty else None,
    }).reset_index()
    # ipdb.set_trace()
    df.set_index("date", inplace=True)
    df.reset_index(inplace=True)

    # Standardize column names
    df = df.rename(columns={
        "date": "time",
        "value": "value",
        "station_id": "frequent_station",
        "source": "DWD",

    })
    df["variable"] = parameter_key
    df["latitude"] = lat
    df["longitude"] = lon
    df = df[["latitude", "longitude", "time", "source", "variable", "value"]]
    
    df.to_csv(output_file, index=False)
    print(f"[✓] Saved data to {output_file}")

def fetch_ee_loc(cfg: DictConfig):
    
    param_mapping = cfg.mappings
    provider = cfg.dataset.lower()
    parameter_key = cfg.weather.parameter
    # Validate provider and parameter
    
    if provider not in param_mapping:
        raise ValueError(f"Provider '{provider}' not found in parameter map.")
    if parameter_key not in param_mapping[provider]['variables']:
        raise ValueError(f"Parameter '{parameter_key}' not defined for provider '{provider}'.")
    
    param_info = param_mapping[provider]['params']
    collection = param_info["collection"]
    model = param_info["model"]
    scenario = param_info["scenario"]
    scale = param_info["scale"]
    
    lat = cfg.location.lat
    lon = cfg.location.lon
    distance = cfg.location.buffer_km
    start_date = cfg.time_range.start_date
    end_date = cfg.time_range.end_date
    output_file = cfg.output.filename
    
    ee.Initialize(project='earthengine-462007')
    dataset = ee.ImageCollection(collection)\
            .filter(ee.Filter.date(start_date, end_date))\
            .filter(ee.Filter.eq('model', model))\
            .filter(ee.Filter.eq('scenario', scenario))
    
    variable_name = param_mapping[provider]['variables'][parameter_key].name
    variable_ee = dataset.select(variable_name)

    identifier=0
    out_dir='./'
    # scale = cfg.download.scale
    # retry_delay = cfg.download.retry_delay

    os.makedirs(out_dir, exist_ok=True)

    df = pd.DataFrame([{ "lat": lat, "lon": lon, "id": identifier }])
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["lon"], df["lat"]), crs="EPSG:4326")

    try:
        gdf_ee = geemap.gdf_to_ee(gdf)

        if distance:
            pixel_values = gdf_ee.map(
                lambda f: f.set('ts', variable_ee.getRegion(
                    f.buffer(distance*1e3).bounds().geometry(), scale))
            )
        else:
            pixel_values = gdf_ee.map(
                lambda f: f.set('ts', variable_ee.getRegion(
                    f.geometry(), scale))
            )

        pixel_values_info = pixel_values.getInfo()

        for feature in pixel_values_info['features']:
            data = feature['properties']['ts']
            data_id = feature['properties']['id']
            ipdb.set_trace()
            if data:
                columns = data[0]
                rows = data[1:]
                df_out = pd.DataFrame(rows, columns=columns)
                df_out['time'] = pd.to_datetime(df_out['time'], unit='ms')
                out_path = os.path.join(out_dir, output_file)
                df_out["variable"] = parameter_key
                df_out["latitude"] = lat
                df_out["longitude"] = lon
                df_out["source"] = f"GDDP_{model}_{scenario}"
                df_out.rename(columns=variable_name: "value"}, inplace=True)
                df_out = df_out[["latitude", "longitude", "time", "source", "variable", "value"]]
                df_out.to_csv(out_path, index=False)
                print(f"[\u2713] Saved: {out_path}")
            else:
                print(f"[!] No data for ID {data_id}")

    except Exception as e:
        print(f"[\u2717] Error: {e}")
        time.sleep(retry_delay)
        raise RuntimeError("Failed to download data.")

@hydra.main(config_path="conf", config_name="config", version_base="1.3")
def main(cfg: DictConfig):
    provider = cfg.dataset.lower()

    if provider == "dwd":
        fetch_dwd_loc(cfg)
        print(f"Fetching data for provider: {provider}") 
    elif provider in ["gddp", "era5-land"]:
        fetch_ee_loc(cfg)
        print(f"Fetching data for provider: {provider}") 
    else:
        raise NotImplementedError(f"Provider '{provider}' is not yet supported in this script.")
    
if __name__ == "__main__":
    main()