# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

### Domain Selection

I chose the domain of **ASU Career Services and Career Development** because many students have questions about internships, jobs, career fairs, resume reviews, interview preparation, and campus employment opportunities.

This knowledge is valuable because the information is scattered across ASU websites, Handshake, event pages, Reddit discussions, LinkedIn posts, and student forums. While official websites provide resources, they often do not include real student experiences, tips, and common challenges.

A RAG system can bring together both official information and student experiences, making it easier for students to quickly find relevant and reliable career guidance.


---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #  | Source       | Description                                                                                | URL                                                                                             |
| -- | ------------ | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| 1  | Reddit r/ASU | Student discussion complaining about ASU Career Services effectiveness and support quality | https://www.reddit.com/r/ASU/comments/1mcqhu2/asu_career_services_is_a_joke/                    |
| 2  | Reddit r/ASU | Opinions on whether ASU career fairs are worth attending for internships and jobs          | https://www.reddit.com/r/ASU/comments/1n0vkp1/are_the_career_fairs_worth_it/                    |
| 3  | Reddit r/ASU | General discussion on ASU career fairs, recruiter presence, and student experiences        | https://www.reddit.com/r/ASU/comments/1p1k866/career_fairs_at_asu/                              |
| 4  | Reddit r/ASU | Humorous/frustrated student experience interacting with recruiters at career fairs         | https://www.reddit.com/r/ASU/comments/d66hlt/me_at_the_career_fair_having_to_interact_with/     |
| 5  | Reddit r/ASU | Internship search experiences and student strategies for securing opportunities            | https://www.reddit.com/r/ASU/comments/1scgauk/internships/                                      |
| 6  | Reddit r/ASU | Advice for attending career fairs as a computer science student with limited experience    | https://www.reddit.com/r/ASU/comments/ewbuxa/advice_for_the_career_fair_as_a_cs_student_with/   |
| 7  | Reddit r/ASU | Student questions and answers about preparing for career fairs                             | https://www.reddit.com/r/ASU/comments/7yyyiv/career_fair_questions/                             |
| 8  | Reddit r/ASU | Discussion on CS program outcomes and career opportunities at ASU                          | https://www.reddit.com/r/ASU/comments/uffmaf/cs_program_career_opportunities_and_quality/       |
| 9  | Reddit r/ASU | Debate on whether students with little experience can get internships/jobs                 | https://www.reddit.com/r/ASU/comments/5pw2ov/do_people_in_cs_withoutor_little_experience_get/   |
| 10 | Reddit r/ASU | Student feedback on receiving opportunities through Handshake                              | https://www.reddit.com/r/ASU/comments/1kwsaxg/people_on_handshake_sending_me_opportunities_but/ |
| 11 | Reddit r/ASU | Experiences using Handshake for internship applications and recruiter outreach             | https://www.reddit.com/r/ASU/comments/zbxqbm/has_anyone_utilized_the_handshake_application_any/ |
| 12 | Reddit r/ASU | Discussion about on-campus job availability and hiring process at ASU                      | https://www.reddit.com/r/ASU/comments/10djn8j/oncampus_jobs/                                    |
| 13 | Reddit r/ASU | Student experiences applying for on-campus jobs and response timelines                     | https://www.reddit.com/r/ASU/comments/1tntbho/asu_on_campus_job/                                |


---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 

**Overlap:**

**Reasoning:** 

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**