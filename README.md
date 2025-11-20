# Claude Task Monitor

A live terminal dashboard that shows what Claude Code is working on across all your projects. Watch long-running tasks, training jobs, builds, and migrations in real-time.

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🔄  voice-assistant                                          ┃
┃     Training wakeword model                                  ┃
┃     Processing audio samples 8750/20000                      ┃
┃     ████████░░░░░░░░░░ 43%                    2m ago         ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ ⚠️  home-automation                                          ┃
┃     Database migration                                       ┃
┃     Conflict in migration 0042 - needs review                ┃
┃                                                  5s ago      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**See tasks across all projects. Know when Claude needs your attention. Never lose track of long-running operations.**

## Table of Contents

- [🚀 Quickest Start](#-quickest-start-for-claude-code-users) - Get up and running in 30 seconds
- [See It In Action](#see-it-in-action-30-second-demo) - Try the demo first
- [Installation](#installation) - Set up the monitor
- [Usage](#usage) - Command-line options
- [Integrating with Your Projects](#integrating-with-your-projects) - The easy way vs. manual
- [Status File Format](#status-file-format) - Technical reference
- [Python Helper Functions](#python-helper-functions) - For script integration
- [Tips & Troubleshooting](#tips) - Common issues and solutions

## 🚀 Quickest Start (For Claude Code Users)

**The fastest way to get monitoring in your projects:**

1. **FIRST:** Add permissions to your project's `.clauderc` file:
   ```ini
   # Claude monitor status updates - REQUIRED
   Read(/Users/YOUR_USERNAME/.claude-monitor/**)
   Write(/Users/YOUR_USERNAME/.claude-monitor/**)
   ```
   Replace `YOUR_USERNAME` with your actual username. **This prevents Claude Code from asking for permissions repeatedly.**

2. **Run Claude Code inside this `claude-monitor` directory**
3. **Tell Claude:** *"Add task monitoring to my project at ~/projects/my-awesome-project"*
4. **Claude will automatically** edit that project's `CLAUDE.md` file with monitoring instructions
5. **Next time Claude works there**, you'll see live task updates in this monitor!

See `CLAUDE_MD_TEMPLATE.md` for what gets added to your projects.

**Not using Claude Code?** No problem! You can manually create status files from any script or process (see [Manual Integration](#manual-integration) below).

## See It In Action (30 Second Demo)

Want to see what this looks like before setting up?

```bash
# Terminal 1: Start the monitor
cd /path/to/claude-monitor
./run_monitor.sh

# Terminal 2: Run the demo
cd /path/to/claude-monitor
./run_demo.sh
```

You'll see a live-updating dashboard showing task status, progress bars, and completion notifications.

**Bonus:** Try the chaotic Spaceteam demo for multiple concurrent tasks:
```bash
python3 spaceteam_demo.py
```

## What You Get

- 🔄 **Live updates** - Real-time task monitoring with configurable refresh intervals
- 📊 **Progress tracking** - Visual progress bars and percentage completion
- ⚠️ **Attention alerts** - Highlights tasks that need user intervention
- 🎨 **Rich terminal UI** - Clean, colorful display using the `rich` library
- 🌳 **Multi-project support** - Monitors multiple directory trees simultaneously
- 📁 **Automatic discovery** - Recursively finds all task breadcrumb files
- ⏱️ **Smart filtering** - Auto-hides stale tasks (>10 min for active, >1 hour for errors)

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

### Choose Display Size

The monitor supports 4 display sizes to fit different screen sizes:

```bash
# Tiny mode (default) - compact with progress bar, good for small screens
python3 /path/to/claude-monitor/monitor.py --size tiny

# Small mode - clean columns without progress bar
python3 /path/to/claude-monitor/monitor.py --size small

# Medium mode - separate step and message columns
python3 /path/to/claude-monitor/monitor.py --size medium

# Large mode - all fields including progress percentage
python3 /path/to/claude-monitor/monitor.py --size large
```

**Display Mode Comparison:**
- **Tiny**: Status | Task (single line if tiny_title set, otherwise multi-line) | Progress Bar | Updated
- **Small**: Status | Project | Task | Current Step | Updated
- **Medium**: Status | Project | Task | Current Step | Message | Updated
- **Large**: Status | Project | Task | Current Step | Message | Progress % | Updated

## Integrating with Your Projects

### The Easy Way: Let Claude Do It

**If you're using Claude Code:**

1. Open Claude Code in this `claude-monitor` directory
2. Say: *"Add task monitoring to ~/projects/my-project"*
3. Claude will edit `~/projects/my-project/CLAUDE.md` with the monitoring instructions
4. Done! Next time Claude works there, you'll see live updates

**What Claude adds:** See `CLAUDE_MD_TEMPLATE.md` for the exact instructions that get added to your project's `CLAUDE.md` file.

### Manual Integration

**If you want to set it up yourself or use it from scripts:**

#### Step 1: Configure .clauderc (REQUIRED for Claude Code)

**CRITICAL:** Add these permissions to your project's `.clauderc` file to prevent repeated permission prompts:

```ini
# Claude monitor status updates - REQUIRED
Read(/Users/YOUR_USERNAME/.claude-monitor/**)
Write(/Users/YOUR_USERNAME/.claude-monitor/**)
```

Replace `YOUR_USERNAME` with your actual username (e.g., `/Users/nthmost/.claude-monitor/**`).

#### Step 2: Update Your Project's CLAUDE.md

Add the task monitoring section from `CLAUDE_MD_TEMPLATE.md` to your project's `CLAUDE.md` file. This tells Claude Code to create status files when working on multi-step tasks.

**Before adding to CLAUDE.md, make sure you've added the `.clauderc` permissions above!**

Quick snippet of what to add to CLAUDE.md:

```markdown
## Task Status Reporting

When working on multi-step tasks, create status files in `~/.claude-monitor/` for monitoring.

**Status file location:** `~/.claude-monitor/<project_name>.json`

**For Claude Code:** Use the Write tool directly (not Bash):

Write(
    file_path="/Users/username/.claude-monitor/<project_name>.json",
    content=json.dumps({
        "task_name": "Task description",
        "status": "in_progress",
        "progress_percent": 45,
        "current_step": "Current operation",
        "updated_at": datetime.now(timezone.utc).isoformat()
    }, indent=2)
)
```

#### Step 3: Create Status Files

When working on tasks, create/update status files in `~/.claude-monitor/`:

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
- `tiny_title` (string): Short title for tiny display mode (when set, displays ONLY this instead of project/task/step)

### Multiple Tasks Per Project

Projects can create multiple JSON files to track parallel operations:

```bash
~/.claude-monitor/
├── myproject_main.json       # Main orchestration task
├── myproject_frontend.json   # Frontend build
├── myproject_backend.json    # Backend build
└── myproject_tests.json      # Test suite
```

**Each file appears as a separate row** in the monitor, letting you see all parallel tasks at once. Perfect for:
- Sub-agents working on different parts of a task
- Parallel builds, tests, or deployments
- Multiple training jobs
- Concurrent data processing pipelines

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
