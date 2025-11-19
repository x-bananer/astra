# ASTRA

Automated Student Teamwork Regulating Assistant

ASTRA is an AI-driven system for structured analysis, organization, and improvement of student teamwork for Metropolia students.It helps Metropolia students organize group work, analyze individual contributions, and improve the quality of collaboration through AI supported structure and feedback.

## Foundation of the Project

Group work in small teams of three to five students is an essential part of Metropolia study programs. Students and instructors regularly face several recurring challenges.

• Lack of structure  
Students often do not share a common understanding of how to define tasks, record decisions, or maintain a consistent workflow.

• Uneven contribution  
Some members perform most of the work while others contribute only minimally. This imbalance is difficult to detect within the group and even harder for instructors to evaluate fairly.

• Fragmented tools  
Students use several platforms such as GitHub or GitLab, Trello, and Google Docs. Information is scattered and there is no unified picture of the process.

• No feedback on workflow  
Both instructor feedback and internal retrospectives usually focus on the final result rather than the process that led to it. Students rarely receive guidance on how to improve the workflow itself.

ASTRA is designed to address these issues.

## Core Idea of the System

ASTRA combines three key components.

### Structured Teamwork Model

The system provides a simple and universal approach for student projects.

• formulating tasks and breaking them into smaller units  
• tracking progress of the group and of each participant  
• analysing task ownership and responsibility distribution  
• maintaining transparency and a predictable rhythm of work  

This model serves as a reference point for evaluating the actual work of each group.

### Automated Data Collection

ASTRA collects data from the tools students already use for organizing project work and completing assignments.

• GitHub or GitLab: commits, pull requests, merge requests, activity patterns  
• Trello: task movement, deadlines, participant activity  
• Google Docs: revisions, authorship changes, document development  

Access is limited to the materials explicitly provided by the group.

### AI Based Analysis and Recommendations

Based on the collected data ASTRA provides the group with the following.

**Statistics**  
• contribution and activity of each member  
• stability and pacing of the workflow  
• balance between individual and shared work  

**Problem Identification**  
• contribution imbalance  
• irregular or unstable workflow  
• delays in task completion  
• insufficient documentation  

**Recommendations**  
Short practical suggestions generated from the observed patterns of the group.

Example recommendations  
• Establish a weekly routine of small, clearly defined tasks and update them regularly  
• Keep shared documents up to date during the work instead of summarizing everything at the end  
• Split tasks that stay in progress for too long into smaller units to avoid blocking the workflow  
• Adjust task distribution when one member repeatedly becomes a bottleneck  

## User Workflow

### 1. Registration

Students sign in through a Metropolia Google account if possible or another OAuth method.

### 2. Creating a Group Workspace

One student creates a group and invites the others.

### 3. Connecting Tools

The group adds links to documents and tools from which they want to receive analytics.

• repository in GitLab or GitHub  
• Trello board  
• documents such as Google Docs via share or OAuth and Microsoft Office files  

Each participant grants access only to the files they own.

### 4. Initial Analysis

ASTRA generates a basic report on the current state of the project including contribution, task structure, and documentation.

### 5. Regular Updates

The system periodically collects new data such as commits, board changes, and document revisions.

### 6. Group Dashboard

Students see the following.

• contribution dynamics  
• activity graphs  
• current issues  
• recommendations for process improvement  

### 7. Instructor Report (optional)

The group may generate a short factual report about their collaboration.

## Reference Model of Group Work

This section requires further development. It will contain detailed technical criteria that describe the expected structure, pacing, and collaboration principles used by ASTRA as a reference for evaluating group work.

## Significance for Metropolia

ASTRA helps to do the following.

• improve the quality of group projects  
• support the development of teamwork skills relevant to industry  
• optionally provide instructors with objective data about the group workflow  
• ensure transparency of individual contributions  
• identify problems early during the project  
• teach students essential principles of organized group work  