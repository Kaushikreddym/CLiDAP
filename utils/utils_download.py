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
from datetime import datetime, timedelta
import xarray as xr
import hydra
from omegaconf import DictConfig

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

def list_drive_files(folder_id, service):
    """
    List all files in a Google Drive folder, handling pagination.
    """
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

    return files
def download_drive_file(file_id, local_path, service):
    """
    Download a single file from Drive to a local path.
    """
    request = service.files().get_media(fileId=file_id)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    with io.FileIO(local_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"   → Download {int(status.progress() * 100)}% complete")
def fetch_MSWX(var_cfg):
    param_mapping = var_cfg.mappings
    provider = var_cfg.dataset.lower()
    parameter_key = var_cfg.weather.parameter

    param_info = param_mapping[provider]['variables'][parameter_key]
    folder_id = param_info["folder_id"]

    start_date = var_cfg.time_range.start_date
    end_date = var_cfg.time_range.end_date

    # === 1) Generate expected filenames ===
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    expected_files = []
    current = start
    while current <= end:
        doy = current.timetuple().tm_yday
        basename = f"{current.year}{doy:03d}.nc"
        expected_files.append(basename)
        current += timedelta(days=1)

    output_dir = './data/'
    local_files = []
    missing_files = []

    for basename in expected_files:
        local_path = os.path.join(output_dir, provider, parameter_key, basename)
        if os.path.exists(local_path):
            local_files.append(basename)
        else:
            missing_files.append(basename)

    if not missing_files:
        print(f"✅ All {len(expected_files)} files already exist locally. No download needed.")
        return local_files

    print(f"📂 {len(local_files)} exist, {len(missing_files)} missing — fetching from Drive...")

    # === 2) Connect to Drive ===
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    creds = service_account.Credentials.from_service_account_file(
        param_mapping[provider].params.google_service_account, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)

    # === 3) List all Drive files ===
    drive_files = list_drive_files(folder_id, service)
    valid_filenames = set(missing_files)

    files_to_download = [f for f in drive_files if f['name'] in valid_filenames]

    if not files_to_download:
        print(f"⚠️ None of the missing files found in Drive. Check folder & date range.")
        return local_files

    # === 4) Download missing ===
    for file in files_to_download:
        filename = file['name']
        local_path = os.path.join(output_dir, provider, parameter_key, filename)
        print(f"⬇️ Downloading {filename} ...")
        download_drive_file(file['id'], local_path, service)
        local_files.append(filename)

    return local_files


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
        local_path = os.path.join('./data/',provider,parameter_key.upper(), file_name)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
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

def find_nearest_xy(ds, target_lat, target_lon):
    """
    Given a dataset with curvilinear grid, find the nearest x,y index.
    """
    lat = ds['lat'].values  # shape (y,x) or (x,y)
    lon = ds['lon'].values

    # Flatten to 1D for k-d tree
    lat_flat = lat.flatten()
    lon_flat = lon.flatten()

    tree = cKDTree(np.column_stack((lat_flat, lon_flat)))
    _, idx = tree.query([target_lat, target_lon])
    iy, ix = np.unravel_index(idx, lat.shape)

    return iy, ix

def extract_ts_dwd(cfg: DictConfig):
    data_dir = cfg.output.out_dir  # Hydra will change cwd to the run dir; so this stays relative
    param_mapping = cfg.mappings
    provider = cfg.dataset.lower()
    parameter_key = cfg.weather.parameter
    # Validate provider and parameter
    # ipdb.set_trace()
    param_info = param_mapping[provider]['variables'][parameter_key]
    prefix = param_info["prefix"]
    version = param_info["version"]

    start_date = cfg.time_range.start_date
    end_date = cfg.time_range.end_date

    # Parse dates & extract unique years
    start_year = datetime.fromisoformat(start_date).year
    end_year = datetime.fromisoformat(end_date).year
    years = list(range(start_year, end_year + 1))
    files=[]
    for year in years:
        file_name = f"{prefix}_{year}_{version}_de.nc"
        files.append(os.path.join('./data/',provider,parameter_key.upper(), file_name))

    if not files:
        raise FileNotFoundError(f"No NetCDF files found for {parameter}")

    target_lat = cfg.location.lat
    target_lon = cfg.location.lon

    ts_list = []

    for f in files:
        print(f"📂 Opening: {f}")
        ds = xr.open_dataset(f)

        # Dimensions: (time, y, x) or (time, x, y)
        # lat/lon: 2D
        time_name = [x for x in ds.coords if "time" in x.lower()][0]
        
        iy, ix = find_nearest_xy(ds, target_lat, target_lon)

        print(f"📌 Nearest grid point at (y,x)=({iy},{ix})")
        
        ts = ds[parameter_key].isel(x=ix, y=iy)  # watch order: dims must match

        df = ts.to_dataframe().reset_index()[[time_name, parameter_key]]
        ts_list.append(df)

    # Combine all time series
    ts_all = pd.concat(ts_list).sort_values(by=time_name).reset_index(drop=True)
    
    # Slice on combined DataFrame
    ts_all[time_name] = pd.to_datetime(ts_all[time_name])
    mask = (ts_all[time_name] >= start_date) & (ts_all[time_name] <= end_date)
    ts_all = ts_all.loc[mask].reset_index(drop=True)

    out_dir = hydra.utils.to_absolute_path(cfg.output.out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, cfg.output.filename)

    ts_all.to_csv(out_path, index=False)
    print(f"✅ Saved time series to: {out_path}")

    return ts_all
def extract_ts_MSWX(cfg: DictConfig):
    parameter = cfg.weather.parameter
    provider = cfg.dataset.lower()
    base_dir = './data/'

    target_lat = cfg.location.lat
    target_lon = cfg.location.lon

    start_date = pd.to_datetime(cfg.time_range.start_date)
    end_date = pd.to_datetime(cfg.time_range.end_date)

    # === 1) Rebuild exact basenames ===
    current = start_date
    basenames = []
    while current <= end_date:
        doy = current.timetuple().tm_yday
        basename = f"{current.year}{doy:03d}.nc"
        basenames.append(basename)
        current += timedelta(days=1)

    # === 2) Process only those files ===
    ts_list = []
    missing = []

    for basename in basenames:
        file_path = os.path.join(base_dir, provider, parameter, basename)

        if not os.path.exists(file_path):
            missing.append(basename)
            continue

        print(f"📂 Opening: {file_path}")
        ds = xr.open_dataset(file_path)

        time_name = [x for x in ds.coords if "time" in x.lower()][0]
        data_var = [v for v in ds.data_vars][0]

        ts = ds[data_var].sel(
            lat=target_lat,
            lon=target_lon,
            method='nearest'
        )

        df = ts.to_dataframe().reset_index()[[time_name, data_var]]
        ts_list.append(df)

    if missing:
        print(f"⚠️ Warning: {len(missing)} files were missing and skipped:")
        for m in missing:
            print(f"   - {m}")

    if not ts_list:
        raise RuntimeError("❌ No valid files were found. Cannot extract time series.")

    # === 3) Combine and slice (for safety) ===
    ts_all = pd.concat(ts_list).sort_values(by=time_name).reset_index(drop=True)

    ts_all[time_name] = pd.to_datetime(ts_all[time_name])
    ts_all = ts_all[
        (ts_all[time_name] >= start_date) &
        (ts_all[time_name] <= end_date)
    ].reset_index(drop=True)

    out_dir = hydra.utils.to_absolute_path(cfg.output.out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, cfg.output.filename)

    ts_all.to_csv(out_path, index=False)
    print(f"✅ Saved MSWX time series to: {out_path}")

    return ts_all