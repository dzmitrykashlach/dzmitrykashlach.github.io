---
layout: resume
title: Resume
permalink: /resume/en

---
#### __Contacts__
- [dzmitrykashlach@gmail.com](mailto:dzmitrykashlach@gmail.com)
- [Instagram](https://www.instagram.com/dzmitrykashlach/)
- [Telegram](https://t.me/monowheeller)
- [LinkedIn](https://www.linkedin.com/in/dzmitrykashlach/)  
- Location: Barysaw, Belarus

#### __Summary__
I'm a CNC woodworking machinist and wooden product designer specializing in taking products from concept to finished physical object.

I can cover the complete development and fabrication process:
Concept → 3D modeling → CAM/G-code → CNC machining → hand finishing

My work includes designing wooden decorative products, kitchenware and other small-batch or custom products, preparing CNC toolpaths, selecting milling tools and machining parameters, setting up CNC machines, and completing products by hand.

I also bring 10 years of professional software development experience with Java, Kotlin and Spring Boot. This background has shaped the way I approach physical product development: I’m comfortable working from requirements, breaking complex problems into manageable stages, designing repeatable processes, and taking responsibility for the result end-to-end.

I'm interested in working with individuals, product designers, workshops, manufacturers and other organizations that need someone who can bridge product design, CAD/CAM and actual CNC manufacturing.

I can contribute at different stages of a project — from developing a product from an initial idea to preparing an existing design for CNC production and manufacturing the final piece. 

#### __Work Experience__  

#### `Jul 2026 – now`  Woodworking design engineer & CNC machinist, [DASDwood](https://dasdwood.web.app/)  
Responsibilities:  
- Design wooden decorative, kitchenware and custom products.  
- Develop 3D models and prepare designs for CNC manufacturing.  
- Cover the complete fabrication workflow: concept → 3D modeling → CAM / G-code → CNC machining → hand finishing.  
- Set up and operate a Watsan 0609 Mini CNC router.  
- Select milling tools and determine appropriate machining parameters.  
- Develop and manufacture prototypes and finished wooden products.  
- Refine designs and machining strategies based on physical prototypes and manufacturing results.  

#### `Dec 2024 – now`  Senior Kotlin Developer, [Altabel Group](https://altabel.com/)
Product: Gift cards selling application.  
Environment: Kotlin, Spring Boot, REST API, OAuth, Keycloak, Kubernetes, Elasticsearch, Loki, Grafana, 
MariaDB, Gitlab, 3 backend developers, 1 devops.  
Responsibilities:
- Designed and implemented core backend microservices from scratch.  
- Ensured that backend is able to handle 200-300 RPS with Infinispan cache.  
- Designed MariadDB schema and ElasticSearch indexes.  
- Introduced static code analysis (`detekt` tool) improving code quality and enforcing coding standards across services.  
- Designed and implemented CI/CD: GitLab pipeline, Gitlab agent installation in cluster.  
- Designed and implemented multi-realms(1 realm per 1 organization) authorization architecture leveraging Keycloak.    
- Improved platform reliability by delivering seamless Keycloak upgrades with configuration migrations and template adaptations.  
- Ensured operational visibility by running centralized logging and monitoring with Loki and Grafana.  
- Ensured authorization system resilience by running Keycloak replicas in Kubernetes.    
- Used Cursor AI to accelerate code navigation, refactoring drafts, and test scaffolding while keeping design and final review decisions manual.

#### `Sep 2022 – Nov 2024`  Senior Kotlin Developer, [Altabel Group](https://altabel.com/)
Product: Credit conveyor for issuing loans to individuals.  
Environment: Kotlin, Spring Boot, ELK, PostgreSQL, 5 backend developers.    
Responsibilities:
- Refactored architecture: developed a proxy-microservice which removed tight coupling to internal bank application and enabled integration of external partners into the credit conveyor.  
- Delivered business features per product requests: automatic repayments, cession, integration with an external bank for stable repayment processing.
- Delivered multiple service contracts (REST, Apache Thrift) with unit and integration tests.  
- Implemented Spring Cloud Consul Agent customization for re-registering microservice in case of Consul agent restart.  

#### `Apr 2020 – Jun 2022`  Senior Java Developer, [EPAM](https://epam.com/)
Product: Corporate library.  
Environment: Java, Kotlin, Spring Boot/MVC, MySQL, 5 backend developers  
Responsibilities:
- Reduced manual work for performance analysts by integrating the collaboration system (Spring MVC, Atlassian Confluence, ~100k users, ~1 TB MySQL) with the performance testing engine (REST API, Spring Boot/Data/Security, OAuth 2.0, JWT, Thymeleaf, Apache JMeter).
- Reduced escalations by tuning JVM garbage collector.
- Reduced escalations by optimizing problematic SQL queries (MySQL).
- Developed a continuous performance analysis process and mentored two engineers to follow new flow.  
- Decreased Time to Interactive (TTI) by 0.5s by configuring caching on Akamai CDN.
- Delivered talks for [MJC (Minsk Java Community) School](https://github.com/mjc-school/MJC-School).

#### `Apr 2018 – Jan 2020`  Senior Java Developer, [EPAM](https://epam.com/)
Product: Business process automation for an insurance company.  
Environment: Java, Selenium, MySQL, AWS S3  
Responsibilities:
- Developed automation for day-to-day business processes (insurance domain, WorkFusion, Spring MVC, Java 11, Windows Server, Selenium).
- Decreased escalations by improving monolithic architecture and refactoring code.

#### `Nov 2016 – Mar 2018`  Java Developer, [BlazeMeter LTD](https://blazemeter.com/)
Product: Test-plan generator for Apache JMeter.  
Environment: Java, Apache JMeter, AWS EC2, AWS S3  
Responsibilities:
- Developed a test-plan generator (Java 8, Apache JMeter, Spring Boot, AWS) to improve UX of the SaaS performance testing platform.

#### `Nov 2015 – Oct 2016`  Java Developer, [BlazeMeter LTD](https://blazemeter.com/)  
Product: Java library for CI/CD plugins.  
Environment: Java, Maven, Nexus, REST API  
Responsibilities:
- Designed a Java library for existing CI/CD plugins.

#### `Jan 2013 – Oct 2015`  Java Developer, [BlazeMeter LTD](https://blazemeter.com/)  
Product: CI/CD plugins for a SaaS platform.  
Environment: Java, Maven, Nexus, REST API  
Responsibilities:
- Designed CI/CD plugins (Jenkins, TeamCity, Bamboo) for a performance testing SaaS platform to run load tests within CI/CD pipelines.
- Developed a component for the open-source project [Apache JMeter DNS Cache Manager](https://github.com/apache/jmeter/commit/4468b60dc6f3d1f6ac543fa80d6c4f36a4395e0c) to distribute load evenly from different locations during load testing.

[ #### __Technical Skills__ ]: #

[ - **Languages**: Java (9+ years), Kotlin (4+ years) ]: #
[ - **Backend**: Spring Boot, Spring MVC, Spring Security, Spring Data, Ktor ]: #
[ - **Databases**: PostgreSQL, MySQL, MariaDB, Liquibase, Elasticsearch ]: #
[ - **Infrastructure & CI/CD**: Docker, Jenkins, Kubernetes, Git, GitLab CI, TeamCity ]: #
[ - **Messaging & Integration**: REST APIs, Apache Kafka, Apache Thrift ]: #
[ - **Cloud Infrastructure**: AWS (EC2, S3, Route 53) ]: #
[ - **Caching & Logging**: Infinispan, ELK, Loki ]: #
[ - **Security & Identity**: OAuth 2.0, Keycloak ]: #
[ - **Performance**: JVM tuning, SQL query optimization, application performance analysis ]: #
[ - **Developer Productivity**: Cursor AI ]: #

#### __Foreign Languages__

- English: B2 – upper-intermediate; confident in professional communication and reading/writing technical documentation.

#### __Education__
`2001–2006` Electronics Design, Bachelor, [Belarusian State University of Informatics and Radioelectronics (BSUIR)](https://www.bsuir.by/en/)