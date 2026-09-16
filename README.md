# ShadowTask

ShadowTask is a small Python OOP project that identifies **hidden supporting work** that appears as a consequence of completing a main task.

A task may look simple from the outside:

```text
Deploy Website
```

But completing it may silently create additional work:

```text
Deploy Website
      │
      ├── Update documentation
      ├── Notify support
      ├── Verify monitoring
      ├── Prepare rollback
      └── Update deployment records
```

These supporting activities are called **shadow tasks**.

The purpose of ShadowTask is to make this normally invisible work visible, measurable, and manageable.

---

## Project Structure

```text
ShadowTask/
│
├── shadow_task.py
├── shadow_task_studio.py
├── README.md
└── .gitignore
```

---

## The Problem

Traditional task lists usually contain only explicitly planned work.

For example:

```text
Task:
Launch New Website

Estimated effort:
120 minutes
```

But the actual work may become:

```text
Main Task
120 minutes

Shadow Work
├── Documentation       30 min
├── Team communication  15 min
├── Monitoring setup    45 min
├── Rollback preparation 30 min
└── Record updates      15 min
```

Actual supporting work:

```text
135 minutes
```

So the original task did not tell the complete story.

ShadowTask provides a way to explicitly model that hidden workload.

---

## Core Concept

The project separates:

```text
MAIN TASK
```

from:

```text
SHADOW TASKS
```

A shadow task is work that:

1. Was not originally represented as the main task.
2. Becomes necessary because of the main task.
3. Consumes time or resources.
4. May have its own owner, priority, and status.

---

## Example

Consider:

```text
Main Task:
Deploy Payment Service
```

Shadow tasks might include:

```text
ST-01 → Update deployment documentation
ST-02 → Inform customer support
ST-03 → Verify production monitoring
ST-04 → Prepare rollback procedure
ST-05 → Update release records
```

The system makes these activities visible instead of leaving them buried inside the original task.

---

## Key Features

### 1. Create Main Tasks

Each main task contains:

* Task ID
* Title
* Description
* Owner
* Priority
* Status

Example:

```text
Task ID: DEV-001
Title: Deploy Payment Service
Owner: Backend Team
Priority: High
Status: Pending
```

---

### 2. Add Shadow Tasks

Each shadow task contains:

* Shadow Task ID
* Title
* Reason
* Owner
* Priority
* Status
* Estimated effort

Example:

```text
Shadow ID:
ST-001

Title:
Update deployment documentation

Reason:
Deployment changes require the operational documentation
to be updated.

Owner:
DevOps Team

Effort:
30 minutes
```

---

## Why the "Reason" Matters

The project does not simply treat every subtask as a shadow task.

The system records **why the work exists**.

For example:

```text
Main Task:
Deploy API
```

Then:

```text
Shadow Task:
Notify Support

Reason:
Support needs to know about the API change
before customer issues are reported.
```

This creates a relationship between:

```text
Main Task
    ↓
Why it creates additional work
    ↓
Shadow Task
```

---

## Shadow Work Effort

The project calculates the estimated effort of all shadow tasks.

Example:

```text
Documentation       30 min
Monitoring          45 min
Communication       15 min
Rollback             30 min
-------------------------
Total Shadow Work  120 min
```

This helps reveal workload that may otherwise remain invisible.

---

## Hidden Effort Percentage

If the main task requires:

```text
120 minutes
```

and shadow tasks require:

```text
60 minutes
```

then:

```text
Hidden Effort = 50%
```

This gives a simple comparison between planned main work and supporting work.

It can help reveal tasks whose supporting workload is substantial relative to the original estimate.

---

## Shadow Completion

The system calculates how much of the shadow work has been completed.

Example:

```text
5 Shadow Tasks
3 Completed
```

Completion:

```text
60%
```

This allows users to see whether the main task's supporting work is keeping pace.

---

## Shadow Intensity

The project categorizes the amount of shadow work as:

```text
No Shadow Work
Light Shadow Work
Moderate Shadow Work
Significant Shadow Work
Heavy Shadow Work
```

The classification considers:

* Number of shadow tasks
* Estimated supporting effort

This gives a quick indication of how much invisible work surrounds the main task.

---

## Priority Handling

Shadow tasks can have:

```text
Low
Medium
High
Critical
```

High and critical unfinished shadow tasks can be surfaced separately.

Example:

```text
High Priority
Prepare rollback procedure
Status: Pending
```

This prevents important supporting work from being overlooked simply because it isn't the main task.

---

## Shadow Task Status

Both main tasks and shadow tasks can have:

```text
Pending
In Progress
Completed
Skipped
```

This allows the project to track the lifecycle of supporting work.

---

## Recommendations

The system generates recommendations based on the amount and state of shadow work.

For example:

```text
A large amount of supporting work is still active.
Review whether these activities should become formally
assigned tasks.
```

If hidden effort is large:

