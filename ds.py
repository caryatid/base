#!/use/bin/python
#######################
## |TODO|set up logging|0|
## |62e3ad3a-23e4-4de1-bc35-8d19eb9d130b|2012-11-13 09:52|dave|


import glob, os, re, readline, logging, tempfile, cmd,logging
########################################################################
## settings and objects
#####----------------------------------------------------------------{{{

##############################################
## settings
#####--------------------------------------{{{

L = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename="/home/dave/.ds/ds.log")
readline.set_completer_delims("".join([x for x in readline.get_completer_delims() if not x == '/']))
#####------------------||------------------}}}
## end: settings
##############################################

##############################################
## objects
#####--------------------------------------{{{

class coreData(object):
    def __init__(self):
        L.debug("init of {}".format(self.__class__))
        self.core = None
        self.data = None
        self.completer = None
    def set_core(self, core ):
        self.core = core
        self.completer.set_core(core)
    def set_completer(self, comp):
        self.completer = comp
        self.completer.set_core_data(self)
    def by_index(self, idx=None):
        pass
    def info(self, arg=None):
        """
        info on various objects
        """
        L.debug("running info of {} with arg {}".format(self.__class__, arg))
        print(self.__doc__)
        [print(" --| {}".format(x)) for x in self.by_index(arg)]
    def list(self):
        return self.by_index()
    def add_data(self, data):
        pass
    def remove_data(self, id):
        pass


#########
## hosts
# a simple list -- is index into history for history by host

class hostData(coreData):
    """
    Known hosts
    """
    def __init__(self):
        super(hostData,self).__init__()
        self.set_completer(hostComp()) 
    def by_index(self, idx=None):
        if idx:
            return []
        return ['liszt', 'tchaikovsky', 'dvorak', 'beethoven']

#########
## command
# 
class commandData(coreData):
    """
    Commands available 
    """
    def __init__(self):
        super(commandData, self).__init__()
        self.set_completer(commandComp())
    def by_index(self, idx=None):
        if idx:
            try:
                print(getattr(self, idx).__doc__)
            except:
                L.warning( "no {} command available".format(idx))
            return []
        else:
            return [x[3:] for x in self.core.command.get_names() if x.startswith('do_')]


#########
## data objects
class dataData(coreData):
    """ data types avaliable """
    def __init__(self):
        super(dataData, self).__init__()
        self.set_completer(dataComp())
    def by_index(self, idx=None):
        if idx:
            try:
                return self.core.type[idx].list()
            except KeyError:
                return []
        else:
            return list(self.core.type.keys())



#########
## filelists
class flistData(coreData):
    """
    known files
    """
    def __init__(self):
        super(flistData, self).__init__()
        self.set_completer(flistComp())
        self.data = {}
    def by_index(self, idx=None):
        #######################
        ## |TODO|allow for an all index that is all files|1|
        ## |e09c75ae-e982-4c1b-8905-86276bab7e18|2012-11-02 11:02|dave|
        self.gen_flists()
        if idx:
            if idx in self.data.keys():
                return self.data[idx]
            else:
                return []
        else:
            return list(self.data.keys())
    def gen_filter(self,name):
        fil = set()
        try: 
            with open(os.path.join(self.core.data_dir, name + ".filter")) as n:
                [fil.add(x[:-1]) for x in n.readlines()]
        except IOError as foo:
            print("should {}.filter be created? ".format(name))
        finally:
            with open(os.path.join(self.core.data_dir, "global.filter")) as g:
                [fil.add(x[:-1]) for x in g.readlines()] 
        # convert list to regex or-matcher
        all_fil = "(" + ")|(".join(fil) + ")"
        return re.compile(all_fil)
    def gen_flists(self):
        for fname in glob.glob(self.core.data_dir + "/*.files"):
            L.debug("generating files from: {}".format(fname))
            name = os.path.splitext(os.path.split(fname)[1])[0]
            fil= self.gen_filter(name)
            self.data[name] = []
            L.debug("gen_flists at root: {}".format(self.core.root))
            for top in [(os.path.join(self.core.root, x)[:-1]) for x in open(fname).readlines() if x]:
                if not os.path.isdir(top):
                    self.data[name].append(top)
                else:
                    for dr,dirs, fls in os.walk(top):
                        [dirs.remove(d) for d in dirs if fil.match(d)]
                        fs = [f for f in fls if not fil.match(f)]
                        self.data[name].append(dr)
                        self.data[name].extend(fs) 
                        # for fs_or_ds in (dirs, fls):
                            # keep = []
                            # for f_or_d in fs_or_ds:
                                # if fil.match(f_or_d):
                                    # fs_or_ds.remove(f_or_d)
                                # else:
                                    # keep.append(os.path.join(dr, f_or_d))
                                # self.data[name].extend(keep)

