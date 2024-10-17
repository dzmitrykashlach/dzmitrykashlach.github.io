---
layout: post
title:  "Keycloak Multitenancy: How I've Dropped Spring Security"
date:   2024-10-14 9:00:00 +0300
categories: security
---

I was building a backend for selling gift cards on one of my projects. 
The project was designed to scale by onboarding new retailers who want to sell their gift cards.

We're using Keycloak as our authorization server, and my initial approach was to use Spring Security for JWT token verification. 
However, this proved challenging due to the multitenancy requirement—the entire user base needs to be structured into organizations that users belong to. 
Spring Security became unsuitable because it requires hard-coding the realm in `application.properties`.

Using a separate realm for each organization seemed reasonable, but a new problem arose:
- How do we verify JWT tokens?
- How do we determine which realm a user should request a JWT from?

The solution was to implement a two-phase authorization schema, where the realm URL is stored in the User entity in the master database.
During the first phase, the Android application authorizes itself via clientId and retrieves a list of users attached to the client.
During the second phase, the user authorizes themselves according to their role.

The main challenge to solve was where to verify JWTs if Spring Security was not used.
After some discussion, we decided to do this at the API gateway before requests reach the backend.

Follow-up:
- Add @Scheduled sync job: need to implement leader election
- Alternative approach: Keycloak organizations—to be explored
