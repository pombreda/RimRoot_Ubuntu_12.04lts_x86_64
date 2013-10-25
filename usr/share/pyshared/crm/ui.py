# Copyright (C) 2008 Dejan Muhamedagic <dmuhamedagic@suse.de>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

import sys
import re
import os
import shlex
import time
import bz2

from help import HelpSystem, cmd_help
from vars import Vars
from levels import Levels
from cibconfig import mkset_obj, CibFactory
from cibstatus import CibStatus
from template import LoadTemplate
from cliformat import nvpairs2list
from ra import *
from msg import *
from utils import *
from xmlutil import *

def cmd_end(cmd,dir = ".."):
    "Go up one level."
    levels.droplevel()
def cmd_exit(cmd,rc = 0):
    "Exit the crm program"
    cmd_end(cmd)
    if options.interactive and not options.batch:
        print "bye"
        try:
            from readline import write_history_file
            write_history_file(vars.hist_file)
        except:
            pass
    for f in vars.tmpfiles:
        os.unlink(f)
    sys.exit(rc)

class UserInterface(object):
    '''
    Stuff common to all user interface classes.
    '''
    global_cmd_aliases = {
        "quit": ("bye","exit"),
        "end": ("cd","up"),
    }
    def __init__(self):
        self.help_table = odict()
        self.cmd_table = odict()
        self.cmd_table["help"] = (self.help,(0,1),0,0)
        self.cmd_table["quit"] = (self.exit,(0,0),0,0)
        self.cmd_table["end"] = (self.end,(0,1),0,0)
        self.cmd_aliases = self.global_cmd_aliases.copy()
        if options.interactive:
            self.help_table = help_sys.load_level(self.lvl_name)
    def end_game(self, no_questions_asked = False):
        pass
    def help(self,cmd,topic = ''):
        "usage: help [<topic>]"
        if not self.help_table:
            self.help_table = help_sys.load_level(self.lvl_name)
            setup_help_aliases(self)
        cmd_help(self.help_table,topic)
    def end(self,cmd,dir = ".."):
        "usage: end"
        self.end_game()
        cmd_end(cmd,dir)
    def exit(self,cmd):
        "usage: exit"
        self.end_game()
        cmd_exit(cmd)

class CliOptions(UserInterface):
    '''
    Manage user preferences
    '''
    lvl_name = "options"
    desc_short = "user preferences"
    desc_long = """
Several user preferences are available. Note that it is possible
to save the preferences to a startup file.
"""
    def __init__(self):
        UserInterface.__init__(self)
        self.cmd_table["skill-level"] = (self.set_skill_level,(1,1),0,0)
        self.cmd_table["editor"] = (self.set_editor,(1,1),0,0)
        self.cmd_table["pager"] = (self.set_pager,(1,1),0,0)
        self.cmd_table["user"] = (self.set_crm_user,(0,1),0,0)
        self.cmd_table["output"] = (self.set_output,(1,1),0,0)
        self.cmd_table["colorscheme"] = (self.set_colors,(1,1),0,0)
        self.cmd_table["check-frequency"] = (self.set_check_frequency,(1,1),0,0)
        self.cmd_table["check-mode"] = (self.set_check_mode,(1,1),0,0)
        self.cmd_table["sort-elements"] = (self.set_sort_elements,(1,1),0,0)
        self.cmd_table["wait"] = (self.set_wait,(1,1),0,0)
        self.cmd_table["save"] = (self.save_options,(0,0),0,0)
        self.cmd_table["show"] = (self.show_options,(0,0),0,0)
        setup_aliases(self)
    def set_skill_level(self,cmd,skill_level):
        """usage: skill-level <level>
        level: operator | administrator | expert"""
        return user_prefs.set_skill_level(skill_level)
    def set_editor(self,cmd,prog):
        "usage: editor <program>"
        return user_prefs.set_editor(prog)
    def set_pager(self,cmd,prog):
        "usage: pager <program>"
        return user_prefs.set_pager(prog)
    def set_crm_user(self,cmd,user = ''):
        "usage: user [<crm_user>]"
        return user_prefs.set_crm_user(user)
    def set_output(self,cmd,otypes):
        "usage: output <type>"
        return user_prefs.set_output(otypes)
    def set_colors(self,cmd,scheme):
        "usage: colorscheme <colors>"
        return user_prefs.set_colors(scheme)
    def set_check_frequency(self,cmd,freq):
        "usage: check-frequence <freq>"
        return user_prefs.set_check_freq(freq)
    def set_check_mode(self,cmd,mode):
        "usage: check-mode <mode>"
        return user_prefs.set_check_mode(mode)
    def set_sort_elements(self,cmd,opt):
        "usage: sort-elements {yes|no}"
        if not verify_boolean(opt):
            common_err("%s: bad boolean option"%opt)
            return True
        return user_prefs.set_sort_elems(opt)
    def set_wait(self,cmd,opt):
        "usage: wait {yes|no}"
        if not verify_boolean(opt):
            common_err("%s: bad boolean option"%opt)
            return True
        return user_prefs.set_wait(opt)
    def show_options(self,cmd):
        "usage: show"
        return user_prefs.write_rc(sys.stdout)
    def save_options(self,cmd):
        "usage: save"
        return user_prefs.save_options(vars.rc_file)
    def end_game(self, no_questions_asked = False):
        if no_questions_asked and not options.interactive:
            self.save_options("save")

