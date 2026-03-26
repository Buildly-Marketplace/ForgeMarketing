# Cleanup Scripts

This directory contains maintenance and cleanup scripts for the Marketing Automation System.

## Current Scripts

### `cleanup_github_pages.py`
- **Purpose**: Clean up GitHub Pages related files and configurations
- **Usage**: `python scripts/cleanup/cleanup_github_pages.py`
- **Description**: Removes outdated GitHub Pages files, configurations, and artifacts

## Adding New Cleanup Scripts

When adding new cleanup scripts:

1. Use descriptive names with `cleanup_` prefix
2. Include proper documentation and usage instructions
3. Add error handling and dry-run modes when possible  
4. Test thoroughly before running on production data
5. Update this README with script descriptions

## Best Practices

- Always backup important data before running cleanup scripts
- Use `--dry-run` flags when available to preview changes
- Log cleanup actions for audit trails
- Include confirmation prompts for destructive operations
- Test scripts in development environment first