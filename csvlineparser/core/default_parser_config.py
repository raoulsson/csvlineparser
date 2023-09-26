from __future__ import annotations

import logging
from hashlib import sha256
from io import StringIO

from csvlineparser.core.column_expander import ColumnExpander
from csvlineparser.core.csv_data_type_mapping import CsvDataTypeMapping
from csvlineparser.core.exceptions import IllegalHeaderDataException
from csvlineparser.core.parser_config import ParsingConfig

logger = logging.getLogger(__name__)


class DefaultParserConfig(ParsingConfig):

    def __init__(self, column_definitions: list[list[str | bool | None] | list[str | bool | None | ColumnExpander]], expected_header_sha: str | None):
        super().__init__(column_definitions, expected_header_sha)

    def include_headers(self) -> bool:
        return True

    def aws_compatible(self):
        return True

    def validate_input_header_line(self, header_line: str) -> None:
        if self.expected_header_sha is None:
            return
        sha = sha256(header_line.encode('utf-8')).hexdigest()
        if sha != self.expected_header_sha:
            raise IllegalHeaderDataException(sha)

    def handle_lines(self, line: str, write_buffer: StringIO) -> str:
        clean_line = line
        write_buffer.write(clean_line)
        return clean_line

    def handle_headers(self, line: str) -> str:
        return line

    def provide_csv_datatype_mappings(self) -> dict[int, CsvDataTypeMapping]:
        defs = {}
        row = 0
        for elem in self.column_definitions:
            c = 0
            col_name = 'n/a'
            data_type = None
            required = False
            ignored = False
            rename_to = None
            column_expander = None
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

    def post_action(self) -> None:
        # Nothing to do at end of process from our view
        pass
