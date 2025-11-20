# Claude Task Monitor Integration

Add this section to your project's `CLAUDE.md` to enable task monitoring.

## IMPORTANT: Configure .clauderc First

**CRITICAL:** Before adding the monitoring instructions to your `CLAUDE.md`, you MUST configure permissions in your project's `.clauderc` file. Without this, Claude Code will repeatedly ask for permission to write status files.

### Add to `.clauderc`

Add the following permissions to your project's `.clauderc` file:

```ini
# Claude monitor status updates - REQUIRED for task monitoring
Read(/Users/YOUR_USERNAME/.claude-monitor/**)
Write(/Users/YOUR_USERNAME/.claude-monitor/**)
```

Replace `YOUR_USERNAME` with your actual username. For example:
- macOS/Linux: `/Users/nthmost/.claude-monitor/**` or `/home/username/.claude-monitor/**`
- Windows: `C:/Users/username/.claude-monitor/**`

**Why this is required:**
- Without these permissions in `.clauderc`, Claude Code will prompt for permission every time it tries to update task status
- These permissions are project-specific and persist across sessions
- The `.clauderc` file should be committed to your repository so the permissions apply to all sessions

### Example `.clauderc` section

```ini
# Project file permissions
Read(/path/to/your/project/**)
Write(/path/to/your/project/**)
Edit(/path/to/your/project/**)

# Claude monitor status updates - REQUIRED
Read(/Users/nthmost/.claude-monitor/**)
Write(/Users/nthmost/.claude-monitor/**)

# Git operations
Bash(git:*)
Bash(gh:*)
```

## Instructions for CLAUDE.md

After configuring `.clauderc`, add the following section to your project's `CLAUDE.md` file:

```markdown
## Task Status Reporting

When working on long-running or multi-step tasks in this project, create a task status file for monitoring:

### Status File Location
- **Location:** `~/.claude-monitor/<project_name>.json` (or multiple files for parallel tasks)
- **Purpose:** Allows external monitoring of Claude Code progress
- **Monitored by:** The `claude-monitor` tool (https://github.com/nthmost/claude-monitor)
- **Note:** All projects deposit breadcrumbs in `~/.claude-monitor/` using project-specific filenames
- **Multiple Tasks:** Projects can create multiple JSON files (e.g., `project_task1.json`, `project_task2.json`) to track parallel operations

### When to Create Status Files
- Multi-step tasks (3+ steps)
- Long-running operations (>30 seconds)
- Tasks that may need user intervention
- Background processes (training, downloads, builds)
- **Parallel tasks:** When using sub-agents or running tasks in parallel, create separate JSON files for each task

### Parallel Task Tracking

When Claude Code spawns multiple sub-agents or parallelizes work:

**Create separate status files for each parallel task:**
```python
# Main task
Write(
    file_path="~/.claude-monitor/<project_name>_main.json",
    content=json.dumps({
        "task_name": "Orchestrating parallel build",
        "status": "in_progress",
        "current_step": "Spawned 3 build agents",
        "updated_at": datetime.now(timezone.utc).isoformat()
    }, indent=2)
)

# Sub-agent 1
Write(
    file_path="~/.claude-monitor/<project_name>_frontend.json",
    content=json.dumps({
        "task_name": "Building frontend",
        "status": "in_progress",
        "progress_percent": 30,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }, indent=2)
)

