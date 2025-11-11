#!/usr/bin/env python3
"""
🚀 SPACETEAM DEMO 🚀
Based on the chaotic cooperative mobile game Spaceteam!

Run this from anywhere - it will create status files in ~/.claude-monitor/
"""
import json
import time
import random
from pathlib import Path
from datetime import datetime, timezone
from threading import Thread

MONITOR_DIR = Path.home() / '.claude-monitor'
MONITOR_DIR.mkdir(parents=True, exist_ok=True)

# ACTUAL SPACETEAM-STYLE TECHNOBABBLE
ACTIONS = [
    'SET {} TO {}',
    'ENGAGE {}',
    'ACTIVATE {}',
    'DISENGAGE {}',
    'REVERSE {}',
    'CALIBRATE {}',
    'ADJUST {}',
    'FLIP {}',
    'TURN {} TO {}',
    'ROTATE {}',
]

WIDGETS = [
    'FOOBAR', 'QUANTUM VAPOR', 'FLUX MATRIX', 'SPECTRAL PHASE',
    'CHRONOTRON', 'NEUTRINO FIELD', 'TACHYON PULSE', 'PLASMA COIL',
    'DILITHIUM DRIVE', 'ANTIMATTER POD', 'GYROSCOPIC WHEEL', 'HEISENBERG PAD',
    'HYPERBOLIC CHAMBER', 'INFINITY VALVE', 'KIRLIAN FREQUENCY', 'LAMBDA CORE',
    'NEUTRON FLOW', 'OSCILLATION GRID', 'POLARITY SHIELD', 'QUARK MATRIX',
    'REALITY ANCHOR', 'SINGULARITY BEAM', 'TIME CRYSTAL', 'VORTEX RING',
    'WORMHOLE NODE', 'XENON BUFFER', 'GRAVITON EMITTER', 'BOSON CLOUD',
    'INTERDIMENSIONAL DOOHICKEY', 'SUBSPACE GIZMO', 'TEMPORAL WIDGET',
    'DARK MATTER FLUX', 'COSMIC STRING', 'PROBABILITY DRIVE', 'ENTROPY REVERSER',
    'PARADOX ENGINE', 'CAUSALITY DAMPENER', 'SPACE-TIME FABRIC', 'VACUUM FLUCTUATOR',
]

VALUES = ['1', '2', '3', '4', '5', 'MAXIMUM', 'MINIMUM', 'OPTIMAL', 'CRITICAL', 'NORMAL']

CRISES = [
    'ASTEROID STORM',
    'WORMHOLE COLLAPSE',
    'ALIEN ATTACK',
    'REACTOR OVERLOAD',
    'HULL BREACH',
    'SYSTEMS FAILURE',
    'DIMENSIONAL RIFT',
    'SPACE PIRATES',
    'BLACK HOLE PROXIMITY',
    'TEMPORAL ANOMALY',
    'QUANTUM INSTABILITY',
]

def random_command():
    """Generate random Spaceteam-style command"""
    action = random.choice(ACTIONS)
    widget = random.choice(WIDGETS)
    if '{}' in action:
        count = action.count('{}')
        if count == 2:
            return action.format(widget, random.choice(VALUES))
        else:
            return action.format(widget)
    return action

def update_task_status(filename, task_name, status, progress_percent=None,
                       current_step=None, message=None, needs_attention=False, tiny_title=None):
    """Update a task status file"""
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
    if tiny_title:
        data['tiny_title'] = tiny_title

    with open(MONITOR_DIR / filename, 'w') as f:
        json.dump(data, f, indent=2)

def task_control_panel_1():
    """Chaotic control panel with random tasks"""
    filename = 'panel-alpha.json'

    for i in range(25):
        command = random_command()
        progress = int((i / 25) * 100)

        # Random crisis
        if random.random() < 0.15:
            update_task_status(
                filename,
                '⚡ PANEL ALPHA',
                'error',
                progress_percent=progress,
                current_step=f'⚠️ {random.choice(CRISES)}!',
                message=command,
                needs_attention=True,
                tiny_title='⚡ ALPHA'
            )
            time.sleep(3)
        else:
            update_task_status(
                filename,
                '⚡ PANEL ALPHA',
                'in_progress',
                progress_percent=progress,
                current_step=command,
                message=f'Urgency: {"!!!" if random.random() < 0.3 else "!!"}',
                tiny_title='⚡ ALPHA'
            )
            time.sleep(random.uniform(0.8, 2))

    update_task_status(
        filename,
        '⚡ PANEL ALPHA',
        'completed',
        progress_percent=100,
        message='ALL SYSTEMS NOMINAL!',
        tiny_title='⚡ ALPHA'
    )

