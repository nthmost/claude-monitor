# Claude Task Monitor

## Project Overview

This is a general-purpose monitoring tool for tracking Claude Code task progress across multiple projects. It provides a live terminal interface that displays task status, progress, and alerts from any project that drops status breadcrumb files.

## Key Components

- **monitor.py**: Main monitoring script with Rich-based terminal UI
- **demo_task.py**: Demo script showing example task status updates
- **spaceteam_demo.py**: Fun Spaceteam-style chaos demo with technobabble commands
- **CLAUDE_MD_TEMPLATE.md**: Template for integrating monitoring into other projects
- **run_monitor.sh**: Convenience script for launching the monitor
- **run_demo.sh**: Script to run the demo task

## Architecture

### How It Works

1. Projects drop JSON status files in `~/.claude-monitor/` using unique filenames (e.g., `project_name.json`)
2. The monitor scans this directory for `*.json` files at regular intervals (default: 2 seconds)
3. Status information is displayed in a live-updating terminal UI
4. Stale tasks are automatically filtered based on status and age:
   - Active tasks (`in_progress`, `pending`, `waiting`): Hidden after 10 minutes of inactivity
   - Error/blocked tasks: Hidden after 1 hour
   - Completed tasks: Hidden after 30 minutes
   - Tasks older than 24 hours are never loaded from disk

### Display Size Modes

The monitor supports 4 display size modes via `--size` argument to accommodate different screen sizes:

**Tiny Mode** (`--size tiny`, default):
- Compact view optimized for small screens
- Columns: Status, Project/Task (flexible width), Progress (bar), Updated
- Only 4 columns to maximize horizontal space
- Progress bar is smaller (8 chars) to give more space to Project/Task column
- Project/Task column shows: tiny_title/project name, task name, current step (multi-line)
- Supports optional `tiny_title` field for custom short labels

**Small Mode** (`--size small`):
- Clean columnar layout
- Columns: Status, Project, Task, Current Step, Updated
- Each piece of info gets its own column
- No progress bar (text-based step info instead)

**Medium Mode** (`--size medium`):
- Expanded view with separate columns
- Columns: Status, Project, Task, Current Step, Message, Updated
- Current Step and Message in separate columns
- Good for larger screens where you want detail

**Large Mode** (`--size large`):
- Maximum information display
- Columns: Status, Project, Task, Current Step, Message, Progress %, Updated
- All available fields shown
- Best for wide/high-resolution displays

### Display Design Details

- **Status column**: Shows only emoji (🔄, ⚠️, ✅, ❌), no redundant text
- **Full-width tables**: All tables expand to terminal width with `expand=True`
- **Row separators**: `show_lines=True` adds horizontal lines between task rows for clarity
- **Time tracking**: "Updated" column shows relative time (e.g., "5s ago", "2m ago", "3h ago")
- **Completed tasks table**: Shows up to 10 recently completed tasks in full table format (same across all sizes)
- **Minimal header**: Removed "Press Ctrl+C to exit" and "Update interval" lines to maximize vertical space for task display

### Status File Format

```json
{
  "task_name": "Task description",
  "status": "in_progress",
  "progress_percent": 45,
  "current_step": "Current operation",
  "message": "Additional context",
  "needs_attention": false,
  "updated_at": "2025-11-10T14:30:00Z"
}
```

**Required fields:**
- `task_name` (string): Brief description
- `status` (string): One of: `pending`, `in_progress`, `blocked`, `waiting`, `completed`, `error`
- `updated_at` (string): ISO 8601 timestamp

**Optional fields:**
- `progress_percent` (int): 0-100 completion percentage
- `current_step` (string): What's happening now
- `message` (string): Additional context
- `needs_attention` (bool): User intervention required
- `tiny_title` (string): Short title for tiny display mode (replaces project name in Project/Task column)

## Usage

### Running the Monitor

```bash
# Using wrapper script
/path/to/claude-monitor/run_monitor.sh

# Direct Python invocation
python3 monitor.py

# With custom options
python3 monitor.py --watch ~/.claude-monitor --interval 5.0
```

### Command-Line Arguments

- `--watch`: Directories to watch for status files (default: `~/.claude-monitor`)
- `--interval`: Update interval in seconds (default: 2.0)
- `--breadcrumb`: Filename pattern to match (default: `*.json`)
- `--size`: Display size mode: `tiny` (default), `small`, `medium`, or `large`

### Examples

```bash
# Tiny mode (default) - for small screens
./run_monitor.sh

# Small mode - clean columns without progress bar
./run_monitor.sh --size small

# Medium mode - separate step and message columns
./run_monitor.sh --size medium

# Large mode - all fields including progress percentage
./run_monitor.sh --size large
```

### Creating Status Files

When working on multi-step or long-running tasks in ANY project:

1. Create/update a status file at `~/.claude-monitor/<project_name>.json`
2. Use the project name as the filename (without spaces)
3. Update the file whenever status changes significantly
4. Set `needs_attention: true` when user input is required

### Python Helper Function

```python
import json
from pathlib import Path
from datetime import datetime, timezone

def update_task_status(
    project_name: str,
    task_name: str,
    status: str,
    progress_percent: int = None,
    current_step: str = None,
    message: str = None,
    needs_attention: bool = False
):
    """Update Claude task monitoring status file."""
    status_file = Path.home() / '.claude' / 'monitor' / f'{project_name}.json'
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
```

## Task Monitoring Protocol

When working on tasks in this or other projects:

### When to Create Status Files

- Multi-step tasks (3+ distinct steps)
- Long-running operations (>30 seconds)
- Tasks that may require user intervention
- Background processes (builds, training, downloads, migrations)

