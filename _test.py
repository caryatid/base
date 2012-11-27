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
        self.parsed = None
        
    def traverse(self, tokens, tree, alt):
        if alt < 2:
            buf = ' ' 
        else:
            buf = '.'

        if tree is None:
            return []
        elif len(tokens) == 0:
            return []
        if len(tokens) == 1:
            return [x+buf for x in tree if x.startswith(tokens[0])]
        else:
            if tokens[0] in tree.keys():
                return self.traverse(tokens[1:], tree[tokens[0]], alt)
            else:
                return []
        return []
    def complete(self, text, state):
        #########
        ## position based completion
        # for each position there is a completer data available 
        # position will remain but completion can narrow the
        # data by adding '.' period chars
        # foo.grue.bar.lorem may reference something like
        # data['foo']['grue']['bar']['lorem']

        L.debug('complete text: {}, state: {}'.format(text,state))
        line = readline.get_line_buffer()
        results = []
        args = line.split()
        if not args: 
            results =  list(self.logics[0].keys())
        else:
            if line[-1] == ' ':
                args.append('')
            L.debug("args; {}".format(args))
            self.parsed = [self.traverse(index.split('.'), data, len(index.split('.'))) 
                    for index, data in zip(args,  self.logics + [None]) ]
            results = self.parsed[-1]
        L.debug(results)
        L.debug("--| " + results[state])
        return results[state]
             

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
                },
            'tool': {
                'hammer': None,
                'saw': None,
                'table': None,
                },
            },
        ]




completer = ARLCompleter(cmds)
#VocabCompleter(['ace', 'bandages', 'for', 'every', 'zombie', 'attack', 'is', 'wise'])

readline.set_completer(completer.complete)
line = input('p.dizzle> ')



