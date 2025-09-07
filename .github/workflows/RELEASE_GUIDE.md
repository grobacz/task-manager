# GitHub Release Guide

## Automatic Workflows

### Master Branch Builds
Every push to the `master` branch will:
1. Build executables for Ubuntu 20.04, 22.04, and 24.04
2. Compress executables with UPX
3. Upload development artifacts (retained for 7 days)
4. **No release is created** - artifacts only for testing

### Release Creation

#### Method 1: Git Tag (Recommended)
```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

This will automatically:
1. Trigger the GitHub Actions workflow
2. Build executables for Ubuntu 20.04, 22.04, and 24.04
3. Compress executables with UPX
4. Create a GitHub release with all files attached
5. Retain artifacts for 30 days

#### Method 2: Manual Workflow Dispatch
1. Go to the **Actions** tab in your GitHub repository
2. Select the **Build and Release** workflow
3. Click **Run workflow**
4. Enter the version number (e.g., `v1.0.1`)
5. Click **Run workflow**

## Development Workflow

### Testing Changes
1. Push to `master` branch
2. GitHub Actions will build executables automatically
3. Download artifacts from the Actions tab for testing
4. Artifacts are named `task-tracker-ubuntu-XX.XX-dev`
5. Test thoroughly before creating a release

## Troubleshooting

### Build Failures

**Common Issue**: `ModuleNotFoundError: No module named 'gi'`
- **Cause**: GTK4 system packages not properly installed or accessible
- **Solution**: The build script automatically detects CI environments and handles this

**Build Script Features**:
- **Local builds**: Uses virtual environment with system site packages
- **CI builds**: Uses system Python directly with `--break-system-packages` flag
- **Automatic detection**: Checks `CI` and `GITHUB_ACTIONS` environment variables

## Release Artifacts

Each release will include:
- `task-tracker` - Universal executable (Ubuntu 22.04 base, works on most systems)
- `task-tracker-ubuntu-20.04` - Compatibility for older systems  
- `task-tracker-ubuntu-22.04` - Standard LTS version
- `task-tracker-ubuntu-24.04` - Latest LTS version

## Testing Releases

Before creating a release, test locally:
```bash
# Create test release package
./release.sh v1.0.0-test

# Test the executable
cd release-v1.0.0-test
./task-tracker
```

## Version Numbering

Use semantic versioning:
- `v1.0.0` - Major release
- `v1.1.0` - Minor release (new features)
- `v1.0.1` - Patch release (bug fixes)
- `v1.0.0-beta.1` - Pre-release

## Release Notes

The GitHub Actions workflow automatically generates release notes with:
- Download instructions
- System requirements  
- Feature list
- Installation guide

To customize release notes, edit the `body:` section in `.github/workflows/build-release.yml`.