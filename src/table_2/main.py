import pandas as pd

from table_2 import schema
from table_2 import utility

pd.options.display.width = pd.options.display.max_columns = 5000


def load_roles() -> pd.DataFrame:
    return pd.read_feather(utility.LATEST_DATA_ROOT / "table-2-roles.feather")


def filter_roles(roles: pd.DataFrame, keys: schema.Table2Roles) -> pd.DataFrame:
    keys = {k: v for k, v in keys if v}
    return roles[roles[keys.keys()].isin(keys).all(axis=1)]


if __name__ == '__main__':
    filter_keys = schema.Table2Roles(category=["Support"], subcategory=["SASUs"], hierarchy=["County"])
    r = filter_roles(load_roles(), filter_keys)
    print()
