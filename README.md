# robotframework-sysrepolibrary

A testing library for Robot Framework that utilizes the Sysrepo tool internally.

## Installation
Make sure to have Sysrepo and accompanying plugins installed under the `devel` branch (the latest libyang and sysrepo version).

Create a virtual environment, activate it and make sure `pip`, `setuptools` and `wheel` are up to date.
Finally install the package.

```
$ python3 -m venv sysrepolibrary-venv
$ source sysrepolibrary-venv/bin/activate
$ python3 -m pip install --upgrade pip setuptools wheel
$ python3 setup.py install
```

## Tests
`tests/connection.robot` checks if SysrepoLibrary manages to connect and disconnet to Sysrepo, Open and close a session, as well as get, set datastore data. Requires sysrepo-plugin-system.
Note the root privileges when invoking the command (datastore permission issues otherwise, item not found):

Run:

`tests/ # robot examples`

