import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects


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

def ingredient_variety_viz(df: pd.DataFrame) -> plotly.graph_objects.Figure:
    """
    Generate a histogram for how many cuisines an ingredient is used across

    Args:
        df (pd.DataFrame): dataset to use, often is filtered by ingredient usage

    Returns:
        fig: generated histogram
    """
    ingredients = list(df.columns[1:])
    variety_df = df.groupby('cuisine')[ingredients].sum().reset_index()
    variety_df = variety_df[ingredients] > 0
    variety_df = pd.DataFrame(variety_df.sum())
    variety_df.rename(columns={0: 'cuisines'}, inplace=True)
    
    
    fig = px.histogram(variety_df, x='cuisines', title="Histogram For Ingredient Variety", labels={"0":"Cuisines"}, 
                       color_discrete_sequence=["#8c00ff"])
    fig.update_layout(xaxis_title="Amount Of Cuisines An Ingredient Was Used Across", yaxis_title="Count")
    fig.update_traces(marker_line_width=0.4, marker_line_color="black")
    
    return fig