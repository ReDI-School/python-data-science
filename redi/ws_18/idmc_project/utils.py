import numpy as np
import pandas as pd
from pandas_datareader import wb

def get_wb_indicators(country_codes=None, indicator_codes=None, start_year=2007, end_year=2017):
    """
    Gets the World Bank indicators

    Args:
        country_codes ([str]): List of ISO3 country codes
        indicator_codes ([str]): List of World Bank Indicator Codes

    Returns:
        pd.DataFrame: DataFrame with the columns
          -ISO3
          -Country
          -Year
          -Indicator ID
          -Indicator name
          -Indicator category
          -Unit (e.g. €, no. of people, percentage, etc.)
          -Value
          -Source (World Bank Data or IDMC)
    """
    # Download data from the World Bank
    wb_data = wb.download(indicator=indicator_codes, country=country_codes, start=start_year, end=end_year)
    wb_data_reset = wb_data.reset_index()

    # Extract countries information
    wb_countries = wb.get_countries()
    wb_countries = wb_countries[["iso3c", "name"]]

    # Merge the aforementioned dataframes and remove duplicates
    merge = pd.merge(wb_data_reset, wb_countries, left_on='country', right_on="name")
    merge = merge.drop(columns=["name"])

    # Narrow the resulting dataframe
    merge_narrow = merge.melt(id_vars=['country', 'year', 'iso3c'], var_name='indicatorID', value_name='value')

    # Extract indicators information
    wb_indicators = wb.get_indicators()

    # Merge the narrowed dataframe with the World Bank indicators
    merge2 = pd.merge(merge_narrow, wb_indicators, left_on='indicatorID', right_on="id")

    # Remove duplicates, clean, and organize the data
    merge2 = merge2.drop(columns=["id", "source", "sourceNote"])
    merge2 = merge2.rename(index=str, columns={"name": "indicatorName", "topics": "indicatorCategory",
                                               "sourceOrganization": "source"})

    # Organize dataframe
    resulting_df = merge2[
        ['iso3c', 'country', 'year', 'indicatorID', 'indicatorName', 'indicatorCategory', 'unit', 'value', 'source']]

    return resulting_df


def get_idmc_indicators():
    """
    Gets the number of displacements from IDMC

    Returns:
        pd.DataFrame: DataFrame with the columns
          -ISO3
          -Country
          -Year
          -Indicator ID
          -Indicator name
          -Indicator category
          -Unit (e.g. €, no. of people, percentage, etc.)
          -Value
          -Source (World Bank Data or IDMC)
    """
    # Load data from IDMC
    url = 'https://raw.githubusercontent.com/ReDI-School/python-data-science/master/datasets/idmc/idmc_displacement_all_dataset.csv'
    idmc_displacement_all = pd.read_csv(url)

    # Clean data
    idmc_displacement_all = idmc_displacement_all.drop(columns=["Conflict Stock Displacement"])
    idmc_displacement_all = idmc_displacement_all.rename(index=str,
                                                         columns={"Name": "country", "ISO3": "iso3c", "Year": "year",
                                                                  "Conflict New Displacements": "conflictDisplacements",
                                                                  "Disaster New Displacements": "disasterDisplacements"})

    # Narrow dataframe
    merge_narrow = idmc_displacement_all.melt(id_vars=['iso3c', 'country', 'year'], var_name='indicatorName',
                                              value_name='value')

    # Create category name for new indicators
    merge_narrow.loc[:, 'indicatorCategory'] = "Displacement"
    merge_narrow.loc[:, 'source'] = "IDMC"

    # Create IDs for type of displacement
    replace = {"conflictDisplacements": "CO.DI.ID.MC", "disasterDisplacements": "DI.DI.ID.MC"}
    merge_narrow['indicatorID'] = merge_narrow['indicatorName'].map(replace)

    # Add new features
    merge_narrow["unit"] = np.nan

    # Organize dataframe
    merge_narrow = merge_narrow[
        ['iso3c', 'country', 'year', 'indicatorID', 'indicatorName', 'indicatorCategory', 'unit', 'value', 'source']]

    return merge_narrow


def get_wb_and_idmc(indicator_codes=None):
    """
    Combines the information from the WB and IDMC

    Returns:
        pd.DataFrame: DataFrame with the columns
          -ISO3
          -Country
          -Year
          -Indicator ID
          -Indicator name
          -Indicator category
          -Unit (e.g. €, no. of people, percentage, etc.)
          -Value
          -Source (World Bank Data or IDMC)
    """

    # Load data from IDMC
    idmc = get_idmc_indicators()

    # Load data from WB
    world_bank = get_wb_indicators([], indicator_codes)

    # Combine data from WB and IDMC
    concatenation = pd.concat([world_bank, idmc])

    # Organize dataframe
    concatenation = concatenation[
        ['iso3c', 'country', 'year', 'indicatorID', 'indicatorName', 'indicatorCategory', 'unit', 'value', 'source']]

    # Assign year datatype int
    concatenation['year'] = concatenation['year'].astype(int)

    return concatenation


def complete_missing_values(df, list_indicators):
    """
    Add documentation
    """
    dfs = df[df['indicatorName'].isin(list_indicators)]
    country_indicator_mean = dfs.groupby(['iso3c', 'indicatorName'])['value'].transform('mean')
    dfs.loc[dfs.value.isnull(), 'value'] = country_indicator_mean[dfs.value.isnull()]

    return dfs


def unstack_indicators(df):
    df_ = df.copy()

    # Define relevant columns as multiindex
    df_ = df_.set_index(['iso3c', 'year', 'indicatorName'])

    # Unstack indicators column per country/year
    df_.columns.name = 'case'
    df_ = df_.unstack('indicatorName')

    # Remove extra level of columns and reconvert multiindex into columns iso3c and year
    df_.columns = df_.columns.droplevel().tolist()
    df_ = df_.reset_index()

    return df_


def get_indicators_clean_for_type_displacements(df, drop_displacement_type, keep_displacement_type):
    df_ = df.copy()

    # Drop the data for the other type of displacements
    df_ = df_.drop(drop_displacement_type, axis=1)

    # Remove rows (events for a given country and year) where there id not data of that type of displacements
    df_ = df_.dropna(subset=[keep_displacement_type])

    return df_


def calculate_percentage_displacements_per_country_per_year(df, column):
    # Calculate percentage of displacements per number of inhabitants in each country for each year
    column_norm = column + "Norm"
    df[column_norm] = (df[column] / df['Population, total']) * 100

    # Clean final dataframe
    df = df.drop([column, 'Population, total'], axis=1)

    return df


def standarize_indicator(df, indicators):
    df_ = df.copy()
    for indicator in indicators:
        # Standarize data for indicator with mean 0 and standard deviation 1 => (x - mean) / std
        df_[indicator] = (df_[indicator] - df_[indicator].mean()) / df_[indicator].std()

    return df_