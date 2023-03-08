# robotframework-sysrepolibrary

A testing library for Robot Framework that utilizes the Sysrepo tool internally.

## Installation
Make sure to have Sysrepo and accompanying plugins installed under the `devel` branch (the latest libyang and sysrepo version).

Create a virtual environment, activate it and make sure `pip`, `setuptools`, `wheel` and `build` are up to date.

```
$ python3 -m venv sysrepolibrary-venv
$ source sysrepolibrary-venv/bin/activate
$ python3 -m pip install --upgrade pip setuptools wheel build
```

To simply install it:
```
$ python3 -m pip install .
```

### The long way
Build it:
```
$ python3 -m build
```

Two files should be in the `dist` directory. 
The `tar.gz` file is a source distribution whereas the `.whl` file is a built distribution.
Newer `pip` versions preferentially install built distributions, but will fall back to source distributions if needed.

Install it:
```
$ python3 -m pip install path/to/dist/build/file
```

## Examples
`examples/connection.robot` shows how SysrepoLibrary connects and disconnets to Sysrepo as well as opens and closes a session.
Note the root privileges when invoking the command (datastore permission issues otherwise, item not found):

Run:

`# robot examples`

