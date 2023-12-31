"""
Data Processing Module
-----------------------

This module provides functions to process and reformat data from the World Bank and the International Labour Organization (ILO). The module includes functions for reading, cleaning, and reshaping data from these sources.

Functions
---------
wbdata(filename, save_file=False)
    Process the World Bank data and reformat it for analysis.

    Parameters
    ----------
    filename : str
        The path to the World Bank data in an Excel file.
    save_file : bool, optional
        Whether to save the processed data as a CSV file. The default is False.

    Returns
    -------
    df : pandas.DataFrame
        The processed World Bank data in a structured format.

ilodata(filename, save_file=False)
    Process the ILO data and reformat it for analysis.

    Parameters
    ----------
    filename : str
        The path to the ILO data in a CSV file.
    save_file : bool, optional
        Whether to save the processed data as a CSV file. The default is False.

    Returns
    -------
    df : pandas.DataFrame
        The processed ILO data in a structured format.

Notes
-----
- The module is designed to process specific data formats from the World Bank and ILO.
- The processed data is returned in a structured format suitable for analysis.

Example
-------
# Process World Bank data
wb_data = wbdata("world_bank_data.xlsx")

# Process ILO data
ilo_data = ilodata("ilo_data.csv")

"""

import pandas as pd


def wbdata(filename: str, save_file: bool = False):

    """Process the World Bank data.

    Parameters
    ----------
    filename : str
        The path to the World Bank data. This is an excel file.
    save_file : bool, optional
        Whether to save the processed data as a csv file. The default is True.

    Returns
    -------
    df : pandas.DataFrame
        The processed World Bank data.

    """
    # Read the data
    df = pd.read_excel(filename, sheet_name="Data", skipfooter=2, na_values="..")

    # Drop unnecessary columns
    df.drop(columns=["Country Code", "Series Code"], inplace=True)

    # Reorganize the data
    df = df.melt(id_vars=["Country Name", "Series Name"], var_name="Year", value_name="Value")
    df = df.pivot_table(index=["Country Name", "Year"], columns="Series Name", values="Value")
    df.reset_index(inplace=True)

    # Reformat 'Year' column
    df["Year"] = df["Year"].astype(str).str[:4]
    df["Year"] = df["Year"].astype(int)

    # Remove column name
    df.columns.name = None

    # Save the data
    if save_file:
        file_name = filename.split(".")[0] + "_long.csv"
        df.to_csv(file_name, index=False)

    return df


def ilodata(filename: str, save_file: bool = False):

    """Process the ILO data.

    Parameters
    ----------
    filename : str
        The path to the ILO data. This is a csv file.
    save_file : bool, optional
        Whether to save the processed data as a csv file. The default is True.

    Returns
    -------
    df : pandas.DataFrame
        The processed ILO data.

    """
    # Read the data (only col 0, 4, 5, 6)
    df = pd.read_csv(filename, usecols=[0, 4, 5, 6])

    # Rename interest columns
    df.rename(columns={"ref_area.label": "Country Name",
                       "classif1.label": "Sector",
                       "time": "Year",
                       "obs_value": "Value"}, inplace=True)

    df.pivot_table(index=["Country Name", "Year"], columns="Sector", values="Value")
    df.reset_index(inplace=True)

    # Rename sector columns
    df.columns = df.columns.str.split().str[-1]

    # Calculate percentages of total employment
    df["Manufacturing (% of total employment)"] = df["Manufacturing"] / df["Total"] * 100
    df["Services (% of total employment)"] = df["Services"] / df["Total"] * 100
    df["Agriculture (% of total employment)"] = df["Agriculture"] / df["Total"] * 100

    # Select only relevant columns
    df = df.iloc[:, -3:]

    # Change country names to match World Bank data
    df["Country Name"].replace({"Congo, Democratic Republic of the": "Congo, Dem. Rep.",
                                "Tanzania, United Republic of": "Tanzania"}, inplace=True)

    # Remove column name
    df.columns.name = None

    # Save the data
    if save_file:
        file_name = filename.split(".")[0] + "_long.csv"
        df.to_csv(file_name, index=False)

    return df
Gen