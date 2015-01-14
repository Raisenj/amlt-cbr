#!/usr/bin/python

import cmd
import readline
import rlcompleter
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

class Console(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        cmd.completekey='tab'

    def do_help(self,args):
        '''Help'''
        cmd.Cmd.do_help(self, args) 

    ## Command definitions ##
    def do_hist(self, args):
        """Print a list of commands that have been entered"""
        print self._hist

    def do_exit(self, args):
        """Exits from the console"""
        return -1
    ## Override methods in Cmd object ##
    
    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}

    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd documentation, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)   ## Clean up command completion
        print "Exiting..."

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        self._hist += [ line.strip() ]
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        try:
            exec(line) in self._locals, self._globals
        except Exception, e:
            print e.__class__, ":", e
            cmd.Cmd.do_help(self, None)


if __name__ == '__main__':
        console = Console()
        console.cmdloop()


