"""Contains app controllers.

Controllers serve as a middleware between Model and View
"""
import os
import zlib

import models
# from hw11_Flask_practice import utils
from utils import upload
import datetime as dt
import pathlib as pth
import PIL.Image
import typing as t
import io


class StorageError(Exception):
    pass

class FileExistsError(StorageError):
    def __init__(self, id=None):
        self.id = id
    
    def __str__(self):
        msg = 'File already exists'
        if self.id is not None:
            msg += f' (id: {self.id})'
        return msg


class Storage:
    """Provides interface to files based on File model."""
    __slots__ = 'dir', 'db', '_Model', 'max_file_size'

    def __init__(self, directory, db, model, max_file_size):
        self.dir = pth.Path(directory)
        self.db = db
        self._Model = model
        self.max_file_size = max_file_size
        # ensure directory exists
        self.dir.mkdir(exist_ok=True)


    def init_app(self, app):
        """Bind storage to app to make it accessible as app.storage."""
        app.storage = self
    
    def load(self, filename_or_id, **kwargs):
        if isinstance(filename_or_id, int):
            # assuming id is passed
            id = filename_or_id
            dbf = self._Model.get_by_id(id)
            filename = dbf.name
        else:
            filename = filename_or_id
        filename = self._lookup_filename(filename)
        file = open(file=filename, mode='rb', **kwargs)
        return file, filename

    def __getitem__(self, filename_or_id):
        """Alias to load() method with default arguments"""
        return self.load(filename_or_id=filename_or_id)

    def __contains__(self, val):
        if isinstance(val, io.BufferedIOBase):
            return self.has_file(val)
        return self.has_name(val)
    
    def has_name(self, filename):
        res = self._Model.get_by_filename(filename)
        return res is not None
          
    def has_file(self, iobuf, *, fastcheck=False, hash=None):
        ret = self.get_filenames(
            iobuf=iobuf, fastcheck=fastcheck, hash=hash)
        return bool(ret)

    def get_filenames(self, iobuf, *args, **kwargs):
        files = self.get_files(iobuf=iobuf, *args, **kwargs)
        return tuple([f.name for f in files])

    def get_files(self, iobuf, *, fastcheck=False, hash=None):
        if hash is None:
            hash = self._Model.compute_hash(iobuf)

        # try finding existing files with the same hash
        samehash = self._Model.find_by_hash(hash)
 
        if samehash and fastcheck:
            return tuple(samehash)

        # if found same hash, compare with disk file byte-by-byte
        for item in samehash:
            path = self.dir.joinpath(item.name)
            with open(path, 'rb') as f:
                issame = upload.compare_buffers(f, iobuf)
            if issame:
                return (item, )
        
        return tuple()

    def store(self,
              iobuf: io.BufferedIOBase,
              name: str,
              uploaded_at: t.Optional[dt.datetime]=None,
              *,
              unify_name: t.Optional[bool]=True,
              fastcheck: t.Optional[bool]=False,
              autocommit: t.Optional[bool]=True):
        """Store file-like object in database, as well as on disk.
        
        Args:
            iobuf: file-like object (binary mode) providing
                   file data
            name: original filename,
                  from where file extension is extracted
            uploaded_at: date when user uploaded the file
            unify_name: determines whether to store under original
                        name, or use unified (aka uuid) name instead
            fastlookup: whether check only by hash match and don't
                        compare files byte-by-byte
            autocommit: whether to automatically push File entry to db
                        or just return the ORM object - Transient
        """
        if not self._check_file_ext(name):
            raise Exception('not valid extension')

        if not self._check_file_size(iobuf):
            raise Exception('big size')


        iobuf = self._remove_metadata_from_buffered_io(iobuf)

        if uploaded_at is None:
            uploaded_at = dt.datetime.now()

        hash = self._Model.compute_hash(iobuf)

        # try finding existing files with the same hash
        existing = self.get_files(
            iobuf, fastcheck=fastcheck, hash=hash)
        if existing:
            raise FileExistsError(existing[0].id)

        # get only filename part
        name = pth.Path(pth.Path(name).name)

        # replace base with uuid, leaving .extension
        if unify_name:
            stem = upload.own_uuid(creation_date=uploaded_at)
            name = name.with_stem(stem)

        iobuf.seek(0)       # rewind buffer
        path = self.dir.joinpath(name)

        name = str(name)

        dbfile = self._Model(name=name,
                             hash=hash,
                             uploaded_at=uploaded_at)

        with open(path, 'xb') as diskfile:
            for chunk in upload.iter_chunked(iobuf):
                diskfile.write(chunk)

        if autocommit:
            self.db.session.add(dbfile)
            self.db.session.commit()

        return dbfile
    
    def _lookup_filename(self, filename):
        """Ensure file always resides under directory"""
        path = self.dir.joinpath(pth.Path(filename).name)
        return str(path)

    def get_all_id(self):
        return self._Model.get_all_id()

    def _check_file_ext(self, name: str,):
        ext = os.path.splitext(name)[1]
        if ext in ('.jpg', '.jpeg', '.jfif', '.png'):
            return True

    def _check_file_size(self, iobuf: io.BufferedIOBase):
        iobuf.seek(0, io.SEEK_END)
        file_size = iobuf.tell()
        iobuf.seek(0)
        if file_size > self.max_file_size:
            return False
        return True

    def _remove_metadata_from_buffered_io(self, iobuf: io.BufferedIOBase):
        iobuf.seek(0)
        image = PIL.Image.open(iobuf)
        new_buffer = io.BytesIO()
        image.save(new_buffer, format=image.format)
        new_buffer.seek(0)
        return new_buffer



