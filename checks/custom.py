
def check_duplicates_ids(df, tag_column='tag', value_column='value', regex='id[0-9].@root'):
    """
    Checks if there are duplicates of 'id' tags within a component. If there are duplicates within each component,
    return True and the associated title of the component. If there are no duplicates, return False.

    :param df: DataFrame of component in flattened XML (e.g. immunizations, advance directives etc.)
    :type df: pd.DataFrame()
    :param tag_column: key column name of dataframe
    :type tag_column: str
    :param value_column: value column name of dataframe
    :type value_column: str
    :param regex: regex pattern to find the root attribute within id tags
    :type regex: str
    :return: (True/False, title of component)
    :rtype: tuple(boolean, str)
    """
    new_df = df[df[tag_column].str.contains(regex, regex=True)]
    title = df.loc[df[tag_column] == 'title', value_column].values[0]
    duplicated = new_df[new_df.duplicated(subset=value_column)]
    if not duplicated.empty:
        return (title, "Duplicates are present")
    else:
        return (title, "No Duplicates")


