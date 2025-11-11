# Claude Task Monitor Integration

Add this section to your project's `CLAUDE.md` to enable task monitoring.

## Instructions for CLAUDE.md

Add the following section to your project's `CLAUDE.md` file:

```markdown
## Task Status Reporting

When working on long-running or multi-step tasks in this project, create a task status file for monitoring:

### Status File Location
- **Location:** `~/.claude-monitor/<project_name>.json`
- **Purpose:** Allows external monitoring of Claude Code progress
- **Monitored by:** The `claude-monitor` tool (https://github.com/nthmost/claude-monitor)
- **Note:** All projects deposit breadcrumbs in `~/.claude-monitor/` using project-specific filenames

### When to Create Status Files
- Multi-step tasks (3+ steps)
- Long-running operations (>30 seconds)
- Tasks that may need user intervention
- Background processes (training, downloads, builds)

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
- `tiny_title` (string): Short title for tiny display mode (e.g., "Training", "Building", "Testing")

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
        "tiny_title": "Training",  # Optional: short title for tiny display mode
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
