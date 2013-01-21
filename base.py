#!/usr/bin/python
import readline, logging, re, collections, os,glob, shlex, itertools 
from io import StringIO

L = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename="/home/dave/code/base/_test.log"
        , format="%(levelname)s:%(lineno)d:%(name)s:%(message)s")

readline.parse_and_bind('tab: complete')
# readline.set_completer_delims(readline.get_completer_delims())
L.debug(readline.get_completer_delims())

class coreData(collections.UserDict):
    def __init__(self, d=None, delim='.'):
        super(coreData, self).__init__(d)
        L.debug("init of {}".format(self.__class__))
        self.name = 'core'
        self.id = 'UUID PLEASE'
        self.ok_delims = '.:-|;^,'
    def find(self, tokens):
        data = self
        if tokens:
            for x in tokens:
                try:
                    if not x == '':
                        data = data[x]
                except TypeError:
                    pass
                except KeyError:
                    pass
        return data
                    
    def get_delim(self):
        # intersection of current ok_delims and ok_delims of keys
        delims = set()
        try:
            delims = set.intersection(set(self.ok_delims), *[self[d].get_delim() for d in self])
        except:
            delims = set(self.ok_delims)
        delims.add(' ')
        return delims

########
# data objects
class dataData(coreData):
    """ data types avaliable """
    def __init__(self, d=None, delim=':'):
        super(dataData, self).__init__(d, delim)
        self.name = 'data'
        self['flists'] =  flistData()
        self.ok_delims = ':.,^h'
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
        self.ok_delims = ':^,'
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
        # readline.set_completer_delims(' ')
        self.name = 'commands'

    def split(self, txt, data):
        x =  re.findall(re.compile(r'[^' + re.escape(str(data.get_delim())) + r']+'), txt)
        try:
            if txt[-1] in data.get_delim():
                L.debug('adding')
                x.append('')
        except IndexError:
            L.debug('no split')
        return x

                    


    def complete(self, text, state):
        # +------/ recreating complete with iter concepts \-------{{{
        # |  TODO  | recreating complete with iter concepts
        
        # +-------/ 9929f175-52d6-4d04-81da-44dd133b7886 \--------}}}
        results = []
        tmp_results = []
        cmd_line = [[y for y in x.split(':')]  for x in shlex.split(readline.get_line_buffer())]
        if readline.get_line_buffer()[-1] == ' ':
            cmd_line.append([''])
        L.debug(cmd_line)
        if len(cmd_line) < 1:
            results = [x for x in self]
        else:
            tmp_results = []
            cmd = self.find(cmd_line[0])
            self.params = [self.params[0]] + cmd.params 
            for arg, data in zip(cmd_line, self.params + [ None ]):
                tmp_results = []
                if data:
                    tmp_results = [x for x in data.find(arg)]
        if tmp_results:
            results = tmp_results
        results = [ x + ':' for x in results if x.startswith(text.replace(':', ''))]
        return results[state]

        
        # old_delims = readline.get_completer_delims()
        # L.debug('complete text: {}, state: {}'.format(text,state))
        # # get arguments
        # line = readline.get_line_buffer()
        # args = shlex.split(line)
        # if args and line[-1] == ' ':
            # args.append('')
            # text = ''
        # # split into args
        # # if args 1 or less complete on this data's keys
        # results = []
        # tmp_results = []
        # first_delim = ' ' 
        # if len(args) <= 1:
            # results =  [x for x in self]
        # else:
            # a = self.split(args[0], self)
            # cmd = self.find(a)
            # L.debug('cmd is {}'.format(cmd.name))
            # try:
                # self.params = [self.params[0]] + cmd.params
            # except AttributeError:
                # L.debug('no attribute params')
            
            # L.debug('parameters')
            # L.debug([x.name for x in self.params])
            # for arg,data in zip(args, self.params + [None]):
                # tmp_results = []
                # if not data:
                    # L.debug('not data')
                # else:
                    # L.debug('arg: {} at data: {}'.format(arg, [x for x in data]))
                    # readline.set_completer_delims(str(data.get_delim()))
                    # tok = self.split(arg, data)
                    # if len(tok) > 0 and (not tok[0] in data):
                        # tmp_results = [x for x in data]
                    # else:
                        # tmp_results = [x for x in data.find(tok)]
                # if tmp_results:
                    # first_delim = [x for x in self.ok_delims if x in data.get_delim() and x != ' '][0]
                    # L.debug(first_delim)
        # if tmp_results:
            # results = tmp_results
        # if results:
            # L.debug('results: {} :: text: {}'.format(results, text))
            # L.debug(readline.get_completer_delims())
            # results = [x + first_delim for x in results if x.startswith(text.replace(' ', ''))]
        # return results[state]

class infoCommand(commandData):
    def __init__(self, d=None, delim='.'):
        super(infoCommand,self).__init__(d, delim)
        self.params = [dataData(), flistData() ]


if __name__== '__main__':
    completer = commandData()
    completer['info'] = infoCommand()
    readline.set_completer(completer.complete)
    line = input('p.dizzle> ')
