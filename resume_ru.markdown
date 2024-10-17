---
layout: page
title: Резюме
permalink: /resume/ru

---
#### __Контакты__
- [dzmitrykashlach@pm.me](mailto:dzmitrykashlach@pm.me)
- [Telegram](https://t.me/monowheeller)
- [LinkedIn](https://www.linkedin.com/in/dzmitrykashlach/)

#### __Кратко обо мне__
- Разработка и рефакторинг серверных приложений (Kotlin 2.0/Java 21, Spring Boot/Ktor, гексогональная архитектура).
- Поиск и устранение проблем производительности в высоконагруженных монолитных приложениях (Spring MVC).
- Разработка CI/CD скриптов для деплоя (GitLab, Jenkins, TeamCity, etc.).
- Разработка несложного UI на Angular 14 (3–4 вкладки, CRUD).
- Опыт работы по Scrum (LeSS) и Kanban.

#### __Проекты__
#### `Dec 2024 – now`  Старший Kotlin разработчик, [Altabel Group](https://altabel.com/)
Продукт: Приложение для продажи подарочных карт.  
Стэк: Kotlin 2.0, Spring Boot 3.0, REST API OAuth 2.0, Keycloak, Kubernetes, Elasticsearch, Infinispan, Loki, Grafana, MariaDB, Gitlab.  
Обязанности:
- Дизайн и разработка основных бэкенд-микросервисов с нуля.  
- С Infinispan cache обеспечил способность бэкенда обрабатывать 200–300 RPS.
- Дизайн схемы MariaDB и индексов Elasticsearch.  
- Настройка контроля качества кода на базе инструмента `detekt`.  
- Дизайн и реализация CI/CD: пайплайн GitLab, установка агента Gitlab в кластере.  
- Дизайн и реализация multi-realm системы авторизации (1 realm на 1 организацию) на базе Keycloak.  
- Обновление Keycloak и связанных конфигураций.  
- Адаптация шаблонов в Keycloak.  
- Настройка и управление репликами Keycloak в кластере Kubernetes.  
- Настройка и управление системой логирования и мониторинга: Loki, Grafana.  

#### `Sep 2022 – Nov 2024`  Старший Kotlin разработчик, [Altabel Group](https://altabel.com/)
Продукт: Кредитный конвейер для выдачи кредитов физическим лицам.  
Стэк: Kotlin 1.8, Spring Boot 3.0, Ktor, ELK  
Обязанности:
- Рефакторинг Open API: уход от привязки к внутреннему приложению для возможности интеграции внешних партнёров.
- Разработка функционала по запросам владельца продукта: автоматические погашения, цессия, интеграция с внешним банком для повышения стабильности погашений.
- Участие в обсуждении архитектуры, разработка кода по принципам гексогональной архитектуры, реализация контрактов сервисов (REST, Apache Thrift), интеграционные и юнит-тесты.

#### `Apr 2020 – Jun 2022`  Старший Java разработчик, [EPAM](https://epam.com/)
Продукт: Корпоративная библиотека.  
Стэк: Java 11, Kotlin, Spring Boot/MVC  
Обязанности:
- Сократил количество ручной работы для аналитиков производительности посредством интеграции системы (корпоративный инструмент для совместной работы, Spring MVC, Atlassian Confluence, ~100k пользователей, ~1 TB MySQL) с системой для нагрузочного тестирования (REST API, Spring Boot/Data/Security, OAuth 2.0, JWT, Thymeleaf, Apache JMeter).
- Сократил количество обращений от пользователей через настройку JVM GC.
- Сократил количество обращений от пользователей через оптимизацию проблемного SQL-запроса (MySQL).
- Установил процесс анализа производительности приложения и обучил этому двух разработчиков.
- Уменьшил Time to Interactive (TTI) на 0.5 сек. через настройку кэширования на Akamai CDN.
- Провёл несколько лекций для [MJC (Minsk Java Community) School](https://github.com/mjc-school/MJC-School).

#### `Apr 2018 – Jan 2020`  Старший Java разработчик, [EPAM](https://epam.com/)
Продукт: Автоматизация бизнес-процессов для страховой компании.  
Стэк: Java 11, Selenium, MySQL, AWS S3  
Обязанности:
- Разработал автоматизацию для производственных бизнес-процессов (домен страхования, платформа WorkFusion, Spring MVC, Java 11, Windows Server, Selenium).
- Уменьшил количество обращений от пользователей через улучшение архитектуры существующей автоматизации (монолит) и рефакторинг кода.

#### `Nov 2016 – Mar 2018`  Java разработчик, [BlazeMeter LTD](https://blazemeter.com/)
Продукт: Генератор тест-планов для Apache JMeter.  
Стэк: Java 11, Apache JMeter, AWS EC2, AWS S3  
Обязанности:
- Разработал генератор тест-планов (Java 8, Apache JMeter, Spring Boot, AWS) для улучшения UX SaaS-платформы нагрузочного тестирования.

#### `Nov 2015 – Oct 2016`  Java разработчик, [BlazeMeter LTD](https://blazemeter.com/)  
Продукт: Java библиотека для CI/CD плагинов.  
Стэк: Java 8, Maven, Nexus, REST API  
Обязанности:
- Разработал библиотеку на Java для существующих CI/CD плагинов (Java 8, Maven, Nexus, REST API) для встраивания нагрузочного тестирования в CI/CD процесс.

#### `Jan 2013 – Oct 2015`  Java разработчик, [BlazeMeter LTD](https://blazemeter.com/)  
Продукт: CI/CD плагины для SaaS-платформы.  
Стэк: Java 8, Maven, Nexus, REST API  
Обязанности:
- Разработал плагины для интеграции CI/CD систем с SaaS-платформой для нагрузочного тестирования (Jenkins, TeamCity, Bamboo).
- Разработал компонент для open-source проекта [Apache JMeter DNS Cache Manager](https://github.com/apache/jmeter/commit/4468b60dc6f3d1f6ac543fa80d6c4f36a4395e0c), позволяющий равномерно распределить нагрузку с разных локаций во время нагрузочного тестирования.

#### __Навыки__

| Название                                    | Уровень     | Кол-во лет опыта |
|---------------------------------------------|-------------|------------------|
| Java (17)                                   | Продвинутый | 9                |
| Kotlin (2.0)                                | Средний     | 4                |
| SQL (PostgreSQL, MySQL, MariaDB, Liquibase) | Продвинутый | 6                |
| Spring (MVC, Boot, Security, Data)          | Продвинутый | 4                |
| Ktor                                        | Средний     | 1                |
| ORM (Hibernate, Exposed)                    | Средний     | 2                |
| CI/CD (Docker, Jenkins, TeamCity)           | Продвинутый | 4                |
| Брокеры сообщений (Apache Kafka)            | Средний     | 1                |
| AWS (EC2, S3, Route 53)                     | Продвинутый | 3                |
| NoSQL (Elasticsearch)                       | Средний     | 1                |
| Кэш (Infinispan)                            | Средний     | 1                |
| Logging (ELK, Loki)                         | Средний     | 1                |
| Git                                         | Продвинутый | 8                |
| REST API                                    | Продвинутый | 5                |
| RPC (Apache Thrift)                         | Средний     | 1                |
| OAuth 2.0 (Keycloak)                        | Средний     | 1                |
| Анализ производительности                   | Продвинутый | 2                |

#### __Образование__
`2001–2006` Дизайн электроники, Специалист, [Belarusian State University of Informatics and Radioelectronics (BSUIR)](https://www.bsuir.by/en/)


#### __Сертификаты__
- [Spring Security • Udemy, Feb 2023](https://ude.my/UC-d0221e26-3509-4cdd-82c6-3d02470424ad)
- [Apache Kafka for Java Developers using Spring Boot • Udemy, Mar 2023](https://ude.my/UC-d0221e26-3509-4cdd-82c6-3d02470424ad)
- [Advanced Algorithms (Graph Algorithms) in Java • Udemy, Apr 2024](https://ude.my/UC-ba9a724b-b57b-41eb-9031-7d7920a4ff62)