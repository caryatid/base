#!/usr/bin/python

import readline, logging, re, collections, os,glob, shlex, itertools
from io import StringIO
L = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename="/home/dave/code/admin/_test.log"
        , format="%(levelname)s:%(lineno)d:%(name)s:%(message)s")

readline.parse_and_bind('tab: complete')
readline.set_completer_delims(readline.get_completer_delims())
L.debug(readline.get_completer_delims())

class coreData(collections.UserDict):
   def __init__(self, d=None, delim='.'):
       super(coreData, self).__init__(d)
       L.debug("init of {}".format(self.__class__))
       self.name = ""
       self.id = 'UUID PLEASE'
       self.ok_delims = set('._-|:;^,')

   def get_delim(self):
       # intersection of current ok_delims and ok_delims of keys
       delims = set()
       try:
           L.debug('who')
           [L.debug('keys are {}'.format(x)) for x in self]
           delims = set.intersection(self.ok_delims, *[self[d].get_delim() for d in self])
           L.debug('when: {}'.format(delims))
       except :
           L.debug('whatever') 
           delims = self.ok_delims
       return delims

 
########
# data objects
class dataData(coreData):
    """ data types avaliable """
    def __init__(self, d=None, delim=':'):
        super(dataData, self).__init__(d, delim)
        self.name = 'data'
        self['flists'] =  flistData()
        # self['hosts'] = hostData()
        # self['commands'] = commandData()

#########
## filelists
class flistData(coreData):
    """
    known files
    """
    def __init__(self, d=None, delim='^'):
        super(flistData, self).__init__(d, delim)
        self.root = '/home/dave'
        self.data_dir = os.path.join(self.root, '.ds')
        self.gen_flists() 
        self.name = 'flists'
        self.delim = ':'
    def gen_filter(self,name):
        fil = set()
        try: 
            with open(os.path.join(self.data_dir, name + ".filter")) as n:
                [fil.add(x[:-1]) for x in n.readlines()]
        except IOError as foo:
            print("should {}.filter be created? ".format(name))
        finally:
            with open(os.path.join(self.data_dir, "global.filter")) as g:
                [fil.add(x[:-1]) for x in g.readlines()] 
        # convert list to regex or-matcher
        all_fil = "(" + ")|(".join(fil) + ")"
        return re.compile(all_fil)
    def gen_flists(self):
        L.debug('entering gen_flists')
        for fname in glob.glob(self.data_dir + "/*.files"):
            name = os.path.splitext(os.path.split(fname)[1])[0]
            fil= self.gen_filter(name)
            self[name] = {}
            for top in [(os.path.join(self.root, x)[:-1]) 
                    for x in open(fname).readlines() if x]:
                if not os.path.isdir(top):
                    self[name][top] = 'top level dir'
                else:
                    for dr,dirs, fls in os.walk(top):
                        [dirs.remove(d) for d in dirs if fil.match(d)]
                        fs = [f for f in fls if not fil.match(f)]
                        for fn in fs:
                            self[name][os.path.join(dr, fn)] = 'fstat here'

class commandData(coreData):
    def __init__(self,  d=None, delim='.'):
        super(commandData,self).__init__(d, delim)
        self.params = [self]
        self.parsed = None
        readline.set_completer_delims(' ')
        self.name = 'commands'
    def parse(self, tokens, tree):
        L.debug('tok is {}'.format(tokens))
        try: 
            ds = set(readline.get_completer_delims())
            ds.add(tree.delim)
            readline.set_completer_delims(''.join(list(ds)))
        except AttributeError:
            L.debug('attribute error')
            pass
        if tree is None:
            return []
        elif len(tokens) == 0:
            return [x for x in tree]
        if len(tokens) == 1:
            return [x for x in tree if x.startswith(tokens[0])]
        else:
            if tokens[0] in tree.keys():
                L.debug('^^^^^^^^^^^')
                return self.parse(tokens[1:], tree[tokens[0]])
            else:
                return []
        return []
    def split(self, data):
        x =  re.findall(re.compile(r'[^' + re.escape(readline.get_completer_delims() + self.delim) + r']+'), data)
        return x

    def complete(self, text, state):
        L.debug('complete text: {}, state: {}'.format(text,state))
        line = readline.get_line_buffer()
        args = shlex.split(line)
        if args and line[-1] == ' ':
            args.append('')
        L.debug(args)
        # split into args
        # if args 1 or less complete on this data's keys
        results = []
        if not args:
            results =  [x for x in self]
        else:
            tmp = self.parse(self.split(args[0]), self)
            L.debug('tmp is {}'.format(tmp))
            if tmp:
                try:
                    self.params = [self.params[0]] + self[tmp[0]].params
                    L.debug([x.name for x in self.params])
                except KeyError as e:
                    L.debug('no dice, key: {} {}'.format(tmp[0], e))
            arg_count = []
            for arg,data in zip(args, self.params + [None]) :
                arg_count.append(arg)
                tok = self.split(arg)
                if arg[-1] in readline.get_completer_delims():
                    tok.append('')
                results = self.parse(tok, data)
        L.debug('results: {}'.format(results))
        return results[state]

class infoCommand(commandData):
    def __init__(self, d=None, delim='.'):
        super(infoCommand,self).__init__(d, delim)
        self.params = [dataData(), flistData()]


            
        # if args:
        # tokens = lex.split(arg)
        
            # # else set self.params to arg[0].params
        # # parse args : return list of possible options
        # results = []
        # args = line.split()
        # if not args: 
            # results =  list(self.logics[0].keys())
        # else:
            # L.debug("args: {}".format(args))
            # self.parsed = []
            # for index, data in zip(args,  self.logics + [None]): 
                # old_delims = readline.get_completer_delims()
                # delim_re = re.compile(r'[^' + re.escape(readline.get_completer_delims()) + r']+')
                # a = delim_re.findall(index)
                # if a[-1][-1] == data.delim:
                    # L.debug('neat')
                    # a.append('')
                # L.debug('433' +str(a))
                # self.parsed.append(self.traverse(a, data))
                # L.debug(self.parsed)
            # results = self.parsed[-1]
        # L.debug("--| " + results[state])
        # return results[state]
             


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

if __name__== '__main__':
    completer = commandData(  )
    completer['info'] = infoCommand()
    readline.set_completer(completer.complete)
    line = input('p.dizzle> ')



