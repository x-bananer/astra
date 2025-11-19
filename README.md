# ASTRA
*Automated Student Teamwork Regulating Assistant*

ASTRA is an AI-driven system that supports Metropolia IT students in organizing their group work, understanding participation patterns, and strengthening collaboration through structured guidance and reflective feedback.

## Foundation of the Project

Group work in small teams of three to five students is an essential part of Metropolia IT study programs. However, when organizing group work, students regularly face recurring challenges.

- **Lack of information and structure**
    
    In groups, students often do not share a common understanding of how to define tasks, record decisions, or maintain a consistent workflow.

- **Uneven contribution**
    
    Some students naturally take on more tasks while others may  have fewer opportunities to contribute, and without structured reflection these patterns can remain unclear to the group.

- **Fragmented tools**
    
    For carrying out group assignments, students usually use several platforms such as GitHub or GitLab, Trello, and Google Docs. Due to the tools being used separately, the group has limited visibility into how their work aligns, fits together and progresses.

- **No feedback on workflow**
    
    Both instructor feedback and internal retrospectives usually focus on the final result rather than the process that led to it. Students rarely receive guidance on how to improve the workflow itself.

ASTRA is designed to address these issues.

## Core Idea of the System

ASTRA combines three key components.

### Structured Teamwork Model

The system provides a simple and universal approach for student projects.

- formulating tasks and breaking them into smaller units  
- tracking progress of the group
- maintaining transparency and a predictable rhythm of work  

This model serves as a reference point for evaluating the actual work of each group.

### Automated Data Collection

ASTRA draws on information from the tools students already use to help the group reflect on their workflow and improve their collaboration.

- GitHub or GitLab: commits, pull requests, merge requests,activity patterns  
- Trello: task movement, deadlines, participant activity  
- Google Docs: revisions, authorship changes, documentdevelopment  

Access is limited to the materials explicitly provided by the group.

### AI Based Analysis and Recommendations

Based on the collected data ASTRA provides the group with the following.

**Statistics**  
- an overview of how the group’s work is distributed  
- indicators of workflow pacing  

**Process Insight**  
- signs of inconsistent pacing  
- patterns that may slow down task progression

**Recommendations**  
- short practical suggestions that help the group strengthen their workflow based on observed patterns.

## User Workflow

**1. Registration**

    Students sign in through a Metropolia Google account ifpossible or another OAuth method.

**2. Creating a Group Workspace**

    One student creates a group and invites the others.

**3. Connecting Tools**

The group adds links to documents and tools from which theywant to receive analytics:
- repository in GitLab or GitHub  
- Trello board  
- documents such as Google Docs via share or OAuth and Microsoft Office files  

**4. Initial Analysis**

ASTRA generates a basic reflective report on the current state of the project.

**5. Regular Updates**

The system periodically collects new data such as commits,board changes, and document revisions to update reflectivereports.

**6. Group Dashboard**

Students see the following:
- contribution dynamics
- activity graphs  
- current issues
- recommendations for process improvement  

**7. Instructor Report (optional)**

The group may generate a short factual report about their collaboration.

## Reference Model of Group Work

TODO: идеальная модель, эталон

## Significance for Metropolia

ASTRA helps to do the following.

- enhance the effectiveness and clarity of group work  
- support the development of teamwork skills relevant toindustry  
- highlight areas where the workflow could be strengthened  
- support students in developing practical skills forstructured and collaborative project work