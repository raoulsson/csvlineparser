from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from io import StringIO

from csvlineparser.core.column_expander import ColumnExpander
from csvlineparser.core.csv_data_type_mapping import CsvDataTypeMapping

logger = logging.getLogger(__name__)

"""
[
    ['customer_email', 'string', True, False, None, None],
    ['billing_address_addressee', 'string', True, False, 'billing_address_name', None],
    ['billing_address_line1', 'string', True, False, None, None],
    ['line_item_subtotal', 'double', True, False, None,
     ColumnExpander(['line_item_subtotal', 'line_item_subtotal_ccy'], MyFieldSplitter())],
    ['text_area_name', 'string', False, True, None, None],
    ['text_area_data', 'string', False, False, 'customer_comment', None],
]"""
refDataColDef_v0_1_1 = None

expected_header_sha = "add sha256 of in file header here"


class ParsingConfig(ABC):
    """
    Cleans the in file.
    - Checks the header, on changes it fails fast.
    - Removes the header
    - Removes leading and trailing double quotes on each line
    - Replaces double, double quotes with single, double quotes
    - Replaces commas with double quotes with %COMMA%. This will have to be replaced back as soon as the CSV world can
    be left behind safely.
    We implement a subclass here to do the Swissmicros specifics
    """

    def __init__(self, column_definitions: list[list[str | bool | None] | list[str | bool | None | ColumnExpander]], expected_header_sha: str | None):
        super().__init__()
        self.column_definitions = column_definitions
        self.expected_header_sha = expected_header_sha

    @abstractmethod
    def include_headers(self) -> bool:
        pass

    @abstractmethod
    def aws_compatible(self):
        pass

    @abstractmethod
    def validate_input_header_line(self, header_line: str) -> None:
        """
        sha = sha256(header_line.encode('utf-8')).hexdigest()
        if sha != expected_header_sha:
            raise IllegalHeaderDataException(sha)
        """
        pass

    @abstractmethod
    def handle_lines(self, line: str, write_buffer: StringIO) -> str:
        """
        clean_line = line
        write_buffer.write(clean_line)
        return clean_line
        """
        pass

    @abstractmethod
    def handle_headers(self, line: str) -> str:
        return line

    @abstractmethod
    def provide_csv_datatype_mappings(self) -> dict[int, CsvDataTypeMapping]:
        """
        defs = {}
        row = 0
        for elem in refDataColDef_v0_1_1:
            c = 0
            col_name = 'n/a'
            data_type = None
            required = False
            ignored = False
            rename_to = None
            for val in elem:
                if c == 0:
                    col_name = val
                if c == 1:
                    data_type = val
                if c == 2:
                    required = val
                if c == 3:
                    ignored = val
                if c == 4:
                    rename_to = val
                if c == 5:
                    column_expander = val
                c += 1
            column_def = CsvDataTypeMapping(col_name, data_type, required, ignored, rename_to, column_expander)
            defs[row] = column_def
            row += 1
        return defs
        """
        pass

    @abstractmethod
    def post_action(self) -> None:
        pass
