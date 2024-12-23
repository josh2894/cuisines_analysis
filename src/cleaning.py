import pandas as pd
import os
from utils import load_env_vars
import warnings


def load_data():
    """
    Load data from json into dataframe and drop id column

    Returns:
        df (pd.DataFrame): loaded dataset
    """
    load_env_vars()
    cuisines_ingredients_path = os.getenv('cuisines_ingredients_json')
    with open (cuisines_ingredients_path, "r") as data:
        json_data = data.read()
    data = json.loads(json_data)
    df = pd.DataFrame(data)
    
    df.drop(columns=['id'], inplace=True) # id column isn't needed
    return df

def ingredients_one_hot(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies one-hot encoding to ingredients

    Args:
        df (pd.DataFrame): intial dataset 

    Returns:
        df_ingredients (pd.DataFrame): one-hot encoded ingredients
    """
    df_ingredients = df['ingredients'].apply(pd.Series) # Takes ingredients out of list, goes to 1 ingredient per column
    df_ingredients = pd.get_dummies(df_ingredients, prefix='', prefix_sep='')
    return df_ingredients

def split_dataset(df_expanded: pd.DataFrame) -> list:
    """
    Splits dataset into 21 pieces

    Args:
        df_expanded (pd.DataFrame): large dataset that needs to be split into pieces

    Returns:
        split_df_list: list containing the dataframe pieces
    """
    split_df_list = []
    x = int(len(df_expanded.index) / 21) # Number of rows for each piece
    for num in range(21):
        split_df = df_expanded.iloc[num*x : (num+1)*x, :]
        split_df_list.append(split_df)
    
    return split_df_list

def pieces_group_columns(split_df_list: list) -> list:
    """
    Update each piece of the dataset by grouping the columns

    Args:
        split_df_list: ungrouped dataset pieces 

    Returns:
        split_df_list: dataset pieces after grouped by column
    """
    warnings.filterwarnings('ignore')
    for i in range(len(split_df_list)):
        split_df_list[i] = split_df_list[i].groupby(split_df_list[i].columns, axis=1).sum()
        
    return split_df_list

def concat_pieces(split_df_list: list, cuisine_col: pd.Series) -> pd.DataFrame:
    """
    Concatenates grouped dataset pieces with cuisine column

    Args:
        split_df_list: dataset pieces grouped by column
        cuisine_col (pd.Series): column that contains the cuisines

    Returns:
        df_final (pd.DataFrame): concatenated, cleaned dataset
    """
    cuisine_col = pd.DataFrame(cuisine_col)
    df_ingredients_final = pd.concat(split_df_list, axis=0)
    df_final = pd.concat([cuisine_col, df_ingredients_final], axis=1)
    
    return df_final