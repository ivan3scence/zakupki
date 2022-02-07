import pandas as pd
import os
from openpyxl import load_workbook
# def paste_to_base(base_file):
#     base = pd.read_excel(base_file, sheet_name="1")
#     flag = pd.DataFrame({'Ссылка на Решение об одностороннем отказе от исполнения контракта':["01.10.2022"]})
#     # startrow = writer.sheets['Sheet1'].max_row
#     dfs = pd.read_excel("zakupki_30_01_2022.xlsx", sheet_name="1")
#     # print(dfs.to_dict())
#     res = pd.concat([flag, dfs])
#     res = base.append([flag, dfs])
#     res.to_excel(base_file, sheet_name="1", index=False, header=False)

# paste_to_base("zakupki_rastorjenie_base copy.xlsx")


df = pd.read_excel("zakupki_30_01_2022.xlsx", sheet_name="1")
# print(df)
with pd.ExcelWriter("zakupki_rastorjenie_base copy.xlsx", mode="a", engine="openpyxl", if_sheet_exists="new") as writer:
    df.to_excel(writer, sheet_name="1")

# append_df_to_excel("zakupki_rastorjenie_base copy.xlsx", df, sheet_name="1")