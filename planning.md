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

**Chunk size: 200 tokens** 

**Overlap: 30 tokens**

**Reasoning:** I will use fixed-size chunking with overlap because the Reddit discussions contain comments of different lengths. Some comments are short, while others are much longer. A chunk size of 300 tokens will help keep related information together, and a 50-token overlap will help preserve context between chunks. This approach will improve retrieval accuracy and reduce the chance of losing important information when the text is split into multiple chunks.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 (Sentence Transformers)

**Top-k:** 5

**Production tradeoff reflection:** I will use the all-MiniLM-L6-v2 embedding model because it is free, open-source, lightweight, and performs well for semantic search tasks. I will retrieve the top 5 most relevant chunks for each query. If I were deploying this system for real users, I would compare different open-source embedding models based on retrieval accuracy, speed, context understanding, multilingual support, and hardware requirements before selecting the final model.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about the usefulness of ASU career fairs? | Students generally say career fairs help with networking, meeting recruiters, practicing interviews, and sometimes obtaining internships or jobs. |
| 2 | What do students think about ASU Career Services? | Students have mixed opinions. Some feel Career Services provides limited help, while others believe it offers guidance but cannot directly create job opportunities. |
| 3 | Is Handshake useful for finding internships and jobs? | Students report both positive and negative experiences. Some found internships and jobs through Handshake, while others received irrelevant job recommendations or few responses. |
| 4 | What advice do students give for finding on-campus jobs? | Students recommend tailoring resumes and cover letters, following application instructions carefully, networking with staff and professors, and applying consistently. |
| 5 | What strategies do students recommend for improving internship and job opportunities? | Students recommend attending career fairs, building projects, networking with recruiters, applying early, gaining research experience, and improving resumes and interview skills. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->


1. The discussions contain noisy data such as advertisements, deleted comments, usernames, and Reddit interface text. This may reduce retrieval quality if irrelevant content is retrieved.

2. Similar topics appear across multiple discussions. For example, career fairs, internships, and Handshake are discussed repeatedly. This may cause the system to retrieve overlapping or repetitive information instead of the most relevant answer.

3. Important information may be split across multiple chunks. If related comments are separated during chunking, the retrieved answer may miss important context.

4. Some discussions contain personal opinions that may conflict with each other. The system may retrieve different viewpoints for the same question, making it difficult to generate a single clear answer.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

Document Ingestion -> Chunking -> Embedding + Vector Store -> Retrieval -> Generation

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


I will use Claude Code to help build the pipeline.

- For document ingestion and cleaning, I will give Claude Code the project requirements, the Architecture section, and the file format. I will ask it to write Python code for loading and cleaning the discussion files. I will verify the output by checking that all discussion files are loaded correctly and that the text matches the source data.

- For chunking, I will give Claude Code my Chunking Strategy section and ask it to implement fixed-size chunking with a chunk size of 300 tokens and an overlap of 50 tokens. I will verify the output by checking the chunk sizes and making sure the context is preserved.

- For embeddings and vector storage, I will give Claude Code my Retrieval Approach section and ask it to use a free embedding model such as BAAI/bge-small-en-v1.5. I will verify the output by checking that the embeddings are created and stored correctly.

- For retrieval and generation, I will give Claude Code my Evaluation Plan and Architecture section and ask it to implement top-k retrieval with k = 5. I will verify the output by testing the system with my evaluation questions and checking whether the answers match the expected answers.

- For debugging, I will use Claude Code to fix errors and improve the code. I will verify each change by running the pipeline again and checking that it still follows my project requirements.

**Milestone 3 — Ingestion and chunking:**
total chunks =105

**Milestone 4 — Embedding and retrieval:**

============================================================
Top 5 results for: "What do students say about the usefulness of ASU career fairs?"
============================================================

  [1] similarity=0.6853  distance=0.3147  |  discussion2.txt + discussion3.txt  |  chunk_index=19  |  200 tokens
I go to school online and won’t be able to attend the career fairs in-person.

Prestigious_View_401
9mo ago
Yes

Hefty-Revenue5547
9mo ago
Yes have gotten multiple interviews and offers from them

Best-Law5722
9mo ago
Finance ‘25 (undergraduate)

burnt_books
9mo ago
I got my first internship at the career fair! You've got this

