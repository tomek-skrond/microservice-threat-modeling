# Repository info
This repo stores code and results for my threat modeling of microservice and monolithic architecture.

Threat Modeling tools that are analyzed:
- Microsoft Threat Modeling Tool
- IriusRisk Community Edition

The analysis consists of the following:
- parsing raw report data copied from report
- serializing report data into CSV file
- analysis of:
    - number of Threats per component
    - Threats Risk Level
    - Threat type per component (eg. SQL Injection, MitM, Broken Access Control etc.)
    - Threat type relevancy for each component