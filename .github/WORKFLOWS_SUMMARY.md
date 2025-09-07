# GitHub Actions Workflows Summary

## Overview

The Task Tracker project now has two GitHub Actions workflows that provide comprehensive CI/CD automation:

## 1. Build and Release (`build-release.yml`)

### Triggers:
- **Master Branch Push**: Every push to master branch
- **Version Tags**: Tags matching `v*` pattern (e.g., `v1.0.0`, `v1.2.3`)
- **Manual Dispatch**: Can be triggered manually from GitHub Actions UI

### Behavior by Trigger:

#### Master Branch Pushes:
- ✅ Builds executables for Ubuntu 20.04, 22.04, 24.04
- ✅ Compresses with UPX
- ✅ Uploads artifacts named `task-tracker-ubuntu-XX.XX-dev`
- ✅ Artifacts retained for 7 days
- ❌ **No release created** (development builds only)

#### Version Tags:
- ✅ Builds executables for Ubuntu 20.04, 22.04, 24.04
- ✅ Compresses with UPX
- ✅ Uploads artifacts named `task-tracker-ubuntu-XX.XX`
- ✅ Artifacts retained for 30 days
- ✅ **Creates GitHub release** with all executables attached
- ✅ Auto-generates release notes

#### Manual Dispatch:
- Same as version tags
- User specifies version number in UI

### Build Matrix:
```yaml
ubuntu-version: ['20.04', '22.04', '24.04']
```

### Artifacts Created:
- `task-tracker` - Universal executable (Ubuntu 22.04 base)
- `task-tracker-ubuntu-20.04` - LTS compatibility
- `task-tracker-ubuntu-22.04` - Current LTS
- `task-tracker-ubuntu-24.04` - Latest LTS

## 2. Test Build (`test-build.yml`)

### Triggers:
- **Branch Pushes**: `main`, `develop` branches (excludes master)
- **Pull Requests**: PRs targeting `main`, `master`, `develop`

### Behavior:
- ✅ Single Ubuntu latest build
- ✅ Tests build process
- ✅ Verifies executable runs
- ✅ Uploads test artifact for 7 days
- ❌ No release created

## Workflow Coordination

- **master branch**: Handled by `build-release.yml` (development builds)
- **main/develop branches**: Handled by `test-build.yml` (test builds)
- **Pull requests**: Handled by `test-build.yml` (validation)
- **Version tags**: Handled by `build-release.yml` (releases)

## Development Workflow

1. **Feature Development**: Work on feature branches
2. **Pull Request**: Create PR to master → triggers test build
3. **Merge to Master**: Merge PR → triggers development build
4. **Test**: Download dev artifacts from GitHub Actions
5. **Release**: Create version tag → triggers release build

## Release Process

### Automatic:
```bash
git tag v1.0.0
git push origin v1.0.0
```

### Manual:
1. Go to Actions tab
2. Select "Build and Release"
3. Click "Run workflow"
4. Enter version (e.g., `v1.0.1`)
5. Click "Run workflow"

## Artifact Management

| Trigger | Artifact Name | Retention | Release Created |
|---------|---------------|-----------|-----------------|
| Master push | `task-tracker-ubuntu-XX.XX-dev` | 7 days | No |
| Version tag | `task-tracker-ubuntu-XX.XX` | 30 days | Yes |
| Manual dispatch | `task-tracker-ubuntu-XX.XX` | 30 days | Yes |
| Test branches | `test-build-task-tracker` | 7 days | No |

## System Requirements (for builds)

All builds require:
- Ubuntu runner with GTK4 system libraries
- Python 3.12
- PyInstaller
- UPX compression
- wmctrl (for always-on-top functionality)

## Security

- Uses `GITHUB_TOKEN` for release creation
- No external secrets required
- All dependencies installed from official repositories