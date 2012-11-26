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
            return [x+'.' for x in tree if x.startswith(tokens[0])]
        else:
            if tokens[0] in tree.keys():
                return self.traverse(tokens[1:], tree[tokens[0]])
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
        ### 
        # at each logics step perform '.' splitting and completion

        # determine our argument position
        # 0 indexed
        args = readline.get_line_buffer().split()
        i=[]
        if (args and '.' in args[-1]) or text:
            i = args[:-1]
        pos = len(i)
        L.debug(pos)
        # assign logic data appropriately
        logic = self.logics[pos]
        # split current argument on '.' and 
        if args:
            L.debug(args[-1])
            d = args[-1]
            L.debug(d.split('.'))
            data = d.split('.')
            # complete via recursive traversal of completer data
            results = self.traverse(data, logic) + [None] 
            return results[state]
             
        
        # i = len(readline.get_line_buffer().split()) 
        # if text: 
            # i = i -1
        # i = 0 if i < 0 else i
        # L.debug("index into logics is: {}".format(i))
        # logic = self.logics[i]
        # L.debug(logic)
        # try:
            # try:
                # tokens = readline.get_line_buffer().split()[-1].split('.')
                # # tokens = re.findall(r'[^\.]+', readline.get_line_buffer().split()[-1])
            # except IndexError:
                # tokens = []
            # if not tokens or readline.get_line_buffer()[-1] in '.':
                # tokens.append('')
            # results = self.traverse(tokens, logic) + [None]
            # L.debug(tokens)
            # L.debug(results)
            # return results[state]
        # except Exception as e:
            # print(e)

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



