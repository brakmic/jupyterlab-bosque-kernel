from pygments.lexer import RegexLexer, bygroups
from pygments.token import Text, Comment, Keyword, Name, Operator, Punctuation, String, Number, Constant

# Based on https://github.com/BosqueLanguage/bosque-language-tools/blob/main/syntaxes/bosque.tmLanguage.json 

class BosqueLexer(RegexLexer):
    """
    A Pygments lexer for the Bosque programming language.
    """
    name = 'Bosque'
    url = 'https://bosque-lang.org'
    aliases = ['bosque', "bsq"]
    filenames = ['*.bsq']
    mimetypes = ['text/x-bosque']

    # Define keyword categories
    CONTROL_KEYWORDS = [
        'abort', 'assert', 'if', 'elif', 'else', 'fn', 'pred', 'let', 'match',
        'ref', 'return', 'switch', 'then', 'var', 'yield', 'ensures', 'invariant',
        'example', 'requires', 'validate', 'softcheck', 'errtest', 'chektest'
    ]

    OTHER_KEYWORDS = [
        'recursive', 'action', '_debug', 'bsqon', 'example', 'do', 'fail',
        'implements', 'debug', 'release', 'safety', 'spec', 'test', 'api',
        'as', 'concept', 'const', 'declare', 'enum', 'entity', 'ensures',
        'field', 'function', 'invariant', 'method', 'namespace', 'of',
        'provides', 'requires', 'in', 'task', 'datatype', 'using', 'validate',
        'when', 'event', 'status', 'resource', 'predicate', 'softcheck',
        'errtest', 'chektest', 'operator', 'variant'
    ]

    # Combine all keywords into a single list
    KEYWORDS = CONTROL_KEYWORDS + OTHER_KEYWORDS

    # Create regex patterns
    KEYWORDS_REGEX = r'\b(' + '|'.join(KEYWORDS) + r')\b'
    CONSTANTS_LANGUAGE_REGEX = r'\b(none|true|false|fail|ok|some|result|option|env|this|self)\b'
    CONSTANTS_NUMERIC_REGEX = r'\b(([0-9]+)[inIN])\b|\b((([0-9]+))[R]|(([0-9]+)/([0-9]+)[R]))\b|\b(([0-9]+\.[0-9]+([eE][-+]?[0-9]+)?[fd]))\b|\b([0-9]+)\b'
    TYPES_REGEX = r'\b((([A-Z][_a-zA-Z0-9]+)::)*([A-Z][_a-zA-Z0-9]+))\b|\b[A-Z]\b'
    VARIABLES_REGEX = r'\b([$]|([$]?([_a-z]|[_a-z][_a-zA-Z0-9]+)))\b'
    FUNCTION_NAME_REGEX = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*(?=\()'

    tokens = {
        'root': [
            (r'\s+', Text),  # Whitespace

            # Single-line comments: %%
            (r'%%.*$', Comment.Single),

            # Multi-line comments: %** ... *% and %* ... *%
            (r'%\*\*', Comment.Multiline, 'comment-multiline-double-dash'),
            (r'%\*', Comment.Multiline, 'comment-multiline'),

            # Double-quoted strings: "..."
            (r'"', String.Double, 'string-double'),

            # Single-quoted strings: '...'
            (r"'", String.Single, 'string-single'),

            # Keywords
            (KEYWORDS_REGEX, Keyword),

            # Language Constants
            (CONSTANTS_LANGUAGE_REGEX, Constant.Language),

            # Numeric Constants
            (CONSTANTS_NUMERIC_REGEX, Constant.Numeric),

            # Types
            (TYPES_REGEX, Name.Class),

            # Variables
            (VARIABLES_REGEX, Name.Variable),

            # Function names (identifier followed by '(')
            (FUNCTION_NAME_REGEX, Name.Function),

            # Operators
            (r'[+\-*/=<>!]+', Operator),

            # Punctuation
            (r'[{}()\[\];,]', Punctuation),
        ],

        # Multi-line comment with %**
        'comment-multiline-double-dash': [
            (r'\*%', Comment.Multiline, '#pop'),
            (r'[^*%]+', Comment.Multiline),
            (r'[*/%]+', Comment.Multiline),
        ],

        # Multi-line comment with %*
        'comment-multiline': [
            (r'\*%', Comment.Multiline, '#pop'),
            (r'[^*%]+', Comment.Multiline),
            (r'[*/%]+', Comment.Multiline),
        ],

        # Double-quoted string state
        'string-double': [
            (r'\\\'', String.Escape),                # Escaped single quote
            (r'\\.', String.Escape),                 # Other escape sequences
            (r'[^"\\]+', String.Double),             # Non-escape characters
            (r'"', String.Double, '#pop'),           # Closing quote
        ],

        # Single-quoted string state
        'string-single': [
            (r'\\"', String.Escape),                 # Escaped double quote
            (r'\\.', String.Escape),                 # Other escape sequences
            (r"[^'\\]+", String.Single),             # Non-escape characters
            (r"'", String.Single, '#pop'),           # Closing quote
        ],
    }
