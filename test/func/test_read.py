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

import requests
import unittest

from subprocess import Popen, PIPE


class ReadTest(unittest.TestCase):

    def test_read_access(self):
        # Ray authenticates using temp auth
        r = requests.get('http://127.0.0.1:8080/auth/v1.0',
                         headers={'X-Storage-User': 'test:tester',
                                  'X-Storage-Pass': 'testing'})
        storage_url = r.headers.get('x-storage-url')
        auth_token = r.headers.get('x-auth-token')

        # Ray creates a container to hold some objects.
        requests.put('{}/saiof_test_read_access'.format(storage_url),
                     headers={'X-Auth-Token': auth_token})

        # He now creates an object in the new container.
        requests.put('{}/saiof_test_read_access/object'.format(storage_url),
                     headers={'X-Auth-Token': auth_token},
                     data='Some test data')

        # Ray mounts his his SAIO using SAIO Fuse.
        p = Popen(['./saio_fuse', '/tmp/saio_fuse'],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        self.assertEqual(err, '')
        self.assertEqual(p.returncode, 0)
        self.assertIn('total 4', output)
        self.assertIn('-r--r--r-- 1 rhawkins rhawkins 14 Jan  4 21:50 object',
                      output)

        # He performs a container listing using Swift's API and the
        # mounted directory, verifing that they are equivalent.
        ## HTTP GET http://127.0.0.1:8080
        ##          v1/AUTH_test/test_read_access?format=json
        ## ls -l /tmp/saio_fuse/v1/AUTH_test/test_read_access

        # He then reads an object using Swift's API and the mounted
        # directory, verifying that they are the same.
        ##  HTTP GET http://127.0.0.1:8080/v1/AUTH_test/test_read_access/object
        ## cat /tmp/saio_fuse/v1/AUTH_test/test_read_access/object


if __name__ == '__main__':
    unittest.main()
