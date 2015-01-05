SAIO Fuse
=========

Fuse filesystem for a SAIO (Swift All-In-One).

For example the command:
```
$ curl -XGET -H'x-auth-token: AUTH_tk88b37b33021546728a8ab4221a4cf8f3' http://127.0.0.1:8080/v1/AUTH_test/container/object
```

Would have the same result as:
```
$ cat mount_dir/v1/AUTH_test/container/object
```
