#!/usr/bin/env python3
"""
Demo script showing how to integrate with Claude Task Monitor

This simulates a long-running task that updates its status periodically.
Run this while the monitor is running to see it in action.
"""

import json
import time
from pathlib import Path
from datetime import datetime, timezone


def update_task_status(
    task_name: str,
    status: str,
    progress_percent: int = None,
    current_step: str = None,
    message: str = None,
    needs_attention: bool = False,
    status_file: Path = Path.home() / '.claude' / 'monitor' / 'demo.json'
):
    """Update Claude task monitoring status file."""
    # Ensure directory exists
    status_file.parent.mkdir(parents=True, exist_ok=True)

    data = {
        'task_name': task_name,
        'status': status,
        'updated_at': datetime.now(timezone.utc).isoformat()
    }

    if progress_percent is not None:
        data['progress_percent'] = progress_percent
    if current_step:
        data['current_step'] = current_step
    if message:
        data['message'] = message
    if needs_attention:
        data['needs_attention'] = needs_attention

    with open(status_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"[{status}] {task_name}: {current_step or message or ''}")


def demo_simple_task():
    """Demo a simple task with progress"""
    print("\n=== Demo: Simple Task ===\n")

    # Start
    update_task_status(
        task_name="Processing Dataset",
        status="pending",
        message="Initializing..."
    )
    time.sleep(2)

    # In progress
    for i in range(0, 101, 10):
        update_task_status(
            task_name="Processing Dataset",
            status="in_progress",
            progress_percent=i,
            current_step=f"Processing batch {i//10 + 1}/11"
        )
        time.sleep(1)

    # Complete
    update_task_status(
        task_name="Processing Dataset",
        status="completed",
        progress_percent=100,
        message="Processed 10,000 records"
    )
    time.sleep(2)


def demo_task_with_error():
    """Demo a task that encounters an error"""
    print("\n=== Demo: Task with Error ===\n")

    # Start
    update_task_status(
        task_name="Downloading Large File",
        status="in_progress",
        progress_percent=0,
        current_step="Connecting to server..."
    )
    time.sleep(2)

    # Progress
    for i in range(0, 60, 20):
        update_task_status(
            task_name="Downloading Large File",
            status="in_progress",
            progress_percent=i,
            current_step=f"Downloaded {i}%"
        )
        time.sleep(2)

    # Error!
    update_task_status(
        task_name="Downloading Large File",
        status="error",
        progress_percent=60,
        message="Connection timeout",
        needs_attention=True
    )
    print("\n⚠️  Task encountered an error and needs attention!")
    print("Check the monitor to see the alert.")
    time.sleep(5)


def demo_blocked_task():
    """Demo a task that gets blocked and needs user input"""
    print("\n=== Demo: Blocked Task ===\n")

    # Start
    update_task_status(
        task_name="Database Migration",
        status="in_progress",
        progress_percent=0,
        current_step="Analyzing schema..."
    )
    time.sleep(2)

    # Progress
    for i in range(0, 60, 20):
        update_task_status(
            task_name="Database Migration",
            status="in_progress",
            progress_percent=i,
            current_step=f"Migrating table {i//20 + 1}/4"
        )
        time.sleep(2)

    # Blocked
    update_task_status(
        task_name="Database Migration",
        status="blocked",
        progress_percent=50,
        message="Conflict in migration 0042 - manual intervention needed",
        needs_attention=True
    )
    print("\n⚠️  Task is blocked and needs your attention!")
    print("Simulating user resolving the issue...")
    time.sleep(5)

    # Resume
    update_task_status(
        task_name="Database Migration",
        status="in_progress",
        progress_percent=60,
        current_step="Resuming migration..."
    )
    time.sleep(2)

    # Complete
    for i in range(60, 101, 20):
        update_task_status(
            task_name="Database Migration",
            status="in_progress",
            progress_percent=i,
            current_step=f"Migrating table {i//20 + 1}/4"
        )
        time.sleep(2)

    update_task_status(
        task_name="Database Migration",
        status="completed",
        progress_percent=100,
        message="Successfully migrated all tables"
    )
    time.sleep(2)


def main():
    print("=" * 60)
    print("Claude Task Monitor - Demo")
    print("=" * 60)
    print("\nThis script will simulate various task scenarios.")
    print("Start the monitor in another terminal to see the updates:")
    print("  ./run_monitor.sh")
    print("\nPress Ctrl+C to stop at any time.\n")

    try:
        # Run demos
        demo_simple_task()
        demo_task_with_error()
        # Don't run blocked demo by default since it needs attention
        # demo_blocked_task()

        print("\n" + "=" * 60)
        print("Demo complete!")
        print("=" * 60)
        print("\nThe status file will remain until deleted.")
        print("Delete it with: rm ~/.claude-monitor/demo.json")

    except KeyboardInterrupt:
        print("\n\nDemo stopped.")
        update_task_status(
            task_name="Demo Task",
            status="completed",
            message="Interrupted by user"
        )


if __name__ == "__main__":
    main()
