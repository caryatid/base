#!/use/bin/python 

import glob, os, re, readline, logging, tempfile, cmd,logging,collections
########################################################################
## settings and objects
#####----------------------------------------------------------------{{{

##############################################
## settings
#####--------------------------------------{{{

L = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename="/home/dave/.ds/ds.log"
        , format="%(levelname)s:%(lineno)d:%(name)s:%(message)s")
readline.set_completer_delims("".join([x for x in readline.get_completer_delims() if not x == '/']))
#####------------------||------------------}}}
## end: settings
##############################################

##############################################
## objects
#####--------------------------------------{{{

class coreCommand(object):
    def __init__(self, core):
        L.debug("init of {}".format(self.__class__))
        self.args = None 
        self.core = core
        self.valdiated_args = []
        self.check_prev = None
        self.name = None
    def __call__(self, args):
        a = args.split()
        L.debug("calling __call__ from class: {} with args: {}".format(self.__class__,
            a))
        self.validated_args = []
        prev_arg = a[0] if a else None
        prev_data = None
        for arg, possibilities, prev in zip(a, self.args, self.check_prev):
            arg_tuple = (arg, [])
            if not prev:
                [arg_tuple[1].append(data) for data in possibilities 
                        if arg in data.by_index()]
            else:
                L.debug("prev_arg: {}".format(prev_arg))
                arg_tuple[1].append(self.core.type[prev_arg])
            self.validated_args.append(arg_tuple)
            prev_arg = arg
            prev_data = arg_tuple[1]
        L.debug("validated args: {}".format(self.validated_args))
        self.execute()
    def set_args(self):
        self.args = [self.core.data[x] for x in self.str_args]
    def execute(self):
        pass
    def complete(self,text, state):
        



        self.set_args()
        L.debug("complete at class: {}".format(self.__class__))
        i = 0
        args = line.split()[1:]
        completions=[]
        if text:
            i = i - 1
            i = 0 if (i < 0) else i
            prev_arg = line.split()[-2]
        else:
            prev_arg = line.split()[-1]
        i = len(args)
        try:
            self.args[i]
        except IndexError:
            L.debug("IndexError")
            self.str_args.append('!')
            self.set_args()

        L.debug("length: {}".format(i))
        if not self.check_prev[i]:
            prev_arg = None 
        for d in self.args[i]:
            if prev_arg:
                try:
                    completions.extend(d[prev_arg])
                    self.str_args[-1].append(d.name)
                    self.set_args()
                    L.debug("nice: prev_arg: {}".format(prev_arg))
                except KeyError:
                    L.debug("oops: prev_arg: {}".format(prev_arg))
            else:
                completions.extend(d)

        return completions
   
class infoCommand(coreCommand):
    def __init__(self, core):
        super(infoCommand, self).__init__(core)
        self.name = 'info'
        self.str_args = ['*']
        self.args = []
    def execute(self):
        L.debug("execute in: {}".format(self.__class__))
        L.debug("validtated_args: {}".format(self.validated_args)) 
        for args in self.validated_args:
            [x.info(args[0]) for x in args[1]]
        pass



class coreData(collections.UserDict):
   def __init__(self, core, *data, **kwargs):
       super(coreData, self).__init__(data)
       L.debug("init of {}".format(self.__class__))
       self.name = ""
       self.id = 'UUID PLEASE'
       self.core = core
       self.completer = subComp(self, core)
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
       [print(" --| {}".format(x)) for x in self.by_index(arg)]
       self.extra_info(arg)
       
       pass


#########
## hosts
# a simple list -- is index into history for history by host

class hostData(coreData):
    """
    Known hosts
    """
    def __init__(self, core):
        super(hostData,self).__init__(core)
        self.set_name = "hosts"
        # self.completer = hostComp(self, self.core)
        for x in ['liszt', 'tchaikovsky', 'dvorak', 'beethoven']:
            self[x] = None

#########
## command

class commandData(coreData):
    """
    Commands available 
    """
    def __init__(self, core):
        super(commandData, self).__init__(core)
        # self.completer =commandComp(self, core)
        self['info'] = infoCommand(self.core)
        self.name = 'commands'


########
# data objects
class dataData(coreData):
    """ data types avaliable """
    def __init__(self, core):
        super(dataData, self).__init__(core)
        # self.completer=dataComp(self, self.core)
        self.name = 'data'
        self['flists'] =  flistData(self.core)
        self['hosts'] = hostData(self.core)
        self['commands'] = commandData(self.core)

#########
## history

class subComp(cmd.Cmd):
    def __init__(self, data, core):
        L.debug("init of {}".format(self.__class__))
        cmd.Cmd.__init__(self)
        self.core = core
        self.data = data
    def set_core(self, core):
        self.core = core
    def set_core_data(self,  type):
        self.core_data = type
    def gen_comp(self, prev_arg=None):
        return [x for x in self.data]
    def find_in_list(self, x, ls):
        return [f for f in ls if f.startswith(x)]
    def do_info(self, args):
        self.core.commands['info'](args)
    def complete_info(self, text, line, begi, endi):
        completions =  self.core.data['commands']['info'].complete(text, line, begi, endi)
        if text:
            completions = self.find_in_list(text, completions)
        return completions
    def do_EOF(self, line):
        return True

class dataComp(subComp):
    def __init__(self, data, core):
        super(dataComp, self).__init__(data, core)
        self.msg = "Data Completion"

class commandComp(subComp):
    def __init__(self, data, core):
        super(commandComp, self).__init__(data, core)
        self.msg = "Command Completion"
class flistComp(subComp):
    def __init__(self, data, core):
        super(flistComp, self).__init__(data, core)
        self.msg = "Flist Completion"
        
class hostComp(subComp):
    def __init__(self, data, core):
        super(hostComp, self).__init__(data, core)


class daCore(object):
    data_dir=os.path.expanduser("~/.ds")
    def __init__(self):
        self.root =  os.getcwd()
        self.root = '/home/dave'
        self.data = {}
        self.data = dataData(self)
        return
    def ch_dir(self, dir):
        self.root = dir
    def run(self):
        self.data.completer.cmdloop()
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