class CibShadow(UserInterface):
    '''
    CIB shadow management class
    '''
    lvl_name = "cib"
    desc_short = "manage shadow CIBs"
    desc_long = """
A shadow CIB is a regular cluster configuration which is kept in
a file. The CRM and the CRM tools may manage a shadow CIB in the
same way as the live CIB (i.e. the current cluster configuration).
A shadow CIB may be applied to the cluster in one step.
"""
    extcmd = ">/dev/null </dev/null crm_shadow"
    extcmd_stdout = "</dev/null crm_shadow"
    def __init__(self):
        UserInterface.__init__(self)
        self.cmd_table["new"] = (self.new,(1,3),1,0)
        self.cmd_table["delete"] = (self.delete,(1,1),1,0)
        self.cmd_table["reset"] = (self.reset,(1,1),1,0)
        self.cmd_table["commit"] = (self.commit,(1,1),1,1)
        self.cmd_table["use"] = (self.use,(0,2),1,0)
        self.cmd_table["diff"] = (self.diff,(0,0),1,0)
        self.cmd_table["list"] = (self.list,(0,0),1,0)
        self.cmd_table["import"] = (self.pe_import,(1,2),1,0)
        self.cmd_table["cibstatus"] = StatusMgmt
        self.chkcmd()
        setup_aliases(self)
    def chkcmd(self):
        try:
            ext_cmd("%s 2>&1" % self.extcmd)
        except os.error:
            no_prog_err(self.extcmd)
            return False
        return True
    def new(self,cmd,name,*args):
        "usage: new <shadow_cib> [withstatus] [force] [empty]"
        if not is_filename_sane(name):
            return False
        for par in args:
            if not par in ("force","--force","withstatus","empty"):
                syntax_err((cmd,name,par), context = 'new')
                return False
        if "empty" in args:
            new_cmd = "%s -e '%s'" % (self.extcmd,name)
        else:
            new_cmd = "%s -c '%s'" % (self.extcmd,name)
        if user_prefs.get_force() or "force" in args or "--force" in args:
            new_cmd = "%s --force" % new_cmd
        if ext_cmd(new_cmd) == 0:
            common_info("%s shadow CIB created"%name)
            self.use("use",name)
            if "withstatus" in args:
                cib_status.load("shadow:%s" % name)
    def _find_pe(self,infile):
        'Find a pe input'
        for p in ("%s/%s", "%s/%s.bz2", "%s/pe-*-%s.bz2"):
            fl = glob.glob(p % (vars.pe_dir,infile))
            if fl:
                break
        if not fl:
            common_err("no %s pe input file"%infile)
            return ''
        if len(fl) > 1:
            common_err("more than one %s pe input file: %s" % \
                (infile,' '.join(fl)))
            return ''
        return fl[0]
    def pe_import(self,cmd,infile,name = None):
        "usage: import {<file>|<number>} [<shadow>]"
        if name and not is_filename_sane(name):
            return False
        # where's the input?
        if not os.access(infile,os.F_OK):
            if "/" in infile:
                common_err("%s: no such file"%infile)
                return False
            infile = self._find_pe(infile)
            if not infile:
                return False
        if not name:
            name = os.path.basename(infile)
        # read input
        try:
            f = open(infile)
        except IOError,msg:
            common_err("open: %s"%msg)
            return
        s = ''.join(f)
        f.close()
        # decompresed and rename shadow if it ends with .bz2
        if infile.endswith(".bz2"):
            name = name.replace(".bz2","")
            s = bz2.decompress(s)
        # copy input to the shadow
        try:
            f = open(shadowfile(name), "w")
        except IOError,msg:
            common_err("open: %s"%msg)
            return
        f.write(s)
        f.close()
        # use the shadow and load the status from there
        return self.use("use",name,"withstatus")
    def delete(self,cmd,name):
        "usage: delete <shadow_cib>"
        if not is_filename_sane(name):
            return False
        if vars.cib_in_use == name:
            common_err("%s shadow CIB is in use"%name)
            return False
        if ext_cmd("%s -D '%s' --force" % (self.extcmd,name)) == 0:
            common_info("%s shadow CIB deleted"%name)
        else:
            common_err("failed to delete %s shadow CIB"%name)
            return False
    def reset(self,cmd,name):
        "usage: reset <shadow_cib>"
        if not is_filename_sane(name):
            return False
        if ext_cmd("%s -r '%s'" % (self.extcmd,name)) == 0:
            common_info("copied live CIB to %s"%name)
        else:
            common_err("failed to copy live CIB to %s"%name)
            return False
    def commit(self,cmd,name):
        "usage: commit <shadow_cib>"
        if not is_filename_sane(name):
            return False
        if ext_cmd("%s -C '%s' --force" % (self.extcmd,name)) == 0:
            common_info("commited '%s' shadow CIB to the cluster"%name)
        else:
            common_err("failed to commit the %s shadow CIB"%name)
            return False
    def diff(self,cmd):
        "usage: diff"
        s = get_stdout(add_sudo("%s -d" % self.extcmd_stdout))
        page_string(s)
    def list(self,cmd):
        "usage: list"
        if options.regression_tests:
            for t in listshadows():
                print t
        else:
            multicolumn(listshadows())
    def _use(self,name,withstatus):
        # Choose a shadow cib for further changes. If the name
        # provided is empty, then choose the live (cluster) cib.
        # Don't allow ' in shadow names
        if not name or name == "live":
            os.unsetenv(vars.shadow_envvar)
            vars.cib_in_use = ""
            if withstatus:
                cib_status.load("live")
        else:
            os.putenv(vars.shadow_envvar,name)
            vars.cib_in_use = name
            if withstatus:
                cib_status.load("shadow:%s" % name)
    def use(self,cmd,name = '', withstatus = ''):
        "usage: use [<shadow_cib>] [withstatus]"
        # check the name argument
        if name and not is_filename_sane(name):
            return False
        if name and name != "live":
            if not os.access(shadowfile(name),os.F_OK):
                common_err("%s: no such shadow CIB"%name)
                return False
        if withstatus and withstatus != "withstatus":
            syntax_err((cmd,withstatus), context = 'use')
            return False
        # If invoked from configure
        # take special precautions
        try:
            prev_level = levels.previous().myname()
        except:
            prev_level = ''
        if prev_level != "cibconfig":
            self._use(name,withstatus)
            return True
        if not cib_factory.has_cib_changed():
            self._use(name,withstatus)
            # new CIB: refresh the CIB factory
            cib_factory.refresh()
            return True
        saved_cib = vars.cib_in_use
        self._use(name,'') # don't load the status yet
        if not cib_factory.is_current_cib_equal(silent = True):
            # user made changes and now wants to switch to a
            # different and unequal CIB; we refuse to cooperate
            common_err("the requested CIB is different from the current one")
            if user_prefs.get_force():
                common_info("CIB overwrite forced")
            elif not ask("All changes will be dropped. Do you want to proceed?"):
                self._use(saved_cib,'') # revert to the previous CIB
                return False
        self._use(name,withstatus) # now load the status too
        return True

def check_transition(inp,state,possible_l):
    if not state in possible_l:
        common_err("input (%s) in wrong state %s" % (inp,state))
        return False
    return True