Career fairs at ASU
Has anyone ever actually benefited from an ASU career fair? I have never heard a single positive thing about it. Does anyone else feel the same way?

wardevil345
7mo ago
It’s fun to go but for me it didn’t really benefit me just a bunch of free stuff

Brilliant-Bottle-413
7mo ago
I’ve been to most of the career fairs starting my sophomore year. Most of the time they just tell you to apply online after talking to them. I want to say I only got like 2-3

  [2] similarity=0.6576  distance=0.3424  |  discussion3.txt  |  chunk_index=21  |  200 tokens
nor what positions they were hiring for. They told me about their company and then said to look online for job openings

The employers had NOTHING to do with my degree/career objectives - even though the job fair ads said jobs for all majors. I do not want to work for solar companies, teach for america, or home health care, or sell insurance lol

So, no - I have never benefited from an ASU career fair. But I recommend that you go to at least one so you can have your own experience - and hopefully you will have a better experience than I have.

Commercial_Amoeba669
OP
7mo ago
Unfortunately I have been to over 5 of them and I had the worst experience.

Pure-Try-9434
7mo ago
I was able to get both my offers this year indirectly from going to SCMA career fairs and networking. I cannot speak to how other career fairs will benefit but for supply chain, it definitely helps. It doesn’t hurt to build

  [3] similarity=0.5650  distance=0.4350  |  discussion3.txt  |  chunk_index=23  |  200 tokens
of them even getting a job.

TexturedClouds03
7mo ago
I think it can be helpful, especially if you’re outgoing and can make a good impressions in person. If you have relevant qualifications or can relate to the recruiters you talk to I think it can get you opportunities you prolly wouldn’t otherwise.

Ok-Cost-5079
7mo ago
CS '24
I was able to get an internship offer at a relatively large company because of the career fair. I had already applied prior to attending the career fair but it wasn’t going anywhere. After speaking to the recruiter, my resume got passed to the technical/behavioral stage, so I do think it helps. Regardless, I have found it a good place to get advice from recruiters as well as to build up confidence by pitching yourself if you need that

LowerSlowerOlder
7mo ago
I’d like to answer as someone who volunteers at an ASU career fair every year. If you

  [4] similarity=0.5496  distance=0.4504  |  discussion3.txt  |  chunk_index=20  |  200 tokens
sophomore year. Most of the time they just tell you to apply online after talking to them. I want to say I only got like 2-3 interviews out of all the career fairs I went to. I got more interviews from just applying online, but I would recommend still going and trying because it does increase your odds of a job/internship.

Whole_Bid_360
7mo ago
I went to the fulton one this september and I got a job from an employer that I met at the career fair. It is not useless but it is not guaranteed.

Constant_Minimum_569
7mo ago
I ended up getting my first job at the CAVC career fair.

CynicalSunDevil
7mo ago
With every ASU and MCCC career fair I have attended, I have experienced either:

The people at the table could not tell me salary nor what positions they were hiring for. They told me about their company and then said to look online for job openings

The employers had NOTHING to do with

  [5] similarity=0.5421  distance=0.4579  |  discussion5.txt  |  chunk_index=34  |  200 tokens
2mo ago
MechE ‘27 (undergraduate)
Honestly you gotta be proactive in your sophomore year. You likely wont get an internship before your junior year, but any connections you make before the fall hiring season are more valuable than connections you make during the hiring season.

Ready_Youth249
2mo ago
Networking is alright. Though you won’t be pushed, you have to take the initiative yourself. Career Fairs are more like marketing events by companies to market their organisation. ASU is a pretty diverse university so you won’t have any issues adjusting and you’ll be more than happy being an international student here.

MousseStandard4471
OP
2mo ago
People on this thread are at a completely different viewpoint, whats the state of CS there gng😭😭

Ready_Youth249
2mo ago
Too many enrolments and not half as many opportunities as enrolments. Make of that what you will.

StepLucky9830
2mo ago
Much like

============================================================
Top 5 results for: "What do students say about the usefulness of ASU career fairs?"
============================================================

  [1] similarity=0.6853  distance=0.3147  |  discussion2.txt + discussion3.txt  |  chunk_index=19  |  200 tokens
I go to school online and won’t be able to attend the career fairs in-person.

Prestigious_View_401
9mo ago
Yes

