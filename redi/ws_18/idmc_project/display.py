import pandas as pd

def extract_factors_dataframe_from_ols_summary(summary):
    """
    Extracts the table from the summary that contains the coefficients and the statistical information
    Rename columns and sort coefficients based on the values of the coefficients

    Returns: (for more details see blog post previously mentioned)
       pd.DataFrame: DataFrame with the columns
          - coef: coefficient Bi from the linear regression
          - std err: estandard error
          - t: t-value for the given factor
          - P-value: calculated p-value
          - [0.025: minimum limit of the confidence interval
          - 0.975]: maximum limit in the confidence interval
    """
    df_summary = pd.read_html(
            summary.tables[1].as_html(),
            header=0, 
            index_col='Unnamed: 0'
    )[0]
    df_summary = df_summary.rename(columns={'Unnamed: 0':'features'})
    df_summary = df_summary.sort_values(by="P>|t|", ascending=False)
    df_summary = df_summary.rename(columns={'P>|t|':'P-value'})
    df_summary = df_summary.reset_index().rename(columns={"index":"features"})
    return df_summary

