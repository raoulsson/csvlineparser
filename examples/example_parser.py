from __future__ import annotations

import logging
import sys

from csvlineparser.clientutils import csv_file_logger
from csvlineparser.clientutils.file_handler import FileHandler
from csvlineparser.core.column_expander import ColumnExpander
from csvlineparser.core.csvlineparser import CsvLineParser
from csvlineparser.core.default_parser_config import DefaultParserConfig
from examples.price_ccy_splitter import PriceCCYSplitter
from examples.year_month_day_splitter import YearMonthDaySplitter

# uncomment to log to file
csv_file_logger.init()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    """ example, parsing a csv file """
    logger.info('Running example')

    """ Specify the input and output file paths """
    in_file_path = 'in/sample-raw-input.csv'
    out_file_path = 'out/sample-clean.csv'
    """ Optionally add an excel output file """
    out_excel_path = 'out/sample-clean.xlsx'

    """
    Build the sha256 of the header column to make sure the input file has the expected header. Especially useful if
    the input file is provided by a third party or different occasions, when the input might have changed over time.
    """
    expected_header_sha = "c551587bfca31449332989a377d59eb5f7bb6f1fb39dce862930094340299723"

    """
    Per column, specify the original name in the csvfile, the datatype, if the column is required, if the column should 
    be ignored, a possible rename and a column expander. The column expander is used to split a column into multiple
    new cells. 
    
    In the example, we rename the misspelled column 'stattus' to 'status', and we split the column 'created_on' into 
    three new columns 'created_on_year', 'created_on_month' and 'created_on_day'. We also split the column 'subtotal'
    into two new columns 'subtotal' and 'subtotal_ccy'. And the column 'tax' is ignored, because it is not needed.
    """
    column_definition = [
        ['order_id', 'string', True, False, None, None],
        ['stattus', 'string', True, False, 'status', None],
        ['created_on', 'datetime', True, False, None, ColumnExpander(['created_on', 'created_on_year', 'created_on_month', 'created_on_day'], YearMonthDaySplitter())],
        ['customer_name', 'string', True, False, None, None],
        ['items_count', 'int', True, False, None, None],
        ['subtotal', 'double', True, False, None, ColumnExpander(['subtotal', 'subtotal_ccy'], PriceCCYSplitter())],
        ['tax', 'double', True, True, None, None],
        ['discounts_total', 'double', True, False, None, ColumnExpander(['discounts_total', 'discounts_total_ccy'], PriceCCYSplitter())],
        ['customer_comment', 'string', False, False, None, None],
    ]

    file_handler = FileHandler()
    if file_handler.file_exists(out_file_path):
        file_handler.delete_file(out_file_path)

    """ At least the column_definitions are required to build the parser config """
    default_parser_config = DefaultParserConfig(column_definition, expected_header_sha)

    csv_line_parser = CsvLineParser(default_parser_config)
    csv_line_parser.parse_csv(in_file_path, out_file_path, out_excel_path)


if __name__ == '__main__':
    main()
