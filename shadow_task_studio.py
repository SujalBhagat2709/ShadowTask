from shadow_task import ShadowTask


def print_task(task):
    print("\n" + "-" * 60)
    print(f"Task ID       : {task['task_id']}")
    print(f"Title         : {task['title']}")
    print(f"Description   : {task['description']}")
    print(f"Owner         : {task['owner']}")
    print(f"Priority      : {task['priority']}")
    print(f"Status        : {task['status']}")
    print(f"Shadow Tasks  : {len(task['shadow_tasks'])}")
    print("-" * 60)


def create_task(system):
    print("\n=== Create Main Task ===")

    task_id = input("Task ID: ").strip()
    title = input("Title: ").strip()
    description = input("Description: ").strip()
    owner = input("Owner: ").strip()

    priority = (
        input(
            "Priority (low/medium/high/critical): "
        )
        .strip()
        .lower()
    )

    try:
        system.create_task(
            task_id=task_id,
            title=title,
            description=description,
            owner=owner,
            priority=priority,
        )

        print("\nMain task created successfully.")

    except ValueError as error:
        print(f"\nError: {error}")


def add_shadow_task(system):
    print("\n=== Add Shadow Task ===")

    task_id = input("Main Task ID: ").strip()
    shadow_id = input("Shadow Task ID: ").strip()
    title = input("Shadow task title: ").strip()
    reason = input(
        "Why does this hidden work become necessary? "
    ).strip()
    owner = input("Owner: ").strip()

    priority = (
        input(
            "Priority (low/medium/high/critical): "
        )
        .strip()
        .lower()
    )

    effort_input = input(
        "Estimated effort (minutes): "
    ).strip()

    try:
        estimated_minutes = float(effort_input)

        system.add_shadow_task(
            task_id=task_id,
            shadow_id=shadow_id,
            title=title,
            reason=reason,
            owner=owner,
            priority=priority,
            estimated_minutes=estimated_minutes,
        )

        print("\nShadow task added successfully.")

    except ValueError as error:
        print(f"\nError: {error}")


def update_main_status(system):
    print("\n=== Update Main Task Status ===")

    task_id = input("Task ID: ").strip()

    status = (
        input(
            "Status "
            "(pending/in_progress/completed/skipped): "
        )
        .strip()
        .lower()
    )

    try:
        system.update_task_status(
            task_id,
            status,
        )

        print("\nMain task status updated.")

    except ValueError as error:
        print(f"\nError: {error}")


def update_shadow_status(system):
    print("\n=== Update Shadow Task Status ===")

    task_id = input("Main Task ID: ").strip()
    shadow_id = input("Shadow Task ID: ").strip()

    status = (
        input(
            "Status "
            "(pending/in_progress/completed/skipped): "
        )
        .strip()
        .lower()
    )

    try:
        system.update_shadow_status(
            task_id,
            shadow_id,
            status,
        )

        print("\nShadow task status updated.")

    except ValueError as error:
        print(f"\nError: {error}")


def show_all_tasks(system):
    tasks = system.list_tasks()

    print("\n=== All Main Tasks ===")

    if not tasks:
        print("No tasks recorded.")
        return

    for task in tasks:
        print_task(task)


def show_task_details(system):
    task_id = input("\nEnter Task ID: ").strip()

    try:
        task = system.get_task(task_id)

        if task is None:
            raise ValueError(
                f"Task '{task_id}' was not found."
            )

        print_task(task)

        print("\nShadow Tasks:")

        if not task["shadow_tasks"]:
            print("  No shadow work recorded.")
            return

        for shadow in task["shadow_tasks"]:
            print("\n  " + "-" * 45)
            print(
                f"  Shadow ID   : "
                f"{shadow['shadow_id']}"
            )
            print(
                f"  Title       : "
                f"{shadow['title']}"
            )
            print(
                f"  Reason      : "
                f"{shadow['reason']}"
            )
            print(
                f"  Owner       : "
                f"{shadow['owner']}"
            )
            print(
                f"  Priority    : "
                f"{shadow['priority']}"
            )
            print(
                f"  Status      : "
                f"{shadow['status']}"
            )
            print(
                f"  Effort      : "
                f"{shadow['estimated_minutes']} minutes"
            )

    except ValueError as error:
        print(f"\nError: {error}")


def analyze_task(system):
    task_id = input("\nEnter Task ID: ").strip()

    main_effort_input = input(
        "Estimated main task effort in minutes "
        "(optional, press Enter to skip): "
    ).strip()

    try:
        if main_effort_input:
            main_effort = float(main_effort_input)
        else:
            main_effort = 0

        system.display_analysis(
            task_id,
            main_effort,
        )

    except ValueError as error:
        print(f"\nError: {error}")


def show_recommendation(system):
    task_id = input("\nEnter Task ID: ").strip()

    main_effort_input = input(
        "Main task effort in minutes "
        "(optional, press Enter to skip): "
    ).strip()

    try:
        if main_effort_input:
            main_effort = float(main_effort_input)
        else:
            main_effort = 0

        print("\n=== Recommendation ===")

        print(
            system.generate_recommendation(
                task_id,
                main_effort,
            )
        )

    except ValueError as error:
        print(f"\nError: {error}")


def find_by_owner(system):
    task_id = input("\nEnter Main Task ID: ").strip()
    owner = input("Owner name: ").strip()

    try:
        results = system.find_shadow_tasks_by_owner(
            task_id,
            owner,
        )

        print("\n=== Shadow Tasks by Owner ===")

        if not results:
            print("No matching shadow tasks found.")
            return

        for shadow in results:
            print(
                f"{shadow['shadow_id']} | "
                f"{shadow['title']} | "
                f"{shadow['status']} | "
                f"{shadow['estimated_minutes']} min"
            )

    except ValueError as error:
        print(f"\nError: {error}")


def main():
    system = ShadowTask()

    while True:
        print("\n" + "=" * 60)
        print("                 SHADOW TASK STUDIO")
        print("=" * 60)

        print("1. Create Main Task")
        print("2. Add Shadow Task")
        print("3. Update Main Task Status")
        print("4. Update Shadow Task Status")
        print("5. View All Tasks")
        print("6. View Task Details")
        print("7. Analyze Task")
        print("8. Show Recommendation")
        print("9. Find Shadow Tasks by Owner")
        print("10. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            create_task(system)

        elif choice == "2":
            add_shadow_task(system)

        elif choice == "3":
            update_main_status(system)

        elif choice == "4":
            update_shadow_status(system)

        elif choice == "5":
            show_all_tasks(system)

        elif choice == "6":
            show_task_details(system)

        elif choice == "7":
            analyze_task(system)

        elif choice == "8":
            show_recommendation(system)

        elif choice == "9":
            find_by_owner(system)

        elif choice == "10":
            print(
                "\nExiting Shadow Task Studio. Goodbye!"
            )
            break

        else:
            print(
                "\nInvalid choice. Please select 1-10."
            )


if __name__ == "__main__":
    main()
