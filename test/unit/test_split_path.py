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

import unittest

from saio_fuse import _split_path


class SplitPathTest(unittest.TestCase):

    def test_root_path(self):
        v, a, c, o = _split_path('/')
        self.assertEqual(v, None)
        self.assertEqual(a, None)
        self.assertEqual(c, None)
        self.assertEqual(o, None)

    def test_version_path(self):
        v, a, c, o = _split_path('/v1')
        self.assertEqual(v, 'v1')
        self.assertEqual(a, None)
        self.assertEqual(c, None)
        self.assertEqual(o, None)

    def test_account_path(self):
        v, a, c, o = _split_path('/v1/a')
        self.assertEqual(v, 'v1')
        self.assertEqual(a, 'a')
        self.assertEqual(c, None)
        self.assertEqual(o, None)

    def test_container_path(self):
        v, a, c, o = _split_path('/v1/a/c')
        self.assertEqual(v, 'v1')
        self.assertEqual(a, 'a')
        self.assertEqual(c, 'c')
        self.assertEqual(o, None)

    def test_short_object_path(self):
        v, a, c, o = _split_path('/v1/a/c/o')
        self.assertEqual(v, 'v1')
        self.assertEqual(a, 'a')
        self.assertEqual(c, 'c')
        self.assertEqual(o, 'o')

    def test_long_object_path(self):
        v, a, c, o = _split_path('/v1/a/c/o/l/o/n/g')
        self.assertEqual(v, 'v1')
        self.assertEqual(a, 'a')
        self.assertEqual(c, 'c')
        self.assertEqual(o, 'o/l/o/n/g')


if __name__ == '__main__':
    unittest.main()
