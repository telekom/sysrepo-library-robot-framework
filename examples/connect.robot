*** Settings ***
Library     BuiltIn
Library     SysrepoLibrary


*** Variables ***
${First Connection ID}   0
${First Session ID}      0
${Running Datastore}     running
${Xpath Interfaces}      /ietf-system:system
${Format}                xml


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

Sysrepo Read/Write Datastore
    [Documentation]                 Read/Write Sysrepo plugin system Datastore
    ${Session Running}=             Open Datastore Session    ${Connection Default}    ${Running Datastore}
    ${Data}=                        Get Datastore Data    ${Connection Default}     ${Session Running}    ${Xpath Interfaces}    ${Format} 
    Log To Console                  \nDatastore ${Running Datastore} data:\n${Data}
    Edit Datastore Config    ${Connection Default}     ${Session Running}    ${Data}   ${Format} 

