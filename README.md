# Claude Task Monitor

A general-purpose monitoring tool for tracking Claude Code task progress across multiple projects. Perfect for keeping an eye on long-running operations, training jobs, or any multi-step tasks.

## Overview

This monitor watches for JSON status files in `~/.claude-monitor/` that Claude Code (or any process) creates to report task status. It displays a live-updating terminal interface showing active tasks, their progress, and which ones need attention.

## Features

- 🔄 **Live updates** - Real-time task monitoring with configurable refresh intervals
- 📊 **Progress tracking** - Visual progress bars and percentage completion
- ⚠️ **Attention alerts** - Highlights tasks that need user intervention
- 🎨 **Rich terminal UI** - Clean, colorful display using the `rich` library
- 🌳 **Multi-project support** - Monitors multiple directory trees simultaneously
- 📁 **Automatic discovery** - Recursively finds all task breadcrumb files
- ⏱️ **Age filtering** - Ignores stale tasks (>24 hours old)

## Installation

### Prerequisites

- Python 3.x
- `pip` for installing dependencies

### Setup

1. **Clone or navigate to the repository:**
   ```bash
   cd /path/to/claude-monitor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Dependencies:
   - `rich` - Terminal UI library

3. **Run the monitor:**

   **Option 1: Using the wrapper script (recommended)**
   ```bash
   ./run_monitor.sh
   ```

   **Option 2: Direct Python invocation**
   ```bash
   python3 monitor.py
   ```

### Create an Alias (Optional)

Add to `~/.zshrc` or `~/.bashrc` (adjust path to your installation):

```bash
alias claude-monitor='/path/to/claude-monitor/run_monitor.sh'
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

Now you can just run:
```bash
claude-monitor
```

## Usage

### Basic Usage

Monitor the default status file directory (`~/.claude-monitor`):

```bash
python3 /path/to/claude-monitor/monitor.py
```

### Custom Watch Paths

Monitor additional status file directories:

```bash
python3 /path/to/claude-monitor/monitor.py --watch ~/.claude-monitor ~/custom-monitor
```

### Adjust Update Interval

Change refresh rate (default: 2 seconds):

```bash
python3 /path/to/claude-monitor/monitor.py --interval 5.0
```

### Custom Breadcrumb Filename

Use a different status filename:

```bash
python3 /path/to/claude-monitor/monitor.py --breadcrumb .my_task_status.json
```

## Integrating with Your Projects

To enable monitoring in your projects, you need to:

1. Update your project's `CLAUDE.md` with task monitoring instructions
2. Create status files in `~/.claude-monitor/<project_name>.json` when working on long-running tasks

### Step 1: Update CLAUDE.md

See `CLAUDE_MD_TEMPLATE.md` for complete instructions to add to your project's `CLAUDE.md`.

Quick snippet:

```markdown
## Task Status Reporting

When working on multi-step tasks, create status files in `~/.claude-monitor/` for monitoring.

Status file location: `~/.claude-monitor/<project_name>.json`

Status file format:
```json
{
  "task_name": "Training Model",
  "status": "in_progress",
  "progress_percent": 45,
  "current_step": "Step 9000/20000",
  "message": "Training neural network",
  "needs_attention": false,
  "updated_at": "2025-11-10T14:30:00Z"
}
```

Status values: `pending`, `in_progress`, `blocked`, `waiting`, `completed`, `error`

### For Claude Code: Use Write Tool

**IMPORTANT:** Claude Code should use the **Write tool** directly to create/update status files, NOT Bash with heredocs. This avoids permission prompts.

```python
Write(
    file_path="/Users/username/.claude-monitor/<project_name>.json",
    content=json.dumps({...}, indent=2)
)
```
```

### Step 2: Create Status Files

When Claude Code works on tasks in your project, it should create/update status files in `~/.claude-monitor/`:

**Example: Starting a task**
```json
{
  "task_name": "Running Benchmark Suite",
  "status": "in_progress",
  "progress_percent": 0,
  "current_step": "Initializing models",
  "updated_at": "2025-11-10T14:00:00Z"
}
```

**Example: Task needs attention**
```json
{
  "task_name": "Database Migration",
  "status": "blocked",
  "message": "Conflict in migration 0042",
  "needs_attention": true,
  "updated_at": "2025-11-10T14:15:00Z"
}
```

**Example: Task completed**
```json
{
  "task_name": "Running Benchmark Suite",
  "status": "completed",
  "progress_percent": 100,
  "message": "Results saved to benchmarks/results/",
  "updated_at": "2025-11-10T14:45:00Z"
}
```

## Status File Format

### Required Fields

- `task_name` (string): Brief description of the task
- `status` (string): One of: `pending`, `in_progress`, `blocked`, `waiting`, `completed`, `error`
- `updated_at` (string): ISO 8601 timestamp