class Template(UserInterface):
    '''
    Configuration templates.
    '''
    lvl_name = "template"
    def __init__(self):
        UserInterface.__init__(self)
        self.cmd_table["new"] = (self.new,(2,),1,0)
        self.cmd_table["load"] = (self.load,(0,1),1,0)
        self.cmd_table["edit"] = (self.edit,(0,1),1,0)
        self.cmd_table["delete"] = (self.delete,(1,2),1,0)
        self.cmd_table["show"] = (self.show,(0,1),0,0)
        self.cmd_table["apply"] = (self.apply,(0,2),1,0)
        self.cmd_table["list"] = (self.list,(0,1),0,0)
        setup_aliases(self)
        self.init_dir()
        self.curr_conf = ''
    def init_dir(self):
        '''Create the conf directory, link to templates'''
        if not os.path.isdir(vars.tmpl_conf_dir):
            try:
                os.makedirs(vars.tmpl_conf_dir)
            except os.error,msg:
                common_err("makedirs: %s"%msg)
                return
    def get_depends(self,tmpl):
        '''return a list of required templates'''
        # Not used. May need it later.
        try:
            tf = open("%s/%s" % (vars.tmpl_dir, tmpl),"r")
        except IOError,msg:
            common_err("open: %s"%msg)
            return
        l = []
        for s in tf:
            a = s.split()
            if len(a) >= 2 and a[0] == '%depends_on':
                l += a[1:]
        tf.close()
        return l
    def replace_params(self,s,user_data):
        change = False
        for i in range(len(s)):
            word = s[i]
            for p in user_data:
                # is parameter in the word?
                pos = word.find('%' + p) 
                if pos < 0:
                    continue
                endpos = pos + len('%' + p)
                # and it isn't part of another word?
                if re.match("[A-Za-z0-9]", word[endpos:endpos+1]):
                    continue
                # if the value contains a space or
                # it is a value of an attribute
                # put quotes around it
                if user_data[p].find(' ') >= 0 or word[pos-1:pos] == '=':
                    v = '"' + user_data[p] + '"'
                else:
                    v = user_data[p]
                word = word.replace('%' + p, v)
                change = True # we did replace something
            if change:
                s[i] = word
        if 'opt' in s:
            if not change:
                s = []
            else:
                s.remove('opt')
        return s
    def generate(self,l,user_data):
        '''replace parameters (user_data) and generate output
        '''
        l2 = []
        for piece in l:
            piece2 = []
            for s in piece:
                s = self.replace_params(s,user_data)
                if s:
                    piece2.append(' '.join(s))
            if piece2:
                l2.append(' \\\n\t'.join(piece2))
        return '\n'.join(l2)
    def process(self,config = ''):
        '''Create a cli configuration from the current config'''
        try:
            f = open("%s/%s" % (vars.tmpl_conf_dir, config or self.curr_conf),'r')
        except IOError,msg:
            common_err("open: %s"%msg)
            return ''
        l = []
        piece = []
        user_data = {}
        # states
        START = 0; PFX = 1; DATA = 2; GENERATE = 3
        state = START
        err_buf.start_tmp_lineno()
        rc = True
        for inp in f:
            err_buf.incr_lineno()
            if inp.startswith('#'):
                continue
            if type(inp) == type(u''):
                inp = inp.encode('ascii')
            inp = inp.strip()
            try:
                s = shlex.split(inp)
            except ValueError, msg:
                common_err(msg)
                continue
            while '\n' in s:
                s.remove('\n')
            if not s:
                if state == GENERATE and piece:
                    l.append(piece)
                    piece = []
            elif s[0] in ("%name","%depends_on","%suggests"):
                continue
            elif s[0] == "%pfx":
                if check_transition(inp,state,(START,DATA)) and len(s) == 2:
                    pfx = s[1]
                    state = PFX
            elif s[0] == "%required":
                if check_transition(inp,state,(PFX,)):
                    state = DATA
                    data_reqd = True
            elif s[0] == "%optional":
                if check_transition(inp,state,(PFX,DATA)):
                    state = DATA
                    data_reqd = False
            elif s[0] == "%%":
                if state != DATA:
                    common_warn("user data in wrong state %s" % state)
                if len(s) < 2:
                    common_warn("parameter name missing")
                elif len(s) == 2:
                    if data_reqd:
                        common_err("required parameter %s not set" % s[1])
                        rc = False
                elif len(s) == 3:
                    user_data["%s:%s" % (pfx,s[1])] = s[2]
                else:
                    common_err("%s: syntax error" % inp)
            elif s[0] == "%generate":
                if check_transition(inp,state,(DATA,)):
                    state = GENERATE
                    piece = []
            elif state == GENERATE:
                if s:
                    piece.append(s)
            else:
                common_err("<%s> unexpected" % inp)
        if piece:
            l.append(piece)
        err_buf.stop_tmp_lineno()
        f.close()
        if not rc:
            return ''
        return self.generate(l,user_data)
    def new(self,cmd,name,*args):
        "usage: new <config> <template> [<template> ...] [params name=value ...]"
        if not is_filename_sane(name):
            return False
        if os.path.isfile("%s/%s" % (vars.tmpl_conf_dir, name)):
            common_err("config %s exists; delete it first" % name)
            return False
        lt = LoadTemplate(name)
        rc = True
        mode = 0
        params = {}
        for s in args:
            if mode == 0 and s == "params":
                params["id"] = name
                mode = 1
            elif mode == 1:
                a = s.split('=')
                if len(a) != 2:
                    syntax_err(args, context = 'new')
                    rc = False
                else:
                    params[a[0]] = a[1]
            elif not lt.load_template(s):
                rc = False
        if rc:
            lt.post_process(params)
        if not rc or not lt.write_config(name):
            return False
        self.curr_conf = name
    def config_exists(self,name):
        if not is_filename_sane(name):
            return False
        if not os.path.isfile("%s/%s" % (vars.tmpl_conf_dir, name)):
            common_err("%s: no such config" % name)
            return False
        return True
    def delete(self,cmd,name,force = ''):
        "usage: delete <config> [force]"
        if force:
            if force != "force" and force != "--force":
                syntax_err((cmd,force), context = 'delete')
                return False
        if not self.config_exists(name):
            return False
        if name == self.curr_conf:
            if not force and not user_prefs.get_force() and \
                    not ask("Do you really want to remove config %s which is in use?" % self.curr_conf):
                return False
            else:
                self.curr_conf = ''
        os.remove("%s/%s" % (vars.tmpl_conf_dir, name))
    def load(self,cmd,name = ''):
        "usage: load [<config>]"
        if not name:
            self.curr_conf = ''
            return True
        if not self.config_exists(name):
            return False
        self.curr_conf = name
    def edit(self,cmd,name = ''):
        "usage: edit [<config>]"
        if not name and not self.curr_conf:
            common_err("please load a config first")
            return False
        if name:
            if not self.config_exists(name):
                return False
            edit_file("%s/%s" % (vars.tmpl_conf_dir, name))
        else:
            edit_file("%s/%s" % (vars.tmpl_conf_dir, self.curr_conf))
    def show(self,cmd,name = ''):
        "usage: show [<config>]"
        if not name and not self.curr_conf:
            common_err("please load a config first")
            return False
        if name:
            if not self.config_exists(name):
                return False
            print self.process(name)
        else:
            print self.process()
    def apply(self,cmd,*args):
        "usage: apply [<method>] [<config>]"
        method = "replace"
        name = ''
        if len(args) > 0:
            i = 0
            if args[0] in ("replace","update"):
                method = args[0]
                i += 1
            if len(args) > i:
                name = args[i]
        if not name and not self.curr_conf:
            common_err("please load a config first")
            return False
        if name:
            if not self.config_exists(name):
                return False
            s = self.process(name)
        else:
            s = self.process()
        if not s:
            return False
        tmp = str2tmp(s)
        if not tmp:
            return False
        set_obj = mkset_obj("NOOBJ")
        rc = set_obj.import_file(method,tmp)
        try: os.unlink(tmp)
        except: pass
        return rc
    def list(self,cmd,templates = ''):
        "usage: list [templates]"
        if templates == "templates":
            multicolumn(listtemplates())
        else:
            multicolumn(listconfigs())

def manage_attr(cmd,attr_ext_commands,*args):
    if len(args) < 3:
        bad_usage(cmd,' '.join(args))
        return False
    attr_cmd = None
    try:
        attr_cmd = attr_ext_commands[args[1]]
    except KeyError:
        bad_usage(cmd,' '.join(args))
        return False
    if not attr_cmd:
        bad_usage(cmd,' '.join(args))
        return False
    if args[1] == 'set':
        if len(args) == 4:
            if not is_name_sane(args[0]) \
                    or not is_name_sane(args[2]) \
                    or not is_value_sane(args[3]):
                return False
            return ext_cmd(attr_cmd%(args[0],args[2],args[3])) == 0
        else:
            bad_usage(cmd,' '.join(args))
            return False
    elif args[1] in ('delete','show'):
        if len(args) == 3:
            if not is_name_sane(args[0]) \
                    or not is_name_sane(args[2]):
                return False
            return ext_cmd(attr_cmd%(args[0],args[2])) == 0
        else:
            bad_usage(cmd,' '.join(args))
            return False
    else:
        bad_usage(cmd,' '.join(args))
        return False

def rm_meta_attribute(node,attr,l):
    '''
    Build a list of nvpair nodes which contain attribute
    (recursively in all children resources)
    '''
    for c in node.childNodes:
        if not is_element(c):
            continue
        if c.tagName == "meta_attributes":
            nvpair = get_attr_in_set(c,attr)
            if nvpair:
                l.append(nvpair)
        elif is_child_rsc(c) and not c.parentNode.tagName == "group":
            rm_meta_attribute(c,attr,l)
def clean_inferior_attributes(node,attr):
    'Remove attr from all resources below'
    l = []
    for c in node.childNodes:
        if is_child_rsc(c):
            rm_meta_attribute(c,attr,l)
    rmnodes(l)
def set_deep_meta_attr(attr,value,rsc_id):
    '''
    If the referenced rsc is a primitive that belongs to a group,
    then set its attribute.
    Otherwise, go up to the topmost resource which contains this
    resource and set the attribute there and remove all the
    attributes which may be set in its children.
    '''
    target_node = rsc2node(rsc_id)
    if not target_node:
        common_error("resource %s does not exist" % rsc_id)
        return False
    if not (target_node.tagName == "primitive" and \
        target_node.parentNode.tagName == "group"):
        target_node = get_topmost_rsc(target_node)
    clean_inferior_attributes(target_node,attr)
    for n in get_set_nodes(target_node,"meta_attributes",1):
        set_attr(n,attr,value)
    return commit_rsc(target_node)

def get_max_clone(id):
    v = get_meta_param(id,"clone-max")
    try:
        cnt = int(v)
    except:
        cnt = len(listnodes())
    return cnt