Hefty-Revenue5547
9mo ago
Yes have gotten multiple interviews and offers from them

Best-Law5722
9mo ago
Finance ‘25 (undergraduate)

burnt_books
9mo ago
I got my first internship at the career fair! You've got this

Career fairs at ASU
Has anyone ever actually benefited from an ASU career fair? I have never heard a single positive thing about it. Does anyone else feel the same way?

wardevil345
7mo ago
It’s fun to go but for me it didn’t really benefit me just a bunch of free stuff

Brilliant-Bottle-413
7mo ago
I’ve been to most of the career fairs starting my sophomore year. Most of the time they just tell you to apply online after talking to them. I want to say I only got like 2-3

  [2] similarity=0.6576  distance=0.3424  |  discussion3.txt  |  chunk_index=21  |  200 tokens
nor what positions they were hiring for. They told me about their company and then said to look online for job openings

The employers had NOTHING to do with my degree/career objectives - even though the job fair ads said jobs for all majors. I do not want to work for solar companies, teach for america, or home health care, or sell insurance lol

So, no - I have never benefited from an ASU career fair. But I recommend that you go to at least one so you can have your own experience - and hopefully you will have a better experience than I have.

Commercial_Amoeba669
OP
7mo ago
Unfortunately I have been to over 5 of them and I had the worst experience.

Pure-Try-9434
7mo ago
I was able to get both my offers this year indirectly from going to SCMA career fairs and networking. I cannot speak to how other career fairs will benefit but for supply chain, it definitely helps. It doesn’t hurt to build

  [3] similarity=0.5650  distance=0.4350  |  discussion3.txt  |  chunk_index=23  |  200 tokens
of them even getting a job.

TexturedClouds03
7mo ago
I think it can be helpful, especially if you’re outgoing and can make a good impressions in person. If you have relevant qualifications or can relate to the recruiters you talk to I think it can get you opportunities you prolly wouldn’t otherwise.

Ok-Cost-5079
7mo ago
CS '24
I was able to get an internship offer at a relatively large company because of the career fair. I had already applied prior to attending the career fair but it wasn’t going anywhere. After speaking to the recruiter, my resume got passed to the technical/behavioral stage, so I do think it helps. Regardless, I have found it a good place to get advice from recruiters as well as to build up confidence by pitching yourself if you need that

LowerSlowerOlder
7mo ago
I’d like to answer as someone who volunteers at an ASU career fair every year. If you

  [4] similarity=0.5496  distance=0.4504  |  discussion3.txt  |  chunk_index=20  |  200 tokens
sophomore year. Most of the time they just tell you to apply online after talking to them. I want to say I only got like 2-3 interviews out of all the career fairs I went to. I got more interviews from just applying online, but I would recommend still going and trying because it does increase your odds of a job/internship.

Whole_Bid_360
7mo ago
I went to the fulton one this september and I got a job from an employer that I met at the career fair. It is not useless but it is not guaranteed.

Constant_Minimum_569
7mo ago
I ended up getting my first job at the CAVC career fair.

CynicalSunDevil
7mo ago
With every ASU and MCCC career fair I have attended, I have experienced either:

The people at the table could not tell me salary nor what positions they were hiring for. They told me about their company and then said to look online for job openings

The employers had NOTHING to do with

  [5] similarity=0.5421  distance=0.4579  |  discussion5.txt  |  chunk_index=34  |  200 tokens
2mo ago
MechE ‘27 (undergraduate)
Honestly you gotta be proactive in your sophomore year. You likely wont get an internship before your junior year, but any connections you make before the fall hiring season are more valuable than connections you make during the hiring season.

Ready_Youth249
2mo ago
Networking is alright. Though you won’t be pushed, you have to take the initiative yourself. Career Fairs are more like marketing events by companies to market their organisation. ASU is a pretty diverse university so you won’t have any issues adjusting and you’ll be more than happy being an international student here.

MousseStandard4471
OP
2mo ago
People on this thread are at a completely different viewpoint, whats the state of CS there gng😭😭

Ready_Youth249
2mo ago
Too many enrolments and not half as many opportunities as enrolments. Make of that what you will.

StepLucky9830
2mo ago
Much like

Query: Is Handshake useful for finding internships and jobs?

