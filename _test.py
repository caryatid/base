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
    def find(self, tokens):
        retval = []
        if len(tokens) == 0:
            retval =  self
        else:
            try:
                retval = self[tokens[0]].find(tokens[1:])
            except KeyError:
                L.debug('incomplete entry')
                retval = self
            except AttributeError:
                L.debug('terminal object')
                retval = self[tokens[0]]
        return retval
    def get_delim(self):
        # intersection of current ok_delims and ok_delims of keys
        delims = set()
        try:
            delims = set.intersection(self.ok_delims, *[self[d].get_delim() for d in self])
        except :
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
        self.ok_delims = set('!.,^:')
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
        self.ok_delims = set(',^:')
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
    def split(self, txt, data):
        x =  re.findall(re.compile(r'[^' + re.escape(str(data.get_delim())) + r']+'), txt)
        try:
            if txt[-1] in data.get_delim():
                L.debug('adding')
                x.append('')
        except IndexError:
            L.debug('no split')
        L.debug('split arg: {} is {}'.format(txt,x))
        return x

    def complete(self, text, state):
        # I need a list of canidates indexed by current argument
        # that then gets filtered by the current text and returned
        L.debug('complete text: {}, state: {}'.format(text,state))
        # get arguments
        line = readline.get_line_buffer()
        args = shlex.split(line)
        if args and line[-1] == ' ':
            args.append('')
        L.debug('args: {}'.format(args))
        # split into args
        # if args 1 or less complete on this data's keys
        results = []
        if not args:
            results =  [x for x in self]
        else:
            a = self.split(args[0], self)
            L.debug('hello: {}'.format(a))
            cmd = self.find(a)
            L.debug('cmd is {}'.format(cmd.name))
            if cmd.params:
                L.debug('if on {}'.format(type(cmd)))
                try:
                    self.params = [self.params[0]] + cmd.params
                    L.debug('parameters')
                    L.debug([x.name for x in self.params])
                except KeyError as e:
                    L.debug('no dice, key: {} {}'.format(cmd[0], e))
                L.debug('args: {}'.format(args))
            for arg,data in zip(args, self.params + [None] ) :
                L.debug([x.name for x in self.params])
                readline.set_completer_delims(str(data.get_delim()))
                L.debug(readline.get_completer_delims())
                L.debug('arg: {} at data: {}'.format(arg, [x for x in data]))
                if not data:
                    L.debug('not data')
                    results = []
                else:
                    tok = self.split(arg, data)
                    L.debug('tok: {}'.format(tok))
                    d = data.find(tok)
                    results = [x for x in d]
                try: 
                    tmp = [x for x in data.get_delim() if x in self.ok_delims][0]
                    L.debug(tmp)
                    results = [x + tmp for x in results if x.startswith(text)]
                except Exception as e:
                    L.debug('error: {}'.format(e))
        L.debug('results: {}'.format(results))
        return results[state]

class infoCommand(commandData):
    def __init__(self, d=None, delim='.'):
        super(infoCommand,self).__init__(d, delim)
        self.params = [dataData(), flistData()]


if __name__== '__main__':
    completer = commandData()
    completer['info'] = infoCommand()
    readline.set_completer(completer.complete)
    line = input('p.dizzle> ')