def cleanup_resource(rsc,node = ''):
    if not is_name_sane(rsc) or not is_name_sane(node):
        return False
    if not node:
        rc = ext_cmd(RscMgmt.rsc_cleanup_all%(rsc)) == 0
    else:
        rc = ext_cmd(RscMgmt.rsc_cleanup%(rsc,node)) == 0
    return rc

class RscMgmt(UserInterface):
    '''
    Resources management class
    '''
    lvl_name = "resource"
    desc_short = "resources management"
    desc_long = """
Everything related to resources management is available at this
level. Most commands are implemented using the crm_resource(8)
program.
"""
    rsc_status_all = "crm_resource -L"
    rsc_status = "crm_resource -W -r '%s'"
    rsc_showxml = "crm_resource -q -r '%s'"
    rsc_setrole = "crm_resource --meta -r '%s' -p target-role -v '%s'"
    rsc_migrate = "crm_resource -M -r '%s' %s"
    rsc_unmigrate = "crm_resource -U -r '%s'"
    rsc_cleanup = "crm_resource -C -r '%s' -H '%s'"
    rsc_cleanup_all = "crm_resource -C -r '%s'"
    rsc_param =  {
        'set': "crm_resource -r '%s' -p '%s' -v '%s'",
        'delete': "crm_resource -r '%s' -d '%s'",
        'show': "crm_resource -r '%s' -g '%s'",
    }
    rsc_meta =  {
        'set': "crm_resource --meta -r '%s' -p '%s' -v '%s'",
        'delete': "crm_resource --meta -r '%s' -d '%s'",
        'show': "crm_resource --meta -r '%s' -g '%s'",
    }
    rsc_failcount = {
        'set': "crm_attribute -t status -n 'fail-count-%s' -N '%s' -v '%s' -d 0",
        'delete': "crm_attribute -t status -n 'fail-count-%s' -N '%s' -D -d 0",
        'show': "crm_attribute -t status -n 'fail-count-%s' -N '%s' -G -d 0",
    }
    rsc_utilization =  {
        'set': "crm_resource -z -r '%s' -p '%s' -v '%s'",
        'delete': "crm_resource -z -r '%s' -d '%s'",
        'show': "crm_resource -z -r '%s' -g '%s'",
    }
    rsc_refresh = "crm_resource -R"
    rsc_refresh_node = "crm_resource -R -H '%s'"
    rsc_reprobe = "crm_resource -P"
    rsc_reprobe_node = "crm_resource -P -H '%s'"
    def __init__(self):
        UserInterface.__init__(self)
        self.cmd_table["status"] = (self.status,(0,1),0,0)
        self.cmd_table["start"] = (self.start,(1,1),0,1)
        self.cmd_table["stop"] = (self.stop,(1,1),0,1)
        self.cmd_table["restart"] = (self.restart,(1,1),0,1)
        self.cmd_table["promote"] = (self.promote,(1,1),0,1)
        self.cmd_table["demote"] = (self.demote,(1,1),0,1)
        self.cmd_table["manage"] = (self.manage,(1,1),0,0)
        self.cmd_table["unmanage"] = (self.unmanage,(1,1),0,0)
        self.cmd_table["migrate"] = (self.migrate,(1,4),0,1)
        self.cmd_table["unmigrate"] = (self.unmigrate,(1,1),0,1)
        self.cmd_table["param"] = (self.param,(3,4),1,1)
        self.cmd_table["meta"] = (self.meta,(3,4),1,1)
        self.cmd_table["utilization"] = (self.utilization,(3,4),1,1)
        self.cmd_table["failcount"] = (self.failcount,(3,4),0,0)
        self.cmd_table["cleanup"] = (self.cleanup,(1,2),1,1)
        self.cmd_table["refresh"] = (self.refresh,(0,1),0,0)
        self.cmd_table["reprobe"] = (self.reprobe,(0,1),0,1)
        self.cmd_aliases.update({
            "status": ("show","list",),
            "migrate": ("move",),
            "unmigrate": ("unmove",),
        })
        setup_aliases(self)
    def status(self,cmd,rsc = None):
        "usage: status [<rsc>]"
        if rsc:
            if not is_name_sane(rsc):
                return False
            return ext_cmd(self.rsc_status % rsc) == 0
        else:
            return ext_cmd(self.rsc_status_all) == 0
    def start(self,cmd,rsc):
        "usage: start <rsc>"
        if not is_name_sane(rsc):
            return False
        return set_deep_meta_attr("target-role","Started",rsc)
    def restart(self,cmd,rsc):
        "usage: restart <rsc>"
        if not is_name_sane(rsc):
            return False
        common_info("ordering %s to stop" % rsc)
        if not self.stop("stop",rsc):
            return False
        if not wait4dc("stop", not options.batch):
            return False
        common_info("ordering %s to start" % rsc)
        return self.start("start",rsc)
    def stop(self,cmd,rsc):
        "usage: stop <rsc>"
        if not is_name_sane(rsc):
            return False
        return set_deep_meta_attr("target-role","Stopped",rsc)
    def promote(self,cmd,rsc):
        "usage: promote <rsc>"
        if not is_name_sane(rsc):
            return False
        if not is_rsc_ms(rsc):
            common_err("%s is not a master-slave resource" % rsc)
            return False
        return ext_cmd(self.rsc_setrole%(rsc,"Master")) == 0
    def demote(self,cmd,rsc):
        "usage: demote <rsc>"
        if not is_name_sane(rsc):
            return False
        if not is_rsc_ms(rsc):
            common_err("%s is not a master-slave resource" % rsc)
            return False
        return ext_cmd(self.rsc_setrole%(rsc,"Slave")) == 0
    def manage(self,cmd,rsc):
        "usage: manage <rsc>"
        if not is_name_sane(rsc):
            return False
        return set_deep_meta_attr("is-managed","true",rsc)
    def unmanage(self,cmd,rsc):
        "usage: unmanage <rsc>"
        if not is_name_sane(rsc):
            return False
        return set_deep_meta_attr("is-managed","false",rsc)
    def migrate(self,cmd,*args):
        """usage: migrate <rsc> [<node>] [<lifetime>] [force]"""
        rsc = args[0]
        if not is_name_sane(rsc):
            return False
        node = None
        lifetime = None
        force = False
        if len(args) == 2:
            if not args[1] in listnodes():
                if args[1] == "force":
                    force = True
                else:
                    lifetime = args[1]
            else:
                node = args[1]
        elif len(args) == 3:
            if not args[1] in listnodes():
                lifetime = args[1]
                force = True
            else:
                node = args[1]
                if args[2] == "force":
                    force = True
                else:
                    lifetime = args[2]
        elif len(args) == 4:
            if not is_name_sane(args[1]):
                return False
            node = args[1]
            lifetime = args[2]
            if not args[3] == "force":
                syntax_err((cmd,force))
                return False
            force = True
        opts = ''
        if node:
            opts = "--node='%s'" % node
        if lifetime:
            opts = "%s --lifetime='%s'" % (opts,lifetime)
        if force or user_prefs.get_force():
            opts = "%s --force" % opts
        return ext_cmd(self.rsc_migrate % (rsc,opts)) == 0
    def unmigrate(self,cmd,rsc):
        "usage: unmigrate <rsc>"
        if not is_name_sane(rsc):
            return False
        return ext_cmd(self.rsc_unmigrate%rsc) == 0
    def cleanup(self,cmd,*args):
        "usage: cleanup <rsc> [<node>]"
        # Cleanup a resource on a node. Omit node to cleanup on
        # all live nodes.
        if len(args) == 2: # remove
            return cleanup_resource(args[0],args[1])
        else:
            return cleanup_resource(args[0])
    def failcount(self,cmd,*args):
        """usage:
        failcount <rsc> set <node> <value>
        failcount <rsc> delete <node>
        failcount <rsc> show <node>"""
        d = lambda: manage_attr(cmd,self.rsc_failcount,*args)
        return d()
    def param(self,cmd,*args):
        """usage:
        param <rsc> set <param> <value>
        param <rsc> delete <param>
        param <rsc> show <param>"""
        d = lambda: manage_attr(cmd,self.rsc_param,*args)
        return d()
    def meta(self,cmd,*args):
        """usage:
        meta <rsc> set <attr> <value>
        meta <rsc> delete <attr>
        meta <rsc> show <attr>"""
        d = lambda: manage_attr(cmd,self.rsc_meta,*args)
        return d()
    def utilization(self,cmd,*args):
        """usage:
        utilization <rsc> set <attr> <value>
        utilization <rsc> delete <attr>
        utilization <rsc> show <attr>"""
        d = lambda: manage_attr(cmd,self.rsc_utilization,*args)
        return d()
    def refresh(self,cmd,*args):
        'usage: refresh [<node>]'
        if len(args) == 1:
            if not is_name_sane(args[0]):
                return False
            return ext_cmd(self.rsc_refresh_node%args[0]) == 0
        else:
            return ext_cmd(self.rsc_refresh) == 0
    def reprobe(self,cmd,*args):
        'usage: reprobe [<node>]'
        if len(args) == 1:
            if not is_name_sane(args[0]):
                return False
            return ext_cmd(self.rsc_reprobe_node%args[0]) == 0
        else:
            return ext_cmd(self.rsc_reprobe) == 0

