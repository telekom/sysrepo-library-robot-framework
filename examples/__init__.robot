*** Settings ***
Library     SysrepoLibrary

Suite Setup         Create Connection Default
Suite Teardown      Close All Sysrepo Connections And Sessions

*** Keywords ***
Create Connection Default
    ${Connection Default}=      Open Sysrepo Connection
    Set Global Variable         ${Connection Default}

