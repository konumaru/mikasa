import os
import pickle

import pandas as pd

from typing import List, Any


def load_pickle(filepath: str, verbose: bool = True):
    if verbose:
        print(f"Load pickle from {filepath}")
    with open(filepath, "rb") as file:
        return pickle.load(file)


def dump_pickle(data: Any, filepath: str, verbose: bool = True):
    if verbose:
        print(f"Dump pickle to {filepath}")
    with open(filepath, "wb") as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)


def save_cache(filepath: str, use_cache: bool = False):
    """Save return dataframe with pickle.

    Parameters
    ----------
    filename : str
        filename, when save with pickle.
    use_cache : bool, optional
        Is use already cash result then pass method process, by default True

    Example
    -------
    from mikasa.io import save_cache

    @save_cache("path/to/file.pkl", use_cache=False)
    def create_feature(data):
        feature_name = "..."
        return data[target_name]
    """

    def _acept_func(func):
        def run_func(*args, **kwargs):
            dst_dir = filepath.rsplit("/", 1)[0]
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            if use_cache and os.path.exists(filepath):
                return load_pickle(filepath)

            result = func(*args, **kwargs)
            dump_pickle(result, filepath)
            return result

        return run_func

    return _acept_func


def load_feature(feature_files: List):
    data = []
    for filepath in feature_files:
        feature = load_pickle(filepath)
        data.append(feature)
    feature = pd.concat(data, axis=1)
    return feature
