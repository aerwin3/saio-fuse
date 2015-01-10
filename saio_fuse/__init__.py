#!/usr/bin/env python
# Copyright 2015 Richard Hawkins
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from swift.common.utils import split_path as swift_split_path

from stat import S_IFDIR, S_IFREG
from fuse import Operations


def _split_path(path):
    version = None
    account = None
    container = None
    obj = None

    if path == '/':
        return (None, None, None, None)

    if path == '/v1':
        return ('v1', None, None, None)

    version = 'v1'
    account, container, obj = swift_split_path(path[3:], 1, 3,
                                               rest_with_last=True)
    return (version, account, container, obj)


class SAIOFuse(Operations):

    def _list_accounts(self):
        return ['AUTH_test']

    def _list_containers(self, account):
        return ['saiof_test_read_access']

    def _list_objects(self, account, container):
        return ['object']

    def _get_attr_root(self):
        return {
            'st_atime': 1420658919.81,
            'st_ctime': 1420658915.13,
            'st_gid': 1000,
            'st_mode': S_IFDIR | 0o555,
            'st_mtime': 1420658915.13,
            'st_nlink': 2,
            'st_size': 15,
            'st_uid': 1000,
        }

    def _get_attr_account(self, account):
        return {
            'st_atime': 1420658919.81,
            'st_ctime': 1420658915.13,
            'st_gid': 1000,
            'st_mode': S_IFDIR | 0o555,
            'st_mtime': 1420658915.13,
            'st_nlink': 2,
            'st_size': 15,
            'st_uid': 1000,
        }

    def _get_attr_container(self, account, container):
        return {
            'st_atime': 1420658919.81,
            'st_ctime': 1420658915.13,
            'st_gid': 1000,
            'st_mode': S_IFDIR | 0o555,
            'st_mtime': 1420658915.13,
            'st_nlink': 2,
            'st_size': 15,
            'st_uid': 1000,
        }

    def _get_attr_object(self, account, container, object):
        return {
            'st_atime': 1420658919.81,
            'st_ctime': 1420658915.13,
            'st_gid': 1000,
            'st_mode': S_IFREG | 0o444,
            'st_mtime': 1420658915.13,
            'st_nlink': 1,
            'st_size': 15,
            'st_uid': 1000,
        }

    # Filesystem methods
    # ==================

    def getattr(self, path, fh=None):
        version, account, container, obj = _split_path(path)

        if obj:
            return self._get_attr_object(account, container, obj)
        if container:
            return self._get_attr_container(account, container)
        if account:
            return self._get_attr_account(account)
        return self._get_attr_root()

    def readdir(self, path, fh):
        version, account, container, obj = _split_path(path)

        listing = []

        if container is not None:
            listing = self._list_objects(account, container)
        elif account is not None:
            listing = self._list_containers(account)
        elif version is not None:
            listing = self._list_accounts()
        else:
            listing = ['v1']

        dirents = ['.', '..']
        dirents.extend(listing)
        for r in dirents:
            yield r
