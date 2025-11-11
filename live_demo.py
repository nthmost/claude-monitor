#!/usr/bin/env python3
"""
Live demo script that simulates multiple concurrent tasks updating in real-time
"""
import json
import time
import random
from pathlib import Path
from datetime import datetime, timezone
from threading import Thread

MONITOR_DIR = Path.home() / '.claude' / 'monitor'
MONITOR_DIR.mkdir(parents=True, exist_ok=True)

def update_task_status(filename, task_name, status, progress_percent=None,
                       current_step=None, message=None, needs_attention=False):
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

    with open(MONITOR_DIR / filename, 'w') as f:
        json.dump(data, f, indent=2)

def task_training():
    """Simulate a training task"""
    filename = 'ml-training.json'
    for epoch in range(1, 51):
        progress = int((epoch / 50) * 100)
        loss = 1.5 - (epoch * 0.025) + random.uniform(-0.05, 0.05)
        acc = 50 + (epoch * 0.8) + random.uniform(-2, 2)

        update_task_status(
            filename,
            'Training Image Classifier',
            'in_progress',
            progress_percent=progress,
            current_step=f'Epoch {epoch}/50',
            message=f'Loss: {loss:.4f}, Accuracy: {acc:.1f}%'
        )
        time.sleep(0.5)

    update_task_status(
        filename,
        'Training Image Classifier',
        'completed',
        progress_percent=100,
        message='Model saved to models/classifier_v2.pth'
    )

def task_download():
    """Simulate a download task"""
    filename = 'file-download.json'
    total_mb = 2500

    for mb in range(0, total_mb, 50):
        progress = int((mb / total_mb) * 100)
        speed = random.uniform(8, 25)

        update_task_status(
            filename,
            'Downloading Dataset',
            'in_progress',
            progress_percent=progress,
            current_step=f'{mb}/{total_mb} MB',
            message=f'{speed:.1f} MB/s'
        )
        time.sleep(0.3)

    update_task_status(
        filename,
        'Downloading Dataset',
        'completed',
        progress_percent=100,
        message='Download complete: dataset.tar.gz'
    )

def task_tests():
    """Simulate running tests with occasional failures"""
    filename = 'test-suite.json'
    total_tests = 847

    for test in range(1, total_tests + 1):
        progress = int((test / total_tests) * 100)

        # Simulate a failure partway through
        if test == 623:
            update_task_status(
                filename,
                'Running Test Suite',
                'error',
                progress_percent=progress,
                current_step=f'Test {test}/{total_tests}',
                message='FAILED: test_api_authentication - 401 Unauthorized',
                needs_attention=True
            )
            time.sleep(3)
            # "Fix" the issue and continue
            update_task_status(
                filename,
                'Running Test Suite',
                'in_progress',
                progress_percent=progress,
                current_step=f'Test {test}/{total_tests}',
                message='Resuming after fix...'
            )
            time.sleep(1)
        else:
            update_task_status(
                filename,
                'Running Test Suite',
                'in_progress',
                progress_percent=progress,
                current_step=f'Test {test}/{total_tests}'
            )

        time.sleep(0.05)

    update_task_status(
        filename,
        'Running Test Suite',
        'completed',
        progress_percent=100,
        message='All tests passed! ✓'
    )

def task_build():
    """Simulate a build process"""
    filename = 'docker-build.json'

    steps = [
        ('Pulling base image', 8),
        ('Installing system dependencies', 15),
        ('Copying source files', 5),
        ('Installing Python packages', 20),
        ('Compiling assets', 12),
        ('Running security scan', 10),
        ('Optimizing layers', 8),
        ('Tagging image', 2),
    ]

    total_progress = 0
    for step_name, duration in steps:
        chunks = duration * 2
        for i in range(chunks + 1):
            step_progress = int((i / chunks) * 100)
            total_progress = int((sum(d for _, d in steps[:steps.index((step_name, duration))]) +
                                 (duration * i / chunks)) / sum(d for _, d in steps) * 100)

            update_task_status(
                filename,
                'Building Docker Image',
                'in_progress',
                progress_percent=total_progress,
                current_step=f'{step_name} ({step_progress}%)'
            )
            time.sleep(0.3)

    update_task_status(
        filename,
        'Building Docker Image',
        'completed',
        progress_percent=100,
        message='Image: myapp:v2.3.1 (1.2 GB)'
    )

def task_database():
    """Simulate a database operation that gets blocked"""
    filename = 'db-migration.json'

    update_task_status(
        filename,
        'Running Database Migration',
        'in_progress',
        progress_percent=0,
        current_step='Backing up existing data'
    )
    time.sleep(2)

    for i in range(1, 8):
        update_task_status(
            filename,
            'Running Database Migration',
            'in_progress',
            progress_percent=i * 10,
            current_step=f'Applying migration {i}/12'
        )
        time.sleep(1)

    # Simulate getting blocked
    update_task_status(
        filename,
        'Running Database Migration',
        'blocked',
        progress_percent=60,
        current_step='Migration 8/12',
        message='Foreign key constraint conflict in users table',
        needs_attention=True
    )
    time.sleep(5)

    # Resume after "user intervention"
    update_task_status(
        filename,
        'Running Database Migration',
        'in_progress',
        progress_percent=60,
        current_step='Resuming migration 8/12',
        message='Constraint resolved, continuing...'
    )
    time.sleep(1)

    for i in range(8, 13):
        update_task_status(
            filename,
            'Running Database Migration',
            'in_progress',
            progress_percent=50 + (i * 4),
            current_step=f'Applying migration {i}/12'
        )
        time.sleep(1)

    update_task_status(
        filename,
        'Running Database Migration',
        'completed',
        progress_percent=100,
        message='Migrated 287,543 records successfully'
    )

def task_data_processing():
    """Simulate batch data processing"""
    filename = 'data-processor.json'
    total_batches = 150

    for batch in range(1, total_batches + 1):
        progress = int((batch / total_batches) * 100)
        records = random.randint(800, 1200)

        update_task_status(
            filename,
            'Processing Customer Data',
            'in_progress',
            progress_percent=progress,
            current_step=f'Batch {batch}/{total_batches}',
            message=f'{records} records/batch'
        )
        time.sleep(0.2)

    update_task_status(
        filename,
        'Processing Customer Data',
        'completed',
        progress_percent=100,
        message='Processed 152,394 customer records'
    )

if __name__ == '__main__':
    print("🚀 Starting live demo with multiple concurrent tasks...")
    print("Watch your monitor! Tasks will run for about 60-90 seconds.\n")

    # Start all tasks concurrently
    threads = [
        Thread(target=task_training, daemon=True),
        Thread(target=task_download, daemon=True),
        Thread(target=task_tests, daemon=True),
        Thread(target=task_build, daemon=True),
        Thread(target=task_database, daemon=True),
        Thread(target=task_data_processing, daemon=True),
    ]

    for t in threads:
        t.start()
        time.sleep(0.5)  # Stagger starts slightly

    # Wait for all to complete
    for t in threads:
        t.join()

    print("\n✅ Demo complete! All tasks finished.")
    print(f"\nTask files are in: {MONITOR_DIR}")
    print("They will auto-clear from the monitor after 30 minutes.")
    print(f"\nTo clean up now: rm {MONITOR_DIR}/*.json")
