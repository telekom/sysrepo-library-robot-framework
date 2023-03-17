#
# telekom / sysrepo-plugin-system
#
# This program is made available under the terms of the
# BSD 3-Clause license which is available at
# https://opensource.org/licenses/BSD-3-Clause
#
# SPDX-FileCopyrightText: 2023 Deutsche Telekom AG
# SPDX-FileContributor: Sartura Ltd.
#
# SPDX-License-Identifier: BSD-3-Clause
#

*** Settings ***
Library     SysrepoLibrary

Suite Setup         Create Connection Default
Suite Teardown      Close All Sysrepo Connections And Sessions

*** Keywords ***
Create Connection Default
    ${Connection Default}=      Open Sysrepo Connection
    Set Global Variable         ${Connection Default}