def print_node(uname,id,node_type,other,inst_attr,offline):
    """
    Try to pretty print a node from the cib. Sth like:
    uname(id): node_type
        attr1: v1
        attr2: v2
    """
    s_offline = offline and "(offline)" or ""
    if uname == id:
        print "%s: %s%s" % (uname,node_type,s_offline)
    else:
        print "%s(%s): %s%s" % (uname,id,node_type,s_offline)
    for a in other:
        print "\t%s: %s" % (a,other[a])
    for a,v in inst_attr:
        print "\t%s: %s" % (a,v)

class NodeMgmt(UserInterface):
    '''
    Nodes management class
    '''
    lvl_name = "node"
    desc_short = "nodes management"
    desc_long = """
A few node related tasks such as node standby are implemented
here.
"""
    node_standby = "crm_attribute -N '%s' -n standby -v '%s' %s"
    node_delete = "cibadmin -D -o nodes -X '<node uname=\"%s\"/>'"
    node_delete_status = "cibadmin -D -o status -X '<node_state uname=\"%s\"/>'"
    node_clear_state = "cibadmin %s -o status --xml-text '<node_state id=\"%s\" uname=\"%s\" ha=\"active\" in_ccm=\"false\" crmd=\"offline\" join=\"member\" expected=\"down\" crm-debug-origin=\"manual_clear\" shutdown=\"0\"/>'"
    hb_delnode = "/usr/share/heartbeat/hb_delnode '%s'"
    crm_node = "crm_node"
    node_fence = "crm_attribute -t status -U '%s' -n terminate -v true"
    dc = "crmadmin -D"
    node_attr = {
        'set': "crm_attribute -t nodes -U '%s' -n '%s' -v '%s'",
        'delete': "crm_attribute -D -t nodes -U '%s' -n '%s'",
        'show': "crm_attribute -G -t nodes -U '%s' -n '%s'",
    }
    node_status = {
        'set': "crm_attribute -t status -U '%s' -n '%s' -v '%s'",
        'delete': "crm_attribute -D -t status -U '%s' -n '%s'",
        'show': "crm_attribute -G -t status -U '%s' -n '%s'",
    }
    node_utilization = {
        'set': "crm_attribute -z -t nodes -U '%s' -n '%s' -v '%s'",
        'delete': "crm_attribute -z -D -t nodes -U '%s' -n '%s'",
        'show': "crm_attribute -z -G -t nodes -U '%s' -n '%s'",
    }
    def __init__(self):
        UserInterface.__init__(self)
        self.cmd_table["status"] = (self.status,(0,1),0,0)
        self.cmd_table["show"] = (self.show,(0,1),0,0)
        self.cmd_table["standby"] = (self.standby,(0,2),0,1)
        self.cmd_table["online"] = (self.online,(0,1),0,1)
        self.cmd_table["fence"] = (self.fence,(1,1),0,1)
        self.cmd_table["delete"] = (self.delete,(1,1),0,0)
        self.cmd_table["clearstate"] = (self.clearstate,(1,1),0,1)
        self.cmd_table["attribute"] = (self.attribute,(3,4),0,1)
        self.cmd_table["utilization"] = (self.utilization,(3,4),0,1)
        self.cmd_table["status-attr"] = (self.status_attr,(3,4),0,1)
        self.cmd_aliases.update({
            "show": ("list",),
        })
        setup_aliases(self)
    def status(self,cmd,node = None):
        'usage: status [<node>]'
        return ext_cmd("%s -o nodes"%cib_dump) == 0
    def show(self,cmd,node = None):
        'usage: show [<node>]'
        doc = cibdump2doc()
        if not doc:
            return False
        nodes_node = get_conf_elem(doc, "nodes")
        status = get_conf_elem(doc, "status")
        if not nodes_node:
            return False
        for c in nodes_node.childNodes:
            if not is_element(c) or c.tagName != "node":
                continue
            if node and c.getAttribute("uname") != node:
                continue
            type = uname = id = ""
            inst_attr = []
            other = {}
            for attr in c.attributes.keys():
                v = c.getAttribute(attr)
                if attr == "type":
                    type = v
                elif attr == "uname":
                    uname = v
                elif attr == "id":
                    id = v
                else:
                    other[attr] = v
            for c2 in c.childNodes:
                if not is_element(c2):
                    continue
                if c2.tagName == "instance_attributes":
                    inst_attr += nvpairs2list(c2)
            offline = False
            for c2 in status.getElementsByTagName("node_state"):
                if uname != c2.getAttribute("uname"):
                    continue
                offline = c2.getAttribute("crmd") == "offline"
            print_node(uname,id,type,other,inst_attr,offline)
    def standby(self,cmd,*args):
        'usage: standby [<node>] [<lifetime>]'
        node = None
        lifetime = None
        if not args:
            node = vars.this_node
        if len(args) == 1:
            if not args[0] in listnodes():
                node = vars.this_node
                lifetime = args[0]
            else:
                node = args[0]
        elif len(args) == 2:
            node = args[0]
            lifetime = args[1]
        if lifetime not in (None,"reboot","forever"):
            common_err("bad lifetime: %s" % lifetime)
            return False
        if not is_name_sane(node):
            return False
        opts = ''
        if lifetime:
            opts = "--lifetime='%s'" % lifetime
        else:
            opts = "--lifetime='forever'"
        return ext_cmd(self.node_standby%(node,"on",opts)) == 0
    def online(self,cmd,node = None):
        'usage: online [<node>]'
        if not node:
            node = vars.this_node
        if not is_name_sane(node):
            return False
        return ext_cmd(self.node_standby%(node,"off","--lifetime='forever'")) == 0
    def fence(self,cmd,node):
        'usage: fence <node>'
        if not node:
            node = vars.this_node
        if not is_name_sane(node):
            return False
        if not user_prefs.get_force() and \
                not ask("Do you really want to shoot %s?" % node):
            return False
        return ext_cmd(self.node_fence%(node)) == 0
    def clearstate(self,cmd,node):
        'usage: clearstate <node>'
        if not is_name_sane(node):
            return False
        if not user_prefs.get_force() and \
                not ask("Do you really want to drop state for node %s?" % node):
            return False
        return ext_cmd(self.node_clear_state%("-M -c",node,node)) == 0 and \
            ext_cmd(self.node_clear_state%("-R",node,node)) == 0
    def delete(self,cmd,node):
        'usage: delete <node>'
        if not is_name_sane(node):
            return False
        if not node in listnodes():
            common_err("node %s not found in the CIB" % node)
            return False
        rc = True
        if cluster_stack() == "heartbeat":
            rc = ext_cmd(self.hb_delnode%node) == 0
        else:
            node_states = {}
            for s in stdout2list("%s -l" % self.crm_node):
                a = s.split()
                if len(a) != 3:
                    common_warn("%s bad format: %s" % (self.crm_node,s))
                    continue
                # fmt: id uname status
                # remove only those in state "lost"
                if a[1] == node:
                    node_states[a[2]] = 1
                    if a[2] == "lost":
                        ec = ext_cmd("%s --force -R %s" % (self.crm_node,a[0]))
                        if ec != 0:
                            common_warn('"%s --force -R %s" failed, rc=%d' % (self.crm_node,a[0],ec))
            if not node_states:
                common_info("node %s not found by %s" % (node,self.crm_node))
            elif "member" in node_states:
                common_info("node %s appears to be still active" % node)
                common_info("check output of %s -l" % self.crm_node)
                rc = False
            elif not "lost" in node_states:
                common_err("node %s's state not recognized: %s" % (node,node_states.keys()))
                common_info("check output of %s -l" % self.crm_node)
                rc = False
        if rc:
            if ext_cmd(self.node_delete%node) != 0 or \
                    ext_cmd(self.node_delete_status%node) != 0:
                common_err("failed to remove %s from the CIB" % node)
                rc = False
        if rc:
            common_info("node %s deleted" % node)
        else:
            common_err('failed to delete node %s' % node)
        return rc
    def attribute(self,cmd,*args):
        """usage:
        attribute <node> set <rsc> <value>
        attribute <node> delete <rsc>
        attribute <node> show <rsc>"""
        d = lambda: manage_attr(cmd,self.node_attr,*args)
        return d()
    def utilization(self,cmd,*args):
        """usage:
        utilization <node> set <rsc> <value>
        utilization <node> delete <rsc>
        utilization <node> show <rsc>"""
        d = lambda: manage_attr(cmd,self.node_utilization,*args)
        return d()
    def status_attr(self,cmd,*args):
        """usage:
        status-attr <node> set <rsc> <value>
        status-attr <node> delete <rsc>
        status-attr <node> show <rsc>"""
        d = lambda: manage_attr(cmd,self.node_status,*args)
        return d()

