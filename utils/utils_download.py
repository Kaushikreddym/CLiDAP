import pandas as pd
from wetterdienst import Settings
from wetterdienst.provider.dwd.observation import DwdObservationRequest
import geemap
import ee
import ipdb
import geopandas as gpd
from omegaconf import DictConfig
import os
import yaml
import time
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore", category=Warning)

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
    df['source'] = 'DWD'
    # Standardize column names
    df = df.rename(columns={
        "date": "time",
        "value": "value",
        "station_id": "frequent_station",

    })
    df["variable"] = parameter_key
    df["latitude"] = lat
    df["longitude"] = lon
    df = df[["latitude", "longitude", "time", "source", "variable", "value"]]
    
    df.to_csv(output_file, index=False)
    print(f"[✓] Saved data to {output_file}")
    return df
def fetch_ee_loc(cfg: DictConfig):
    ee.Initialize(project='earthengine-462007')

    provider = cfg.dataset.lower()
    variable_name = cfg.weather.parameter
    ee_image_collection = cfg.mappings[provider].params.collection
    
    # Prepare the image collection
    sd = cfg.time_range.start_date
    ed = cfg.time_range.end_date
    var_name = cfg.mappings[provider].variables[variable_name].name
    if provider=='gddp':
        model = cfg.mappings[provider].params.model
        scenario = cfg.mappings[provider].params.scenario
        dataset = ee.ImageCollection(ee_image_collection)\
                    .filter(ee.Filter.date(sd, ed))\
                    .filter(ee.Filter.eq('model', model))\
                    .filter(ee.Filter.eq('scenario', scenario))
    elif provider=='era5-land':
        dataset = ee.ImageCollection(ee_image_collection)\
                    .filter(ee.Filter.date(sd, ed))
    else:
        raise ValueError(f"Provider '{provider}' is not supported for Earth Engine data fetching.")    
    image_var = dataset.select(var_name)

    
    lat = cfg.location.lat
    lon = cfg.location.lon
    # identifier = cfg.location.id
    out_dir = cfg.output.out_dir
    # buffer = cfg.location.buffer_km
    buffer = None
    scale = cfg.mappings[provider].params.scale
    # retry_delay = cfg.download.retry_delay

    os.makedirs(out_dir, exist_ok=True)

    df = pd.DataFrame([{ "lat": lat, "lon": lon, "id": 0}])
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["lon"], df["lat"]), crs="EPSG:4326")

    try:
        gdf_ee = geemap.gdf_to_ee(gdf)

        # if buffer:
        #     pixel_values = gdf_ee.map(
        #         lambda f: f.set('ts', image_var.getRegion(
        #             f.buffer(buffer*1e3).bounds().geometry(), scale))
        #     )
        # else:
        pixel_values = gdf_ee.map(
            lambda f: f.set('ts', image_var.getRegion(
                f.geometry(), scale))
        )
        # ipdb.set_trace()
        pixel_values_info = pixel_values.getInfo()

        for feature in pixel_values_info['features']:
            data = feature['properties']['ts']
            data_id = feature['properties']['id']

            if data:
                columns = data[0]
                rows = data[1:]
                df_out = pd.DataFrame(rows, columns=columns)

                out_path = os.path.join(out_dir, f'{data_id}_data.csv')
                df_out.to_csv(out_path, index=False)
                print(f"[\u2713] Saved: {out_path}")
            else:
                print(f"[!] No data for ID {data_id}")

    except Exception as e:
        print(f"[\u2717] Error: {e}")
        # time.sleep(retry_delay)
        raise RuntimeError("Failed to download data.")

def fetch_ee_loc_mod(cfg: DictConfig):
    # Initialize Earth Engine
    ee.Initialize(project='earthengine-462007')

    provider = cfg.dataset.lower()
    variable_name = cfg.weather.parameter
    ee_image_collection = cfg.mappings[provider].params.collection

    sd = cfg.time_range.start_date
    ed = cfg.time_range.end_date
    var_name = cfg.mappings[provider].variables[variable_name].name
    scale = cfg.mappings[provider].params.scale
    out_dir = cfg.output.out_dir

    lat = cfg.location.lat
    lon = cfg.location.lon

    # Handle model/scenario if needed
    if provider == 'gddp':
        model = cfg.mappings[provider].params.model
        scenario = cfg.mappings[provider].params.scenario
        dataset = ee.ImageCollection(ee_image_collection) \
            .filter(ee.Filter.date(sd, ed)) \
            .filter(ee.Filter.eq('model', model)) \
            .filter(ee.Filter.eq('scenario', scenario))
    elif provider == 'era5-land':
        dataset = ee.ImageCollection(ee_image_collection) \
            .filter(ee.Filter.date(sd, ed))
    else:
        raise ValueError(f"Provider '{provider}' is not supported.")

    image_var = dataset.select(var_name)
    point = ee.Geometry.Point(lon, lat)

    os.makedirs(out_dir, exist_ok=True)
    results = []

    print(f"[i] Fetching time series for point: ({lat}, {lon})")

    # Use a client-side list of images
    image_list = image_var.toList(image_var.size())
    n_images = image_var.size().getInfo()

    for i in tqdm(range(n_images), desc="Processing images"):
        try:
            img = ee.Image(image_list.get(i))
            date = img.date().format('YYYY-MM-dd').getInfo()

            value = img.reduceRegion(
                reducer=ee.Reducer.first(),
                geometry=point,
                scale=scale,
                bestEffort=True
            ).get(var_name)

            value = value.getInfo() if value else None
            results.append({"date": date, var_name: value})
        except Exception as e:
            print(f"[!] Skipping image {i} due to error: {e}")
            continue

    df_out = pd.DataFrame(results)
    out_path = os.path.join(out_dir, f'point_timeseries.csv')
    df_out.to_csv(out_path, index=False)
    print(f"[✓] Saved timeseries to: {out_path}")