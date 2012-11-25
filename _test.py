#!/usr/bin/python

import readline, logging, re
L = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename="/home/dave/code/admin/_test.log"
        , format="%(levelname)s:%(lineno)d:%(name)s:%(message)s")

readline.parse_and_bind('tab: complete')
readline.set_completer_delims(readline.get_completer_delims() + '.')
L.debug(readline.get_completer_delims())
class VocabCompleter(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def complete(self, text, state):
        results = [ x+' 'for x in self.vocab if x.startswith(text)] + [None]
        return results[state]


class ARLCompleter(object):
    def __init__(self, logic):
        self.logic = None
        self.logics = logic
        
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
        L.debug('complete text: {}, state: {}'.format(text,state))
        i = len(readline.get_line_buffer().split()) - 1
        i = 0 if i < 0 else i
        
        self.logic = self.logics[i]
        try:
            tokens = re.findall(r'[^\.]+', readline.get_line_buffer().split()[-1])
            if not tokens or readline.get_line_buffer()[-1] in ' .':
                tokens.append('')
            results = self.traverse(tokens, self.logic) + [None]
            L.debug(tokens)
            L.debug(results)
            return results[state]
        except Exception as e:
            print(e)

cmds = [
        {
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
            },
        {
            'unit': {
                'actor': None,
                'commander': None,
                'chief funny pants': None,
                }
            }
        ]




completer = ARLCompleter(cmds)
#VocabCompleter(['ace', 'bandages', 'for', 'every', 'zombie', 'attack', 'is', 'wise'])

readline.set_completer(completer.complete)
line = input('p.dizzle> ')



