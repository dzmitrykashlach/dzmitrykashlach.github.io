---
layout: post
title:  "Keycloak multitenancy: how I've dropped Spring Security"
date:   2024-10-14 9:00:00 +0300
categories: security
---

- attempt to add Spring Security to application.yml - no way
- decided to take approach 1 tenant - 1 realm;
- But how to ensure that keycloak user base is equal to master data ?
- Add @Scheduled sync job: need to do leader election
- other possible approach: Keycloak organizations - to follow up;
