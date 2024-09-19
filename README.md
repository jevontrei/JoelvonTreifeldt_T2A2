# Title

Joel von Treifeldt
#15517

# do i need to grant permissions in psql?

Note:

- All links to online material should have corresponding screenshots included in submission.
- i.e. make sure Trello link is public! etc! and make heaps of screenshots, starting early on

MAKE A TABLE OF CONTENTS

- [Title](#title)
- [do i need to grant permissions in psql?](#do-i-need-to-grant-permissions-in-psql)
- [R1](#r1)
- [R2](#r2)
- [R3](#r3)
- [R4](#r4)
- [R5](#r5)
- [R6](#r6)
- [R7](#r7)
- [R8](#r8)
- [.](#)
- [.](#-1)
- [.](#-2)
- [.](#-3)
- [.](#-4)
- [.](#-5)
- [.](#-6)
- [.](#-7)
- [.](#-8)
- [.](#-9)
- [.](#-10)
- [.](#-11)
- [.](#-12)

# R1

Explain the problem that this app will solve, and explain how this app solves or addresses the problem.

# R2

Describe the way tasks are allocated and tracked in your project.

# R3

List and explain the third-party services, packages and dependencies used in this app.

# R4

Explain the benefits and drawbacks of this app’s underlying database system.

# R5

Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app.

# R6

Design an entity relationship diagram (ERD) for this app’s database, and explain how the relations between the diagrammed models will aid the database design.

This should focus on the database design BEFORE coding has begun, eg. during the project planning or design phase.

<!-- how to display mermaid diagram in markdown? -->
```
erDiagram
    Patient ||--o{ Treat : "has optional"
    Doctor ||--o{ Treat : "provides optional"
    Patient ||--o{ Log : "records optional"
    Treat ||--o{ Appointment : "schedules optional"

    Patient {
        int patient_id PK
        string name
        string email
        string password
        date dob
        string sex
        string diagnoses
        boolean is_admin
    }

    Doctor {
        int doc_id PK
        string name
        string email
        string password
    }

    Treat {
        int treat_id PK
        int patient_id FK
        int doc_id FK
        date start_date
        date end_date
    }

    Appointment {
        int appt_id PK
        date datetime
        string place
        int cost
        string status
        int treat_id FK
    }

    Log {
        int log_id PK
        date date
        string symptom
        string duration
        string severity
        int patient_id FK
    }
```

# R7

Explain the implemented models and their relationships, including how the relationships aid the database implementation.

This should focus on the database implementation AFTER coding has begun, eg. during the project development phase.

# R8

Explain how to use this application’s API endpoints. Each endpoint should be explained, including the following data for each endpoint:

HTTP verb
Path or route
Any required body or header data
Response

...

# .

<!-- CMP1001-6.2: JUSTIFIES the purpose and goal of the developed application.
6 to >5 pts
HD
Provides a DETAILED explanation about the problem being solved by the developed application AND about how the app addresses the problem, and DOES use any objective references or statistics to support their answer. -->

# .

<!-- CMP1001-2.3: DESCRIBES the way tasks are planned and tracked in the project.
6 to >5 pts
HD
Meets D, and includes proof of THOROUGH usage of specific task management tools THROUGH THE LENGTH OF THE PROJECT.

"Meets D" means disctinction. look at rubric table: F, P, C, D, HD -->

# .

<!-- CMP1001-1.2: DESCRIBES the third party services, packages or dependencies that are used in the developed application.
6 to >5 pts
HD
The description provided is DETAILED, and the description details ALL of the services, packages or dependencies that are used in the developed application. -->

# .

<!-- CMP1001-2.4: IDENTIFY AND DESCRIBE the benefits and drawbacks of a chosen database system.
6 to >5 pts
HD
Meets D, and describes benefits AND drawbacks to a thorough level of detail. -->

# .

<!-- CMP1001-1.3: EXPLAINS the features and functionalities of an object-relational mapping (ORM) system
6 to >5 pts
HD
Explains MULTIPLE features or functionalities of an ORM to a THOROUGH level of detail, supporting the explanation with AT LEAST ONE code example. -->

# .

<!-- PMG1003-2.1, PMG1003-7.3: EXPLAINS a plan for normalised database relations.
12 to >10 pts
HD
Meets D, and the explanation includes comparisons to how AT LEAST ONE model or relations would look in other levels of normalisation than the one shown in the ERD. -->

# .

<!-- CMP1001-7.2: DESCRIBES the project’s models in terms of the relationships they have with each other.
6 to >5 pts
HD
Meets D, and includes appropriate code examples supporting the descriptions. -->

# .

<!-- CMP1001-1.4: IDENTIFY AND DESCRIBE the application’s API endpoints.
6 to >5 pts
HD
Meets D, applied to ALL of the application’s API endpoints. -->

# .

<!-- PGM1003-2.2: IMPLEMENTS a normalised database design.
6 to >5 pts
HD
Meets D with no duplication and ideal model implementation. -->

# .

<!-- PGM1003-6.2: IMPLEMENTS a database design that appropriately addresses the requirements of the planned scenario.
6 to >5 pts
HD
Meets D and represents a highly optimised or normalised solution. -->

# .

<!-- PGM1003-4.1: IMPLEMENTS database queries that provide correct data for the given scenario.
6 to >5 pts
HD
Implements queries that provide ALL data needed for a working solution, and the queries are suitably complex and optimised. -->

# .

<!-- PGM1003-4.2: WRITES code comments that demonstrate how the queries implemented correctly represent the database structure.
6 to >5 pts
HD
ALL queries or model methods are commented to a THOROUGH level of detail, with reference to a style guide or comment style guide in the project documentation. -->

# .

<!-- PGM1003-5.2: IMPLEMENTS sanitization and validation techniques on user input to maintain data integrity
6 to >5 pts
HD
Validates ALL user input AND sanitises user input where relevant. -->
