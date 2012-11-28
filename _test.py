#!/usr/bin/python

import readline, logging, re, collections, os,glob, shlex, itertools
L = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename="/home/dave/code/admin/_test.log"
        , format="%(levelname)s:%(lineno)d:%(name)s:%(message)s")

readline.parse_and_bind('tab: complete')
readline.set_completer_delims(readline.get_completer_delims())
L.debug(readline.get_completer_delims())

class coreData(collections.UserDict):
   def __init__(self, *data, **kwargs):
       super(coreData, self).__init__(data)
       L.debug("init of {}".format(self.__class__))
       self.name = ""
       self.id = 'UUID PLEASE'
       self.delim = '.'
   def extra_info(self, idx=None):
       """ override for extra coreData subclass info """
       pass
   def info(self, arg=None):
       """
       info on various objects
       """
       #######################
       ## |TODO|formatter for info output|4|
       ## |0abec356-e9fa-4184-8503-64cf4754b300|2012-11-14 20:18|dave|
       # should be nice

       print(self.__doc__)
       [print(" --| {}".format(x)) for x in self]
       self.extra_info(arg)
       
       pass

 
########
# data objects
class dataData(coreData):
    """ data types avaliable """
    def __init__(self):
        super(dataData, self).__init__()
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
    def __init__(self):
        super(flistData, self).__init__()
        self.root = '/home/dave'
        self.data_dir = os.path.join(self.root, '.ds')
        self.gen_flists() 
        self.name = 'flists'
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

class ARLCompleter(object):
    def __init__(self,  logic):
        self.logic = None
        self.logics = logic
        self.parsed = None

    def traverse(self, arg, tree):
        delim = ' ' 
        try:
            delim = ' ' + tree.delim
        except AttributeError:
            delim = ' '
        readline.set_completer_delims(delim)
        tokens =  arg.split(delim)
        if tree is None:
            return []
        elif len(tokens) == 0:
            return []
        if len(tokens) == 1:
            return [x+delim[-1] for x in tree if x.startswith(tokens[0])]
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
        line = readline.get_line_buffer()
        L.debug(''.join(['{:^5}'.format(c) for c in line]))
        L.debug(''.join(['{:^5}'.format(n) for n in range(len(line))]))
        L.debug('begi: {}, endi: {}'.format(readline.get_begidx(), readline.get_endidx()))
                
        results = []
        args = line.split()
        if not args: 
            results =  list(self.logics[0].keys())
        else:
            if line[-1] == ' ':
                args.append('')
            L.debug("args; {}".format(args))
            self.parsed = []
            for index, data in zip(args,  self.logics + [None]): 

                old_delims = readline.get_completer_delims()
                self.parsed.append(self.traverse(index, data))
                L.debug(index.split(':'))
            results = self.parsed[-1]
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

if __name__== '__main__':
    completer = ARLCompleter( [dataData(), flistData()] )
    readline.set_completer(completer.complete)
    line = input('p.dizzle> ')