def task_control_panel_2():
    """Another chaotic control panel"""
    filename = 'panel-beta.json'

    for i in range(20):
        command = random_command()
        progress = int((i / 20) * 100)

        # Blocked/needs help
        if random.random() < 0.12:
            widget = random.choice(WIDGETS)
            update_task_status(
                filename,
                '🔧 PANEL BETA',
                'blocked',
                progress_percent=progress,
                current_step=f'{widget} IS STUCK!',
                message='SOMEONE HELP ME WITH THIS!',
                needs_attention=True,
                tiny_title='🔧 BETA'
            )
            time.sleep(3)
        else:
            update_task_status(
                filename,
                '🔧 PANEL BETA',
                'in_progress',
                progress_percent=progress,
                current_step=command,
                message='DOING IT! DOING IT!',
                tiny_title='🔧 BETA'
            )
            time.sleep(random.uniform(0.9, 2.2))

    update_task_status(
        filename,
        '🔧 PANEL BETA',
        'completed',
        progress_percent=100,
        message='PANEL SECURE!',
        tiny_title='🔧 BETA'
    )

def task_control_panel_3():
    """Yet another chaotic control panel"""
    filename = 'panel-gamma.json'

    for i in range(22):
        command = random_command()
        progress = int((i / 22) * 100)

        update_task_status(
            filename,
            '⚙️ PANEL GAMMA',
            'in_progress',
            progress_percent=progress,
            current_step=command,
            message=f'Status: {"CRITICAL!" if random.random() < 0.2 else "OK"}',
            tiny_title='⚙️ GAMMA'
        )
        time.sleep(random.uniform(0.7, 2.1))

    update_task_status(
        filename,
        '⚙️ PANEL GAMMA',
        'completed',
        progress_percent=100,
        message='GAMMA STABLE!',
        tiny_title='⚙️ GAMMA'
    )

def task_engineering():
    """Engineering panel with emergencies"""
    filename = 'engineering.json'

    commands = [
        ('REROUTE AUXILIARY POWER', 'Power systems'),
        ('VENT PLASMA MANIFOLD', 'Cooling systems'),
        ('SEAL BULKHEAD 7', 'Hull integrity'),
        ('OVERRIDE SAFETY PROTOCOL', '⚠️ Safety systems'),
        ('ACTIVATE EMERGENCY THRUSTERS', 'Navigation'),
        ('JETTISON CARGO BAY', 'Mass reduction'),
        ('ENGAGE EMERGENCY WARP', 'FTL systems'),
    ]

    for i, (cmd, system) in enumerate(commands):
        progress = int(((i + 1) / len(commands)) * 100)

        # Critical moment
        if i == 3:
            update_task_status(
                filename,
                '🔥 ENGINEERING',
                'error',
                progress_percent=progress,
                current_step='⚠️⚠️ CORE BREACH! ⚠️⚠️',
                message='EVACUATE ENGINEERING DECK!',
                needs_attention=True,
                tiny_title='🔥 ENGINE'
            )
            time.sleep(4)

        update_task_status(
            filename,
            '🔥 ENGINEERING',
            'in_progress',
            progress_percent=progress,
            current_step=cmd,
            message=f'{system} responding...',
            tiny_title='🔥 ENGINE'
        )
        time.sleep(random.uniform(1.5, 2.5))

    update_task_status(
        filename,
        '🔥 ENGINEERING',
        'completed',
        progress_percent=100,
        message='Engineering crisis resolved!',
        tiny_title='🔥 ENGINE'
    )

def task_weapons():
    """Weapons control with rapid fire commands"""
    filename = 'weapons.json'

    targets = ['ENEMY SHIP', 'ASTEROID', 'SPACE PIRATE', 'ALIEN VESSEL', 'HOSTILE DRONE']

    update_task_status(
        filename,
        '💥 WEAPONS',
        'in_progress',
        progress_percent=0,
        current_step='POWERING UP WEAPONS',
        message='Charging laser banks...',
        tiny_title='💥 WEAPONS'
    )
    time.sleep(2)

    for i in range(8):
        progress = int(((i + 1) / 8) * 100)
        target = random.choice(targets)

        commands = [
            f'TARGET {target}',
            f'LOCK ONTO {target}',
            f'FIRE AT {target}',
            'RELOAD MISSILES',
            'CHARGE LASER CANNON',
            'ARM TORPEDOES',
        ]

        update_task_status(
            filename,
            '💥 WEAPONS',
            'in_progress',
            progress_percent=progress,
            current_step=random.choice(commands),
            message='PEW PEW PEW! 💥',
            tiny_title='💥 WEAPONS'
        )
        time.sleep(random.uniform(1, 2))

    update_task_status(
        filename,
        '💥 WEAPONS',
        'completed',
        progress_percent=100,
        message='ALL HOSTILES DESTROYED!',
        tiny_title='💥 WEAPONS'
    )

