SAIO Fuse
=========

Fuse file system for a SAIO (Swift All-In-One).

<strong>Note:</strong>  This project is currently in the development phase and
should be considered non-working/unstable until this note is removed.

For example the command:
```
$ curl -XGET -H'x-auth-token: AUTH_tk88b37b33021546728a8ab4221a4cf8f3' http://127.0.0.1:8080/v1/AUTH_test/container/object
```

Would have the same result as:
```
$ cat mount_dir/v1/AUTH_test/container/object
```