class RA(UserInterface):
    '''
    CIB shadow management class
    '''
    lvl_name = "ra"
    desc_short = "resource agents information center"
    desc_long = """
This level contains commands which show various information about
the installed resource agents. It is available both at the top
level and at the `configure` level.
"""
    provider_classes = ["ocf"]
    def __init__(self):
        UserInterface.__init__(self)
        self.cmd_table["classes"] = (self.classes,(0,0),0,0)
        self.cmd_table["list"] = (self.list,(1,2),1,0)
        self.cmd_table["providers"] = (self.providers,(1,2),1,0)
        self.cmd_table["meta"] = (self.meta,(1,3),1,0)
        self.cmd_aliases.update({
            "meta": ("info",),
        })
        setup_aliases(self)
    def classes(self,cmd):
        "usage: classes"
        for c in ra_classes():
            if c in self.provider_classes:
                print "%s / %s" % (c,' '.join(ra_providers_all(c)))
            else:
                print "%s" % c
    def providers(self,cmd,ra_type,ra_class = "ocf"):
        "usage: providers <ra> [<class>]"
        print ' '.join(ra_providers(ra_type,ra_class))
    def list(self,cmd,c,p = None):
        "usage: list <class> [<provider>]"
        if not c in ra_classes():
            common_err("class %s does not exist" % c)
            return False
        if p and not p in ra_providers_all(c):
            common_err("there is no provider %s for class %s" % (p,c))
            return False
        if options.regression_tests:
            for t in ra_types(c,p):
                print t
        else:
            multicolumn(ra_types(c,p))
    def meta(self,cmd,*args):
        "usage: meta [<class>:[<provider>:]]<type>"
        if len(args) > 1: # obsolete syntax
            ra_type = args[0]
            ra_class = args[1]
            if len(args) < 3:
                ra_provider = "heartbeat"
            else:
                ra_provider = args[2]
        else:
            if args[0] in vars.meta_progs:
                ra_class = args[0]
                ra_provider = ra_type = None
            else:
                ra_class,ra_provider,ra_type = disambiguate_ra_type(args[0])
        ra = RAInfo(ra_class,ra_type,ra_provider)
        if not ra.mk_ra_node():
            return False
        try:
            page_string(ra.meta_pretty())
        except:
            return False

def ptestlike(simfun,def_verb,cmd,*args):
    verbosity = def_verb  # default verbosity
    nograph = False
    scores = False
    utilization = False
    actions = False
    for p in args:
        if p == "nograph":
            nograph = True
        elif p == "scores":
            scores = True
        elif p == "utilization":
            utilization = True
        elif p == "actions":
            actions = True
        elif re.match("^vv*$", p):
            verbosity = p
        else:
            bad_usage(cmd,' '.join(args))
            return False
    return simfun(nograph, scores, utilization, actions, verbosity)

class StatusMgmt(UserInterface):
    '''
    The CIB status section management user interface class
    '''
    lvl_name = "cibstatus"
    def __init__(self):
        UserInterface.__init__(self)
        self.cmd_table["show"] = (self.show,(0,1),1,0)
        self.cmd_table["save"] = (self.save,(0,1),2,0)
        self.cmd_table["load"] = (self.load,(1,1),2,0)
        self.cmd_table["origin"] = (self.origin,(0,0),1,0)
        self.cmd_table["node"] = (self.edit_node,(2,2),2,0)
        self.cmd_table["op"] = (self.edit_op,(3,5),2,0)
        self.cmd_table["run"] = (self.run,(0,3),1,0)
        self.cmd_table["simulate"] = (self.simulate,(0,3),1,0)
        self.cmd_table["quorum"] = (self.quorum,(1,1),1,0)
        setup_aliases(self)
    def myname(self):
        '''Just return some id.'''
        return "cibstatus"
    def load(self,cmd,org):
        "usage: load {<file>|shadow:<cib>|live}"
        return cib_status.load(org)
    def save(self,cmd,dest = None):
        "usage: save [<file>|shadow:<cib>]"
        return cib_status.save(dest)
    def origin(self,cmd):
        "usage: origin"
        state = cib_status.modified and " (modified)" or ""
        print "%s%s" % (cib_status.origin,state)
    def show(self,cmd,changed = ""):
        "usage: show [changed]"
        if changed:
            if changed != "changed":
                syntax_err((cmd,changed))
                return False
            else:
                return cib_status.list_changes()
        return cib_status.show()
    def quorum(self,cmd,opt):
        "usage: quorum <bool>"
        if not verify_boolean(opt):
            common_err("%s: bad boolean option"%opt)
            return False
        return cib_status.set_quorum(is_boolean_true(opt))
    def edit_node(self,cmd,node,state):
        "usage: node <node> {online|offline|unclean}"
        return cib_status.edit_node(node,state)
    def edit_op(self,cmd,op,rsc,rc,op_status = None,node = ''):
        "usage: op <operation> <resource> <exit_code> [<op_status>] [<node>]"
        if rc in vars.lrm_exit_codes:
            num_rc = vars.lrm_exit_codes[rc]
        else:
            num_rc = rc
        if not num_rc.isdigit():
            common_err("%s exit code invalid" % num_rc)
            return False
        num_op_status = op_status
        if op_status:
            if op_status in vars.lrm_status_codes:
                num_op_status = vars.lrm_status_codes[op_status]
            if not num_op_status.isdigit():
                common_err("%s operation status invalid" % num_op_status)
                return False
        return cib_status.edit_op(op,rsc,num_rc,num_op_status,node)
    def run(self,cmd,*args):
        "usage: run [nograph] [v...] [scores] [utilization]"
        return ptestlike(cib_status.run,'',cmd,*args)
    def simulate(self,cmd,*args):
        "usage: simulate [nograph] [v...] [scores] [utilization]"
        return ptestlike(cib_status.simulate,'',cmd,*args)

