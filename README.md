# csvlineparser

A CSV Parser that cleans a messy CSV file, with optional Excel export...
The CSV Parser is based on a BNF grammar, and the parser is built using a recursive descent parser.
Parsing line by line, character by character...

See in example/example_parser.py and the files in the in and out folders.

### From the Example

```python
def main():
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

    """ At least the column_definitions are required to build the parser config """
    default_parser_config = DefaultParserConfig(column_definition, expected_header_sha)

    csv_line_parser = CsvLineParser(default_parser_config)
    csv_line_parser.parse_csv(in_file_path, out_file_path, out_excel_path)


if __name__ == '__main__':
    main()
```


### Background

Based on https://secondboyet.com/articles/csvparser.html by Julian M Bucknall, rewritten in Python by raoulsson.

BNF Grammar:

    csvFile ::= (csvRecord)* 'EOF'
    csvRecord ::= csvStringList ('\n' | 'EOF')
    csvStringList ::= rawString [',' csvStringList]
    rawString := optionalSpaces [rawField optionalSpaces)]
    optionalSpaces ::= whitespace*
    whitespace ::= ' ' | '\t'
    rawField ::= simpleField | quotedField 
    simpleField ::= (any char except \n, EOF, \t, space, comma or double quote)+
    quotedField ::= '"' escapedField '"'
    escapedField ::= subField ['"' '"' escapedField]
    subField ::= (any char except double quote or EOF)+

## Installation

    Clone and run 'make init'. Or, without cloning, to install it as a module, 
    'pip install csvlineparser' should work as well...

    Also make sure to have these packages installed:
        - openpyxl
        - xlsxwriter
        - pandas