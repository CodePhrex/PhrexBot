# SVC-03 deployment lifecycle

The read-only Test-PhrexServiceDeployment.ps1 utility reports expected file presence and observed service/task state. It never installs, stops, starts or removes anything. Missing or inaccessible service/task state is not proof of absence. File presence does not establish integrity, ACL safety or readiness. No secrets are read. Run only against the intended installation directory.

## Installation contract
Future installer must validate pinned wrapper provenance, protected paths and runtime compatibility; require administrator authorization; provision explicit least-privilege identity and restricted data access; securely back up persistent data; require verified exclusive activation; register service without starting it until configuration is validated. Abort on uncertainty. Never use implicit LocalSystem or embed credentials. Preserve the current task until migration approval.

## Removal contract
Future removal utility must verify exact service identity and installation ownership, obtain explicit approval, stop service gracefully and verify child exit before unregistering. Preserve databases, logs and credentials by default. Never recursively delete an arbitrary supplied path. Restore the previous scheduled task only after service exit and explicit rollback approval.

## Pending implementation
Mutating installer/uninstaller, wrapper integrity verification, ACL validation, service-compatible launcher, automated tests and live acceptance remain deferred until SVC-04 through SVC-08. Track under D01-D03/D18/D19. This milestone provides preflight and lifecycle specification only.
