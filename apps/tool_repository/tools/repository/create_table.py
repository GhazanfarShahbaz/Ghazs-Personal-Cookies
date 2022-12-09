# UNFINISHED -> Used for creating dynamic models and db files

# import os

# from typing import Dict

# SQL_ALCEMY_DATA_TYPES: Dict[str, str] = {
#     "Big Integer": "BigInteger",
#     "Bool": "Boolean",
#     "Date": "DateTime",
#     "Enum": "Enum",
#     "Float": "Float",
#     "Integer": "Interval",
#     "Large Binary": "Large Binary",
#     "Match Type": "MatchType",
#     "Numeric": "Numeric",
#     "PickleType": "PickleType",
#     "Schema Type": "SchemaType",
#     "Small Integer": "SmallInteger",
#     "String": "String",
#     "Text": "Text",
#     "Time": "Time",
#     "Unicode": "Unicode",
#     "Unicode Text": "UnicodeText"
# }


# def get_tab_string(tab: int) -> str:
#     return "\t"*tab


# def get_column_type_string(column_type_properties: dict) -> str:
#     column_type: str = column_type_properties["type"]

#     if column_type in {"String", "DateTime"}:
#         column_type = f"{column_type}({column_type_properties["type"]["additionalProperties"]})"

#     return column_type


# def get_column_string(column_properties: dict) -> str:
#     column_name: str = f"\"{column_properties["columnName"]}\""
#     column_type: str = get_column_type_string(column_properties["columnType"])
#     additional_properties: str = ""

#     for param, value in column_properties.items():
#         additional_properties += f". {param}={value}"

#     column_property_string: str = f"\{column_properties["columnName"]}\" "
#     return f"{column_name} = Column({column_name}, {column_type} {additional_properties})\n"


# # does not support parent child relationships yet
# def table_request_to_string(table_request: dict) -> str:
#     tab = 0
#     table_string: str = f"class {table_request["tableName"].title()}(Base):\n"

#     tab += 1
#     table_string += get_tab_string(tab) + f"__tablename__ = f"{table_request["tableName"].lower()}\"\n"
#     table_string += get_tab_string(tab) + \
#         get_column_string(table_request["keyColumn"])

#     for additional_column in table_request["additionalColumns"]:
#         table_string += get_tab_string(tab) + \
#             get_column_string(additional_column)

#     # init logic here

#     # to dict logic here

# # logic to create create, delete and update file for table here
