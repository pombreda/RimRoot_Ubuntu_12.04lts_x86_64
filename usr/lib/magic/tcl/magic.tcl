# Wishrc startup for ToolScript (magic)
#
# For installation:  Put this file and also magicwrap.so into
# directory /usr/lib/magic/tcl, and set the "load" line below
# to point to the location of magicwrap.so.  Also see comments
# in shell script "magic.sh".

global Opts
  
# If we called magic via the non-console script, then we want to reset
# the environment variable HOME to its original value.
   
load /usr/lib/magic/tcl/tclmagic.so

# It is important to make sure no magic commands overlap with Tcl built-in
# commands, because otherwise the namespace import will fail.

proc pushnamespace { name } {

   set y [namespace eval ${name} info commands ::${name}::*]
   set z [info commands]

# Watch especially for magic "wizard" commands, as we don't want to confuse
# the literal "*" with a regular expression *.  "regsub" below takes care of it.

   foreach v $y {
      regsub -all {\*} $v {\\*} i
      set x [namespace tail $i]
      if {[lsearch $z $x] < 0} { 
         namespace import $i                       
      }
   }
}

proc popnamespace { name } {
   set z [info commands]
   set l [expr [string length ${name}] + 5]

   while {[set v [lsearch $z ${name}_tcl_*]] >= 0} {
      set y [lindex $z $v]
      set w [string range $y $l end]
      interp alias {} ::$w {}
      rename ::$y ::$w
      puts "Info: replacing ::$w with ::$y"
   }
   namespace forget ::${name}::*
}

#----------------------------------------------------------------------
# Define the drcstate procedure expected by the background DRC code.

proc magic::drcstate {option} {
   # (Null proc---see wrapper.tcl for a useful version)
}

#-----------------------------------------------------------------
# Define these console routines so that they don't produce errors
# when Magic is run in batch mode

if {[catch {tkcon title}]} {
   proc magic::suspendout {} {}
   proc magic::resumeout {} {}
   proc magic::dialog {} {}
   proc magic::consolegeometry {} {}
   proc magic::consolefocus {} {}
}

#----------------------------------------------------------------------
# Cross-Application section
#----------------------------------------------------------------------

# Check namespaces for existence of other applications
set UsingIRSIM 0
set UsingXCircuit 0
set UsingNetgen 0
set nlist [namespace children]
foreach i $nlist {
   switch $i {
      ::irsim { set UsingIRSIM 1 }
      ::xcircuit { set UsingXCircuit 1 }
      ::netgen { set UsingNetgen 1 }
   }
}

# Setup IRSIM assuming that the Tcl version is installed.
# We do not need to rename procedure irsim to NULL because it is
# redefined in a script, which simply overwrites the original.

proc irsim { args } {
   global CAD_ROOT
   set irsimscript [glob -nocomplain ${CAD_ROOT}/irsim/tcl/irsim.tcl]
   if { ${irsimscript} == {} } {
      puts stderr "\"irsim\" requires Tcl-based IRSIM version 9.6 or newer."
      puts stderr "Could not find script \"irsim.tcl\".  If IRSIM is installed in a"
      puts stderr "place other than CAD_ROOT (=${CAD_ROOT}), use the command"
      puts stderr "\"source <path>/irsim.tcl\" before doing \"irsim\"."
   } else {
      source $irsimscript
      eval {irsim} $args
   }
}

# Setup Xcircuit assuming that the Tcl version is installed.

proc xcircuit { args } {
   global CAD_ROOT
   global argc
   global argv
   set xcircscript [glob -nocomplain ${CAD_ROOT}/xcircuit*/xcircuit.tcl]
   if { ${xcircscript} == {} } {
      puts stderr "\"xcircuit\" requires Tcl-based XCircuit version 3.1 or newer."
      puts stderr "Could not find script \"xcircuit.tcl\".  If XCircuit is installed in a"
      puts stderr "place other than CAD_ROOT (=${CAD_ROOT}), use the command"
      puts stderr "\"source <path>/xcircuit.tcl\"."
   } else {
      # if there are multiple installed versions, choose the highest version.
      if {[llength $xcircscript] > 1} {
	set xcircscript [lindex [lsort -decreasing -dictionary $xcircscript] 0]
      }
      # execute script in the scope of magic, because its variable space is
      # not modularized.
      set argv $args
      set argc [llength $args] 
      uplevel #0 source $xcircscript
   }
}

# Setup Netgen assuming that the Tcl version is installed.

proc netgen { args } {
   global CAD_ROOT
   global argc
   global argv
   set netgenscript [glob -nocomplain ${CAD_ROOT}/netgen/tcl/netgen.tcl]
   if { ${netgenscript} == {} } {
      puts stderr "\"netgen\" requires Tcl-based Netgen version 1.2 or newer."
      puts stderr "Could not find script \"netgen.tcl\".  If Netgen is installed in a"
      puts stderr "place other than CAD_ROOT (=${CAD_ROOT}), use the command"
      puts stderr "\"source <path>/netgen.tcl\"."
   } else {
      set argv $args
      set argc [llength $args] 
      uplevel #0 source $netgenscript
   }
}

# Parse argument list for "-c[onsole]" and "-now[rapper]".

