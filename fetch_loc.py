import hydra
from omegaconf import DictConfig
import os
import yaml
import ipdb

from utils.utils_download import fetch_dwd_loc, fetch_ee_loc
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