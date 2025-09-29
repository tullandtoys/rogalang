"""
Comprehensive test suite for the Rogalang transpiler.
Run with: python test_transpiler.py
"""

import unittest
from transpiler import (
    transpile_rogalang,
    validate_and_preprocess_rogalang,
    StringLiteral,
    STRING_LITERALS,
)


class TestBasicTokenReplacement(unittest.TestCase):
    """Test basic keyword/token replacement."""

    def test_const_keyword(self):
        result = transpile_rogalang("konst a æ 5", _reset_state=True)
        self.assertEqual(result, "const a = 5")

    def test_for_loop(self):
        result = transpile_rogalang("for kvar einaste(x i arr) {}", _reset_state=True)
        self.assertEqual(result, "for(x in arr) {}")

    def test_console_log(self):
        result = transpile_rogalang("sei('hello')", _reset_state=True)
        self.assertEqual(result, "console.log('hello')")

    def test_if_statement(self):
        result = transpile_rogalang("viss(x græla likt mæ y) {}", _reset_state=True)
        self.assertEqual(result, "if(x === y) {}")

    def test_comparison_operators(self):
        result = transpile_rogalang("a græla større enn b", _reset_state=True)
        self.assertEqual(result, "a > b")

    def test_logical_operators(self):
        result = transpile_rogalang("a AO b", _reset_state=True)
        self.assertEqual(result, "a && b")

        result = transpile_rogalang("a ELLE b", _reset_state=True)
        self.assertEqual(result, "a || b")


class TestStringLiterals(unittest.TestCase):
    """Test string literal handling."""

    def test_single_quoted_string(self):
        result = transpile_rogalang("konst a æ 'hello'", _reset_state=True)
        self.assertEqual(result, "const a = 'hello'")

    def test_double_quoted_string(self):
        result = transpile_rogalang('konst a æ "hello"', _reset_state=True)
        self.assertEqual(result, 'const a = "hello"')

    def test_keywords_inside_strings_not_replaced(self):
        result = transpile_rogalang(
            "konst msg æ 'konst is a keyword'", _reset_state=True
        )
        self.assertEqual(result, "const msg = 'konst is a keyword'")

    def test_template_literal_basic(self):
        result = transpile_rogalang("konst msg æ `hello`", _reset_state=True)
        self.assertEqual(result, "const msg = `hello`")

    def test_template_literal_with_expression(self):
        result = transpile_rogalang("sei(`sum: ${2 aog mæ  2}`)", _reset_state=True)
        self.assertEqual(result, "console.log(`sum: ${2 + 2}`)")

    def test_template_literal_with_variable(self):
        result = transpile_rogalang("sei(`name: ${name}`)", _reset_state=True)
        self.assertEqual(result, "console.log(`name: ${name}`)")

    def test_string_with_escaped_quotes(self):
        result = transpile_rogalang(r"konst a æ 'it\'s'", _reset_state=True)
        self.assertEqual(result, r"const a = 'it\'s'")


class TestDelimiterChecking(unittest.TestCase):
    """Test that tokens are only replaced when properly delimited."""

    def test_token_not_in_middle_of_word(self):
        # "konst" should be replaced, but not if it's part of "konstant"
        result = transpile_rogalang("konst konstant æ 5", _reset_state=True)
        self.assertEqual(result, "const konstant = 5")

    def test_operator_as_delimiter(self):
        result = transpile_rogalang("konst a æ b aog mæ  c", _reset_state=True)
        self.assertEqual(result, "const a = b + c")

    def test_parentheses_as_delimiter(self):
        # Test that keyword inside parentheses is replaced
        result = transpile_rogalang("viss(a æ b)", _reset_state=True)
        self.assertEqual(result, "if(a = b)")

    def test_brackets_as_delimiter(self):
        result = transpile_rogalang("arr[konst]", _reset_state=True)
        self.assertEqual(
            result, "arr[const]"
        )  # "konst" between brackets should be replaced


