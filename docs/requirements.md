# Mentoria — Requirements (Draft 1)

Graduation project GP-26-SE-D-03, School of Computing, New Uzbekistan University.
Team: Soibnazarov Avazbek, Mamatov Shohruh, Abdurazzoqov Abdurahmon. Supervisor: Assadullah Tariq.
Status: first draft for supervisor review (Fall Week 10).

## 1. Introduction

**Purpose.** Mentoria is a level-based online learning web platform for learners in Uzbekistan. It brings together self-paced courses, tutor and mentor booking, and free open lectures in one place, and uses a placement test to match learners to content and people at their level.

**Scope.** Four parts:
1. Course marketplace (video, PDF and quiz lessons; search, enrolment, test-mode payment, progress).
2. Tutor finder (profiles, ranked list, booking, reviews).
3. Mentorship (one-to-one advice sessions, free or paid; shares the booking engine with tutors).
4. Free open lectures (recorded library and scheduled live lectures with registration).

Cross-cutting: rule-based adaptive placement test, transparent weighted tutor matching, Zoom meeting creation, admin panel, English and Uzbek interface.

**Roles.**

| Role | Description |
|---|---|
| Student | Browses, enrols in courses, books tutors/mentors, takes placement tests, watches lectures |
| Educator | Creates, prices and publishes courses |
| Tutor | Publishes a profile and availability, teaches booked lessons |
| Mentor | Publishes free time for advice/consulting sessions |
| Admin | Approves courses, verifies tutors and mentors, handles reports |

## 2. Functional requirements

### Accounts (ACC)
- **FR-ACC-01** Users can register with e-mail and password and choose a role (student, educator, tutor, mentor). Admin accounts are created by staff only.
- **FR-ACC-02** Users can log in and log out using JWT authentication.
- **FR-ACC-03** Every API endpoint enforces role-based permissions.
- **FR-ACC-04** Users can view and edit their profile and choose the interface language (EN/UZ).
- **FR-ACC-05** Users can reset a forgotten password by e-mail.

### Courses (CRS)
- **FR-CRS-01** Educators can create, edit and delete their own courses with title, description, subject, level, language and price.
- **FR-CRS-02** Educators can add video, PDF and quiz lessons to a course and order them.
- **FR-CRS-03** A course becomes public only after admin approval.
- **FR-CRS-04** Students can search and filter courses by subject, level, language and price.
- **FR-CRS-05** Students can enrol in a course (after payment if it is paid).
- **FR-CRS-06** Paid lesson files are served only to enrolled students (checked by the backend).
- **FR-CRS-07** The system tracks lesson completion and shows course progress.
- **FR-CRS-08** Students can complete quiz lessons and see their result.

### Open lectures (LEC)
- **FR-LEC-01** Anyone, without login, can browse and watch recorded lectures.
- **FR-LEC-02** Lectures can be filtered by subject and language.
- **FR-LEC-03** Authorised staff/educators can publish recorded lectures and schedule live lectures.
- **FR-LEC-04** Logged-in users can register for a live lecture and receive the join link.

### Tutor and mentor booking (BKG)
- **FR-BKG-01** Tutors and mentors can create a profile (subjects/topics, levels, rate, languages, bio).
- **FR-BKG-02** Tutors and mentors can set weekly availability.
- **FR-BKG-03** Students can view a tutor/mentor profile and available slots.
- **FR-BKG-04** Students can book a free slot; the system never double-books a slot (transaction plus overlap check).
- **FR-BKG-05** Tutors/mentors can confirm or decline a booking; both sides can cancel before the session.
- **FR-BKG-06** Mentor sessions can be free or paid.
- **FR-BKG-07** After a completed session, the student can leave a rating and review.
- **FR-BKG-08** Users receive e-mail notifications for booking requests, confirmations and cancellations.

### Placement test and matching (PLC)
- **FR-PLC-01** A student can take a short placement test per subject.
- **FR-PLC-02** The test is rule-based adaptive: the next question is harder after a correct answer and easier after a wrong one.
- **FR-PLC-03** The score maps to Beginner / Intermediate / Advanced (CEFR A1–C2 for English); the level is saved on the student profile.
- **FR-PLC-04** Course recommendations are based on the student's level.
- **FR-PLC-05** Tutors are ranked with a transparent weighted score: level fit, budget fit, schedule overlap, language, and Bayesian-smoothed rating. No ML.
- **FR-PLC-06** The ranked list shows why a tutor scored as they did.

### Payments (PAY)
- **FR-PAY-01** Students can pay for a course or a paid session in Stripe test mode.
- **FR-PAY-02** If Stripe test mode is not usable, a fake payment service with the same interface is used.
- **FR-PAY-03** Enrolment or booking is activated only after successful payment.
- **FR-PAY-04** Students can see their payment history.

### Zoom (ZOOM)
- **FR-ZOOM-01** When a tutoring or mentoring booking is confirmed, the backend creates a Zoom meeting (Server-to-Server OAuth) and stores the join link.
- **FR-ZOOM-02** When a live lecture is scheduled, the backend creates a Zoom meeting and stores the join link.
- **FR-ZOOM-03** The join link is visible only to the participants of the session or the registered attendees.
- **FR-ZOOM-04** If Zoom fails, the booking remains valid and the failure is logged and can be retried.

