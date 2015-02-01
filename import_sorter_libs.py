# coding=utf-8

std_lib_modules = [
    'abc', 'anydbm', 'argparse', 'array', 'asynchat', 'asyncore', 'atexit',
    'base64', 'BaseHTTPServer', 'bisect', 'bz2', 'calendar', 'cgitb', 'cmd',
    'codecs', 'collections', 'commands', 'compileall', 'ConfigParser',
    'contextlib', 'Cookie', 'copy', 'cPickle', 'cProfile', 'cStringIO',
    'csv', 'datetime', 'dbhash', 'dbm', 'decimal', 'difflib', 'dircache',
    'dis', 'doctest', 'dumbdbm', 'EasyDialogs', 'errno', 'exceptions',
    'filecmp', 'fileinput', 'fnmatch', 'fractions', 'functools', 'gc',
    'gdbm', 'getopt', 'getpass', 'gettext', 'glob', 'grp', 'gzip',
    'hashlib', 'heapq', 'hmac', 'httplib', 'imaplib', 'imp', 'inspect', 'importlib',
    'itertools', 'json', 'linecache', 'locale', 'logging', 'mailbox',
    'math', 'mhlib', 'mmap', 'multiprocessing', 'operator', 'optparse',
    'os', 'pdb', 'pickle', 'pipes', 'pkgutil', 'platform', 'plistlib',
    'pprint', 'profile', 'pstats', 'pwd', 'pyclbr', 'pydoc', 'Queue',
    'random', 're', 'readline', 'resource', 'rlcompleter', 'robotparser',
    'sched', 'select', 'shelve', 'shlex', 'shutil', 'signal',
    'SimpleXMLRPCServer', 'site', 'sitecustomize', 'smtpd', 'smtplib',
    'socket', 'SocketServer', 'sqlite3', 'string', 'StringIO', 'struct',
    'subprocess', 'sys', 'sysconfig', 'tabnanny', 'tarfile', 'tempfile',
    'textwrap', 'threading', 'time', 'timeit', 'trace', 'traceback',
    'unittest', 'urllib', 'urllib2', 'urlparse', 'usercustomize', 'uuid',
    'warnings', 'weakref', 'webbrowser', 'whichdb', 'xml', 'xmlrpclib',
    'zipfile', 'zipimport', 'zlib', 'builtins', '__builtin__', 'thread',
    'binascii', 'statistics', 'unicodedata'
]

def get_std_lib_modules():
    from pkgutil import iter_modules
    modules = []
    r = iter_modules()
    for module in r:
        modules.append(module[1])

        #fs = 'isort -ls -sl {}'.format(file_path)
        #print fs
        #os.popen(fs)