class TestHerligaLondonValidation(unittest.TestCase):
    """Test validation of 'herliga london' requirements."""

    def test_valid_source_single_herliga_london(self):
        lines = ["herliga london\n", "jille konst a æ 5\n"]
        result = validate_and_preprocess_rogalang(lines)
        self.assertEqual(result, ["konst a æ 5\n"])

    def test_valid_source_multiple_herliga_london(self):
        lines = [
            "herliga london\n",
            "jille konst a æ 5\n",
            "herliga london\n",
            "jille konst b æ 10\n",
        ]
        result = validate_and_preprocess_rogalang(lines)
        self.assertEqual(result, ["konst a æ 5\n", "konst b æ 10\n"])

    def test_missing_herliga_london(self):
        lines = ["jille konst a æ 5\n"]
        with self.assertRaises(ValueError) as ctx:
            validate_and_preprocess_rogalang(lines)
        self.assertIn("No 'herliga london' found", str(ctx.exception))

    def test_first_line_not_herliga_london(self):
        lines = ["jille konst a æ 5\n", "herliga london\n"]
        with self.assertRaises(ValueError) as ctx:
            validate_and_preprocess_rogalang(lines)
        self.assertIn("First line must be 'herliga london'", str(ctx.exception))

    def test_gap_too_large_between_herliga_london(self):
        lines = ["herliga london\n"] + ["jille x\n"] * 11 + ["herliga london\n"]
        with self.assertRaises(ValueError) as ctx:
            validate_and_preprocess_rogalang(lines)
        self.assertIn("Gap of", str(ctx.exception))

    def test_too_many_lines_after_last_herliga_london(self):
        lines = ["herliga london\n"] + ["jille x\n"] * 11
        with self.assertRaises(ValueError) as ctx:
            validate_and_preprocess_rogalang(lines)
        self.assertIn("more than 10 lines from end", str(ctx.exception))


class TestJillePrefix(unittest.TestCase):
    """Test jille prefix removal and line filtering."""

    def test_removes_jille_prefix(self):
        lines = ["herliga london\n", "jille konst a æ 5\n"]
        result = validate_and_preprocess_rogalang(lines)
        self.assertEqual(result, ["konst a æ 5\n"])

    def test_filters_out_non_jille_lines(self):
        lines = [
            "herliga london\n",
            "jille konst a æ 5\n",
            "this is a comment\n",
            "jille konst b æ 10\n",
        ]
        result = validate_and_preprocess_rogalang(lines)
        self.assertEqual(result, ["konst a æ 5\n", "konst b æ 10\n"])

    def test_handles_whitespace_before_jille(self):
        lines = ["herliga london\n", "  jille konst a æ 5\n"]
        result = validate_and_preprocess_rogalang(lines)
        self.assertEqual(result, ["konst a æ 5\n"])


