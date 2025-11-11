# Architecture Change: Centralized Breadcrumb Collection

## What Changed

**Before:** Monitor recursively searched project directories for `.claude_task.json` files
**After:** Monitor watches a single centralized directory `~/.claude-monitor/` for `*.json` files

## Why This Is Better

1. **Simpler Monitor** - No need to configure watch paths, just one location
2. **Faster Scanning** - Single directory scan instead of recursive tree walks
3. **Project Independence** - Projects don't need to know about monitor location
4. **Clean Project Dirs** - No breadcrumb files littering project directories
5. **Better Naming** - File names indicate project (e.g., `home_assistant.json`, `llm_router.json`)

## Migration Guide

### For the Monitor

**Old:**
```bash
./run_monitor.sh --watch ~/projects ~/llm-router
```

**New:**
```bash
./run_monitor.sh  # Automatically watches ~/.claude-monitor/
```

### For Projects

**Old CLAUDE.md instruction:**
```markdown
Create `.claude_task.json` in project root
```

**New CLAUDE.md instruction:**
```markdown
Create `~/.claude-monitor/<project_name>.json`
```

**Old Python helper:**
```python
status_file: Path = Path('.claude_task.json')
```

**New Python helper:**
```python
status_file: Path = Path.home() / '.claude' / 'monitor' / 'project_name.json'
# Ensure directory exists
status_file.parent.mkdir(parents=True, exist_ok=True)
```

## Files Updated

- ✅ `monitor.py` - Changed default watch path, breadcrumb pattern matching
- ✅ `demo_task.py` - Updated to use centralized location
- ✅ `~/projects/git/CLAUDE.md` - Updated instructions
- ✅ `~/projects/git/home_assistant_AI_integration/CLAUDE.md` - Updated instructions with helper
- ✅ `CLAUDE_MD_TEMPLATE.md` - Updated template
- 🔄 `README.md` - Needs update
- 🔄 `QUICKSTART.md` - Needs update

## Created

- ✅ `~/.claude-monitor/` directory

## Benefits Summary

- **No configuration needed** - Just run `./run_monitor.sh`
- **Scales better** - Can monitor 100+ projects without performance issues
- **Cleaner** - Project directories stay clean, all breadcrumbs in one place
- **Discoverable** - Easy to see all active tasks: `ls ~/.claude-monitor/`
