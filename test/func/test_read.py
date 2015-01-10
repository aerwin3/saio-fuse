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

import getpass
import requests
import unittest

from subprocess import Popen, PIPE


class ReadTest(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        p = Popen(['umount', '/tmp/saio_fuse'],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if err:
            if 'is not mounted' not in err:
                raise Exception(err)

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

        # Ray creates a directory to mount to.
        p = Popen(['mkdir', '-p', '/tmp/saio_fuse'],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if err:
            raise Exception('Could not create mount point')

        # Ray lists all the accounts
        p = Popen(['ls', '-l', 'mount_dir/v1'],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        self.assertEqual(err, '')
        self.assertEqual(p.returncode, 0)
        user = getpass.getuser()
        # self.assertIn('total 4', output)
        self.assertIn('dr-xr-xr-x 2 {} {} 15 Jan  7 19:28 AUTH_test'.format(
                      user, user), output)

        # Ray lists all the containers for the account
        p = Popen(['ls', '-l', 'mount_dir/v1/AUTH_test'],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        self.assertEqual(err, '')
        self.assertEqual(p.returncode, 0)
        user = getpass.getuser()
        # self.assertIn('total 4', output)
        self.assertIn('dr-xr-xr-x 2 {} {} 15 Jan  7 19:28 '
                      'saiof_test_read_access'.format(
                      user, user), output)

        # Ray lists all the objects in the container
        p = Popen(['ls', '-l', 'mount_dir/v1/AUTH_test/saiof_test_read_access'],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        self.assertEqual(err, '')
        self.assertEqual(p.returncode, 0)
        user = getpass.getuser()
        # self.assertIn('total 4', output)
        self.assertIn('-r--r--r-- 1 {} {} 15 Jan  7 19:28 object'.format(
                      user, user), output)

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
