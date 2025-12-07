# ASTRA
*Automated Student Teamwork Regulating Assistant*

*This project is not an official Metropolia project and has been created as a test assignment.*

ASTRA is an experimental web application designed for Metropolia ICT students as a potential tool for understanding group-work patterns. It gathers metadata from GitHub, Metropolia GitLab, and Google Docs and builds a two-week snapshot of commit timing, edit activity, contributor patterns, and change volume. The system stores cached results for faster loading and uses an AI model to generate simple interpretations based on these metrics. ASTRA is a prototype exploring how student teams might view their workflow through clear statistics and lightweight AI insights and benefit from it.

**Click the image** to watch a short demo video about ASTRA on YouTube:

[![Watch the video](https://img.youtube.com/vi/QWlluvB91OI/maxresdefault.jpg?v=2)](https://www.youtube.com/watch?v=QWlluvB91OI)

## Foundation of the Project

Student project teams often face recurring patterns such as unclear structure, uneven visible contribution, fragmented tools, and limited feedback on how the work actually progresses.

ASTRA is an experiment designed to help teams notice these patterns by presenting a simple two-week picture of their activity across the tools they already use. The idea is not to judge performance, but to make the workflow easier to see and reflect on.

## Core Idea of the System

ASTRA combines three key components.

### 1. Basic Teamwork Model

ASTRA uses a simple conceptual model of healthy student collaboration as a reference when interpreting activity data (steady pacing, small steps, weekly visibility of work, active documentation).

### 2. Automated Data Collection

The system collects metadata and not file contents from tools students already use:
- GitHub / GitLab: commit timestamps, authors, change sizes, activity distribution
- Google Docs: revision history, edit activity, authorship
- Trello: planned future integration (not yet available)

### 3. AI-Based Interpretation

ASTRA produces:
- raw statistics for the last two weeks,
- an AI-generated summary describing pacing patterns, visible contribution shapes, and edit clusters,
- short recommendations grounded in the observed metrics.

(Reports refresh approximately once per hour or when integrations change.)

## User Workflow

1. Students sign in using a Google account.
2. One student creates a group and others join it.
3. The group connects selected repositories and documents.
4. ASTRA generates two reports:
    - Statistics report: raw metrics (commit rhythm, contributor activity, active hours, change volume, revision timeline).
    - AI analysis report: interpreted observations, strengths, risks, and small practical suggestions.
5. Reports update regularly based on new commits or document edits.

## Output Overview

Students can view:
- overall teamwork score with a short explanation,
- pacing, workload balance, and collaboration density scores,
- a short summary of visible workflow patterns,
- strengths and issues with simple explanations,
- recommendations with data-based reasoning,
- next steps (small actions the team can do quickly),
- risks and forecast (what may happen if current patterns continue),
- reflection prompts for individual or team use.

## Significance for Metropolia

ASTRA is designed as an experimental tool that may:
- show a simple two-week overview of how work appears across tools,
- make contributor patterns easier to see,
- provide lightweight AI-generated suggestions based on observable activity,
- support reflection in student teams,
- act as a small educational aid for noticing workflow habits through data rather than assumptions.

## Project setup
The installation instructions are split into two parts:
- backend/README.md - describes how to install and run the backend,
- frontend/README.md - describes how to install and run the frontend.

Please follow both guides to get the full system running locally.