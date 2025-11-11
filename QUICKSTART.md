# Claude Task Monitor - Quick Start

Get up and running in 60 seconds!

## 1. Check Setup

Install dependencies with: `pip install -r requirements.txt` ✅

## 2. Test the Monitor

Open **two terminal windows**.

### Terminal 1: Start the Monitor

```bash
./run_monitor.sh
```

You should see:
```
🔍 Claude Task Monitor

Watching: ~/.claude-monitor
Looking for: *.json
Update interval: 2.0s

Press Ctrl+C to exit
```

### Terminal 2: Run the Demo

```bash
./run_demo.sh
```

Watch Terminal 1 - you should see the task appear, progress through stages, and complete!

## 3. Create Your First Status File

Try it manually:

```bash
mkdir -p ~/.claude-monitor

cat > ~/.claude-monitor/my_test.json << 'EOF'
{
  "task_name": "My First Monitored Task",
  "status": "in_progress",
  "progress_percent": 50,
  "current_step": "Working on something cool",
  "updated_at": "2025-11-10T14:30:00Z"
}
EOF
```

The monitor (if running) will automatically pick it up!

## 4. Integrate with Your Projects

Add to your project's `CLAUDE.md`:

```markdown
## Task Status Reporting

When working on multi-step tasks, create status files in `~/.claude-monitor/<project_name>.json`:

Location: `~/.claude-monitor/<project_name>.json`

```json
{
  "task_name": "Task Description",
  "status": "in_progress",
  "progress_percent": 45,
  "updated_at": "2025-11-10T14:30:00Z"
}
```

Status values: `pending`, `in_progress`, `blocked`, `waiting`, `completed`, `error`

**For Claude Code:** Use the Write tool directly, not Bash heredocs.
```

## 5. Run in Background

Keep the monitor running in a dedicated terminal:

```bash
# Option 1: Dedicated terminal window
./run_monitor.sh

# Option 2: tmux session (recommended)
tmux new -s claude-monitor
./run_monitor.sh
# Detach: Ctrl+B, then D
# Reattach: tmux attach -t claude-monitor

# Option 3: screen session
screen -S claude-monitor
./run_monitor.sh
# Detach: Ctrl+A, then D
# Reattach: screen -r claude-monitor
```

## Common Use Cases

### Choose Display Size

Pick the mode that fits your screen:

```bash
# Tiny (default) - compact with progress bar
./run_monitor.sh

# Small - clean columns, no progress bar
./run_monitor.sh --size small

# Medium - separate step/message columns
./run_monitor.sh --size medium

# Large - all fields including progress %
./run_monitor.sh --size large
```

### Watching Additional Directories

```bash
./run_monitor.sh --watch ~/.claude-monitor ~/custom-monitor
```

### Slower Updates (Less CPU)

```bash
./run_monitor.sh --interval 5.0
```

### Custom Status Directory

```bash
./run_monitor.sh --watch ~/my-custom-status-dir
```

## Python Integration

Add this to your Python scripts:

```python
import json
from pathlib import Path
from datetime import datetime, timezone

def update_task_status(task_name, status, progress_percent=None, message=None,
                      status_file=Path.home() / '.claude-monitor' / 'my_project.json'):
    status_file.parent.mkdir(parents=True, exist_ok=True)

    data = {
        'task_name': task_name,
        'status': status,
        'updated_at': datetime.now(timezone.utc).isoformat()
    }
    if progress_percent is not None:
        data['progress_percent'] = progress_percent
    if message:
        data['message'] = message

    with open(status_file, 'w') as f:
        json.dump(data, f, indent=2)

# Use it:
update_task_status("Training Model", "in_progress", progress_percent=45)
```

## Troubleshooting

### "No active tasks"
- Check that status files exist in `~/.claude-monitor/`
- Verify `updated_at` is recent (within 24 hours)
- Confirm JSON is valid: `python3 -m json.tool < ~/.claude-monitor/project.json`

### Tasks not updating
- Make sure files are being written (check modification time with `ls -la`)
- Verify the monitor is watching the right directory
- Check file permissions

### Monitor performance
- Narrow watch paths to specific directories
- Increase update interval: `--interval 5.0`

## Next Steps

- Read the full [README.md](README.md)
- Check [CLAUDE_MD_TEMPLATE.md](CLAUDE_MD_TEMPLATE.md) for project integration
- Customize the monitor for your workflow

## Tips

1. **Create an alias** in `~/.zshrc` or `~/.bashrc`:
   ```bash
   alias claude-monitor='./run_monitor.sh'
   ```

2. **Use tmux/screen** for persistent monitoring across SSH sessions

3. **Set `needs_attention: true`** for tasks requiring user input - they'll be highlighted in red

4. **Clean up old status files** after tasks complete (or leave them - monitor ignores files >24h old)

---

That's it! You're ready to monitor Claude tasks across all your projects. 🎉
