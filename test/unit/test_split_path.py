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

    def test_split_path(self):
        cases = [('/', (None, None, None, None)),
                 ('/v1', ('v1', None, None, None)),
                 ('/v1/a', ('v1', 'a', None, None)),
                 ('/v1/a/c', ('v1', 'a', 'c', None)),
                 ('/v1/a/c/o', ('v1', 'a', 'c', 'o')),
                 ('/v1/a/c/o/l/o/n/g', ('v1', 'a', 'c', 'o/l/o/n/g'))]
        for case in cases:
            v, a, c, o = _split_path(case[0])
            self.assertEqual(v, case[1][0],
                             msg="version not correct, %s != %s"
                                 % (v, case[1][0]))
            self.assertEqual(a, case[1][1],
                             msg="account not correct, %s != %s"
                                 % (v, case[1][1]))
            self.assertEqual(c, case[1][2],
                             msg="container not correct, %s != %s"
                                 % (v, case[1][2]))
            self.assertEqual(o, case[1][3],
                             msg="object not correct, %s != %s"
                                 % (v, case[1][3]))

if __name__ == '__main__':
    unittest.main()