============================================================
Top 5 results for: "Is Handshake useful for finding internships and jobs?"
============================================================

  [1] similarity=0.7216  distance=0.2784  |  discussion11.txt  |  chunk_index=71  |  200 tokens
dope. im in asu and i look forward to using handshake when i finish school

z123killer
4y ago
Yes got my first and second internship from there, also discovered a lot of companies that I didn't know about from Handshake.

adventureincalm
4y ago
I haven't messed with it too much because I work full-time to help pay for school, but I did get an internship last summer on Handshake.

AgentButteryNipp
3y ago
Lowkey after years and years of jobs and meeting people's the only handshake I've given was through meme'ing. (I mean why wouldnt you shake a hand firmly when offered?) Ok sure id introduce myself, but the majority of interviews would be me enthusiastic to work or looking forward to new opportunities. Greetings are one thing, who you know is another. First impressions can be everything, but how hard or soft your grip a

  [2] similarity=0.5284  distance=0.4716  |  discussion11.txt  |  chunk_index=70  |  200 tokens
has specific “school recruiting” postings that end up having less competition or being favored compared to normal postings, not sure though

No-Struggle8021
OP
4y ago
Nice. By any chance are you an online student

SmokeySpace
4y ago
I am not, I don’t see that having much of an effect though, is there a place in handshake to put whether you are online or not?

No-Struggle8021
OP
4y ago
You may be correct but I'm trying to configure access ATM for handshake but I'm waiting on support. I've heard that opportunities are slim if you're online

mcTankin
4y ago
computer science '21 (undergraduate)
I got my job first job out of college using handshake.

[deleted]
2y ago
thats dope. im in asu and i look forward to using handshake when i finish school

z123killer
4y ago
Yes got

  [3] similarity=0.4934  distance=0.5066  |  discussion10.txt + discussion11.txt  |  chunk_index=69  |  200 tokens