### Admin (ADM)
- **FR-ADM-01** Admins can approve or reject courses.
- **FR-ADM-02** Admins can verify tutor and mentor profiles.
- **FR-ADM-03** Admins can view and handle user reports.
- **FR-ADM-04** Admins can deactivate users and remove content (via Django admin where possible).

## 3. User stories

Priorities use MoSCoW (Must / Should / Could / Won't for this release).

### Student

**US-01 — Register and log in** (Must)
As a student, I want to register and log in so that my progress and bookings are saved.
- I can register with e-mail and password and then log in.
- Wrong credentials show a clear error.
- After login I see only the pages my role allows.

**US-02 — Find a course** (Must)
As a student, I want to search and filter courses so that I find one that fits my subject, level and budget.
- I can filter by subject, level, language and price.
- Results show title, price, level and rating/progress info.
- Only approved courses appear.

**US-03 — Enrol and learn** (Must)
As a student, I want to pay for a course and follow its lessons so that I can learn at my own pace.
- After successful (test) payment I am enrolled.
- I can open video, PDF and quiz lessons and mark them complete.
- My progress percentage is shown.

**US-04 — Take a placement test** (Should)
As a student, I want a short placement test so that I know my level and get relevant recommendations.
- Question difficulty adapts to my previous answer.
- I get a level result at the end.
- Recommended courses and tutors use this level.

**US-05 — Book a tutor** (Must)
As a student, I want to see a ranked list of tutors and book a slot so that I get a lesson that fits my level and schedule.
- I can see why a tutor is ranked high.
- Booked slots can't be booked by anyone else.
- I get a confirmation e-mail and, once confirmed, a Zoom link.

**US-06 — Book a mentor** (Should)
As a student, I want to book a mentoring session so that I can get career or university-application advice.
- I can see the mentor's free time and price (or "free").
- Booking works the same way as for tutors.
- I can cancel before the session.

**US-07 — Watch open lectures** (Must)
As a student, I want to watch free lectures so that I can learn without paying.
- Recorded lectures open without login or payment.
- I can register for a live lecture and receive its link.

**US-08 — Review a tutor** (Should)
As a student, I want to rate and review a tutor after a lesson so that other students can choose better.
- I can review only after a completed booking.
- One review per booking.
- The tutor's average rating updates.

### Educator

**US-09 — Publish a course** (Must)
As an educator, I want to create a course with lessons and a price so that students can find and buy it.
- I can add video, PDF and quiz lessons.
- The course is hidden until an admin approves it.
- I can edit it after publishing.

**US-10 — See my students** (Could)
As an educator, I want to see enrolments and student progress so that I can improve my course.
- I see the number of enrolled students per course.
- I see average progress.

### Tutor

**US-11 — Create a tutor profile** (Must)
As a tutor, I want a profile with subjects, levels, rate and languages so that students can find me.
- I can edit my profile at any time.
- Unverified profiles are marked as such and are not ranked until verified.

**US-12 — Manage availability and bookings** (Must)
As a tutor, I want to set weekly availability and confirm bookings so that I control my schedule.
- Only my free slots can be booked.
- I can confirm or decline a request.
- A Zoom link is created when I confirm.

### Mentor

**US-13 — Offer mentoring sessions** (Should)
As a mentor, I want to publish my free time and set sessions as free or paid so that students can get advice from me.
- I can mark each offer as free or paid with a price.
- The same booking flow as tutors applies.
- Confirmed sessions get a Zoom link.

### Admin

**US-14 — Approve content** (Must)
As an admin, I want to approve courses so that only good-quality courses are public.
- I see a list of courses waiting for approval.
- Approving makes a course visible; rejecting keeps it hidden.

**US-15 — Verify tutors and mentors** (Must)
As an admin, I want to verify tutors and mentors so that students can trust them.
- I can mark a profile as verified or rejected.
- Verification status is visible to students.

**US-16 — Handle reports** (Could)
As an admin, I want to review user reports so that I can remove abusive content or users.
- I can see the report details and the reported item.
- I can deactivate a user or remove content.

## 4. Non-functional requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-PERF-01 | Performance | Pages load in under 3 seconds on a normal connection. |
| NFR-PERF-02 | Performance | API responses take under 500 ms for normal requests. |
| NFR-SEC-01 | Security | No critical OWASP Top 10 issues. |
| NFR-SEC-02 | Security | Passwords are hashed; secrets live only in environment variables, never in the repository. |
| NFR-SEC-03 | Security | Role-based access is enforced on every endpoint. |
| NFR-SEC-04 | Security | Paid media is served only after an enrolment check. |
| NFR-USE-01 | Usability | Task completion rate of at least 90% in user testing. |
| NFR-USE-02 | Usability | SUS score of at least 70 (testing with at least 15 users). |
| NFR-USE-03 | Usability | The interface is available in English and Uzbek. |
| NFR-AVL-01 | Availability | The system runs in Docker Compose on a DigitalOcean server and can be restarted with one command. |
| NFR-AVL-02 | Availability | The booking flow still works if Zoom or e-mail is temporarily unavailable (failures are logged and retried). |
| NFR-QLT-01 | Maintainability | Backend test coverage of at least 70%; CI runs PyTest on every push and pull request. |

## 5. Out of scope

- Our own video-calling system (Zoom is used instead).
- Native mobile apps (responsive web only).
- Real-money payouts to educators, tutors and mentors (payments are test mode only).
- Machine-learning recommendation models (matching is rule-based).
- Live chat.
