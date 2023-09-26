from __future__ import annotations

from io import StringIO

from csvlineparser.clientutils.aware_csv_context_provider import AwareCsvContextProvider
from csvlineparser.clientutils.csv_cleaner_consumer import CsvCleanerConsumer
from csvlineparser.clientutils.file_handler import FileHandler
from csvlineparser.core.char_tokenizer import StringCharTokenizer
from csvlineparser.core.csv_parser import CsvParser
from csvlineparser.core.parser_config import ParsingConfig
from csvlineparser.excelexport.csv_to_excel_exporter import CsvToExcelExporter


class CsvLineParser:

    def __init__(self, parser_config: ParsingConfig):
        self.__file_handler = FileHandler()
        self.__config = parser_config

    def parse_csv(self, in_file_path: str, out_file_path: str, out_excel_path: str | None) -> None:
        with open(in_file_path, mode='r', encoding='UTF-8') as f:
            first_line = f.readline().strip('\n')
            self.__config.validate_input_header_line(first_line)

        my_buffer: StringIO = self.__file_handler.load_text_file_to_buffer(in_file_path)
        write_buffer = StringIO()
        # We load all through the parser, if that works well, we then deliver the lines from memory to the writer
        sct = StringCharTokenizer(my_buffer.getvalue())
        # possibly load this from S3
        data_type_mappings = self.__config.provide_csv_datatype_mappings()
        # We double quote, quotes and put data in quotes that contain commas. For writing.
        cct = CsvCleanerConsumer(has_header=True,
                                 csv_context_provider=AwareCsvContextProvider(data_type_mappings=data_type_mappings,
                                                                              aws_compatible=self.__config.aws_compatible()))

        parser = CsvParser()
        parser.parse(sct, cct)

        # new_line_delimiter = os.linesep
        new_line_delimiter = "\r\n"  # Windows style line endings required by specification,  https://csvlint.io/

        line_count = 0
        for line in cct.get_all():
            if line_count == 0:
                clean_header_line: str = self.__config.handle_headers(line)
                if self.__config.include_headers():
                    write_buffer.write(clean_header_line)
                    write_buffer.write(new_line_delimiter)
            else:
                self.__config.handle_lines(line, write_buffer)
                write_buffer.write(new_line_delimiter)
            line_count += 1
        self.__file_handler.store_buffer_to_file(write_buffer, out_file_path)

        if out_excel_path is not None:
            if self.__file_handler.file_exists(out_excel_path):
                self.__file_handler.delete_file(out_excel_path)

            csv_to_excel_exporter = CsvToExcelExporter()
            csv_to_excel_exporter.export_csv_to_excel(out_file_path, out_excel_path)
