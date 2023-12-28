import pandas as pd
import sys

semantics: pd.DataFrame = None
with open("semantics/semantics.csv", "r") as f:
    semantics = pd.read_csv(f)
assert semantics is not None, "derp"

def herliga_london(linewords):
    try:
        herligalondon = linewords[0].lower() == 'herliga' and linewords[1].lower() == 'london'
        return herligalondon
    except:
        return False

filestr = ""
del semantics['comment']
if __name__ == "__main__":
    dictionary = dict([(key,value) for (key,value) in zip(semantics['rogalang'],semantics['js'])])

    removed_keys = []
    for key in dictionary:
        if type(key) is not str or type(dictionary[key]) is not str:
            removed_keys.append(key)
    for key in removed_keys:
        dictionary.pop(key)

    args = sys.argv
    path = args[1]
    assert "_" not in path, "forbidden character"
    with open(path, "r") as program:
        firstline = program.readline()
        if not herliga_london(firstline.split()):
            raise SystemError('First line has to be "Herliga London" (for performance)')
        herligalondoncounter = 10
        while line := program.readline():
            linewords = line.split() 
            if len(linewords) == 0:
                herligalondoncounter -= 1
                continue
            if linewords[0] != 'jille':
                if herliga_london(linewords):
                    if herligalondoncounter > 5:
                        raise EOFError('No more than one "Herliga London" per 5 lines')
                    elif herligalondoncounter <= 5:
                        herligalondoncounter = 10
                continue
            herligalondoncounter -= 1
            if herligalondoncounter == 0:
                raise EOFError('"Herliga London" required at least every 10 lines')

            in_string = ''
            string_loc = (None,None)
            all_strings = []
            updated_line = line
            for i,char in enumerate(line):
                if char == '_':
                    raise ZeroDivisionError("pleaseDon'tUseThatLetter.ThisIsACamelCaseBasedLanguage.")
                # at start of string
                if in_string == '':
                    if char in ['"', "'", "`"]:
                        string_loc = (i, None)
                        in_string = char
                else:
                    # at end of string
                    if in_string == char:
                        string_loc = (string_loc[0],i)
                        in_string = ''
                        # extract string
                        string = line[string_loc[0]:string_loc[1]+1]
                        all_strings.append(string)
                        # replace string with forbidden character
                        updated_line = updated_line.replace(string, '_')
            
            all_keys_len = [list(filter(lambda x: len(x.split())==i, list(dictionary.keys()))) for i in range(3,0,-1)]
            replace_symbols = ['⍨', '⧍', '⦞']
            for i,keys in enumerate(all_keys_len):
                for key in sorted(keys, key=lambda a: -len(a)):
                    if type(key) == str and key in updated_line:
                        updated_line = updated_line.replace(key, replace_symbols[i])
                        # print(updated_line)
            
            #insert the strings again
            for string in all_strings:
                updated_line = updated_line.replace('_', string, 1)
            
            filestr+=updated_line

with open(path.replace(".rl", "")+".js","w") as f:
    f.write(filestr)

    # ⍨
    # ⧍
    # ⦞
