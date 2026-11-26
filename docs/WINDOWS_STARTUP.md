# Windows startup configuration (RT-03)

Manual, user-authorized installation only. Do not register or start the task until duplicate-instance protection and recovery acceptance are complete.

In Windows Task Scheduler, choose Create Task (not Create Basic Task).

- General: name CodePhrex Phrex; select your own Windows account; Run only when user is logged on; leave Run with highest privileges unchecked.
- Triggers: At log on, specific user (your account).
- Actions: Start a program. Program: absolute path to the repository's .venv\Scripts\pythonw.exe. Arguments: runtime_launcher.py. Start in: absolute repository directory (without surrounding quotes).
- Conditions: review battery and network preferences; allow operation on battery only if desired.
- Settings: allow on-demand run; do not start a new instance if already running; disable the execution time limit. Restart-on-failure settings will be validated in RT-05.
- Save the task only after the runtime acceptance gate. No stored password or elevated account is required.

## Verification
Confirm the task action points to the reviewed local repository, stop any existing foreground instance, start the task on demand, inspect task status and lifecycle logs, and test /phrex status in Slack. Check that inventory timestamps advance. A running task alone is not proof of Slack connectivity.

## Removal
Disable the task, end the task, verify its child process has exited, and delete the task if desired. Preserve .env and the project database.

## Known limitations
pythonw removes the console window; lifecycle logs do not capture child application output. Task Scheduler's instance policy does not prevent manual launches. This configuration starts at sign-in, not before sign-in, and does not operate while the computer is asleep or powered off. This document does not install anything.
