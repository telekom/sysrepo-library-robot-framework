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
Library     BuiltIn
Library     SysrepoLibrary


*** Variables ***
${First Connection ID}   0
${First Session ID}      0
${Running Datastore}     running


*** Test Cases ***
Sysrepo Open And Close Connection
    [Documentation]                 Open and close a Sysrepo connection
    Log To Console                  \nFirst Suite Setup Connection: ${Connection Default}
    Should Be Equal As Integers     ${First Connection ID}   ${Connection Default}

Sysrepo Open And Close Connection and Running Session
    [Documentation]                 Open and close a Sysrepo connection and running datastore session
    Log To Console                  \nFirst Suite Setup Connection: ${Connection Default}
    Should Be Equal As Integers     ${First Connection ID}   ${Connection Default}
    Log To Console                  \nFirst Running Session: ${Connection Default}
    ${Session Running}=             Open Datastore Session    ${Connection Default}    ${Running Datastore}
    Should Be Equal As Integers     ${First Session ID}    ${Session Running}
