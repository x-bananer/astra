# ASTRA
*Automated Student Teamwork Regulating Assistant*

**Click the image** to watch a short demo video about ASTRA on YouTube:

[![Watch the video](https://img.youtube.com/vi/QWlluvB91OI/maxresdefault.jpg?v=2)](https://www.youtube.com/watch?v=QWlluvB91OI)

*This project is not an official Metropolia project and has been created as a test assignment.*

ASTRA is a small experimental web application designed for Metropolia ICT students as a potential tool for improving group-work awareness. It gathers metadata from a group’s GitHub, Metropolia GitLab, and Google Docs and builds a two-week snapshot of commit timing, edit activity, contributor patterns, and change volume. The system stores cached results for faster access and uses an AI model to interpret these metrics and produce short, data-based observations. ASTRA is intended as a way to explore how student teams might view their workflow through clear statistics and simple AI-generated insights.

## Foundation of the Project

Group work in small teams of three to five students is an essential part of Metropolia ICT study programs. However, when organizing group work, students regularly face recurring challenges.

- **Lack of information and structure**

- **Uneven contribution**

- **Fragmented tools**

- **Limited feedback on workflow**

ASTRA is designed to address these issues.

## Core Idea of the System

ASTRA combines three key components.

### 1. Structured Teamwork Model

ASTRA uses a simple conceptual model of healthy student teamwork as a reference point for interpreting real activity data.
This model describes desirable patterns such as:
- steady and predictable work rhythm,
- breaking work into small steps,
- visible weekly contribution from team members,
- keeping documentation active.

### 2. Automated Data Collection

ASTRA collects metadata from the tools students already use in their team work to help teams reflect on how their work unfolds:
- GitHub / GitLab: commit timestamps, authors, change sizes, contribution volume, active hours
- Google Docs: revision timeline, authorship changes, edit activity
- Trello: planned future integration (not yet available)

### 3. AI Based Analysis and Recommendations

Based on the collected data ASTRA provides the group with the following.

**Statistics**

Astra computes raw metrics for the last two weeks, including:
• commit distribution by day and hour
• contributor activity and change volume
• average and largest commit sizes
• Google Docs revision timeline and edit activity
(Statistics refresh at least once per hour or immediately when integrations change.)

**AI Analysis**

The AI layer interprets these metrics and highlights:
• pacing patterns (steady, bursty, quiet periods)
• uneven contribution signals
• unusually large or infrequent commits
• notable document activity gaps or clusters
(Analysis refreshes at least once per hour or immediately when integrations change.)

**Recommendations**

Based on the interpreted patterns, Astra generates:
• short practical suggestions to improve pacing
• tips on splitting work into smaller steps
• suggestions on maintaining clearer documentation flow

## User Workflow

1. Students sign in to the ASTRA website using a Google account.

2. One student creates a group and invites the others.

3. The group adds links to documents and tools.

4. ASTRA generates two types of reports and saves them in the database.
- Statistics report - raw computed metrics for the last two weeks (commit rhythm, contributor activity, active hours, commit sizes, document revision activity).
- AI analysis report - an interpreted summary with strengths, risks, pacing observations, and practical recommendations based on the statistical data.

5. The system collects new data such as commits,board changes, and document revisions to update reports at least once an hour or upon request.

## Output

Students get the following:
- overall score of teamwork quality with a short explanation of what data patterns shaped this evaluation,
- consistency score with an explanation of how steady the team's pacing appears,
- workload balance score showing how visible work is distributed across contributors,
- pacing score describing the rhythm of work across days and hours,
- task completion ratio score reflecting how tasks tend to progress over time,
- collaboration density score describing how many contributors appear active in the provided data,
- summary providing a short overview of the team’s workflow patterns,
- strengths listing positive patterns with explanations of why they matter for teamwork,
- issues describing observable workflow risks with explanations,
- recommendations giving short, actionable suggestions grounded in data,
- next steps offering 1–2 concrete actions the team can do in 5–15 minutes,
- risks outlining possible outcomes if current patterns continue, with data references,
- forecast giving a short prediction of how the workflow may develop,
- reflection prompts providing questions for individual or team self-reflection.

## Significance for Metropolia

ASTRA is designed as a tool that may:

- show and analyse a team’s working rhythm over a two-week period,
- make contributor patterns more visible through raw statistics and AI-generated summaries,
- provide short data-based recommendations grounded in observable patterns,
- support light team reflection through generated strengths, risks, forecasts and prompts,
- act as a small educational aid that helps students notice workflow habits through data rather than assumptions.