# Sub-agent 2
Write(
    file_path="~/.claude-monitor/<project_name>_backend.json",
    content=json.dumps({
        "task_name": "Building backend",
        "status": "in_progress",
        "progress_percent": 45,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }, indent=2)
)
```

**Benefits:**
- Each parallel task appears as a separate row in the monitor
- See progress of all parallel operations simultaneously
- Track which sub-agents need attention independently
- No file write conflicts between parallel tasks

### Status File Format

```json
{
  "task_name": "Training Hey Saga Wakeword Model",
  "status": "in_progress",
  "progress_percent": 45,
  "current_step": "Step 9000/20000 (45%)",
  "message": "Training neural network on GPU",
  "needs_attention": false,
  "updated_at": "2025-11-10T14:30:00Z"
}
```

### Status Values
- `pending` - Task queued but not started
- `in_progress` - Currently working on task
- `blocked` - Waiting for user input or external dependency
- `waiting` - Paused, will resume automatically
- `completed` - Task finished successfully
- `error` - Task failed, needs attention

### Required Fields
- `task_name` (string): Brief description of the task
- `status` (string): One of the status values above
- `updated_at` (string): ISO 8601 timestamp

### Optional Fields
- `progress_percent` (int): 0-100 completion percentage
- `current_step` (string): What's happening right now
- `message` (string): Additional context or status message
- `needs_attention` (bool): Set to `true` if user action required
- `tiny_title` (string): Short title for tiny display mode - when set, ONLY this is shown (not project/task/step) for maximum compactness (e.g., "Training", "Building", "Testing")

### For Claude Code: Use Write Tool

**IMPORTANT:** When creating/updating status files, Claude Code should use the **Write tool** directly, NOT Bash with heredocs.

```python
# Use the Write tool with file_path and JSON content
# Example:
Write(
    file_path="/Users/username/.claude-monitor/<project_name>.json",
    content=json.dumps({
        "task_name": "Training Wakeword Model",
        "status": "in_progress",
        "progress_percent": 45,
        "current_step": "Step 9000/20000",
        "message": "Training neural network",
        "tiny_title": "Training",  # Optional: shows ONLY this in tiny mode (replaces project/task/step)
        "needs_attention": False,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }, indent=2)
)
```

This avoids permission prompts and is the correct tool for file operations.

### Update Frequency
- Update the file whenever status changes significantly
- For long operations, update every 5-10 seconds
- Always update when transitioning between states
- Always update when `needs_attention` becomes `true`

### Example Usage

**Starting a task:**
```json
{
  "task_name": "Installing Dependencies",
  "status": "in_progress",
  "progress_percent": 0,
  "current_step": "Running pip install",
  "updated_at": "2025-11-10T14:00:00Z"
}
```

**Task needs user input:**
```json
{
  "task_name": "Database Migration",
  "status": "blocked",
  "progress_percent": 50,
  "message": "Conflict detected in migration 0042_add_user_table",
  "needs_attention": true,
  "updated_at": "2025-11-10T14:15:00Z"
}
```

**Task completed:**
```json
{
  "task_name": "Training Hey Saga Wakeword Model",
  "status": "completed",
  "progress_percent": 100,
  "message": "Model saved to models/hey_saga.onnx",
  "updated_at": "2025-11-10T14:45:00Z"
}
```

### Cleanup
- Keep the status file until the task is truly finished
- Status files older than 24 hours are ignored by the monitor
- You can delete status files from `~/.claude-monitor/` after task completion if desired
```

## Python Helper Functions

You can also add these helper functions to your project for easy status updates:

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
    """
    Update Claude task monitoring status file.

    Args:
        task_name: Brief description of the task
        status: One of: pending, in_progress, blocked, waiting, completed, error
        progress_percent: Optional 0-100 completion percentage
        current_step: Optional description of current step
        message: Optional additional context
        needs_attention: Set True if user action required
        status_file: Path to status file (default: ~/.claude-monitor/<project_name>.json)
    """
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


# Example usage in your script
if __name__ == '__main__':
    # Starting a task
    update_task_status(
        task_name="Training Wakeword Model",
        status="in_progress",
        progress_percent=0,
        current_step="Loading training data"
    )

    # ... do work ...

    # Update progress
    update_task_status(
        task_name="Training Wakeword Model",
        status="in_progress",
        progress_percent=45,
        current_step="Step 9000/20000"
    )

    # ... more work ...

    # Task needs attention
    update_task_status(
        task_name="Training Wakeword Model",
        status="blocked",
        progress_percent=75,
        message="Out of disk space",
        needs_attention=True
    )

    # ... user resolves issue ...

    # Task completed
    update_task_status(
        task_name="Training Wakeword Model",
        status="completed",
        progress_percent=100,
        message="Model saved to models/hey_saga.onnx"
    )
```

## Integration with Long-Running Scripts

For scripts that already have progress tracking (tqdm, custom progress bars, etc.), you can periodically update the status file:

```python
from tqdm import tqdm
import time

def train_model():
    update_task_status(
        task_name="Training Model",
        status="in_progress",
        progress_percent=0
    )

    total_steps = 20000
    for step in tqdm(range(total_steps)):
        # Do training
        time.sleep(0.01)

        # Update status every 500 steps
        if step % 500 == 0:
            progress = int((step / total_steps) * 100)
            update_task_status(
                task_name="Training Model",
                status="in_progress",
                progress_percent=progress,
                current_step=f"Step {step}/{total_steps}"
            )

    update_task_status(
        task_name="Training Model",
        status="completed",
        progress_percent=100
    )
```
