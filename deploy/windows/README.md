# Windows service wrapper — SVC-02

PhrexIntelligence.xml is a review-only WinSW configuration template, not an installable release. No wrapper binary is bundled. Select and verify a pinned upstream WinSW release and validate its XML schema before installation. The executable and launcher paths are proposed layout, not existing host paths. The current launcher expects a repository-local venv and user-specific data; service compatibility requires subsequent changes and tests.

The wrapper template deliberately uses Manual startup and omits service account credentials and recovery actions. Do not install this template: omitted identity may default to LocalSystem. Installation utilities must explicitly configure a least-privilege identity before first start, restrict ACLs, validate paths and enforce mutually exclusive activation with the existing scheduled task. Final automatic delayed startup and bounded restart policy are deferred until acceptance. Never put tokens or passwords in this XML. Wrapper logs must be restricted and reviewed for secret leakage. The 30-second stop timeout is provisional; child-process shutdown and SQLite integrity require testing.

Proposed layout: administrator-controlled installation root containing wrapper executable/XML, app code and a dedicated runtime; restricted ProgramData data/log directories. Actual paths and runtime provisioning remain pending. No host changes are authorized by this template.

Track limitations under D01-D03, D18 and D19. See docs/WINDOWS_SERVICE.md.
