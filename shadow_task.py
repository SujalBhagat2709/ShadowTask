class ShadowTask:
    VALID_PRIORITIES = {
        "low",
        "medium",
        "high",
        "critical",
    }

    VALID_STATUSES = {
        "pending",
        "in_progress",
        "completed",
        "skipped",
    }

    def __init__(self):
        self.tasks = {}

    def create_task(
        self,
        task_id,
        title,
        description,
        owner,
        priority="medium",
    ):
        if not task_id:
            raise ValueError("Task ID cannot be empty.")

        if task_id in self.tasks:
            raise ValueError("Task ID already exists.")

        priority = priority.lower()

        if priority not in self.VALID_PRIORITIES:
            raise ValueError(
                "Priority must be low, medium, high, or critical."
            )

        self.tasks[task_id] = {
            "task_id": task_id,
            "title": title,
            "description": description,
            "owner": owner,
            "priority": priority,
            "status": "pending",
            "shadow_tasks": [],
        }

    def get_task(self, task_id):
        return self.tasks.get(task_id)

    def list_tasks(self):
        return list(self.tasks.values())

    def add_shadow_task(
        self,
        task_id,
        shadow_id,
        title,
        reason,
        owner,
        priority="medium",
        estimated_minutes=0,
    ):
        task = self._require_task(task_id)

        if not shadow_id:
            raise ValueError("Shadow task ID cannot be empty.")

        existing_ids = {
            shadow["shadow_id"]
            for shadow in task["shadow_tasks"]
        }

        if shadow_id in existing_ids:
            raise ValueError(
                "Shadow task ID already exists for this task."
            )

        priority = priority.lower()

        if priority not in self.VALID_PRIORITIES:
            raise ValueError(
                "Priority must be low, medium, high, or critical."
            )

        if estimated_minutes < 0:
            raise ValueError(
                "Estimated minutes cannot be negative."
            )

        task["shadow_tasks"].append(
            {
                "shadow_id": shadow_id,
                "title": title,
                "reason": reason,
                "owner": owner,
                "priority": priority,
                "status": "pending",
                "estimated_minutes": estimated_minutes,
            }
        )

    def update_task_status(self, task_id, status):
        task = self._require_task(task_id)

        status = status.lower()

        if status not in self.VALID_STATUSES:
            raise ValueError(
                "Status must be pending, in_progress, "
                "completed, or skipped."
            )

        task["status"] = status

    def update_shadow_status(
        self,
        task_id,
        shadow_id,
        status,
    ):
        task = self._require_task(task_id)

        status = status.lower()

        if status not in self.VALID_STATUSES:
            raise ValueError(
                "Status must be pending, in_progress, "
                "completed, or skipped."
            )

        shadow = self._find_shadow_task(
            task,
            shadow_id,
        )

        if shadow is None:
            raise ValueError(
                f"Shadow task '{shadow_id}' was not found."
            )

        shadow["status"] = status

    def get_shadow_tasks(self, task_id):
        task = self._require_task(task_id)

        return task["shadow_tasks"]

    def get_pending_shadow_tasks(self, task_id):
        shadow_tasks = self.get_shadow_tasks(task_id)

        return [
            shadow
            for shadow in shadow_tasks
            if shadow["status"] == "pending"
        ]

    def get_active_shadow_tasks(self, task_id):
        shadow_tasks = self.get_shadow_tasks(task_id)

        return [
            shadow
            for shadow in shadow_tasks
            if shadow["status"]
            in {"pending", "in_progress"}
        ]

    def get_completed_shadow_tasks(self, task_id):
        shadow_tasks = self.get_shadow_tasks(task_id)

        return [
            shadow
            for shadow in shadow_tasks
            if shadow["status"] == "completed"
        ]

    def get_shadow_count(self, task_id):
        return len(self.get_shadow_tasks(task_id))

    def get_completed_count(self, task_id):
        return len(
            self.get_completed_shadow_tasks(task_id)
        )

    def get_pending_count(self, task_id):
        return len(
            self.get_pending_shadow_tasks(task_id)
        )

    def get_shadow_effort(self, task_id):
        shadow_tasks = self.get_shadow_tasks(task_id)

        return sum(
            shadow["estimated_minutes"]
            for shadow in shadow_tasks
        )

    def get_completion_percentage(self, task_id):
        shadow_tasks = self.get_shadow_tasks(task_id)

        if not shadow_tasks:
            return 0

        completed = self.get_completed_count(task_id)

        return round(
            (completed / len(shadow_tasks)) * 100,
            2,
        )

    def get_priority_breakdown(self, task_id):
        shadow_tasks = self.get_shadow_tasks(task_id)

        breakdown = {
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0,
        }

        for shadow in shadow_tasks:
            breakdown[shadow["priority"]] += 1

        return breakdown

    def get_high_priority_shadow_tasks(self, task_id):
        shadow_tasks = self.get_shadow_tasks(task_id)

        return [
            shadow
            for shadow in shadow_tasks
            if shadow["priority"]
            in {"high", "critical"}
            and shadow["status"] != "completed"
        ]

    def get_shadow_intensity(self, task_id):
        task = self._require_task(task_id)

        count = len(task["shadow_tasks"])
        effort = self.get_shadow_effort(task_id)

        if count == 0:
            return "No Shadow Work"

        if count >= 6 or effort >= 240:
            return "Heavy Shadow Work"

        if count >= 4 or effort >= 120:
            return "Significant Shadow Work"

        if count >= 2 or effort >= 60:
            return "Moderate Shadow Work"

        return "Light Shadow Work"

    def get_hidden_effort_percentage(
        self,
        task_id,
        main_task_minutes,
    ):
        if main_task_minutes <= 0:
            raise ValueError(
                "Main task effort must be greater than zero."
            )

        shadow_effort = self.get_shadow_effort(task_id)

        return round(
            (shadow_effort / main_task_minutes) * 100,
            2,
        )

    def find_shadow_tasks_by_owner(
        self,
        task_id,
        owner,
    ):
        shadow_tasks = self.get_shadow_tasks(task_id)

        return [
            shadow
            for shadow in shadow_tasks
            if shadow["owner"].lower() == owner.lower()
        ]

    def find_shadow_tasks_by_reason(
        self,
        task_id,
        keyword,
    ):
        shadow_tasks = self.get_shadow_tasks(task_id)

        keyword = keyword.lower()

        return [
            shadow
            for shadow in shadow_tasks
            if keyword in shadow["reason"].lower()
            or keyword in shadow["title"].lower()
        ]

    def generate_recommendation(
        self,
        task_id,
        main_task_minutes=0,
    ):
        task = self._require_task(task_id)

        shadow_tasks = task["shadow_tasks"]

        if not shadow_tasks:
            return (
                "No shadow work has been identified yet. "
                "Consider checking what supporting actions become "
                "necessary when the main task is performed."
            )

        active = self.get_active_shadow_tasks(task_id)
        high_priority = self.get_high_priority_shadow_tasks(
            task_id
        )
        shadow_effort = self.get_shadow_effort(task_id)

        if main_task_minutes > 0:
            hidden_percentage = (
                self.get_hidden_effort_percentage(
                    task_id,
                    main_task_minutes,
                )
            )
        else:
            hidden_percentage = 0

        if high_priority:
            return (
                f"{len(high_priority)} high-priority shadow task(s) "
                "remain incomplete. Address these supporting tasks "
                "before considering the main task fully complete."
            )

        if (
            main_task_minutes > 0
            and hidden_percentage >= 50
        ):
            return (
                f"Shadow work represents {hidden_percentage}% of the "
                "main task's estimated effort. Consider explicitly "
                "planning these supporting activities instead of "
                "treating them as invisible work."
            )

        if len(active) >= 4:
            return (
                "A large amount of supporting work is still active. "
                "Review whether these activities should become "
                "formally assigned tasks."
            )

        if shadow_effort >= 120:
            return (
                f"{shadow_effort} minutes of supporting work have "
                "been identified. Include this effort in future "
                "planning and estimation."
            )

        return (
            "Shadow work has been identified. Keep these supporting "
            "activities visible so they are not overlooked."
        )

    def analyze(
        self,
        task_id,
        main_task_minutes=0,
    ):
        task = self._require_task(task_id)

        shadow_tasks = task["shadow_tasks"]

        hidden_percentage = None

        if main_task_minutes > 0:
            hidden_percentage = (
                self.get_hidden_effort_percentage(
                    task_id,
                    main_task_minutes,
                )
            )

        return {
            "task_id": task["task_id"],
            "title": task["title"],
            "main_status": task["status"],
            "shadow_count": len(shadow_tasks),
            "completed_shadow_tasks": self.get_completed_count(
                task_id
            ),
            "pending_shadow_tasks": self.get_pending_count(
                task_id
            ),
            "shadow_effort_minutes": self.get_shadow_effort(
                task_id
            ),
            "completion_percentage": self.get_completion_percentage(
                task_id
            ),
            "priority_breakdown": self.get_priority_breakdown(
                task_id
            ),
            "high_priority_open": len(
                self.get_high_priority_shadow_tasks(
                    task_id
                )
            ),
            "shadow_intensity": self.get_shadow_intensity(
                task_id
            ),
            "hidden_effort_percentage": hidden_percentage,
            "recommendation": self.generate_recommendation(
                task_id,
                main_task_minutes,
            ),
        }

    def display_analysis(
        self,
        task_id,
        main_task_minutes=0,
    ):
        analysis = self.analyze(
            task_id,
            main_task_minutes,
        )

        print("\n" + "=" * 60)
        print("SHADOW TASK ANALYSIS")
        print("=" * 60)

        print(f"Task ID              : {analysis['task_id']}")
        print(f"Title                : {analysis['title']}")
        print(f"Main Task Status     : {analysis['main_status']}")
        print(f"Shadow Tasks         : {analysis['shadow_count']}")
        print(
            f"Completed Shadow     : "
            f"{analysis['completed_shadow_tasks']}"
        )
        print(
            f"Pending Shadow       : "
            f"{analysis['pending_shadow_tasks']}"
        )
        print(
            f"Shadow Effort        : "
            f"{analysis['shadow_effort_minutes']} minutes"
        )
        print(
            f"Shadow Completion    : "
            f"{analysis['completion_percentage']}%"
        )
        print(
            f"High-Priority Open   : "
            f"{analysis['high_priority_open']}"
        )
        print(
            f"Shadow Intensity     : "
            f"{analysis['shadow_intensity']}"
        )

        if analysis["hidden_effort_percentage"] is not None:
            print(
                f"Hidden Effort        : "
                f"{analysis['hidden_effort_percentage']}%"
            )

        print("\nPriority Breakdown:")

        for priority, count in (
            analysis["priority_breakdown"].items()
        ):
            print(f"  {priority.title():<10}: {count}")

        print("\nRecommendation:")
        print(analysis["recommendation"])

    def _require_task(self, task_id):
        task = self.get_task(task_id)

        if task is None:
            raise ValueError(
                f"Task '{task_id}' was not found."
            )

        return task

    def _find_shadow_task(
        self,
        task,
        shadow_id,
    ):
        for shadow in task["shadow_tasks"]:
            if shadow["shadow_id"] == shadow_id:
                return shadow

        return None
