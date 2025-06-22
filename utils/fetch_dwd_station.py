
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