class TestComplexExamples(unittest.TestCase):
    """Test realistic, complex code examples."""

    def test_complete_for_loop_with_string(self):
        code = """for kvar einaste(item i items) {
    sei(item)
}"""
        expected = """for(item in items) {
    console.log(item)
}"""
        result = transpile_rogalang(code, _reset_state=True)
        self.assertEqual(result, expected)

    def test_nested_if_else(self):
        code = """viss(a græla større enn b) {
    sei('a wins')
} elle {
    sei('b wins')
}"""
        expected = """if(a > b) {
    console.log('a wins')
} else {
    console.log('b wins')
}"""
        result = transpile_rogalang(code, _reset_state=True)
        self.assertEqual(result, expected)

    def test_array_with_template_literal(self):
        # Note: "i" is the Rogalang keyword for "in", so it gets transpiled
        code = "konst arr æ [`item ${index}`, 'test']"
        expected = "const arr = [`item ${index}`, 'test']"
        result = transpile_rogalang(code, _reset_state=True)
        self.assertEqual(result, expected)

    def test_complex_expression_in_template(self):
        code = "sei(`result: ${a aog mæ  b gange me 2}`)"
        expected = "console.log(`result: ${a + b * 2}`)"
        result = transpile_rogalang(code, _reset_state=True)
        self.assertEqual(result, expected)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and potential problem areas."""

    def test_empty_string(self):
        result = transpile_rogalang("", _reset_state=True)
        self.assertEqual(result, "")

    def test_only_whitespace(self):
        result = transpile_rogalang("   \n  \t  ", _reset_state=True)
        self.assertEqual(result, "   \n  \t  ")

    def test_multiple_spaces_preserved(self):
        result = transpile_rogalang("konst  a  æ  5", _reset_state=True)
        self.assertEqual(result, "const  a  =  5")

    def test_newlines_preserved(self):
        code = "konst a æ 5\nkonst b æ 10"
        expected = "const a = 5\nconst b = 10"
        result = transpile_rogalang(code, _reset_state=True)
        self.assertEqual(result, expected)

    def test_mixed_quotes_in_string(self):
        code = '''konst msg æ "it's a 'test'"'''
        expected = '''const msg = "it's a 'test'"'''
        result = transpile_rogalang(code, _reset_state=True)
        self.assertEqual(result, expected)

    def test_parentheses_escaping(self):
        # Test the _) hack for parentheses
        code = "sei(test)"
        expected = "console.log(test)"
        result = transpile_rogalang(code, _reset_state=True)
        self.assertEqual(result, expected)


class TestStressTest(unittest.TestCase):
    """Stress test with complex, realistic programs."""

    def test_large_program_with_nested_templates(self):
        """Test a complex program with nested template literals and various edge cases."""
        code = """konst users æ [
    {name: 'Alice', age: 30},
    {name: 'Bob', age: 25}
]

konst greeting æ 'Hei'
konst punctuation æ '!'

for kvar einaste(user i users) {
    viss(user.age græla større enn 26) {
        konst msg æ `${greeting}, ${user.name}${punctuation}`
        sei(msg)
        
        konst nestedTemplate æ `User info: ${`Name: ${user.name}, Age: ${user.age}`}`
        sei(nestedTemplate)
        
        konst complexExpression æ `Result: ${user.age aog mæ  5 gange me 2 ta i frå 10}`
        sei(complexExpression)
    } elle viss(user.age græla likt mæ 25) {
        sei(`Exactly ${user.age} years old: ${`Details for ${user.name}`}`)
    } elle {
        sei('Too young')
    }
}

konst multiline æ `Dette e
ein multiline
template literal mæ ${greeting} i den`

sei(multiline)

konst arr æ ['item1', "item2", `item3 ${greeting}`]
for kvar einaste(item i arr) {
    sei(`Processing: ${item}`)
}

konst complex æ `Outer: ${`Middle: ${`Inner: ${greeting}`}`}`
sei(complex)

konst withOperators æ `Sum: ${10 aog mæ  20}, Product: ${5 gange me 3}, Compare: ${10 græla større enn 5}`
sei(withOperators)

viss(greeting græla likt mæ 'Hei' AO punctuation græla likt mæ '!') {
    sei(`Both conditions ${`are ${`truly ${`met`}`}`}`)
}

konst escaped æ 'It\\'s a test'
konst doubleEscaped æ `Message: ${`Quote: ${escaped}`}`
sei(doubleEscaped)"""

        expected = """const users = [
    {name: 'Alice', age: 30},
    {name: 'Bob', age: 25}
]

const greeting = 'Hei'
const punctuation = '!'

for(user in users) {
    if(user.age > 26) {
        const msg = `${greeting}, ${user.name}${punctuation}`
        console.log(msg)
        
        const nestedTemplate = `User info: ${`Name: ${user.name}, Age: ${user.age}`}`
        console.log(nestedTemplate)
        
        const complexExpression = `Result: ${user.age + 5 * 2 - 10}`
        console.log(complexExpression)
    } else if(user.age === 25) {
        console.log(`Exactly ${user.age} years old: ${`Details for ${user.name}`}`)
    } else {
        console.log('Too young')
    }
}

const multiline = `Dette e
ein multiline
template literal mæ ${greeting} i den`