```text
Shadow work represents 60% of the main task's estimated
effort. Consider explicitly planning these supporting
activities instead of treating them as invisible work.
```

The recommendation is intended as a planning signal rather than an automatic decision.

---

## Interactive Studio

The second file provides a command-line interface.

```text
============================================================
                 SHADOW TASK STUDIO
============================================================
1. Create Main Task
2. Add Shadow Task
3. Update Main Task Status
4. Update Shadow Task Status
5. View All Tasks
6. View Task Details
7. Analyze Task
8. Show Recommendation
9. Find Shadow Tasks by Owner
10. Exit
```

The Studio handles interaction while the `ShadowTask` class handles the underlying logic.

---

## Example Workflow

### Step 1 — Create Main Task

```text
Task ID: REL-001
Title: Launch Website
Description: Deploy the new website to production
Owner: Development Team
Priority: High
```

### Step 2 — Add Shadow Work

```text
ST-001
Title: Update documentation
Reason: Release changes require documentation updates
Owner: Documentation Team
Effort: 30 minutes
```

```text
ST-002
Title: Notify support
Reason: Support needs release information
Owner: Support Team
Effort: 15 minutes
```

```text
ST-003
Title: Verify monitoring
Reason: New deployment requires monitoring verification
Owner: DevOps Team
Effort: 45 minutes
```

### Step 3 — Analyze

The system can report:

```text
Shadow Tasks         : 3
Completed Shadow     : 0
Pending Shadow       : 3
Shadow Effort        : 90 minutes
Shadow Completion    : 0%
Shadow Intensity     : Moderate Shadow Work
```

If the main task was estimated at 120 minutes:

```text
Hidden Effort: 75%
```

That reveals something important:

```text
Planned Main Work
       120 min
          +
Supporting Work
        90 min
          ↓
Actual workload is substantially larger
than the original main-task estimate.
```

---

## OOP Concepts Used

### Class

The core implementation uses:

```python
class ShadowTask:
```

### Encapsulation

Task data and shadow-work calculations are maintained inside the class.

### Methods

Important methods include:

```python
create_task()
add_shadow_task()
update_task_status()
update_shadow_status()
get_shadow_tasks()
get_pending_shadow_tasks()
get_completed_shadow_tasks()
get_shadow_effort()
get_completion_percentage()
get_priority_breakdown()
get_high_priority_shadow_tasks()
get_shadow_intensity()
get_hidden_effort_percentage()
generate_recommendation()
analyze()
```

### Data Structures

The project uses:

* Dictionaries
* Lists
* Sets

to maintain tasks and their associated shadow work.

---

## File Responsibilities

### `shadow_task.py`

Contains the core OOP logic.

It handles:

* Main task creation
* Shadow task creation
* Status updates
* Shadow effort calculation
* Completion calculation
* Priority analysis
* Hidden effort calculation
* Shadow intensity
* Recommendations

### `shadow_task_studio.py`

Contains the interactive CLI.

It allows users to:

* Create tasks
* Add hidden work
* Update statuses
* View details
* Analyze workload
* View recommendations

---

## How to Run

Make sure Python is installed.

Run:

```bash
python shadow_task_studio.py
```

No external packages are required.

---

## Real-World Use Cases

ShadowTask can be used for:

### Software Development

```text
Feature Development
      ↓
Documentation
Testing
Deployment
Monitoring
Communication
```

### IT Operations

```text
Server Change
      ↓
Backup
Notification
Monitoring
Rollback preparation
Documentation
```

### Business Operations

```text
New Process
      ↓
Training
Documentation
Communication
Approval
Reporting
```

### Event Planning

```text
Organize Event
      ↓
Venue coordination
Invitations
Equipment
Staff communication
Cleanup
```

---

## Why This Project Is Different

Most task applications focus on:

```text
"What tasks do we have?"
```

ShadowTask asks a different question:

```text
"What additional work appears because
we are doing this task?"
```

That distinction is the main idea behind the project.

It models:

```text
Planned Work
     ↓
Consequences of Planned Work
     ↓
Hidden Supporting Work
     ↓
Actual Workload
```

---

## Future AI Enhancement

The current system requires users to manually identify shadow tasks.

An AI-enhanced version could automatically discover them.

For example:

```text
Main Task:
"Deploy a new payment service"
```

An AI system could suggest:

```text
Possible Shadow Tasks:

✓ Update deployment documentation
✓ Verify monitoring
✓ Notify support
✓ Prepare rollback
✓ Update service inventory
✓ Validate alerts
```

It could also analyze historical projects and learn that certain types of main tasks consistently create similar supporting work.

This would turn ShadowTask into an intelligent **hidden-work discovery system**.

---

## Technologies

* Python
* Object-Oriented Programming
* Dictionaries
* Lists
* Sets
* Command-Line Interface

No external dependencies are required.

---

## License

This project is available for learning, portfolio, and personal development purposes.
