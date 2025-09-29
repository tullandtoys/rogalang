# Rogalang Language Documentation

## Table of Contents
- [Introduction](#introduction)
- [Language Philosophy](#language-philosophy)
- [Syntax Rules](#syntax-rules)
- [Keywords and Operators](#keywords-and-operators)
- [Data Types](#data-types)
- [Control Flow](#control-flow)
- [Functions](#functions)
- [Template Literals](#template-literals)
- [Examples](#examples)
- [Transpiler Implementation](#transpiler-implementation)

---

## Introduction

Rogalang is a Norwegian-inspired esoteric programming language that transpiles to JavaScript. It was created with the philosophy that programming should be an artform, not a chore.

### Why Rogalang?

- **Cultural Expression**: Write code in Norwegian-inspired syntax
- **Artistic Constraints**: Forced structure creates more mindful code
- **Fun Challenge**: Learn to think differently about programming
- **JavaScript Interop**: Compiles to standard JavaScript

---

## Language Philosophy

### The Three Pillars

1. **Herliga London** - Every program must pay homage to the great city with regular declarations
2. **Jille Everything** - Explicit line marking ensures intentional code
3. **CamelCase Purity** - No underscores allowed; embrace the camel!

### Design Goals

- Make programming feel more like creative writing
- Enforce regular rhythm in code structure
- Celebrate Norwegian linguistic heritage
- Transpile seamlessly to JavaScript

---

## Syntax Rules

### 1. The `jille` Prefix

Every executable line must start with `jille`:

```rogalang
jille konst x æ 5        ✓ Valid
konst x æ 5              ✗ Invalid (comment)
    jille konst x æ 5    ✓ Valid (whitespace before jille is ok)
```

**Lines without `jille` are treated as comments** and are ignored by the transpiler.

### 2. Herliga London Requirement

The phrase `herliga london` must appear:
- As the **first line** of every program
- At least **once every 10 lines**
- At least **once in the last 10 lines**

```rogalang
herliga london          ✓ Required first line

jille konst a æ 1
jille konst b æ 2
jille konst c æ 3
jille konst d æ 4
jille konst e æ 5
jille konst f æ 6
jille konst g æ 7
jille konst h æ 8

herliga london          ✓ Required within 10 lines

jille konst i æ 9
```

**Purpose**: This unique requirement ensures your code has rhythm and prevents monotonous programming.

### 3. CamelCase Enforcement

Underscores (`_`) are **forbidden** anywhere in Rogalang code:

```rogalang
jille konst myVariable æ 5         ✓ Valid
jille konst my_variable æ 5        ✗ Invalid
jille konst thisIsGood æ 10        ✓ Valid
```

### 4. Case Sensitivity

Rogalang is **case-insensitive** for the special keyword `herliga london`, but **case-sensitive** for all other keywords:

```rogalang
Herliga London    ✓ Valid
HERLIGA LONDON    ✓ Valid
herliga london    ✓ Valid

Jille konst x     ✗ Invalid (must be lowercase 'jille')
jille Konst x     ✗ Invalid (must be lowercase 'konst')
```

---

## Keywords and Operators

### Variable Declaration

| JavaScript | Rogalang | Example |
|------------|----------|---------|
| `const` | `konst` | `jille konst x æ 5` |
| `let` | `la` | `jille la y æ 10` |
| `var` | `greia` | `jille greia z æ 15` |

### Control Flow

| JavaScript | Rogalang | Example |
|------------|----------|---------|
| `if` | `viss` | `jille viss(x græla likt mæ 5)` |
| `else` | `elle` | `jille elle` |
| `for` | `for kvar einaste` | `jille for kvar einaste(i i arr)` |
| `while` | `imens` | `jille imens(x græla større enn 0)` |
| `do` | `gjer` | `jille gjer` |
| `switch` | `bytta` | `jille bytta(x)` |
| `case` | `tilfelle` | `jille tilfelle 1:` |
| `default` | `vanleg` | `jille vanleg:` |
| `break` | `gje deg` | `jille gje deg` |
| `continue` | `vidare` | `jille vidare` |

### Functions

| JavaScript | Rogalang | Example |
|------------|----------|---------|
| `function` | `arbeidskar` | `jille arbeidskar test()` |
| `return` | `spytt ud` | `jille spytt ud resultat` |
| `await` | `venta` | `jille venta getData()` |
| `yield` | `gje` | `jille gje verdi` |

### Classes and Objects

| JavaScript | Rogalang |
|------------|----------|
| `class` | `KLASSE` |
| `new` | `nye` |
| `this` | `deherane` |
| `extends` | `udvi` |
| `super` | `græla` |
| `static` | `stilleståane` |
| `implements` | `love å sjå ut som` |
| `interface` | `koss det ska sjå ut` |

### Visibility Modifiers

| JavaScript | Rogalang |
|------------|----------|
| `public` | `offentle` |
| `private` | `pillefygert` |
| `protected` | `gjømte` |

### Assignment Operators

| JavaScript | Rogalang | Meaning |
|------------|----------|---------|
| `=` | `æ` | Assign |
| `+=` | `øge mæ` | Add and assign |
| `-=` | `minke mæ` | Subtract and assign |
| `*=` | `ganges mæ` | Multiply and assign |
| `/=` | `deles mæ` | Divide and assign |
| `%=` | `moduleres mæ` | Modulo and assign |
| `**=` | `eksponensieres mæ` | Exponentiate and assign |

### Arithmetic Operators

| JavaScript | Rogalang | Meaning |
|------------|----------|---------|
| `+` | `aog mæ` | Add |
| `-` | `ta i frå` | Subtract |
| `*` | `gange me` | Multiply |
| `/` | `delt me` | Divide |
| `%` | `rest frå deling på` | Modulo |
| `++` | `aog mæ ein` | Increment |
| `--` | `trekk frå ein` | Decrement |

### Comparison Operators

| JavaScript | Rogalang | Meaning |
|------------|----------|---------|
| `==` | `likt mæ` | Equal |
| `===` | `græla likt mæ` | Strictly equal |
| `!=` | `græla ulikt` | Not equal |
| `!==` | `ulikt` | Strictly not equal |
| `>` | `græla større enn` | Greater than |
| `<` | `græla mindre enn` | Less than |
| `>=` | `større enn` | Greater than or equal |
| `<=` | `mindre enn` | Less than or equal |

### Logical Operators

| JavaScript | Rogalang |
|------------|----------|
| `&&` | `AO` |
| `\|\|` | `ELLE` |
| `!` | `INKJE` |

### Bitwise Operators

| JavaScript | Rogalang |
|------------|----------|
| `&` | `bedevis AO` |
| `\|` | `bedevis ELLE` |
| `^` | `bedevis betinga ombytting` |
| `~` | `bedevis INKJE` |
| `<<` | `venstreskift` |
| `>>` | `høgreskift` |
| `>>>` | `høgreskift usignert` |

### Special Values

| JavaScript | Rogalang |
|------------|----------|
| `true` | `forrektigt` |
| `false` | `raoaradl` |
| `null` | `inkje` |

### Built-in Functions

| JavaScript | Rogalang |
|------------|----------|
| `console.log` | `sei` |
| `typeof` | `typeof` |

### Module System

| JavaScript | Rogalang |
|------------|----------|
| `import` | `ta inn` |
| `export` | `send ud` |

### Error Handling

| JavaScript | Rogalang |
|------------|----------|
| `try` | `prøv` |
| `catch` | `fang` |
| `finally` | `endele` |
| `throw` | `heilt texas` |

---

## Data Types

Rogalang uses the same data types as JavaScript:

### Primitives

```rogalang
herliga london

jille konst nummer æ 42
jille konst tekst æ 'Hallo'
jille konst sannhet æ forrektigt
jille konst løgn æ raoaradl
jille konst ingenting æ inkje

herliga london
```

### Arrays

```rogalang
herliga london

jille konst liste æ [1, 2, 3, 4, 5]
jille konst ord æ ['hei', 'verden', 'fra', 'rogalang']

herliga london
```

### Objects

```rogalang
herliga london

jille konst person æ {
jille     navn: 'Ola',
jille     alder: 25,
jille     by: 'Stavanger'
jille }

herliga london
```

---

## Control Flow

### If-Else Statements

```rogalang
herliga london

jille konst alder æ 20

jille viss(alder græla større enn 18) {
jille     sei('Du e vaksen')
jille } elle {
jille     sei('Du e mindreårig')
jille }

herliga london
```

### For Loops

```rogalang
herliga london

jille konst tall æ [1, 2, 3, 4, 5]

jille for kvar einaste(nummer i tall) {
jille     sei(nummer)
jille }

herliga london
```

### While Loops

```rogalang
herliga london

jille la teller æ 0

jille imens(teller græla mindre enn 5) {
jille     sei(teller)
jille     teller aog mæ ein
jille }

herliga london
```

### Switch Statements

```rogalang
herliga london

jille konst dag æ 3

jille bytta(dag) {
jille     tilfelle 1:
jille         sei('Måndag')
jille         gje deg
jille     tilfelle 2:
jille         sei('Tysdag')
jille         gje deg
jille     tilfelle 3:
jille         sei('Onsdag')
jille         gje deg
jille     vanleg:
jille         sei('Ukjent dag')
jille }

herliga london
```

---

## Functions

### Function Declaration

```rogalang
herliga london

jille arbeidskar leggSammen(a, b) {
jille     spytt ud a aog mæ b
jille }

jille konst resultat æ leggSammen(5, 3)
jille sei(resultat)

herliga london
```

### Arrow Functions

```rogalang
herliga london

jille konst multipliser æ (a, b) => a gange me b

jille sei(multipliser(4, 5))

herliga london
```

### Async/Await

```rogalang
herliga london

jille async arbeidskar hentData() {
jille     konst data æ venta fetch('api.example.com')
jille     spytt ud data
jille }

herliga london
```

---

## Template Literals

Rogalang supports template literals with embedded expressions:

```rogalang
herliga london

jille konst navn æ 'Ola'
jille konst alder æ 25

jille sei(`Hei, eg heite ${navn} og eg e ${alder} år gamal`)

herliga london
```

Template expressions are recursively transpiled, so you can use Rogalang syntax inside them:

```rogalang
herliga london

jille konst a æ 5
jille konst b æ 3

jille sei(`Summen e ${a aog mæ b}`)

herliga london
```

### Multi-line Template Literals

```rogalang
herliga london

jille konst melding æ `Dette e ein
jille multi-line streng
jille i Rogalang!`

jille sei(melding)

herliga london
```

---

## Examples

### Example 1: Hello World

```rogalang
herliga london

jille konst melding æ 'Hei verden!'
jille sei(melding)

herliga london
```

**Transpiles to:**

```javascript
const melding = 'Hei verden!'
console.log(melding)
```

### Example 2: Iteration with Filtering

```rogalang
herliga london

jille konst ord æ ['hei', 'verden', 'rogalang', 'test']

jille for kvar einaste(word i ord) {
jille     viss(word græla likt mæ 'rogalang') {
jille         sei(word)
jille     }
jille }

herliga london
```

**Transpiles to:**

```javascript
const ord = ['hei', 'verden', 'rogalang', 'test']

for(word in ord) {
    if(word === 'rogalang') {
        console.log(word)
    }
}
```

### Example 3: Template Literal with Calculation

```rogalang
herliga london

jille sei(`Dette e ein test egentlig. 2 aog mæ 2 æ ${2 aog mæ 2}`)

herliga london
```

**Transpiles to:**

```javascript
console.log(`Dette e ein test egentlig. 2 + 2 = ${2 + 2}`)
```

### Example 4: Complex Control Flow

```rogalang
herliga london

jille konst tall æ [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

jille for kvar einaste(num i tall) {
jille     viss(num rest frå deling på 2 græla likt mæ 0) {
jille         sei(`${num} e partall`)
jille     } elle {
jille         sei(`${num} e oddetall`)
jille     }
jille }

herliga london
```

### Example 5: Function with Multiple Operations

```rogalang
herliga london

jille arbeidskar beregnAreal(lengde, bredde) {
jille     konst areal æ lengde gange me bredde
jille     spytt ud areal
jille }

jille konst resultat æ beregnAreal(10, 5)
jille sei(`Arealet e ${resultat}`)

herliga london
```

---

## Transpiler Implementation

### How It Works

The Rogalang transpiler (`transpiler.py`) works in several stages:

#### 1. Validation and Preprocessing

```python
validate_and_preprocess_rogalang(lines)
```

- Checks that first line is `herliga london`
- Verifies `herliga london` appears at least every 10 lines
- Removes all non-`jille` lines (comments)
- Strips `jille` prefix from executable lines

#### 2. String Literal Extraction

- Identifies all string literals (single quotes, double quotes, backticks)
- Replaces them with placeholders (`str0`, `str1`, etc.)
- Recursively transpiles template expressions within backtick strings

#### 3. Token Replacement

- Reads keyword mappings from `semantics/semantics.csv`
- Replaces Rogalang tokens with JavaScript equivalents
- Uses regex with word boundaries to prevent partial matches

#### 4. String Literal Restoration

- Inserts transpiled string literals back into code
- Template expressions are already transpiled from step 2

#### 5. Cleanup

- Removes temporary delimiters
- Returns final JavaScript code

### Running the Transpiler

**From file:**
```bash
python transpiler.py > output.js
```

**Programmatically:**
```python
from transpiler import validate_and_preprocess_rogalang, transpile_rogalang

with open('program.rl', 'r') as f:
    lines = f.readlines()

processed = validate_and_preprocess_rogalang(lines)
js_code = transpile_rogalang(''.join(processed), _reset_state=True)
print(js_code)
```

### Adding New Keywords

To add new keywords, simply edit `semantics/semantics.csv`:

```csv
js,rogalang,comment
newKeyword,nyttNorsktOrd,description
```

The transpiler automatically loads all mappings from this file.

---

## Error Messages

### Common Errors

**Error:** `No 'herliga london' found in source file`
- **Fix:** Add `herliga london` as the first line

**Error:** `First line must be 'herliga london'`
- **Fix:** Move `herliga london` to be the very first line

**Error:** `Gap of X lines between 'herliga london'`
- **Fix:** Add more `herliga london` declarations (max 10 lines apart)

**Error:** `ValueError` during transpilation
- **Fix:** Check for syntax errors in your Rogalang code
- Ensure all lines start with `jille` (except `herliga london`)
- Verify you're not using underscores

---

## Best Practices

### 1. Consistent Herliga London Placement

Don't just place `herliga london` every 10 lines mechanically. Use it to structure your code logically:

```rogalang
herliga london

Function declarations
jille arbeidskar setup() { ... }

herliga london

Main program logic
jille konst data æ getData()
jille processData(data)

herliga london
```

### 2. Use Comments Wisely

Remember: lines without `jille` are comments!

```rogalang
herliga london

This is a comment explaining the next section
jille konst x æ 5

Another comment here
jille sei(x)

herliga london
```

### 3. CamelCase Naming

Embrace camelCase for all identifiers:

```rogalang
jille konst minVariabel æ 10
jille arbeidskar minFunksjon() { ... }
jille KLASSE MinKlasse { ... }
```

### 4. Readable Template Literals

Break long template strings across multiple lines:

```rogalang
jille sei(`Dette e ein lang melding
jille som går over fleire linjer
jille for å gjere den meir lesbar`)
```

---

## Philosophy: Why These Rules?

### Herliga London

The recurring `herliga london` requirement forces you to think about code structure. It prevents massive blocks of code and encourages modular thinking. Also if your code doesn't make you want to say "herliga london" you haven't written good code.

### Jille Prefix

Explicit line marking makes every line of code intentional. It's the opposite of "invisible" syntax - you must actively choose to make a line executable.

### No Underscores

This enforces consistency and makes reading code easier. It's a constraint that breeds creativity in naming.

---

## Contributing to Rogalang

Want to add features or fix bugs? Here's how:

1. Fork the repository
2. Create a feature branch
3. Add your changes (remember: no underscores!)
4. Write tests in `test_transpiler.py`
5. Submit a pull request

### Future Roadmap

- [ ] Randomized `herliga london` placement validation (prevent predictable patterns)
- [ ] Better string handling (move from replacement to proper parsing)
- [ ] Source maps for debugging
- [ ] Browser-based transpiler
- [ ] Syntax highlighting for editors
- [ ] Package manager integration

---

## FAQ

**Q: Why Rogalending?**  
A: Why not? It is a nice dialect.

**Q: Is this a joke language?**  
A: No.

**Q: Can I use this in production?**  
A: Technically yes, since it transpiles to JavaScript. Practically... probably not recommended 😄

**Q: How do I pronounce "jille"?**  
A: Like "yil-leh" (roughly).

**Q: What does "herliga london" mean?**  
A: "Herliga" means "glorious/magnificent" and "London" is... London! So "Glorious London!"

**Q: Why "æ" for assignment?**  
A: It's the Norwegian letter æ, which is how some Rogalendinger say "is". We love rogalending!

---

## License

See [LICENSE](LICENSE) file for details.

---

## Credits

Created by the team at tullandtoys programming.

*Remember: Programming shouldn't be a chore; it should be an artform!*

---

**Herliga London!** 🎨🇳🇴