class CibConfig(UserInterface):
    '''
    The configuration class
    '''
    lvl_name = "configure"
    desc_short = "CRM cluster configuration"
    desc_long = """
The configuration level.

Note that you can change the working CIB at the cib level. It is
advisable to configure shadow CIBs and then commit them to the
cluster.
"""
    def __init__(self):
        UserInterface.__init__(self)
        self.cmd_table["erase"] = (self.erase,(0,1),1,0)
        self.cmd_table["verify"] = (self.verify,(0,0),1,0)
        self.cmd_table["refresh"] = (self.refresh,(0,0),1,0)
        self.cmd_table["ptest"] = (self.ptest,(0,3),1,0)
        self.cmd_table["commit"] = (self.commit,(0,1),1,1)
        self.cmd_table["upgrade"] = (self.upgrade,(0,1),1,0)
        self.cmd_table["show"] = (self.show,(0,),1,0)
        self.cmd_table["edit"] = (self.edit,(0,),1,0)
        self.cmd_table["filter"] = (self.filter,(1,),1,0)
        self.cmd_table["delete"] = (self.delete,(1,),1,0)
        self.cmd_table["default-timeouts"] = (self.default_timeouts,(1,),1,0)
        self.cmd_table["rename"] = (self.rename,(2,2),1,0)
        self.cmd_table["save"] = (self.save,(1,2),1,0)
        self.cmd_table["load"] = (self.load,(2,3),1,0)
        self.cmd_table["node"] = (self.conf_node,(1,),1,0)
        self.cmd_table["primitive"] = (self.conf_primitive,(2,),1,0)
        self.cmd_table["group"] = (self.conf_group,(2,),1,0)
        self.cmd_table["clone"] = (self.conf_clone,(2,),1,0)
        self.cmd_table["ms"] = (self.conf_ms,(2,),1,0)
        self.cmd_table["location"] = (self.conf_location,(2,),1,0)
        self.cmd_table["colocation"] = (self.conf_colocation,(2,),1,0)
        self.cmd_table["order"] = (self.conf_order,(2,),1,0)
        self.cmd_table["property"] = (self.conf_property,(1,),1,0)
        self.cmd_table["rsc_defaults"] = (self.conf_rsc_defaults,(1,),1,0)
        self.cmd_table["op_defaults"] = (self.conf_op_defaults,(1,),1,0)
        self.cmd_table["xml"] = (self.conf_xml,(1,),1,0)
        self.cmd_table["monitor"] = (self.conf_monitor,(2,2),1,0)
        self.cmd_table["role"] = (self.conf_role,(2,),2,0)
        self.cmd_table["user"] = (self.conf_user,(2,),2,0)
        self.cmd_table["ra"] = RA
        self.cmd_table["cib"] = CibShadow
        self.cmd_table["cibstatus"] = StatusMgmt
        self.cmd_table["template"] = Template
        self.cmd_table["_test"] = (self.check_structure,(0,0),1,0)
        self.cmd_table["_regtest"] = (self.regression_testing,(1,1),1,0)
        self.cmd_table["_objects"] = (self.showobjects,(0,0),1,0)
        self.cmd_aliases.update({
            "colocation": ("collocation",),
            "ms": ("master",),
        })
        setup_aliases(self)
        cib_factory.initialize()
    def myname(self):
        '''Just return some id.'''
        return "cibconfig"
    def check_structure(self,cmd):
        return cib_factory.check_structure()
    def regression_testing(self,cmd,param):
        return cib_factory.regression_testing(param)
    def showobjects(self,cmd):
        cib_factory.showobjects()
    def show(self,cmd,*args):
        "usage: show [xml] [<id>...]"
        if not cib_factory.is_cib_sane():
            return False
        err_buf.buffer() # keep error messages
        set_obj = mkset_obj(*args)
        err_buf.release() # show them, but get an ack from the user
        return set_obj.show()
    def filter(self,cmd,filter,*args):
        "usage: filter <prog> [xml] [<id>...]"
        if not cib_factory.is_cib_sane():
            return False
        err_buf.buffer() # keep error messages
        set_obj = mkset_obj(*args)
        err_buf.release() # show them, but get an ack from the user
        return set_obj.filter(filter)
    def edit(self,cmd,*args):
        "usage: edit [xml] [<id>...]"
        if not cib_factory.is_cib_sane():
            return False
        err_buf.buffer() # keep error messages
        set_obj = mkset_obj(*args)
        err_buf.release() # show them, but get an ack from the user
        return set_obj.edit()
    def _verify(self, set_obj_semantic, set_obj_all):
        rc1 = set_obj_all.verify()
        if user_prefs.check_frequency != "never":
            rc2 = set_obj_semantic.semantic_check(set_obj_all)
        else:
            rc2 = 0
        return rc1 and rc2 <= 1
    def verify(self,cmd):
        "usage: verify"
        if not cib_factory.is_cib_sane():
            return False
        set_obj_all = mkset_obj("xml")
        return self._verify(set_obj_all, set_obj_all)
    def save(self,cmd,*args):
        "usage: save [xml] <filename>"
        if not cib_factory.is_cib_sane():
            return False
        if args[0] == "xml":
            f = args[1]
            set_obj = mkset_obj("xml")
        else:
            f = args[0]
            set_obj = mkset_obj()
        return set_obj.save_to_file(f)
    def load(self,cmd,*args):
        "usage: load [xml] {replace|update} {<url>|<path>}"
        if not cib_factory.is_cib_sane():
            return False
        if args[0] == "xml":
            if len(args) != 3:
                syntax_err(args, context = 'load')
                return False
            url = args[2]
            method = args[1]
            set_obj = mkset_obj("xml","NOOBJ")
        else:
            if len(args) != 2:
                syntax_err(args, context = 'load')
                return False
            url = args[1]
            method = args[0]
            set_obj = mkset_obj("NOOBJ")
        return set_obj.import_file(method,url)
    def delete(self,cmd,*args):
        "usage: delete <id> [<id>...]"
        if not cib_factory.is_cib_sane():
            return False
        return cib_factory.delete(*args)
    def default_timeouts(self,cmd,*args):
        "usage: default-timeouts <id> [<id>...]"
        if not cib_factory.is_cib_sane():
            return False
        return cib_factory.default_timeouts(*args)
    def rename(self,cmd,old_id,new_id):
        "usage: rename <old_id> <new_id>"
        if not cib_factory.is_cib_sane():
            return False
        return cib_factory.rename(old_id,new_id)
    def erase(self,cmd,nodes = None):
        "usage: erase [nodes]"
        if not cib_factory.is_cib_sane():
            return False
        if nodes:
            if nodes == "nodes":
                return cib_factory.erase_nodes()
            else:
                syntax_err((cmd,nodes), context = 'erase')
        else:
            return cib_factory.erase()
    def refresh(self,cmd):
        "usage: refresh"
        if not cib_factory.is_cib_sane():
            return False
        if options.interactive and cib_factory.has_cib_changed():
            if not ask("All changes will be dropped. Do you want to proceed?"):
                return
        cib_factory.refresh()
    def ptest(self,cmd,*args):
        "usage: ptest [nograph] [v...] [scores] [utilization] [actions]"
        if not cib_factory.is_cib_sane():
            return False
        set_obj = mkset_obj("xml")
        return ptestlike(set_obj.ptest,'vv',cmd,*args)
    def commit(self,cmd,force = None):
        "usage: commit [force]"
        if force and force != "force":
            syntax_err((cmd,force))
            return False
        if not cib_factory.is_cib_sane():
            return False
        if not cib_factory.has_cib_changed():
            common_info("apparently there is nothing to commit")
            common_info("try changing something first")
            return
        rc1 = cib_factory.is_current_cib_equal()
        rc2 = cib_factory.is_cib_empty() or \
            self._verify(mkset_obj("xml","changed"),mkset_obj("xml"))
        if rc1 and rc2:
            return cib_factory.commit()
        if force or user_prefs.get_force():
            common_info("commit forced")
            return cib_factory.commit(True)
        if ask("Do you still want to commit?"):
            return cib_factory.commit(True)
        return False
    def upgrade(self,cmd,force = None):
        "usage: upgrade [force]"
        if not cib_factory.is_cib_sane():
            return False
        if force and force != "force":
            syntax_err((cmd,force))
            return False
        if user_prefs.get_force() or force:
            return cib_factory.upgrade_cib_06to10(True)
        else:
            return cib_factory.upgrade_cib_06to10()
    def __conf_object(self,cmd,*args):
        "The configure object command."
        if not cib_factory.is_cib_sane():
            return False
        f = lambda: cib_factory.create_object(cmd,*args)
        return f()
    def conf_node(self,cmd,*args):
        """usage: node <uname>[:<type>]
           [attributes <param>=<value> [<param>=<value>...]]
           [utilization <param>=<value> [<param>=<value>...]]"""
        return self.__conf_object(cmd,*args)
    def conf_primitive(self,cmd,*args):
        """usage: primitive <rsc> [<class>:[<provider>:]]<type>
        [params <param>=<value> [<param>=<value>...]]
        [meta <attribute>=<value> [<attribute>=<value>...]]
        [utilization <attribute>=<value> [<attribute>=<value>...]]
        [operations id_spec
            [op op_type [<attribute>=<value>...] ...]]"""
        return self.__conf_object(cmd,*args)
    def conf_group(self,cmd,*args):
        """usage: group <name> <rsc> [<rsc>...]
        [params <param>=<value> [<param>=<value>...]]
        [meta <attribute>=<value> [<attribute>=<value>...]]"""
        return self.__conf_object(cmd,*args)
    def conf_clone(self,cmd,*args):
        """usage: clone <name> <rsc>
        [params <param>=<value> [<param>=<value>...]]
        [meta <attribute>=<value> [<attribute>=<value>...]]"""
        return self.__conf_object(cmd,*args)
    def conf_ms(self,cmd,*args):
        """usage: ms <name> <rsc>
        [params <param>=<value> [<param>=<value>...]]
        [meta <attribute>=<value> [<attribute>=<value>...]]"""
        return self.__conf_object(cmd,*args)
    def conf_location(self,cmd,*args):
        """usage: location <id> <rsc> {node_pref|rules}

        node_pref :: <score>: <node>

        rules ::
          rule [id_spec] [$role=<role>] <score>: <expression>
          [rule [id_spec] [$role=<role>] <score>: <expression> ...]

        id_spec :: $id=<id> | $id-ref=<id>
        score :: <number> | <attribute> | [-]inf
        expression :: <simple_exp> [bool_op <simple_exp> ...]
        bool_op :: or | and
        simple_exp :: <attribute> [type:]<binary_op> <value>
                      | <unary_op> <attribute>
                      | date <date_expr>
        type :: string | version | number
        binary_op :: lt | gt | lte | gte | eq | ne
        unary_op :: defined | not_defined"""
        return self.__conf_object(cmd,*args)
    def conf_colocation(self,cmd,*args):
        """usage: colocation <id> <score>: <rsc>[:<role>] <rsc>[:<role>]
        """
        return self.__conf_object(cmd,*args)
    def conf_order(self,cmd,*args):
        """usage: order <id> score-type: <first-rsc>[:<action>] <then-rsc>[:<action>]
        [symmetrical=<bool>]"""
        return self.__conf_object(cmd,*args)
    def conf_property(self,cmd,*args):
        "usage: property [$id=<set_id>] <option>=<value>"
        return self.__conf_object(cmd,*args)
    def conf_rsc_defaults(self,cmd,*args):
        "usage: rsc_defaults [$id=<set_id>] <option>=<value>"
        return self.__conf_object(cmd,*args)
    def conf_op_defaults(self,cmd,*args):
        "usage: op_defaults [$id=<set_id>] <option>=<value>"
        return self.__conf_object(cmd,*args)
    def conf_xml(self,cmd,*args):
        "usage: xml <xml>"
        return self.__conf_object(cmd,*args)
    def conf_monitor(self,cmd,*args):
        "usage: monitor <rsc>[:<role>] <interval>[:<timeout>]"
        return self.__conf_object(cmd,*args)
    def conf_user(self,cmd,*args):
        """user <uid> {roles|rules}

        roles :: role:<role-ref> [role:<role-ref> ...]
        rules :: rule [rule ...]

        (See the role command for details on rules.)"""
        return self.__conf_object(cmd,*args)
    def conf_role(self,cmd,*args):
        """role <role-id> rule [rule ...]

        rule :: acl-right cib-spec [attribute:<attribute>]

        acl-right :: read | write | deny

        cib-spec :: xpath-spec | tag-ref-spec
        xpath-spec :: xpath:<xpath> | shortcut
        tag-ref-spec :: tag:<tag> | ref:<id> | tag:<tag> ref:<id>

        shortcut :: meta:<rsc>[:<attr>]
                    params:<rsc>[:<attr>]
                    utilization:<rsc>
                    location:<rsc>
                    property[:<attr>]
                    node[:<node>]
                    nodeattr[:<attr>]
                    nodeutil[:<node>]
                    status"""
        return self.__conf_object(cmd,*args)
    def end_game(self, no_questions_asked = False):
        if cib_factory.has_cib_changed():
            if no_questions_asked or not options.interactive or \
                ask("There are changes pending. Do you want to commit them?"):
                self.commit("commit")
        cib_factory.reset()