console.log(multiline)

const arr = ['item1', "item2", `item3 ${greeting}`]
for(item in arr) {
    console.log(`Processing: ${item}`)
}

const complex = `Outer: ${`Middle: ${`Inner: ${greeting}`}`}`
console.log(complex)

const withOperators = `Sum: ${10 + 20}, Product: ${5 * 3}, Compare: ${10 > 5}`
console.log(withOperators)

if(greeting === 'Hei' && punctuation === '!') {
    console.log(`Both conditions ${`are ${`truly ${`met`}`}`}`)
}

const escaped = 'It\\'s a test'
const doubleEscaped = `Message: ${`Quote: ${escaped}`}`
console.log(doubleEscaped)"""

        result = transpile_rogalang(code, _reset_state=True)
        self.assertEqual(result, expected)

    def test_deeply_nested_template_literals(self):
        """Test template literals nested 4 levels deep."""
        code = "konst deep æ `L1: ${`L2: ${`L3: ${`L4: hello`}`}`}`"
        expected = "const deep = `L1: ${`L2: ${`L3: ${`L4: hello`}`}`}`"
        result = transpile_rogalang(code, _reset_state=True)
        self.assertEqual(result, expected)

    def test_template_with_all_operator_types(self):
        """Test template literals containing various Rogalang operators."""
        code = """konst test æ `
Arithmetic: ${a aog mæ  b ta i frå c gange me d delt me e}
Comparison: ${x græla større enn y AO z græla mindre enn w}
Logical: ${p AO q ELLE r}
Assignment: Would be outside template
`"""
        expected = """const test = `
Arithmetic: ${a + b - c * d / e}
Comparison: ${x > y && z < w}
Logical: ${p && q || r}
Assignment: Would be outside template
`"""
        result = transpile_rogalang(code, _reset_state=True)
        self.assertEqual(result, expected)

    def test_mixed_string_types_with_templates(self):
        """Test mixing single quotes, double quotes, and template literals."""
        code = """konst single æ 'single'
konst double æ "double"
konst template æ `template ${single} and ${double}`
konst nested æ `outer ${"inner double"} and ${'inner single'} mixed`"""
        expected = """const single = 'single'
const double = "double"
const template = `template ${single} and ${double}`
const nested = `outer ${"inner double"} and ${'inner single'} mixed`"""
        result = transpile_rogalang(code, _reset_state=True)
        self.assertEqual(result, expected)

    def test_template_with_special_characters(self):
        """Test template literals with special characters and edge cases."""
        code = r"""konst special æ `Test: ${a}, ${b}, ${c}`
konst withNewline æ `Line1
Line2 ${x}
Line3`
konst withTab æ `Tab	here ${y}`"""
        expected = r"""const special = `Test: ${a}, ${b}, ${c}`
const withNewline = `Line1
Line2 ${x}
Line3`
const withTab = `Tab	here ${y}`"""
        result = transpile_rogalang(code, _reset_state=True)
        self.assertEqual(result, expected)


class TestStateIsolation(unittest.TestCase):
    """Test that global state is properly reset between calls."""

    def test_independent_transpilation_calls(self):
        # Test that independent calls with reset produce correct results
        # This indirectly tests that state is reset properly
        code1 = "konst msg1 æ 'first'"
        code2 = "konst msg2 æ 'second'"

        result1 = transpile_rogalang(code1, _reset_state=True)
        result2 = transpile_rogalang(code2, _reset_state=True)

        # Each should produce correct independent results
        self.assertEqual(result1, "const msg1 = 'first'")
        self.assertEqual(result2, "const msg2 = 'second'")

        # Running the same code again should produce the same result
        result1_again = transpile_rogalang(code1, _reset_state=True)
        self.assertEqual(result1, result1_again)

    def test_multiple_calls_produce_same_result(self):
        code = "konst a æ 'hello'"
        result1 = transpile_rogalang(code, _reset_state=True)
        result2 = transpile_rogalang(code, _reset_state=True)
        self.assertEqual(result1, result2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
