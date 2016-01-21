'''
Created on Feb 8, 2013

@author: yaocheng
'''

import os


class FlatDocument(object):
    """
    A document in file system which contains raw text of record
    Specify a function to decide record boundry
    Iterable so one can do 'for raw_record in doc'
    """
    @property
    def path(self):
        return self._path
        
    @path.setter
    def path(self, p):
        err_msg = self._open_path(p)
        if err_msg:
            print err_msg
        
    def _open_path(self, p):
        try:
            self._fp = open(p, 'r')
        except TypeError:
            return 'Given path is not a string.'
        except IOError:
            return 'Can not open file %(path)s' % {'path': p}
        self._path = p
        
    @property
    def isrecord(self):
        return self._isrecord
        
    @isrecord.setter
    def isrecord(self, func):
        try:
            func('')
        except TypeError:
            print 'Need a string processing function as record examiner.'
            return
        self._isrecord = func
    
    def __init__(self, path=None, isrecord=None):
        if path:
            err_msg = self._open_path(path)
            if err_msg:
                print err_msg
                return
        else:
            self._path = None
            self._fp = None
        if isrecord:
            self.isrecord = isrecord
        else:
            self._isrecord = None
            #def dummy_func_always_return_True(text):
            #    return True
            #self._isrecord = dummy_func_always_return_True
        
    def __iter__(self):
        if not self._fp:
            print 'Path has not been set. Nothing to iterate.'
            return
        if not self._isrecord:
            # if no isrecord can be found, spit each line as a record
            for line in self._fp:
                yield line
        else:
            record_buf = ''
            for line in self._fp:
                record_buf += line
                decision = self._isrecord(record_buf)
                if decision is True:
                    yield record_buf
                    record_buf = ''
                elif decision is False:
                    continue
                else:
                    print '"isrecord" function does not always return a boolean value. Iteration stopped.'
                    break
        self._fp.seek(0) # move fp back to the begining of the file
        
    def close(self):
        try:
            self._fp.close()
        except IOError:
            print 'Something wrong when trying to close the document file'
            return
        self._isrecord = None
        
        
def unpack(record, delimiter=None):
    if not delimiter:
        # if delimiter is omitted, use python default to break record
        try:
            return record.split()
        except AttributeError:
            print 'Type of the record is not string.'
            return
    if type(delimiter) not in [tuple, list]:
        # if single delimiter is passed in, pack it into a tuple first
        delimiter = (delimiter)
    items = [record]
    for d in delimiter:
        # for a tuple of delimiters, use first one to break down the record, then
        # second to further break down resulted elements, and so on
        temp = []
        for i in items:
            try:
                temp.extend(i.split(d))
            except AttributeError:
                print 'Type of the record is not string.'
                return
            except TypeError:
                print 'Delimiter %(d)s is not string.' % {'d': d}
                return
        items = temp
    return items


def get_immediate_path(path):
    """
    If path to a file is passed in, return the path enclosed in a list;
    If path to a folder is passed in, get all immediate sub-paths within the folder, return as a list
    If path doesn't exist, print a message then return an empty list
    """
    if os.path.exists(path):
        if os.path.isdir(path):
            return [os.path.join(path, f) for f in os.listdir(path)]
        else:
            return [path]
    else:
        print 'Given path does not exist.'
        return []

def extend_name(old_name, fix, delimiter='_', option=2):
    """
    option can be [0, 1, 2]
    0: add fix as extension
    1: add fix as prefix
    2: add fix as suffix
    """
    try:
        pieces = old_name.split('.')
        if len(pieces) == 1:
            f_n = pieces[0]
            f_ex = None
        else:
            f_n = '.'.join(pieces[:-1])
            f_ex = pieces[-1]
        if option == 0:
            pieces.append(fix)
            new_name = '.'.join(pieces)
        elif option == 1:
            if f_ex:
                new_name = '.'.join([delimiter.join([fix, f_n]), f_ex])
            else:
                new_name = delimiter.join([fix, f_n])
        elif option == 2:
            if f_ex:
                new_name = '.'.join([delimiter.join([f_n, fix]), f_ex])
            else:
                new_name = delimiter.join([f_n, fix])
        else:
            print 'Invalid option. Return old name.'
            new_name = old_name
        return new_name
    except AttributeError:
        print 'Provided file name or delimiter may not be string.'
        return old_name
    except TypeError:
        print 'Provided fix may not be string.'
        return old_name

def replace_xml_predefined_char(buf):
    for pair in [('&lt;', '<'),
                 ('&gt;', '>'),
                 ('&amp;', '&'),
                 ('&apos;', "'"),
                 ('&quot;', '"')]:
        buf = buf.replace(pair[0], pair[1])
    return buf




def utility_test():
    test_record = 'this is a test record'
    print unpack(test_record)
    print unpack(5)
    print unpack(test_record, ('a', 5))
    return

if __name__ == '__main__':
    utility_test()