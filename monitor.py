#!/usr/bin/env python3
"""
Claude Task Monitor - General-purpose monitor for Claude Code task status across projects

Watches for JSON breadcrumb files dropped by Claude Code sessions and displays
their status in a live-updating terminal interface.

Usage:
    python3 monitor.py                    # Watch default locations
    python3 monitor.py --watch ~/projects # Watch specific directory tree
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.console import Group
from rich.text import Text

console = Console()


class TaskStatus:
    """Represents a single Claude task from a breadcrumb file"""

    def __init__(self, project_path: Path, data: Dict[str, Any]):
        self.project_path = project_path
        self.project_name = project_path.name
        self.data = data
        self.file_mtime = None

    @property
    def task_name(self) -> str:
        return self.data.get('task_name', 'Unnamed Task')

    @property
    def status(self) -> str:
        """Current status: pending, in_progress, blocked, completed, error"""
        return self.data.get('status', 'unknown')

    @property
    def progress_percent(self) -> Optional[int]:
        return self.data.get('progress_percent')

    @property
    def current_step(self) -> Optional[str]:
        return self.data.get('current_step')

    @property
    def message(self) -> Optional[str]:
        return self.data.get('message')

    @property
    def tiny_title(self) -> Optional[str]:
        """Optional short title for tiny display mode"""
        return self.data.get('tiny_title')

    @property
    def needs_attention(self) -> bool:
        return self.data.get('needs_attention', False)

    @property
    def updated_at(self) -> Optional[str]:
        return self.data.get('updated_at')

    @property
    def age_seconds(self) -> Optional[float]:
        """How old is this breadcrumb?"""
        if not self.file_mtime:
            return None
        return time.time() - self.file_mtime

    def get_emoji(self) -> str:
        """Get status emoji"""
        emoji_map = {
            'pending': '⏳',
            'in_progress': '🔄',
            'blocked': '⚠️',
            'completed': '✅',
            'error': '❌',
            'waiting': '⏸️',
            'unknown': '❓'
        }
        return emoji_map.get(self.status, '❓')

    def get_color(self) -> str:
        """Get status color for rich formatting"""
        color_map = {
            'pending': 'yellow',
            'in_progress': 'cyan',
            'blocked': 'red',
            'completed': 'green',
            'error': 'red',
            'waiting': 'dim',
            'unknown': 'dim'
        }
        return color_map.get(self.status, 'white')


class ClaudeMonitor:
    """Monitors Claude task breadcrumbs across projects"""

    def __init__(self, watch_paths: List[Path], breadcrumb_filename: str = '.claude_task.json'):
        self.watch_paths = watch_paths
        self.breadcrumb_filename = breadcrumb_filename
        self.tasks: Dict[str, TaskStatus] = {}  # project_path -> TaskStatus

    def scan_for_breadcrumbs(self):
        """Scan watch paths for breadcrumb files"""
        found_tasks = {}

        for watch_path in self.watch_paths:
            if not watch_path.exists():
                continue

            # Look for breadcrumb files - handle both patterns and specific filenames
            if '*' in self.breadcrumb_filename:
                # Pattern matching (e.g., *.json)
                breadcrumb_files = watch_path.glob(self.breadcrumb_filename)
            else:
                # Specific filename with recursive search
                breadcrumb_files = watch_path.rglob(self.breadcrumb_filename)

            for breadcrumb_file in breadcrumb_files:
                try:
                    # Extract project name from filename (remove extension)
                    # e.g., "home_assistant.json" -> "home_assistant"
                    project_name = breadcrumb_file.stem

                    mtime = breadcrumb_file.stat().st_mtime

                    # Only load if file was modified in last 24 hours
                    age = time.time() - mtime
                    if age > 86400:  # 24 hours
                        continue

                    with open(breadcrumb_file, 'r') as f:
                        data = json.load(f)

                    # Create a pseudo-path object with the project name
                    pseudo_path = Path(project_name)
                    task = TaskStatus(pseudo_path, data)
                    task.file_mtime = mtime
                    found_tasks[str(breadcrumb_file)] = task

                except (json.JSONDecodeError, OSError) as e:
                    # Skip malformed or inaccessible files
                    pass

        self.tasks = found_tasks

    def get_active_tasks(self) -> List[TaskStatus]:
        """Get tasks that are not completed, sorted by priority"""
        active = []
        for t in self.tasks.values():
            if t.status == 'completed':
                continue

            # Filter out stale tasks based on status
            if t.age_seconds is not None:
                # Error/blocked tasks: show for 1 hour
                if t.status in ('error', 'blocked') and t.age_seconds > 3600:
                    continue
                # Other active tasks: show for 10 minutes
                if t.status in ('in_progress', 'pending', 'waiting') and t.age_seconds > 600:
                    continue

            active.append(t)

        # Sort: needs_attention first, then by status priority, then by age
        status_priority = {
            'blocked': 0,
            'error': 1,
            'waiting': 2,
            'in_progress': 3,
            'pending': 4,
            'unknown': 5
        }

        def sort_key(task: TaskStatus):
            return (
                not task.needs_attention,  # needs_attention first (False < True)
                status_priority.get(task.status, 99),
                task.age_seconds or 0
            )

        active.sort(key=sort_key)
        return active

    def get_completed_tasks(self) -> List[TaskStatus]:
        """Get recently completed tasks"""
        completed = []
        for t in self.tasks.values():
            if t.status == 'completed':
                # Only show completed tasks from last 30 minutes
                if t.age_seconds is None or t.age_seconds <= 1800:
                    completed.append(t)

        completed.sort(key=lambda t: t.file_mtime or 0, reverse=True)
        return completed[:10]  # Show last 10 completed


def create_task_table(tasks: List[TaskStatus], title: str) -> Table:
    """Create a rich table for tasks"""
    table = Table(title=title, show_header=True, border_style="cyan", expand=True, show_lines=True)
    table.add_column("Status", width=10)
    table.add_column("Project", style="cyan", width=20)
    table.add_column("Task", style="white", no_wrap=False)
    table.add_column("Progress", width=25)
    table.add_column("Updated", width=12, style="dim")

    for task in tasks:
        # Status with emoji only
        status_text = task.get_emoji()

        # Project name
        project_name = task.project_name

        # Task name with current step and message
        task_desc = f"[bold]{task.task_name}[/bold]"
        if task.current_step:
            task_desc += f"\n[dim]{task.current_step}[/dim]"
        if task.message and task.message != task.current_step:
            task_desc += f"\n[italic]{task.message}[/italic]"

        # Progress indicator
        progress = ""
        if task.progress_percent is not None:
            bar_length = 20
            filled = int(bar_length * task.progress_percent / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            progress = f"[{task.get_color()}]{bar}[/{task.get_color()}]\n{task.progress_percent}%"
        elif task.message:
            progress = f"[dim]{task.message}[/dim]"

        # Time since update
        if task.age_seconds is not None:
            if task.age_seconds < 60:
                time_str = f"{int(task.age_seconds)}s ago"
            elif task.age_seconds < 3600:
                time_str = f"{int(task.age_seconds/60)}m ago"
            else:
                time_str = f"{int(task.age_seconds/3600)}h ago"
        else:
            time_str = ""

        # Highlight if needs attention
        row_style = "bold red" if task.needs_attention else None

        table.add_row(
            status_text,
            project_name,
            task_desc,
            progress,
            time_str,
            style=row_style
        )

    return table


def create_summary_panel(monitor: ClaudeMonitor) -> Panel:
    """Create summary statistics panel"""
    total = len(monitor.tasks)
    active = len(monitor.get_active_tasks())
    completed = len([t for t in monitor.tasks.values() if t.status == 'completed'])
    needs_attention = len([t for t in monitor.tasks.values() if t.needs_attention])

    summary_text = (
        f"[cyan]Total Tasks:[/cyan] {total}  "
        f"[yellow]Active:[/yellow] {active}  "
        f"[green]Completed:[/green] {completed}  "
    )
    if needs_attention > 0:
        summary_text += f"[red bold]⚠️  Needs Attention:[/red bold] {needs_attention}"

    return Panel(summary_text, title="📊 Claude Task Monitor", border_style="cyan bold", expand=True)


def format_time_ago(age_seconds: Optional[float]) -> str:
    """Format age in seconds to human-readable time ago string"""
    if age_seconds is None:
        return ""
    if age_seconds < 60:
        return f"{int(age_seconds)}s ago"
    elif age_seconds < 3600:
        return f"{int(age_seconds/60)}m ago"
    else:
        return f"{int(age_seconds/3600)}h ago"


def create_active_tasks_tiny(active_tasks: List[TaskStatus]) -> Table:
    """Tiny mode: Compact view with small progress bar, optimized for tiny screens"""
    table = Table(title="🔄 Active Tasks", show_header=True, border_style="yellow", expand=True, show_lines=True)
    table.add_column("Status", width=8)
    table.add_column("Project/Task", style="cyan", width=18)
    table.add_column("Details", style="white", no_wrap=False)
    table.add_column("Progress", width=12)
    table.add_column("Updated", width=10, style="dim")

    for task in active_tasks:
        status_text = task.get_emoji()

        # Use tiny_title if available, otherwise project name
        project_task = task.tiny_title or task.project_name

        # Task details: name, current step, and message
        task_details = f"[bold]{task.task_name}[/bold]"
        if task.current_step:
            task_details += f"\n[dim]{task.current_step}[/dim]"
        if task.message and task.message != task.current_step:
            task_details += f"\n[italic dim]{task.message}[/italic dim]"

        # Smaller progress bar (8 chars instead of 20)
        progress = ""
        if task.progress_percent is not None:
            bar_length = 8
            filled = int(bar_length * task.progress_percent / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            progress = f"[{task.get_color()}]{bar}[/{task.get_color()}]\n{task.progress_percent}%"
        elif task.current_step:
            # Show current step in progress column if no percentage
            progress = f"[dim]{task.current_step[:20]}[/dim]"

        row_style = "bold red" if task.needs_attention else None
        table.add_row(
            status_text,
            project_task,
            task_details,
            progress,
            format_time_ago(task.age_seconds),
            style=row_style
        )

    return table


def create_active_tasks_small(active_tasks: List[TaskStatus]) -> Table:
    """Small mode: Status + Project + Task + Current Step + Updated"""
    table = Table(title="🔄 Active Tasks", show_header=True, border_style="yellow", expand=True, show_lines=True)
    table.add_column("Status", width=8)
    table.add_column("Project", style="cyan", width=20)
    table.add_column("Task", style="white")
    table.add_column("Current Step", style="dim")
    table.add_column("Updated", width=12, style="dim")

    for t in active_tasks:
        step_info = t.current_step or t.message or ""
        row_style = "bold red" if t.needs_attention else None

        table.add_row(
            t.get_emoji(),
            t.project_name,
            t.task_name,
            step_info,
            format_time_ago(t.age_seconds),
            style=row_style
        )

    return table


def create_active_tasks_medium(active_tasks: List[TaskStatus]) -> Table:
    """Medium mode: Add Message column separate from Current Step"""
    table = Table(title="🔄 Active Tasks", show_header=True, border_style="yellow", expand=True, show_lines=True)
    table.add_column("Status", width=8)
    table.add_column("Project", style="cyan", width=18)
    table.add_column("Task", style="white", width=25)
    table.add_column("Current Step", style="dim", width=25)
    table.add_column("Message", style="italic dim", width=25)
    table.add_column("Updated", width=12, style="dim")

    for t in active_tasks:
        row_style = "bold red" if t.needs_attention else None

        table.add_row(
            t.get_emoji(),
            t.project_name,
            t.task_name,
            t.current_step or "",
            t.message or "",
            format_time_ago(t.age_seconds),
            style=row_style
        )

    return table


def create_active_tasks_large(active_tasks: List[TaskStatus]) -> Table:
    """Large mode: All fields including progress percentage"""
    table = Table(title="🔄 Active Tasks", show_header=True, border_style="yellow", expand=True, show_lines=True)
    table.add_column("Status", width=8)
    table.add_column("Project", style="cyan", width=18)
    table.add_column("Task", style="white", width=25)
    table.add_column("Current Step", style="dim", width=25)
    table.add_column("Message", style="italic dim", width=25)
    table.add_column("Progress", width=8, justify="right")
    table.add_column("Updated", width=12, style="dim")

    for t in active_tasks:
        row_style = "bold red" if t.needs_attention else None
        progress_str = f"{t.progress_percent}%" if t.progress_percent is not None else ""

        table.add_row(
            t.get_emoji(),
            t.project_name,
            t.task_name,
            t.current_step or "",
            t.message or "",
            progress_str,
            format_time_ago(t.age_seconds),
            style=row_style
        )

    return table


def create_display(monitor: ClaudeMonitor, size: str = "small") -> Group:
    """Create the full display layout

    Args:
        monitor: ClaudeMonitor instance
        size: Display size mode - 'tiny', 'small', 'medium', or 'large'
    """
    components = []

    # Summary panel
    components.append(create_summary_panel(monitor))

    # Active tasks table (size-dependent)
    active_tasks = monitor.get_active_tasks()
    if active_tasks:
        if size == "tiny":
            components.append(create_active_tasks_tiny(active_tasks))
        elif size == "small":
            components.append(create_active_tasks_small(active_tasks))
        elif size == "medium":
            components.append(create_active_tasks_medium(active_tasks))
        elif size == "large":
            components.append(create_active_tasks_large(active_tasks))
        else:
            # Default to small
            components.append(create_active_tasks_small(active_tasks))
    else:
        components.append(Panel(
            "[green]No active tasks - all quiet! 🎉[/green]",
            border_style="green",
            expand=True
        ))

    # Recently completed tasks (expanded view)
    completed_tasks = monitor.get_completed_tasks()
    if completed_tasks:
        completed_table = Table(title="✅ Recently Completed", show_header=True, border_style="green", expand=True)
        completed_table.add_column("Project", style="cyan", width=20)
        completed_table.add_column("Task", style="white")
        completed_table.add_column("Message", style="dim")
        completed_table.add_column("Completed", width=12, style="dim")

        for t in completed_tasks[:10]:  # Show up to 10 completed tasks
            if t.age_seconds is not None:
                if t.age_seconds < 60:
                    time_str = f"{int(t.age_seconds)}s ago"
                elif t.age_seconds < 3600:
                    time_str = f"{int(t.age_seconds/60)}m ago"
                else:
                    time_str = f"{int(t.age_seconds/3600)}h ago"
            else:
                time_str = ""

            completed_table.add_row(
                t.project_name,
                t.task_name,
                t.message or "",
                time_str
            )

        components.append(completed_table)

    return Group(*components)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Monitor Claude Code tasks across projects")
    parser.add_argument(
        '--watch',
        nargs='+',
        default=['~/.claude-monitor'],
        help='Directories to watch for task breadcrumbs (default: ~/.claude-monitor)'
    )
    parser.add_argument(
        '--interval',
        type=float,
        default=2.0,
        help='Update interval in seconds (default: 2.0)'
    )
    parser.add_argument(
        '--breadcrumb',
        default='*.json',
        help='Breadcrumb filename pattern to look for (default: *.json)'
    )
    parser.add_argument(
        '--size',
        choices=['tiny', 'small', 'medium', 'large'],
        default='tiny',
        help='Display size mode: tiny (compact with progress bar), small (clean columns), medium (separate step/message), large (all fields)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Show startup info (watching paths, breadcrumb pattern, display size)'
    )

    args = parser.parse_args()

    # Expand paths
    watch_paths = [Path(p).expanduser().resolve() for p in args.watch]

    # Only show startup info in debug mode
    if args.debug:
        console.print("[cyan]🔍 Claude Task Monitor[/cyan]\n")
        console.print(f"[dim]Watching: {', '.join(str(p) for p in watch_paths)}[/dim]")
        console.print(f"[dim]Looking for: {args.breadcrumb}[/dim]")
        console.print(f"[dim]Display size: {args.size}[/dim]\n")

    monitor = ClaudeMonitor(watch_paths, args.breadcrumb)

    try:
        with Live(console=console, refresh_per_second=1/args.interval) as live:
            while True:
                monitor.scan_for_breadcrumbs()
                display = create_display(monitor, size=args.size)
                live.update(display)
                time.sleep(args.interval)

    except KeyboardInterrupt:
        console.print("\n[yellow]Monitor stopped[/yellow]")
        return 0


if __name__ == "__main__":
    sys.exit(main())
