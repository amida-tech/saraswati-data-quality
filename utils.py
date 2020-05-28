import pandas as pd
import xmltodict
from collections import OrderedDict


def CCDAIngest(filepath):
    """
    Ingest C-CDA xml files and parse them into a pandas DataFrame.

    The Pandas DataFrame will contain two columns, tag and value. Tag represents each tag parsed from the XML, value
    represents the value from that tag.

    Within tag, there are items prepended by a '@' or '.'. @ represents an attribute, and '.' represents the next level
    in the nested XML

    :param filepath: filepath to C-CDA file
    :type filepath: str
    :return: DataFrame with two columns, tag and value
    :rtype: pd.DataFrame()
    """
    agg = []

    with open(filepath, 'rb') as f:
        xml_content = xmltodict.parse(f)

    flattened_xml = flatten_dict(xml_content)

    for k,v in flattened_xml.items():
        agg.append((k,v))

    return pd.DataFrame(agg, columns=['tag', 'value'])

def CCDAIngest_fromstring(XML):
    """
    Ingest C-CDA xml files and parse them into a pandas DataFrame.

    The Pandas DataFrame will contain two columns, tag and value. Tag represents each tag parsed from the XML, value
    represents the value from that tag.

    Within tag, there are items prepended by a '@' or '.'. @ represents an attribute, and '.' represents the next level
    in the nested XML

    :param filepath: filepath to C-CDA file
    :type filepath: str
    :return: DataFrame with two columns, tag and value
    :rtype: pd.DataFrame()
    """
    agg = []

    xml_content = xmltodict.parse(XML)

    flattened_xml = flatten_dict(xml_content)

    for k, v in flattened_xml.items():
        agg.append((k, v))

    return pd.DataFrame(agg, columns=['tag', 'value'])

def find_nested_indexes(CCDA):
    """
    The outputs of CCDAIngest() will have items that are of type 'list', these are instances where further nesting
    in the xml was not parsed by the initial parser. This function finds those items so that they can be processed further

    :param CCDA: DataFrame output from CCDAIngest()
    :type CCDA: pd.DataFrame()
    :return: list of indexes where values are of type 'list'
    :rtype: list
    """
    nested_indexes = []

    for i, val in enumerate(CCDA.value):
        if type(val) == list:
            nested_indexes.append(i)

    return nested_indexes

def get_components(CCDA, nested_indexes, key='tag'):
    nested_ccda_df = CCDA.loc[nested_indexes]
    index = nested_ccda_df[nested_ccda_df[key].str.contains('component')].index
    return nested_ccda_df.loc[index[0]].value

def flatten_dict(d):
    """
    Recursively flattens C-CDA(XML). This function will roughly flatten out the C-CDA into a series of key value pairs.
    Each key is a tag within the XML, and each value is the associated value with that tag.

    NOTE: repeated tags in the same level (e.g. Informants, Components, Particiapnts) will be grouped into one key,
    and have a list of values (one for each repeated tag)

    :param d: C-CDA(XML) parsed into dict
    :type d: dict
    :return: list of key value pairs that represent each tag and its associated value
    :rtype: OrderedDict
    """
    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten_dict(value).items():
                    yield key + "." + subkey, subvalue
            else:
                yield key, value

    return OrderedDict(items())


def flatten_dict_detailed(d):
    """
    Extension of flatten_dict() written to parse the nested items (from repeated tags at the same level) into a completely
    flat XML structure.

    :param d:
    :type d: dict
    :return: list of key value pairs that represent each tag and its associated value
    :rtype: OrderedDict
    """
    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for i, (subkey, subvalue) in enumerate(flatten_dict_detailed(value).items()):
                    yield key + f'{i}' + "." + subkey, subvalue

            elif isinstance(value, list):
                for i, val in enumerate(value):
                    if isinstance(val, str):
                        yield key + f'{i}', val
                    if isinstance(val, dict):
                        for subkey, subvalue in flatten_dict_detailed(val).items():
                            yield key + f'{i}' + "." + subkey, subvalue
                    if isinstance(val, list):
                        yield flatten_dict_detailed(val)

            else:
                yield key, value

    return OrderedDict(items())
