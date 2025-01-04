import pandas as pd
import numpy as np
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
    Generate a histogram for how many cuisines ingredients are used across

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


def cuisine_top_ingredients(df: pd.DataFrame, cuisine: str, top_n: int) -> pd.Series:
    """
    Shows n most used ingredients for a specified cuisine

    Args:
        df (pd.DataFrame): original dataset
        cuisine (str): cuisine to be examined
        top_n (int): how many top ingredients to show

    Returns:
        top_ingredients (pd.Series): the n most used ingredients 
    """
    df_cuisine = df[df["cuisine"] == cuisine] # Filters df to only have dishes from the chosen cuisine
    ingredient_usage = df_cuisine.iloc[:, 1:].sum(axis=0) # How many times each ingredient is used
    top = list(np.argsort(ingredient_usage.values)[-top_n:]) # Returns indexes of greatest values
    top_ingredients = ingredient_usage[top].sort_values(ascending=False)

    return top_ingredients


def ingredient_top_cuisines(df: pd.DataFrame, ingredient_list: list) -> plotly.graph_objects.Figure:
    """
    Displays how many times each cuisine used the specified ingredient(s)

    Args:
        df (pd.DataFrame): original dataset
        ingredient_list (list): list of ingredients to be checked

    Returns:
        fig: bar graph displaying the information
    """
    if len(ingredient_list) > 0:
        ingredient_list.append('cuisine') # So the cuisine column is inlcluded
        ingredient_df = df[ingredient_list]
        # Using sum to get dishes with all the ingredients. The -1 accounts for "cuisine" being in the list
        ingredient_df = ingredient_df[ingredient_df.iloc[:, 0:-1].sum(axis=1) == len(ingredient_list) - 1]
        ingredient_df = pd.DataFrame(ingredient_df.groupby('cuisine')['cuisine'].count().sort_values(ascending=False))
        
        # Making the bar chart based on ingredient_df
        fig = px.histogram(ingredient_df, x=ingredient_df.index, y='cuisine', title='Most Common Cuisines for Chosen Ingredient',
                        labels={'index':'Cuisine'}, color_discrete_sequence=['#00d8d8'])
        fig.update_layout(xaxis_title='Cuisines', yaxis_title='Amount of Dishes')
        fig.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace('sum of cuisine', 'Count')))
        fig.update_traces(marker_line_width=1.2, marker_line_color='black')
        return fig
    
    else:
        return


def cuisine_uniqueness(df: pd.DataFrame, cuisine: str, usage_filter: int) -> plotly.graph_objects.Figure:
    df_cuisine = df[df['cuisine'] == cuisine]
    df_cuisine_filtered = ingredient_usage_filter(df_cuisine, usage_filter) # Gets all the ingredients that are used usage_filter or more times in the chosen cuisine
    
    filtered_ingredients_cols = list(df_cuisine_filtered.columns)
    df_filtered = df[filtered_ingredients_cols] # Original dataset, filtered to only have the ingredients in filtered_ingredient_cols
    df_grouped = df_filtered.groupby('cuisine')[filtered_ingredients_cols[1:]].sum() # Shows how many times each cuisine used each of the ingredients
    df_grouped.drop(cuisine, axis=0, inplace=True) # Drop the chosen cuisine because we are looking for other cuisines only
    df_grouped = df_grouped >= usage_filter # Converts every value to True if the cuisine used the ingredient usage_filter times, False otherwise
 
    ingredients_distinct_cuisines = df_grouped.sum() # pd.Series, for each ingredient shows how many other cuisines ingredient was used usage_filter or more times 

    fig = px.histogram(ingredients_distinct_cuisines, x=ingredients_distinct_cuisines, 
                       title=f'{cuisine.title()} Ingredient Uniqueness For Ingredients Used {usage_filter}+ Times', 
                       labels={"x":"Cuisines"}, nbins=20)
    fig.update_layout(xaxis_title="Amount Of Other Cuisines Ingredient Was Used " + str(usage_filter) + "+ Times",
                      yaxis_title="Ingredients Count")
    fig.update_traces(marker_line_width=0.6, marker_line_color="black")
    
    return fig