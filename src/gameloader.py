'''

'''
import bz2
import gzip
import zipfile
import json
from cStringIO import StringIO
from eventdispatcher import event_handler

import imp
import config

class GameLoader(object):
    '''
    GameLoader automatically finds the correct plugin for a glog.  Accepts decompressed gamelogs and bz2 and gziped glogs. 

    :param event_dispatcher: Event dispatcher to register event handlers with
    :type event_dispatcher: EventDispatcher instance
    '''
    def __init__(self, event_dispatcher):
        self.magic_dict = {
                '\x1f\x8b\x08': 'gz',
                '\x42\x5a\x68': 'bz2',
                '\x50\x4b\x07': 'zip',  # Common zip magic numbers
                '\x50\x4b\x05': 'zip',
                '\x50\x4b\x04': 'zip',
                '\x50\x4b\x03': 'zip',
                }

        self.log_queue = []
        self.queue_idx = 0
        self.max_len = max(len(i) for i in self.magic_dict)

        self.ed = event_dispatcher
        self.ed.register_class_for_events(self)

    def determine_type(self, s):
        '''
        Determine the type of glog by the first few characters of the glog.

        Returns 'gz', 'bz2', or 'json' depending on the type of glog.
        'json' will be returned regardless of whehter the string is valid json or not.  
        This function merely indicates whether or not a file is compressed or not.  
        If the file is not compressed, it is assumed to be json.  It will be validated later.


        :param s: The first few characters of the glog
        :type s: string

        :rtype: string
        '''
        for magic, filetype in self.magic_dict.items():
            if s.startswith(magic):
                return filetype
        return 'json' # hopefully

    def decompress(self, data, ftype):
        '''
        Decompresses the string based on the file type.  Returns decompressed string.

        :param data: Full compressed glog string 
        :type data: string

        :param ftype: String representing the type of compression
        :type data: string

        :rtype: string
        '''
        if ftype == 'bz2':
            self.queue_log(bz2.decompress(data))
        elif ftype == 'gz':
            gz = gzip.GzipFile(filename='bogus.glog', mode='rb', 
                    fileobj=StringIO(data))
            self.queue_log(gz.read())
        elif ftype == 'zip':
            z = zipfile.ZipFile(StringIO(data), 'r')
            for f in z.namelist():
                self.queue_log(z.read(f))
        else:
            raise Exception('Unknown Decompression Scheme')

    def queue_log(self, glog):

        data = json.loads(glog)

        if self.queue_idx >= len(self.log_queue):
            self.ed.dispatch_event('on_run_gamelog', data)

        self.log_queue += [data]

    @event_handler
    def on_load_gamelog_file(self, glog_list):

        for glog in glog_list:
            self.load(glog)
            

    @event_handler
    def on_load_gamelog_str(self, str_list):
        for glog in str_list:
            self.loads(glog)

    def load(self, path):
        '''
        Loading a glog from a file path.

        :param path: Path to desired glog to load
        :type path: string
        '''

        with open(path) as f:
            file_start = f.read(self.max_len)

        ftype = self.determine_type(file_start)

        output = ''
        if ftype != 'json':
            with open(path, 'rb') as f:
                output = f.read()
            self.decompress(output, ftype)
        else:
            with open(path, 'r') as f:
                output = f.read()
            self.queue_log(output)

    def loads(self, data):
        '''
        Loads a glog from memory

        :param data: Data for the glog (compressed or decompressed)
        :type data: string
        '''

        ftype = self.determine_type(data[:self.max_len])

        if ftype != 'json':
            self.decompress(data, ftype)
        else:
            self.queue_log(data)
