'''

'''
import json
import bz2
import gzip
import zipfile
from cStringIO import StringIO

import imp
import config
import os

class GameLoader(object):
    '''
    GameLoader automatically finds the correct plugin for a glog.  Accepts decompressed gamelogs and bz2 and gziped glogs. 
    '''
    def __init__(self):
        self.magic_dict = {
                '\x1f\x8b\x08': 'gz',
                '\x42\x5a\x68': 'bz2',
                '\x50\x4b\x07': 'zip',
                '\x50\x4b\x05': 'zip',
                '\x50\x4b\x04': 'zip',
                '\x50\x4b\x03': 'zip',
                }

        self.max_len = max(len(i) for i in self.magic_dict)

    def load_glog(self, string):
        '''
        Loads a glog into memory.

        :param string: The decompressed json string
        :type string: string
        '''
        data = json.loads(string)

        game_name = data['gameName'].lower()
        path = os.path.join(config.PLUGIN_DIR, 
                game_name, 'main.py')

        game = imp.load_source(game_name, path)


    def determine_type(self, s):
        '''
        Determine the type of glog by the first few characters of the glog.

        Returns 'gz', 'bz2', or 'json' depending on the type of glog.

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
            return bz2.decompress(data)
        elif ftype == 'gz':
            gz = gzip.GzipFile(filename='bogus.glog', mode='rb', fileobj=StringIO(data))
            return gz.read()
        elif ftype == 'zip':
            z = zipfile.ZipFile(StringIO(data), 'r')
            return z.read(z.namelist()[0])

        else:
            raise Exception('Unknown Decompression Scheme')
            

    def load(self, path):
        '''
        Loading a glog from a file path.

        :param path: Path to desired glog to load
        :type path: string
        '''

        with open(path) as f:
            file_start = f.read(self.max_len)

        ftype = self.determine_type(file_start)
        print ftype

        output = ''
        if ftype != 'json':
            with open(path, 'rb') as f:
                output = f.read()
            output = self.decompress(output, ftype)
        else:
            with open(path, 'r') as f:
                output = f.read()

        self.load_glog(output)

    def loads(self, data):
        '''
        Loads a glog from memory

        :param data: Data for the glog (compressed or decompressed)
        :type data: string
        '''

        ftype = self.determine_type(data[:self.max_len])

        if ftype != json:
            data = self.decompress(data, ftype)

        self.load_glog(data)