set cellname ""
set do_wrapper true
set do_recover false
set argafter {magic::initialize}
set x {}
for {set i 0} {$i < $argc} {incr i 1} {
   set x [lindex $argv $i]
#
# Command-line argument handling goes here
# We have to handle all of magic's command line arguments so we can
# figure out if a cell has been named for preloading.
#
   switch -regexp -- $x {
      ^-now(rap)?(per)?$ {	  ;# This regexp accepts -now, -nowrap, and -nowrapper
	 set do_wrapper false
      }
      ^-dnull {
	 set do_wrapper false
         lappend argafter $x
      }
      ^-r(e)?(cover)?$ {
	 set do_recover true
      }
      ^-rc(file)?$ {
         lappend argafter $x
         incr i 1
         lappend argafter [lindex $argv $i]
      }
      ^-d -
      ^-g -
      ^-m -
      ^-i -
      ^-T {
         lappend argafter $x
         incr i 1
         lappend argafter [lindex $argv $i]
      }
      ^-F {
         lappend argafter $x
         incr i 1
         lappend argafter [lindex $argv $i]
         incr i 1
         lappend argafter [lindex $argv $i]
      }
      ^-D -
      ^-n* {
         lappend argafter $x
      }
      default {
         set cellname $x
         lappend argafter $x
      }
   }
}

if {$do_wrapper} {
  source ${CAD_ROOT}/magic/tcl/wrapper.tcl
  lappend argafter "-nowindow" ;# Set no-initial-window option in magic.
}
unset x i do_wrapper
eval $argafter 			;# magic::initialize ${argv}

#----------------------------------------------------------------------
# Check for presence of padlist manager script and include it

if {[file exists ${CAD_ROOT}/magic/tcl/padlist.tcl]} {
   source ${CAD_ROOT}/magic/tcl/padlist.tcl
   set Opts(padlist) 0
}

#----------------------------------------------------------------------
# Check for presence of the miscellaneous tools script and include it

if {[file exists ${CAD_ROOT}/magic/tcl/tools.tcl]} {
   source ${CAD_ROOT}/magic/tcl/tools.tcl
   set Opts(tools) 0
}

#----------------------------------------------------------------------
# Check for presence of the mazerouter script and include it

if {[file exists ${CAD_ROOT}/magic/tcl/mazeroute.tcl]} {
   source ${CAD_ROOT}/magic/tcl/mazeroute.tcl
   set Opts(mazeroute) 0
}

#----------------------------------------------------------------------
# Check for presence of the toolkit script and include it

if {[file exists ${CAD_ROOT}/magic/tcl/toolkit.tcl]} {
   source ${CAD_ROOT}/magic/tcl/toolkit.tcl
   set Opts(toolkit) 0
}

#----------------------------------------------------------------------
# Magic start function drops back to interpreter after initialization & setup

set auto_noexec 1	;# don't EVER call UNIX commands w/o "shell" in front

# Have we called magic from tkcon or a clone thereof?  If so, set MagicConsole

if {[lsearch [interp aliases] tkcon] != -1} {
   set MagicConsole tkcon
   catch {wm withdraw .}

   # Get rid of some overlapping tkcon commands which are not needed.

   if {[lsearch [info commands] orig_edit] < 0} {rename edit orig_edit}
   if {[lsearch [info commands] orig_dump] < 0} {rename dump orig_dump}
   if {[lsearch [info commands] orig_what] < 0} {rename what orig_what}
} else {
   rename unknown tcl_unknown
   proc unknown { args } {
      # CAD tools special:
      # Check for commands which were renamed to tcl_(command)

      set cmd [lindex $args 0]
      if {[lsearch [info commands] tcl_$cmd] >= 0} {
         set arglist [concat tcl_$cmd [lrange $args 1 end]]
         set ret [catch {eval $arglist} result]
         if {$ret == 0} {
            return $result
         } else {
            return -code $ret -errorcode $errorCode $result
         }
      }
      return [eval [concat tcl_unknown $args]]
   }
}

# Set up certain commands to act like they do in non-Tcl-based magic;
# These are the commands whose names have been extended so they don't
# conflict with existing Tcl/Tk commands.  This renaming & importing
# *requires* the special code in the magic Tcl command dispatcher to
# find and deal with each of these renamed commands!

if {[lsearch [info commands] orig_clock] < 0} {rename clock orig_clock}
if {[lsearch [info commands] tcl_flush] < 0} {rename flush tcl_flush}
if {[lsearch [info commands] tcl_load] < 0} {rename load  tcl_load}
if {[lsearch [info commands] tcl_array] < 0} {rename array tcl_array}
if {[lsearch [info commands] tcl_label] < 0} {catch {rename label tcl_label}}
if {[lsearch [info commands] tcl_grid] < 0} {catch {rename grid tcl_grid}}

namespace eval magic namespace export *
pushnamespace magic

#----------------------------------------------------------------------
# Read system startup files (mostly macro definitions)
# Read user startup file, if any
# Load initial cell, if any

magic::startup

if {![catch {set toptitle [wm title .]}]} {
   if {[string range $toptitle 0 3] == "wish"} {
      wm withdraw .
   }
   if {[string range $toptitle 0 8] == "magicexec"} {
      wm withdraw .
   }
   unset toptitle
}

# After loading, magic will wander off and do a complete DRC check
# before executing the rest of the script unless we temporarily
# disable the DRC checker.

set drcstate [drc status]
drc off

# Initial window for wrapper, if defined.
# empty string is equivalent to passing NULL cell name.

if {![catch {set winname [magic::openwrapper $cellname]}]} {
   magic::techmanager initall
   magic::scrollupdate $winname
} else {
   # Initial geometry handler for the default window, non-wrapper version
   catch {wm geometry .magic1 ${Opts(geometry)}}
}

# Set a box, and set the view; if no cell has been loaded, choose a default
# view.
if {![box exists]} {
   box 0 0 1 1		;# create a unit box
}
if {[llength $cellname] > 0} {
   view
} else {
   view -9 -9 10 10
}

# The Tcl version handles the "-r" on the command line by calling
# command crash recover.

if {$do_recover} {crash recover}

# Unset global TCL variables so they don't conflict with magic nodes.
unset cellname nlist do_recover

if {$drcstate == 1} {
   drc on
}
unset drcstate