def task_navigation():
    """Navigation with obstacle avoidance"""
    filename = 'navigation.json'

    obstacles = [
        'ASTEROID FIELD',
        'DEBRIS CLOUD',
        'ION STORM',
        'GRAVITY WELL',
        'SPACE ANOMALY',
        'ENEMY MINEFIELD',
        'SOLAR FLARE',
    ]

    for i, obstacle in enumerate(obstacles):
        progress = int(((i + 1) / len(obstacles)) * 100)

        commands = [
            'HARD TO PORT!',
            'DIVE! DIVE! DIVE!',
            'EVASIVE MANEUVERS!',
            'FULL REVERSE!',
            'EMERGENCY TURN!',
            'BARREL ROLL!',
        ]

        update_task_status(
            filename,
            '🎯 NAVIGATION',
            'in_progress',
            progress_percent=progress,
            current_step=f'{random.choice(commands)} - {obstacle}',
            message='HOLD ON TO SOMETHING!',
            tiny_title='🎯 NAV'
        )
        time.sleep(random.uniform(1.2, 2.5))

    update_task_status(
        filename,
        '🎯 NAVIGATION',
        'completed',
        progress_percent=100,
        message='NAVIGATION COMPLETE! Nice flying!',
        tiny_title='🎯 NAV'
    )

def task_crisis_manager():
    """Random crisis events"""
    filename = 'crisis.json'

    for i in range(5):
        crisis = random.choice(CRISES)
        widget = random.choice(WIDGETS)

        update_task_status(
            filename,
            '🚨 CRISIS ALERT',
            'error' if i < 3 else 'blocked',
            progress_percent=20 * (i + 1),
            current_step=f'⚠️ {crisis}! ⚠️',
            message=f'EMERGENCY: {random_command()}!',
            needs_attention=True,
            tiny_title='🚨 CRISIS'
        )
        time.sleep(random.uniform(4, 6))

        update_task_status(
            filename,
            '🚨 CRISIS ALERT',
            'in_progress',
            progress_percent=20 * (i + 1),
            current_step='Crisis averted!',
            message='Phew! That was close!',
            tiny_title='🚨 CRISIS'
        )
        time.sleep(1)

    update_task_status(
        filename,
        '🚨 CRISIS ALERT',
        'completed',
        progress_percent=100,
        message='ALL CRISES RESOLVED! WE SURVIVED!',
        tiny_title='🚨 CRISIS'
    )

def task_shields():
    """Shield management"""
    filename = 'shields.json'

    update_task_status(
        filename,
        '🛡️ SHIELDS',
        'in_progress',
        progress_percent=50,
        current_step='SHIELDS UP',
        message='Deflectors at 50%',
        tiny_title='🛡️ SHIELDS'
    )
    time.sleep(2)

    for i in range(6):
        hit = i + 1
        shield_pct = max(10, 50 - (i * 8))

        update_task_status(
            filename,
            '🛡️ SHIELDS',
            'blocked' if shield_pct < 25 else 'in_progress',
            progress_percent=shield_pct,
            current_step=f'TAKING FIRE! HIT #{hit}',
            message='REROUTE POWER TO SHIELDS!' if shield_pct < 25 else 'Holding...',
            needs_attention=(shield_pct < 25),
            tiny_title='🛡️ SHIELDS'
        )
        time.sleep(2)

    update_task_status(
        filename,
        '🛡️ SHIELDS',
        'completed',
        progress_percent=35,
        message='Enemy retreating! Shields stabilizing.',
        tiny_title='🛡️ SHIELDS'
    )

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 SPACETEAM MISSION SIMULATOR 🚀")
    print("=" * 60)
    print("\nBased on the chaotic cooperative game Spaceteam!")
    print("\n⚠️  PREPARE FOR TECHNOBABBLE CHAOS! ⚠️\n")
    print("Commands like:")
    print("  • SET FOOBAR TO 3!")
    print("  • ENGAGE QUANTUM VAPOR!")
    print("  • REVERSE THE POLARITY!")
    print("  • CALIBRATE HEISENBERG PAD!")
    print("\nWatch your monitor for random crises and emergencies!")
    print("\nDemo will run for ~60-90 seconds.\n")
    print(f"Status files: {MONITOR_DIR}\n")
    print("🎬 LAUNCH SEQUENCE INITIATED...\n")
    time.sleep(1)

    # Start all chaos concurrently
    threads = [
        Thread(target=task_control_panel_1, daemon=True),
        Thread(target=task_control_panel_2, daemon=True),
        Thread(target=task_control_panel_3, daemon=True),
        Thread(target=task_engineering, daemon=True),
        Thread(target=task_weapons, daemon=True),
        Thread(target=task_navigation, daemon=True),
        Thread(target=task_crisis_manager, daemon=True),
        Thread(target=task_shields, daemon=True),
    ]

    for t in threads:
        t.start()
        time.sleep(random.uniform(0.2, 0.6))

    # Wait for mission complete
    for t in threads:
        t.join()

    print("\n" + "=" * 60)
    print("🎉 MISSION SURVIVED! 🎉")
    print("=" * 60)
    print("\nYour ship is held together with duct tape and hope!")
    print("But everyone survived!")
    print("Achievement Unlocked: Space Heroes!\n")
    print(f"Task files will auto-clear after 30 minutes.")
    print(f"To clean up now: rm {MONITOR_DIR}/*.json\n")
