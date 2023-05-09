<h1 align="center">
    Sysrepo Robot Framework Library
</h1>

<p align="center">
    <a href="/../../commits/" title="Last Commit"><img src="https://img.shields.io/github/last-commit/telekom/sysrepo-library-robot-framework?style=flat"></a>
    <a href="/../../issues" title="Open Issues"><img src="https://img.shields.io/github/issues/telekom/sysrepo-library-robot-framework?style=flat"></a>
    <a href="./LICENSE" title="License"><img src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat"></a>
    <a href="https://pypi.org/project/robotframework-sysrepolibrary/" title="PyPi robotframework-sysrepolibrary"><img src="https://img.shields.io/static/v1?label=PyPi&message=robotframework-sysrepolibrary&color=blue&labelColor=yellow"></a>
</p>

<p align="center">
  <a href="#development">Development</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#support-and-feedback">Support</a> •
  <a href="#how-to-contribute">Contribute</a> •
  <a href="#contributors">Contributors</a> •
  <a href="#licensing">Licensing</a>
</p>

The goal of this project is to provide a way to use sysrepo with the [Robot Framework](https://github.com/robotframework/robotframework).

## About this component

This repository contains a Robot Framework Python library wrapper around the [sysrepo-python](https://github.com/sysrepo/sysrepo-python) sysrepo bindings.

The [examples](./examples/) directory contains a simple example test that connects to sysrepo and does some basic validity checks.

## Development

The following additional dependencies are required to work on the library:

* libyang
* sysrepo
* pip
* setuptools
* wheel
* build

#### Installation
The recommended installation method is using [pip](http://pip-installer.org):
```
$ python3 -m pip install robotframework-sysrepolibrary
```

With recent versions of `pip` it is also possible to install directly from the [GitHub](https://github.com/telekom/sysrepo-library-robot-framework) repository. 
To install from the latest source from the master branch, use the following command:
```
$ python3 -m pip install git+https://github.com/telekom/sysrepo-library-robot-framework.git
```

#### Build

First clone the repository:

```
$ git clone https://github.com/telekom/sysrepo-library-robot-framework
```

To build the library run the following commands:
```
$ python3 -m venv sysrepolibrary-venv
$ source sysrepolibrary-venv/bin/activate
$ python3 -m pip install --upgrade pip setuptools wheel build
```

To install it:
```
$ python3 -m pip install .
```

To install the additional dependencies as well (generating the documentation and testing):
```
$ python3 -m pip install .[docs,tests]
```

## Code of Conduct

This project has adopted the [Contributor Covenant](https://www.contributor-covenant.org/) in version 2.0 as our code of conduct. Please see the details in our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). All contributors must abide by the code of conduct.

## Working Language

We decided to apply _English_ as the primary project language.  

Consequently, all content will be made available primarily in English. We also ask all interested people to use English as language to create issues, in their code (comments, documentation etc.) and when you send requests to us. The application itself and all end-user facing content will be made available in other languages as needed.

## Documentation

The documentation for the Sysrepo Robot Framework Library can be generated using the [Sphinx](https://www.sphinx-doc.org/en/master/) documentation generator tool.
The documentation sources are located in [docs/source](./docs/source)

To build the documentation as `HTML` files run while in the root directory:
```
$ sphinx-build -b html docs/source docs/build/html
```

The `-b` option selects a builder in this example it's `HTML`.

To quickly generate the docs use the scripts in the `docs/` directory.
Execute `make` without an argument while in the directory to see which targets are available.

Example for `HTML`:
```
docs/$ make html
```

## Support and Feedback

The following channels are available for discussions, feedback, and support requests:

| Type               | Channel                                                                                                                                                                                            |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Issues**         | <a href="/../../issues/new/choose" title="General Discussion"><img src="https://img.shields.io/github/issues/telekom/sysrepo-library-robot-framework?style=flat-square"></a> </a>                        |
| **Other Requests** | <a href="mailto:opensource@telekom.de" title="Email Open Source Team"><img src="https://img.shields.io/badge/email-Open%20Source%20Team-green?logo=mail.ru&style=flat-square&logoColor=white"></a> |

## How to Contribute

Contribution and feedback is encouraged and always welcome. For more information about how to contribute, the project structure, as well as additional contribution information, see our [Contribution Guidelines](./CONTRIBUTING.md). By participating in this project, you agree to abide by its [Code of Conduct](./CODE_OF_CONDUCT.md) at all times.

## Contributors

Our commitment to open source means that we are enabling -in fact encouraging- all interested parties to contribute and become part of its developer community.

## Licensing

Copyright (C) 2023 Deutsche Telekom AG.

Licensed under the **BSD 3-Clause License** (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License by reviewing the file [LICENSE](./LICENSE) in the repository.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the [LICENSE](./LICENSE) for the specific language governing permissions and limitations under the License.
