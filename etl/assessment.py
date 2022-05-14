''' Ingest Assessment data
'''

import pandas as pd
import geopandas as gpd
from .assess_params import geom_col, value_col, date_col

def drop_missing_geom(df, geom_col=geom_col):
    return df.dropna(subset=[geom_col]).copy()

def fill_missing_vals(df, missing_cols=[value_col,
                                        date_col],
                            missing_fill=[-1.0, -1.0]):
    for i, j in zip(missing_cols, missing_fill):
        df[i].fillna(j, inplace = True)
    return df

def create_lat_lon(df, geom_col=geom_col, lat='lat', lon='lon'):
    geo_ser = gpd.GeoSeries.from_wkt(df[geom_col].values)
    lat_lons = geo_ser.representative_point().apply(lambda i: (i.y, i.x))
    df[lat] = [i[0] for i in lat_lons]
    df[lon] = [i[1] for i in lat_lons]
    return df

def _process(f, clean_funcs = None, read_kwargs = dict(chunksize = 100)):
    for each_chunk in pd.read_csv(f, **read_kwargs):
        if clean_funcs is not None:
            for func in clean_funcs:
                each_chunk = func(each_chunk)
        yield each_chunk

def process(**kwargs):
    clean_funcs = [drop_missing_geom, create_lat_lon, fill_missing_vals]
    return _process(**kwargs, clean_funcs=clean_funcs)
