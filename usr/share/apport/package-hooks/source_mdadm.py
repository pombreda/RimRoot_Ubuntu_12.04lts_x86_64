'''apport package hook for mdadm

(c) 2009 Canonical Ltd.
Author: Steve Beattie <sbeattie@ubuntu.com>

Based on the ideas in debian's /usr/share/bug/mdadm/script
'''

from apport.hookutils import *
from os import path
import re
import glob
import gzip
import subprocess

def get_initrd_files(pattern):
    '''Extract listing of files from the current initrd which match a regex.

       pattern should be a "re" object.  '''

    (_, _, release, _, _) = os.uname()
    try:
        fd = gzip.GzipFile('/boot/initrd.img-' + release, 'rb')
        cpio = subprocess.Popen(['cpio', '-t'], close_fds=True, stderr=subprocess.STDOUT,
		                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    except OSError, e:
        return 'Error: ' + str(e)

    out = cpio.communicate(fd.read())[0]
    if cpio.returncode != 0:
       return 'Error: command %s failed with exit code %i %' % (
           'cpio', cpio.returncode, out)

    lines = ' '
    for line in out.splitlines(True):
        if pattern.search(line):
            lines += ' ' + line
    return lines

def add_info(report):
    attach_hardware(report)
    attach_file(report, '/proc/mounts', 'ProcMounts')
    attach_file_if_exists(report, '/etc/mdadm/mdadm.conf', 'mdadm.conf')
    attach_file(report, '/proc/mdstat', 'ProcMDstat')
    attach_file(report, '/proc/partitions', 'ProcPartitions')
    attach_file(report, '/etc/blkid.tab', 'etc.blkid.tab')
    attach_file_if_exists(report, '/boot/grub/menu.lst', 'GrubMenu.lst')
    attach_file_if_exists(report, '/etc/lilo.conf', 'lilo.conf')

    devices = glob.glob("/dev/[hs]d*")
    for dev in devices:
        report['MDadmExamine' + path_to_key(dev)] = command_output(['/sbin/mdadm', '-E', dev])

    initrd_re = re.compile('md[a/]')
    report['initrd.files'] = get_initrd_files(initrd_re)
