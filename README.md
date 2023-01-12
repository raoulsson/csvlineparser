# csvlineparser

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