### Update Frequency

- When status transitions between states
- Every 5-10 seconds for long operations
- When progress_percent changes by 5% or more
- Immediately when `needs_attention` becomes true

### Cleanup

- Status files are automatically ignored after 24 hours
- You can manually delete files from `~/.claude-monitor/` when tasks are complete
- The monitor handles missing or malformed files gracefully

## Development

### Dependencies

- Python 3.x
- `rich` library for terminal UI (install via `pip install -r requirements.txt`)

### Testing

Run demo tasks to see the monitor in action:

**Basic demo:**
```bash
# Terminal 1: Start the monitor
/path/to/claude-monitor/run_monitor.sh

# Terminal 2: Run demo task
/path/to/claude-monitor/run_demo.sh
```

The basic demo creates a sample task that progresses through various states.

**Spaceteam demo (recommended for fun!):**
```bash
# Run from anywhere - it uses ~/.claude-monitor/
python3 /path/to/claude-monitor/spaceteam_demo.py
```

The Spaceteam demo simulates 8 concurrent chaotic control panels with technobabble commands like "SET FOOBAR TO 3!" and "ENGAGE QUANTUM VAPOR!" inspired by the cooperative mobile game Spaceteam. Features random crises, equipment failures, and dramatic rescues. Great for demonstrating multiple concurrent tasks and stress-testing the UI.

### File Structure

```
/path/to/claude-monitor/
├── monitor.py              # Main monitoring script
├── demo_task.py           # Basic demo task for testing
├── spaceteam_demo.py      # Fun Spaceteam-style chaos demo
├── run_monitor.sh         # Monitor launch script
├── run_demo.sh           # Demo task launch script
├── Pipfile               # Python dependencies
├── Pipfile.lock          # Locked dependencies
├── README.md             # User documentation
├── QUICKSTART.md         # Quick setup guide
├── CLAUDE_MD_TEMPLATE.md # Template for other projects
├── CHANGES.md            # Change log
└── CLAUDE.md            # This file
```

### Extending the Monitor

To add new features or modify behavior:

1. **Custom status colors**: Edit `TaskStatus.get_color()` in monitor.py:88
2. **Custom status emojis**: Edit `TaskStatus.get_emoji()` in monitor.py:75
3. **Table layout**: Modify `create_task_table()` in monitor.py:205
4. **Filtering logic**: Update `get_active_tasks()` in monitor.py:154 or `get_completed_tasks()` in monitor.py:192
5. **Task age thresholds**: Adjust timeout values in `get_active_tasks()` and `get_completed_tasks()`
   - Current: 10 min for active, 1 hour for errors, 30 min for completed
6. **Display dimensions**: Modify column widths in `create_task_table()` for different screen sizes

## Integration with Other Projects

To enable monitoring in another project:

1. Add task monitoring instructions to that project's `CLAUDE.md` (see `CLAUDE_MD_TEMPLATE.md`)
2. Use the helper function to create/update status files
3. Store status files in `~/.claude-monitor/<project_name>.json`
4. Run the monitor to see live updates

## Best Practices

### For Task Status Updates

- Use descriptive task names (e.g., "Training Model" not "Task 1")
- Update status atomically (write to temp file, then rename)
- Include meaningful progress percentages when available
- Set `needs_attention: true` sparingly - only when truly blocked
- Remember: tasks auto-hide after 10 minutes of inactivity, so update regularly for long operations
- Clean up status files when tasks are complete (optional - they auto-expire)

### For Monitor Configuration

- Keep the monitor running in a dedicated terminal or tmux session
- Use project-specific watch paths to reduce scan overhead
- Increase `--interval` if monitoring many projects
- Create shell aliases for common usage patterns
- For small screens: The UI is optimized for vertical space with minimal header and full-width tables

### Design Philosophy

The monitor was designed with these principles:
- **Minimal noise**: Only show emoji status, no redundant text labels
- **Maximum density**: Use full terminal width and show multiple lines per task
- **Smart filtering**: Auto-hide stale tasks based on their status type
- **Glanceable**: Important info (needs attention) jumps out immediately with red highlighting

## Troubleshooting

**Monitor not showing tasks:**
- Check that status files exist in `~/.claude-monitor/`
- Verify JSON is valid (`python3 -m json.tool < file.json`)
- Ensure `updated_at` timestamp is recent (within 24 hours)
- Confirm watch path includes the directory

**Tasks not updating:**
- Verify status files are being written
- Check file permissions
- Ensure timestamps are being updated
- Look for JSON encoding errors

**Performance issues:**
- Increase `--interval` to reduce scan frequency
- Limit `--watch` paths to specific directories
- Consider using more specific `--breadcrumb` patterns

## Future Enhancements

Potential improvements:
- Web-based UI for remote monitoring
- Task history and timeline view
- Desktop/email/webhook notifications
- Task dependency tracking
- Multi-user support
- Priority levels and sorting
- Execution time tracking
- Export to CSV/JSON logs

## Related Tools

- `~/projects/git/home_assistant_AI_integration/saga_assistant/training_scripts/monitor_training.py` - Training-specific monitor that inspired this tool
- `htop`, `watch`, `tail -f` - Classic Unix monitoring tools

## Notes for Claude Code

When working in this project:

1. Test changes using the demo task (`run_demo.sh`)
2. Ensure backward compatibility with existing status file format
3. Update README.md and QUICKSTART.md when adding features
4. Keep the UI responsive and readable at various terminal sizes
5. Handle malformed JSON gracefully (don't crash the monitor)

## License

Free to use and modify for personal or commercial projects.
