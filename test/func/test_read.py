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


class ReadTest(unittest.TestCase):

    def test_read_access(self):
        # Ray creates a container to hold some objects.
        ## HTTP PUT http://127.0.0.1:8080/v1/AUTH_test/test_read_access

        # He now creates an object in the new container.
        ## HTTP PUT http://127.0.0.1:8080/v1/AUTH_test/test_read_access/object

        # Ray mounts his his SAIO using SAIO Fuse.
        ## ./bin/saio_fuse /tmp/saio_fuse

        # He performs a container listing using Swift's API and the
        # mounted directory, verifing that they are equivalent.
        ## HTTP GET http://127.0.0.1:8080/v1/AUTH_test/test_read_access?format=json
        ## ls -l /tmp/saio_fuse/v1/AUTH_test/test_read_access

        # He then reads an object using Swift's API and the mounted
        # directory, verifying that they are the same.
        ##  HTTP GET http://127.0.0.1:8080/v1/AUTH_test/test_read_access/object
        ## cat /tmp/saio_fuse/v1/AUTH_test/test_read_access/object
        pass


if __name__ == '__main__':
    unittest.main()
