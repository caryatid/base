#!/usr/bin/python


import readline
readline.parse_and_bind('tab: complete')
class VocabCompleter(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def complete(self, text, state):
        results = [ x+' 'for x in self.vocab if x.startswith(text)] + [None]
        return results[state]


class ARLCompleter(object):
    def __init__(self, logic):
        self.logic = logic
    def traverse(self, tokens, tree):
        if tree is None:
            return []
        elif len(tokens) == 0:
            return []
        if len(tokens) == 1:
            return [x+' ' for x in tree if x.startswith(tokens[0])]
        else:
            if tokens[0] in tree.keys():
                return self.traverse(tokens[1:], tree[tokens[0]])
            else:
                return []
        return []
    def complete(self, text, state):
        try:
            tokens = readline.get_line_buffer().split()
            if not tokens or readline.get_line_buffer()[-1] == ' ':
                tokens.append('')
            results = self.traverse(tokens, self.logic) + [None]
            return results[state]
        except Exception as e:
            print(e)

cmds = {
        'build': {
            'barracks': None,
            'generator': ['one', 'two','three'],
            'lab': None,
            },
        'train': {
            'riflemen':None,
            'rpg':None,
            'mortar':None,
            },
        'research': {
            'armor':None,
            'weapons':None,
            'food':None,
            },
        }



completer = ARLCompleter(cmds)
#VocabCompleter(['ace', 'bandages', 'for', 'every', 'zombie', 'attack', 'is', 'wise'])

readline.set_completer(completer.complete)
line = input('p.dizzle> ')



