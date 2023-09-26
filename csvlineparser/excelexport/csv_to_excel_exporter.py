from __future__ import annotations

import logging
import sys

import pandas as pd

from csvlineparser.clientutils import csv_file_logger

# Uncomment to log to file
csv_file_logger.init()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CsvToExcelExporter:

    def __init__(self) -> None:
        super().__init__()

    def export_csv_to_excel(self, clean_csv_file_path: str, outfile_path: str) -> None:
        # reading csv file
        df = pd.read_csv(clean_csv_file_path)
        print(df.head())

        # saving xlsx file with auto column size
        writer = pd.ExcelWriter(outfile_path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='sheetName', index=False)

        for column in df:
            column_length = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets['sheetName'].set_column(col_idx, col_idx, column_length)

        writer.close()