hidden. I checked it and there's really nothing useful on there. I explained to my professor that I couldn't mark myself as wanting a job because my current employer may not like me posting that (they probably wouldn't care) but they told me to just take a picture of it "public" then hide it again for the coursework is fine.

Fatun3rd
1y ago
Yeah, sales positions are 80% of the messages that I get as well.

TerribleInvite1978
OP
1y ago
Sometimes its legit messages inviting me to apply

has anyone utilized the HANDSHAKE application any success ?

[deleted]
4y ago
SmokeySpace
4y ago
I got an interview off handshake last year (I only applied to a couple places so that’s not too bad) I think handshake has specific “school recruiting” postings that end up having less competition or being favored compared to normal postings, not sure though

No-Struggle80

  [4] similarity=0.4481  distance=0.5519  |  discussion6.txt  |  chunk_index=46  |  200 tokens
apply, this is your last chance to get an internship before graduation. Apply to 100+ companies on Handshake before mid-February. Have you installed Handshake?

And whatever you do, don't give up or lose hope. That's when you have lost. I didn't get my junior year internship until March and a friend didn't get theirs until early May. Not over till it's over.

civ10
OP
6y ago
Computer Science (Software Engineering)
Yeah I have an up to date linked in and handshake with work experience, overview, resume, skills etc. I applied to about 20 company’s in mid December, but stopped after being out of town then starting up classes. I wanted to overhaul my resume and prepare myself more before applying anywhere else.

Catradorra
6y ago
That's great, just be careful about overpreparing and underapplying - a lot of people make the mistake of waiting too long

  [5] similarity=0.3915  distance=0.6085  |  discussion7.txt  |  chunk_index=50  |  200 tokens
in case you find something else interesting.

Depends. If you make a good impression,  you could spend several minutes chatting with them. The company I got hired by I spent talking to for 15 minutes at their booth.

Go as soon as it starts. However, something I did was go to booths that weren't my top choices first. I did this as a warm up to get rid of my nervousness and felt more comfortable when I did talk to my top choices.

Ask about what kind of work interns do. What's their company culture? What would you do on a daily basis? Any questions that show you're interested about the job AND their company.

These are just my opinions, but this is what I did when I got my internship and job offer.

Good luck tomorrow! It's better to try even if you think you're not ready.

RickMuffy
8y ago
Aerospace BSE - 2016
I will be there tomorrow looking to hire two interns for

============================================================
Top 5 results for: "What strategies do students recommend for improving internship and job opportunities?"
============================================================

  [1] similarity=0.5666  distance=0.4334  |  discussion5.txt  |  chunk_index=33  |  200 tokens
mo ago
MechE ‘27 (undergraduate)
Apply to internships. It’s like finding a job: you search online for “[field] internship”.

darnclem
2mo ago
I'll also throw in that pretty much every school at every university will have some kind of career placement office of some kind that should be helping with things like internships.

MousseStandard4471
OP
2mo ago
Worldly-Awareness-88
2mo ago
Getting an internship is more on you if anything. My best advice is to be proactive your fall semester as a junior. For context, I'm a CS Major and I got a internship at a well-known company just because I was one of the first people to apply. Career fairs are useful if you do your research beforehand.

Ray_RG_YT
2mo ago
MechE ‘27 (undergraduate)
Honestly you gotta be proactive in your sophomore year. You likely wont get an internship before your

  [2] similarity=0.5373  distance=0.4627  |  discussion6.txt  |  chunk_index=46  |  200 tokens
apply, this is your last chance to get an internship before graduation. Apply to 100+ companies on Handshake before mid-February. Have you installed Handshake?

And whatever you do, don't give up or lose hope. That's when you have lost. I didn't get my junior year internship until March and a friend didn't get theirs until early May. Not over till it's over.

civ10
OP
6y ago
Computer Science (Software Engineering)
Yeah I have an up to date linked in and handshake with work experience, overview, resume, skills etc. I applied to about 20 company’s in mid December, but stopped after being out of town then starting up classes. I wanted to overhaul my resume and prepare myself more before applying anywhere else.

Catradorra
6y ago
That's great, just be careful about overpreparing and underapplying - a lot of people make the mistake of waiting too long

  [3] similarity=0.5199  distance=0.4801  |  discussion6.txt  |  chunk_index=45  |  200 tokens
your speech and get the nerves off

ask your favorite companies what they look for in resumes and what type of projects/knowledge would impress them

don’t apply to internships this semester (cause if you do and get rejected, which most likely you will without experience, most companies won’t consider you for another year)

work on a big personal project that you can show the recruiters @next semesters career fair. Then apply then

IMO, I’ve never seen a CS student get an internship without having some project experience.

civ10
OP
6y ago
Computer Science (Software Engineering)
I have two summers left in my undergraduate. It seems counterproductive to not attempt to get an internship this summer. I mean even making a small project to have something seems better than not trying at all.

Catradorra
6y ago
Absolutely apply, this is your last chance to get an internship before graduation. Apply to 100+ companies on Handshake before mid-February. Have you

  [4] similarity=0.5053  distance=0.4947  |  discussion6.txt  |  chunk_index=41  |  200 tokens
tutorial to really help flex your programming brain. I have a internship right now and I have another one in the summer with a different company, be able to talk about your projects and make sure they're interesting and cool and talk about how you went about your implementations and the roadblocks you encountered and how you overcame them. This is important to show you are willing to learn quickly and know how to implement "google foo".

Also you will probably blow in your first few interviews.. I know I did. Look up S.T.A.R. for behavioral and look at leetcode easy for technical practice

GOOD LUCK

civ10
OP
6y ago
Computer Science (Software Engineering)
Thanks!

chilldemon
6y ago
Make sure to use a bunch of tech jargon and buzzwords on your resume but be careful not to paint a dishonest representation of your skills. I would say aim for mild over-exaggeration at best. Then at the career fair

  [5] similarity=0.5008  distance=0.4992  |  discussion7.txt  |  chunk_index=52  |  200 tokens
looking for similar qualities.

[deleted]
8y ago
Cognitive_Miser
8y ago
Not in the CS field but I feel these still apply to anyone and any major:

Don't just ask generic questions like what interns do or what the company culture is like. Everyone asks those and believe me, after you get asked that question the first 3 times it gets old, real quick.

Try to think outside of the norm and ask genuine questions that are of actual interest to you. A good way to break the ice and show your interest across to a potential employer is to ask about their story, how they got to where they are at and tie their responses back in to your experiences and what you want to accomplish. A good follow up question would be to ask if they have any advice or what they would do differently if they were back in your shoes.

After your interactions always ask for a business card or contact information if they do not have one. Within 24-48 hours, send them


**Milestone 5 — Generation and interface:**