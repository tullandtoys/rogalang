from __future__ import annotations
from typing import List
import pandas as pd
import re
import sys


with open("semantics/semantics.csv", "r") as f:
    semantics = pd.read_csv(f)[["js", "rogalang"]].dropna()

if semantics is None or semantics.empty:
    raise ValueError("Failed to load semantics from semantics.csv or file is empty")

semantics_dict = {row["rogalang"]: row["js"] for _, row in semantics.iterrows()}

MAX_LINES_BETWEEN_HERLIGA_LONDON = 10
JILLE_PREFIX = re.compile(r"^\s*jille\s+")


def validate_and_preprocess_rogalang(lines: List[str]) -> List[str]:
    """
    Validate Rogalang source and preprocess by removing herliga london and jille prefix.

    Args:
        lines: List of lines from the Rogalang source file

    Returns:
        Preprocessed lines ready for transpilation

    Raises:
        ValueError: If validation fails
    """
    #########################################################################
    # Check that no line is more than 10 lines away from a 'herliga london' #
    #########################################################################

    # Generate a list of line indices where 'herliga london' appears
    herliga_indices = [
        i for i, line in enumerate(lines) if line.rstrip("\r\n") == "herliga london"
    ]

    if not herliga_indices:
        raise ValueError("No 'herliga london' found in source file")

    # Check first line is 'herliga london'
    if herliga_indices[0] != 0:
        raise ValueError("First line must be 'herliga london'")

    # Check lines after last herliga london
    if len(lines) - 1 - herliga_indices[-1] > MAX_LINES_BETWEEN_HERLIGA_LONDON:
        raise ValueError(
            f"Last 'herliga london' at line {herliga_indices[-1] + 1} is more than {MAX_LINES_BETWEEN_HERLIGA_LONDON} lines from end"
        )

    # Check distance between consecutive herliga london lines
    if len(herliga_indices) > 1:
        gaps = [
            (x1, x2, x2 - x1) for x1, x2 in zip(herliga_indices, herliga_indices[1:])
        ]
        max_gap = max(gaps, key=lambda x: x[2])
        if max_gap[2] > MAX_LINES_BETWEEN_HERLIGA_LONDON:
            raise ValueError(
                f"Gap of {max_gap[2]} lines between 'herliga london' at lines {max_gap[0] + 1} and {max_gap[1] + 1}"
            )

    ########################################################################
    # Remove lines that do not start with 'jille' including herliga london #
    ########################################################################

    processed_lines = [
        JILLE_PREFIX.sub("", ln) for ln in lines if JILLE_PREFIX.match(ln)
    ]
    return processed_lines


###########################
# Process string literals #
###########################

STRING_LITERALS: List[StringLiteral] = []

# Matches:
# - backtick-delimited strings with real newlines
# - double/single-quoted strings without real newlines
STRING_REGEX = re.compile(
    r"(?:`(?:\\.|[\s\S])*`|\"(?:\\.|[^\\\"\n])*\"|'(?:\\.|[^\\'\n])*')"
)

# Matches template expressions like ${exp}
STRING_TEMPLATE_EXPRESSION_REGEX = re.compile(r"\$\{[^\}]*\}")


class StringLiteral:
    """A string literal in Rogalang"""

    def __init__(self, content: str):
        self.string_template_expressions = []

        # Determine quoting style to decide if this is a template literal
        self.quote_char = content[0] if content else ""
        self.is_template = self.quote_char == "`"

        if self.is_template:
            template_expressions = STRING_TEMPLATE_EXPRESSION_REGEX.findall(content)
            for exp in template_expressions:
                # replace the exp in ${exp} with a placeholder index
                content = content.replace(
                    exp, f"${{{len(self.string_template_expressions)}}}"
                )
                # remove the ${ and }
                exp = exp[2:-1]
                # Recursively transpile the template expression
                transpiled_exp = transpile_rogalang(exp)
                self.string_template_expressions.append(transpiled_exp)

        # Persist the content
        self.content = content

    def __str__(self):
        # Only expand placeholders for template literals
        if not self.is_template:
            return self.content

        content = self.content
        for i, exp in enumerate(self.string_template_expressions):
            content = content.replace(f"${{{i}}}", f"${{{exp}}}")
        return content

    def __repr__(self):
        return str(self)


def transpile_rogalang(content: str, _reset_state: bool = False) -> str:
    """
    Transpile Rogalang code to JavaScript.
    This function can be called recursively on template expressions.

    Args:
        content: The Rogalang code to transpile
        _reset_state: Internal flag to reset global state (used for top-level calls)

    Returns:
        The transpiled JavaScript code
    """
    # Reset global state for top-level calls to enable independent test runs
    global STRING_LITERALS
    if _reset_state:
        STRING_LITERALS = []

    # Replace all ) with _) to avoid confusion with the string literal syntax
    full_content = content.replace(")", "_)")
    new_content = ""
    last_position = 0

    # Extract all string literals and add them to the global STRING_LITERALS list
    for match in STRING_REGEX.finditer(full_content):
        before = f".({full_content[last_position : match.start()]}.)"
        new_content += f"{before} str{len(STRING_LITERALS)}"
        STRING_LITERALS.append(StringLiteral(match.group()))
        last_position = match.end()
    full_content = new_content + f".({full_content[last_position:]}.)"

    # Replace all tokens with their semantics, ensuring they're delimited
    # Only include delimiters that exist in Rogalang (not replaced by semantics.csv)
    delimiter_chars = r"\s(){}[\];,.?:"

    for rogalang_token in sorted(semantics_dict, key=len, reverse=True):
        if not rogalang_token:
            continue
        escaped_token = re.escape(rogalang_token)
        # Use word boundaries: match token only when surrounded by delimiters
        # We need to keep the delimiter before the token
        pattern = f"(^|[{delimiter_chars}]){escaped_token}(?=[{delimiter_chars}]|$)"

        def replace_with_delimiter(match):
            return match.group(1) + semantics_dict[rogalang_token]

        full_content = re.sub(pattern, replace_with_delimiter, full_content)

    # Insert string literals back in between code delimiters (pattern: ".(xyz.) str1 .(abc.) str2")
    INSIDE_CODE_REGEX = re.compile(r"\.\(.*?\.\)", re.DOTALL)
    matches = list(INSIDE_CODE_REGEX.finditer(full_content))
    new_content = ""
    for i, match in enumerate(matches):
        # Add the current match
        new_content += match.group()

        # If there's a next match, process the content between them
        if i < len(matches) - 1:
            between = full_content[match.end() : matches[i + 1].start()]
            # Extract string literal index from "str{N}"
            if between.strip().startswith("str"):
                str_index = int(between.strip()[3:])
                new_content += str(STRING_LITERALS[str_index])
            else:
                new_content += between

    # Add any content before first match
    if matches:
        new_content = full_content[: matches[0].start()] + new_content
        # Add any content after last match
        new_content += full_content[matches[-1].end() :]
    else:
        new_content = full_content

    full_content = new_content

    # Remove code delimiters
    full_content = full_content.replace(".(", "").replace(".)", "").replace("_)", ")")

    return full_content


if __name__ == "__main__":
    with open("helloWorld.rl", "r") as f:
        lines = f.readlines()

    # Validate and preprocess the source
    processed_lines = validate_and_preprocess_rogalang(lines)

    # Transpile the main content (template expressions are transpiled recursively during StringLiteral creation)
    full_content = transpile_rogalang("".join(processed_lines), _reset_state=True)
    print(full_content)
