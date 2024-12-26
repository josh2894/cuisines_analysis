import pandas as pd

def ingredient_usage_filter(df: pd.DataFrame, usage_filter: int) -> pd.DataFrame:
    """
    Return the dataset with only ingredients that are used in (usage_filter) or more dishes

    Args:
        df (pd.DataFrame): the intial dataset to be filtered
        usage_filter (int): specifies the cutoff for amount of dishes an ingredient is used in

    Returns:
        filtered_df (pd.DataFrame): dataset with filtered ingredients
    """
    df_cuisine = pd.DataFrame(df['cuisine']) # Just the cuisine column
    df_ingredients = df.iloc[:, 1:] # Just the ingredients
    
    filtered_df = df_ingredients.loc[:, df_ingredients.sum() >= usage_filter]
    filtered_df = pd.concat([df_cuisine, filtered_df], axis=1) # Adding back the cuisine column
    
    return filtered_df