#########
## history
# omg it is a list of dicts for your enjoyment

class subComp(cmd.Cmd):
    def __init__(self):
        L.debug("init of {}".format(self.__class__))
        cmd.Cmd.__init__(self)
        self.prev_arg = None
        self.core = None
        self.core_data = None
        self.check_prev = None
        self.args = None
    def set_args(self, completers=[]):
        comp_list = [y if isinstance(y, list) else [y] for y in completers]
        self.check_prev = [True if '!' in y[0] else False for y in comp_list]
        comp_list = [list(self.core.type.keys()) if '*' in x[0] else x for x in comp_list]
        self.args = [[self.core.type[y].completer for y in x if not y == '!'] for x in comp_list]  
    def set_core(self, core):
        self.core = core
    def set_core_data(self,  type):
        self.core_data = type
    def gen_comp(self):
        if self.prev_arg:
            return self.core_data.by_index(self.prev_arg)
        else:
            return self.core_data.list()
    def set_prev_arg(self, arg):
        self.prev_arg = arg
    def find_in_list(self, x, ls):
        return [f for f in ls if f.startswith(x)]
    def pos_complete(self, text, line, begi, endi):
        (c,a,l) = self.parseline(line)
        completers = None
        i = 0
        args = a.split()
        completions=[]
        prev_arg = None
        i = len(args)
        if text:
            i = i - 1
            i = 0 if (i < 0) else i
            if self.check_prev[i]:
                prev_arg =   l.split()[-2]
        else:
            if self.check_prev[i]:
                prev_arg = l.split()[-1]
        try:
            completers = self.args[i]
            [x.set_prev_arg(prev_arg) for x in [y for y in completers]]
        except:
            completers = None
        if not completers:
            return []
        [completions.extend(x.gen_comp()) for x in completers]
        if text:
            completions = self.find_in_list(text, completions)
        return completions
    def do_list(self, text, line, begi,endi):
        if text:
            self.core_data.by_index(text)
        else:
            self.core_data.list()
    def do_info(self, args):
        #######################
        ## |TODO|move this stuff to a coreData object|8|
        ## |4e18a85f-541f-4e36-b93a-fa038f42be92|2012-11-13 09:52|dave|
        # do_* is where tests for special actions like
        # entering a shell should happen
        # doing so may require access to the self.args -- haven't
        # quite figured out that shit
        a = args.split()
        if len(a) == 0:
            self.core_data.info()
        elif len(a) == 1:
            datas = [x for x in self.core.type.values() if a[0] in x.list()]
            if not datas:
                print("there is nothing matching: {}".format(a[0]))
            [x.info(a[0]) for x in datas]
        elif len(a) == 2:
            data = self.core.type[a[0]]
            data.info(a[1])
    def complete_info(self, text, line, begi, endi):
        self.set_args(['*', '!*'])
        self.core.ch_dir('/home/dave')
        return self.pos_complete(text, line, begi, endi)
    def do_EOF(self, line):
        return True

class dataComp(subComp):
    def __init__(self):
        super(dataComp, self).__init__()
        self.msg = "Data Completion"

class commandComp(subComp):
    def __init__(self):
        super(commandComp, self).__init__()
        self.msg = "Command Completion"
class flistComp(subComp):
    def __init__(self):
        super(flistComp, self).__init__()
        self.msg = "Flist Completion"
        
class hostComp(subComp):
    def __init__(self):
        super(hostComp, self).__init__()


class daCore(object):
    data_dir=os.path.expanduser("~/.ds")
    def __init__(self):
        self.type = {
                'hosts' : hostData(),
               'flists' : flistData(),
               'commands': commandData(),
               'data': dataData(),
                # 'history' : histData(),
                }
        [x.set_core(self) for x in self.type.values()]
        self.command = self.type['commands'].completer
        self.root =  os.getcwd()
        return
    def ch_dir(self, dir):
        self.root = dir
    def run(self):
        self.command.cmdloop()
#####------------------||------------------}}}
## end: objects
##############################################

#####-------------|479a36d8-865a-44a5-b48c-a4003608ad7a|-------------}}}
## end: settings and objects
########################################################################


##############################################
## main
#####--------------------------------------{{{

if __name__  == '__main__':
    core = daCore()
    core.ch_dir('/home/dave')
    core.run()

#####------------------||------------------}}}
## end: main
##############################################