### Optional Fields

- `progress_percent` (integer): 0-100 completion percentage
- `current_step` (string): Description of current operation
- `message` (string): Additional context or details
- `needs_attention` (boolean): Set to `true` if user action is required

## Python Helper Functions

For Python projects, you can use this helper function to update status:

```python
import json
from pathlib import Path
from datetime import datetime, timezone

def update_task_status(
    task_name: str,
    status: str,
    progress_percent: int = None,
    current_step: str = None,
    message: str = None,
    needs_attention: bool = False,
    status_file: Path = Path.home() / '.claude-monitor' / '<project_name>.json'
):
    """Update Claude task monitoring status file."""
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


# Usage example
update_task_status(
    task_name="Training Model",
    status="in_progress",
    progress_percent=45,
    current_step="Step 9000/20000"
)
```

## Example Integration

Here's how to integrate status reporting into a long-running script:

```python
from tqdm import tqdm
import time

def train_model():
    # Start task
    update_task_status(
        task_name="Training Wakeword Model",
        status="in_progress",
        progress_percent=0,
        current_step="Loading data"
    )

    total_steps = 20000
    for step in tqdm(range(total_steps)):
        # Do training work
        time.sleep(0.01)

        # Update status periodically
        if step % 500 == 0:
            progress = int((step / total_steps) * 100)
            update_task_status(
                task_name="Training Wakeword Model",
                status="in_progress",
                progress_percent=progress,
                current_step=f"Step {step}/{total_steps}"
            )

    # Mark complete
    update_task_status(
        task_name="Training Wakeword Model",
        status="completed",
        progress_percent=100,
        message="Model saved to models/hey_saga.onnx"
    )
```

## Display Elements

The monitor shows:

### Summary Panel
- Total tasks being tracked
- Active tasks (not completed)
- Completed tasks
- Tasks needing attention (highlighted in red)

### Active Tasks Table
- Status emoji (⏳ ⚠️ ✅ ❌ etc.)
- Project name
- Task description
- Progress bar and percentage
- Current step or message

### Recently Completed
- Last 3-5 completed tasks
- Collapsed view to save space

## Status Indicators

| Status | Emoji | Color | Meaning |
|--------|-------|-------|---------|
| `pending` | ⏳ | Yellow | Queued, not started |
| `in_progress` | 🔄 | Cyan | Currently working |
| `blocked` | ⚠️ | Red | Needs user intervention |
| `waiting` | ⏸️ | Dim | Paused, will resume |
| `completed` | ✅ | Green | Finished successfully |
| `error` | ❌ | Red | Failed, needs attention |
| `unknown` | ❓ | Dim | Status unclear |

## Tips

### Running in Background

Keep the monitor open in a dedicated terminal:

```bash
# In a terminal window:
python3 /path/to/claude-monitor/monitor.py

# Or with tmux/screen:
tmux new -s claude-monitor
python3 /path/to/claude-monitor/monitor.py
```

### Filtering by Project

Watch only specific projects:

```bash
python3 /path/to/claude-monitor/monitor.py --watch ~/projects/git/home_assistant_AI_integration
```

### Troubleshooting

**No tasks showing up?**
- Check that status files exist in `~/.claude-monitor/`
- Verify the `updated_at` timestamp is within the last 24 hours
- Make sure the JSON is valid (use `python3 -m json.tool < ~/.claude-monitor/project.json`)
- Ensure the watch path includes `~/.claude-monitor` (default)

**Tasks not updating?**
- Ensure the status file is being written regularly
- Check file permissions
- Verify the watch path includes your project directory

**Monitor running slowly?**
- Increase the `--interval` to reduce scan frequency
- Narrow the `--watch` paths to specific project directories

## Architecture

```
/path/to/claude-monitor/
├── monitor.py                    # Main monitoring script
├── README.md                     # This file
└── CLAUDE_MD_TEMPLATE.md         # Template for project CLAUDE.md files

Your projects:
~/projects/my-project/
├── CLAUDE.md                     # Includes task monitoring instructions
~/.claude-monitor/
├── project_name.json              # Status file (created by Claude or scripts)
└── ...
```

## Future Enhancements

Potential improvements:

- [ ] Web UI for remote monitoring
- [ ] Task history and timeline view
- [ ] Notifications (desktop alerts, email, webhook)
- [ ] Task dependencies and workflows
- [ ] Multi-user support
- [ ] Configurable priority levels
- [ ] Task execution time tracking
- [ ] Export task logs to CSV/JSON

## Related Tools

This monitor is inspired by:
- `~/projects/git/home_assistant_AI_integration/saga_assistant/training_scripts/monitor_training.py` - Training-specific monitor with log parsing
- General process monitoring tools like `htop`, `watch`, `tail -f`

## License

Free to use and modify for personal or commercial projects.

---

**Last Updated:** November 2025
