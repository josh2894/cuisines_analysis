import pandas as pd
import os
import json
from utils import load_env_vars
from cleaning import *

def main():
    load_env_vars()
    df = load_data()
    df_ingredients = ingredients_one_hot(df)
    split_df_list = split_dataset(df_ingredients)
    split_df_list = pieces_group_columns(split_df_list)
    
    cuisines = df['cuisine']
    df_final = concat_pieces(split_df_list, cuisines)
        
    processed_data_dir = os.getenv('processed_data_dir')
    destination_path_csv = os.path.join(processed_data_dir, 'cuisines_analysis_final.csv')
    destination_path_parquet = os.path.join(processed_data_dir, 'cuisines_analysis_final.parquet')

    df_final.to_csv(destination_path_csv, index=False)
    df_final.to_parquet(destination_path_parquet, index=False, compression='brotli')

    
if __name__ == '__main__':
    main()    
    