# Rogalang 🇳🇴

A Rogaland-inpsired esoteric programming language respecting the culture of the region that transpiles to JavaScript. Because programming should be an artform, not a chore!

## Quick Start

### Installation

```bash
git clone https://github.com/tullandtoys/rogalang.git
cd rogalang
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install pandas
```

### Your First Rogalang Program

Create a file called `hello.rl`:

```rogalang
herliga london

jille konst melding æ 'Hei verden!'
jille sei(melding)

herliga london
```

Run it:

```bash
python transpiler.py > output.js
node output.js
```

## Core Rules

1. **Every line must start with `jille`** - Lines without it are comments
2. **First line must be `herliga london`** - For performance reasons (and style!)
3. **`herliga london` every 10 lines max** - Keeps your code fresh and exciting
4. **CamelCase only** - No underscores (`_`) allowed anywhere
5. **Rogalandske keywords** - `konst` instead of `const`, `sei` instead of `console.log`, etc.

## Example

```rogalang
herliga london

jille konst tall æ [1, 2, 3, 4, 5]
jille for kvar einaste(nummer i tall) {
jille     sei(nummer)
jille }

herliga london
```

## Documentation

For comprehensive language documentation, see [docs.md](docs.md).

## Contributing

Feel free to submit PRs! Remember: no underscores allowed in your code! 😄

## License

See [LICENSE](LICENSE) file.