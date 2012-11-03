#!/use/bin/python
#######################
# ds runs other commands



# Objects ds knows about   
# commands
#   - info
#   - other commands added
#       - sync
#       - grep
#           - todo 
#       - template 
#       ...
# hosts
# file_lists
#   - filters
# history
#   - general
#   - by column and sub columns
#   - frequency list
##-##
## end: objects
#######################

#######################
## funcs for you


# ask_object(obj, var)
#   - select list of obj from input
# ask(var, msg, list)   
# ask_dir(var)
# ask_file(var)
# ---| TODO |--- ask should do dynamic completion ---| 2012-10-22
# register(cmd, cmd_cmd, hosts, file_lists, locations)

## end: funcs for you
#######################


########################################################################
## settings and objects
#####----------------------------------------------------------------{{{

##############################################
## settings
#####--------------------------------------{{{

data_dir="~/.ds"

#####------------------||------------------}}}
## end: settings
##############################################

##############################################
## objects
#####--------------------------------------{{{

#########
## hosts
# a simple list -- is index into history for history by host
hosts=['localhost']

#########
## filelists
# generated and serialized to basic flat files in data_dir. 
# this way, modifing the files directly is ok

flists={'empty': []}

# +-------------------------------------------------------------------------------------------------------+
# |flists are generated from a name.files file and a name.filter file unioned with                        |
# |a global.filter file.  The name.filter file can force add in specs from the global                     |
# |filter                                                                                                 |
# |                                                                                                       |
# |*.files file is just a list like so:                                                                   |
# |    .pad                                                                                               |
# |    .sync                                                                                              |
# |    .vim                                                                                               |
# |    .vimrc                                                                                             |
# |    .zshrc                                                                                             |
# |    code/admin                                                                                         |
# |handling of special cases [ recursion, symbolic links, mounted filesystems ] is dependent              |
# |on the command being run. Although, recursion may be done at the ds level if requested                 |
# |                                                                                                       |
# |*.filter files are also a list but allows globbing like so:                                            |
# |    *.swp                                                                                              |
# |    *.hi                                                                                               |
# |    *.o                                                                                                |
# |                                                                                                       |
# |after the flist is created then filters can be handled two ways                                        |
# |    1) handed as a list to the command : this would be for commands like rsync that handle filters and |
# |        recursion on their own                                                                         |
# |    2) acutally generate full list of files sans the filtered stuff. This would                        |
# |        be recursion handled here in ds with the filtered stuff seperated out                          |
# |        this is:                                                                                       |
# |            nice because it is consistant across commands                                              |
# |            shitty because it is likely slower than the commands handling                              |
# +-------------------------------------------------------------------------------------------------------+ 

#######################
## |TODO|perhaps a check validity of filelists function|1|
## |e09c75ae-e982-4c1b-8905-86276bab7e18|2012-11-02 11:02|dave|


#########
## history
# omg it is a list of dicts for your enjoyment
history=[{'pwd': None, 'time': None, 'cmd': None, 'filelists': None, 'hosts': None, 'cmd_line': None}]

#########
## commands

# list
# info
# history

# +------------------------------------------------------------------+
# |history is an odd bird: it is a command that is somewhat          |
# |added to every other command so that you may have                 |
# |    ds sync history                                               |
# |     - shows sync history                                         |
# |but there is also the top level history command                   |
# |    ds history [index]                                            |
# |     - where index is one of the history fields                   |
# |you may also sub index from various contexts like so              |
# |    ds history time cmd or ds history filelist pwd                |
# |     - first one would be identical to                            |
# |       ds cmd history time                                        |
# |     - the second would show history items using filelist by pwd  |
# |-- sub indexing is filter by default but could have an option for |
# |-- sorted on index output                                         |
# +------------------------------------------------------------------+ 

#####------------------||------------------}}}
## end: objects
##############################################


#####-------------|479a36d8-865a-44a5-b48c-a4003608ad7a|-------------}}}
## end: settings and objects
########################################################################