class TopLevel(UserInterface):
    '''
    The top level.
    '''
    lvl_name = "."
    crm_mon = "crm_mon -1"
    status_opts = {
        "bynode": "-n",
        "inactive": "-r",
        "ops": "-o",
        "timing": "-t",
        "failcounts": "-f",
    }
    def __init__(self):
        UserInterface.__init__(self)
        self.cmd_table['cib'] = CibShadow
        self.cmd_table['resource'] = RscMgmt
        self.cmd_table['configure'] = CibConfig
        self.cmd_table['node'] = NodeMgmt
        self.cmd_table['options'] = CliOptions
        self.cmd_table['status'] = (self.status,(0,5),0,0)
        self.cmd_table['ra'] = RA
        setup_aliases(self)
        self.help_table["."] = ("","""This is the CRM command line interface program.""")
        for lvl in self.cmd_table.keys():
            try: self.help_table[lvl] = (self.cmd_table[lvl].desc_short, \
                self.cmd_table[lvl].desc_long)
            except: pass
        self.help_table["status"] = ("show cluster status", """
Show cluster status. The status is displayed by crm_mon. Supply
additional arguments for more information or different format.
See crm_mon(8) for more details.

Usage:
...............
        status [<option> ...]

        option :: bynode | inactive | ops | timing | failcounts
...............
""")
        self.help_table["quit"] = ("exit the program", "")
        self.help_table["help"] = ("show help", "")
        self.help_table["end"] = ("go back one level", "")
        setup_help_aliases(self)
    def status(self,cmd,*args):
        """usage: status [<option> ...]
            option :: bynode | inactive | ops | timing | failcounts
        """
        status_cmd = self.crm_mon
        for par in args:
            if par in self.status_opts:
                status_cmd = "%s %s" % (status_cmd, self.status_opts[par])
            else:
                syntax_err((cmd,par), context = 'status')
                return False
        return ext_cmd(status_cmd) == 0

help_sys = HelpSystem()
user_prefs = UserPrefs.getInstance()
options = Options.getInstance()
err_buf = ErrorBuffer.getInstance()
vars = Vars.getInstance()
levels = Levels.getInstance(TopLevel)
cib_status = CibStatus.getInstance()
cib_factory = CibFactory.getInstance()

# vim:ts=4:sw=4:et:
