__doc__ = '''a fake device serves as the 'disk' for the file system'''


import gzip

def with_suffix(filename, suffix):
    '''put a '.gz' at the end of a file name to show that it is
    to be compressed using gzip. if the '.gz' is already there,
    don't change the filename.'''
    if not filename.endswith(suffix):
        return filename + '.'  + suffix
    else:
        return filename



def allocation_size(request_size, chunk_size):
    '''round request_size up to the nearest multiple of chunk_size, 
    but not a 0 or negative multiple, the smallest value that can 
    be returned is chunk_size. if chunk_size is <= 0, then 0 is returned'''
    if chunk_size <= 0:
        return 0
    if request_size <= 0:
        return chunk_size
    return ((request_size + (chunk_size - 1)) // chunk_size) * chunk_size
    




class FakeDisk:

    # page size is 4k (4096)
    page_size = 1 << 12

    
    
    
    def __init__(self, size, bs=None):
        '''create a FakeDisk with a bytearray of the given size.
        if a bytearray is given, then its size overrides the value of size.
        if the given size or bytearray is not a multiple of the page_size,
        the size is rounded up and zoroed padding is added.'''
        # create a new bytearray
        if bs is None:
            self.size = allocation_size(size, FakeDisk.page_size)
            self.bs = bytearray(self.size)
        # create the FakeDisk using an existing byarray
        else:
            # temporary because bs may not be of a valid size
            temp_bs = bs
            temp_size = len(temp_bs)
            if temp_size == allocation_size(temp_size, FakeDisk.page_size):
                self.bs = temp_bs
                self.size = temp_size
            else:
                self.size = allocation_size(temp_size, FakeDisk.page_size)
                self.bs = bytearray(self.size)
                self.bs[:temp_size] = bs
                
            
            

    @staticmethod
    def from_file(filename):
        '''create a FakeDisk object from a file.'''
        f = None
        if filename.endswith('.gz'):
            f = gzip.open(filename)  
        else:
            f = open(fiename, 'rb')
        bs = bytearray(f.read())
        f.close()
        return FakeDisk(bs)



    def to_file(self, filename, compressed=False):
        '''write the disk out to a file.
        optionally use compression'''
        f = None
        if compressed:
            filename_gz = with_suffix(filename, 'gz')
            f = gzip.open(filename_gz)
        else:
            f = open(filename, 'wb')
        f.write(self.bs)
        f.close()
            
    
    
        
        
