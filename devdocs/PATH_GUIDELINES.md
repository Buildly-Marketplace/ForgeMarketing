# Filesystem Path Guidelines

## Overview
This document provides guidelines for handling filesystem paths in ForgeMarketing to ensure cross-platform compatibility, portability, and production readiness.

## ❌ Anti-Patterns (Never Do This)

### 1. Hardcoded Absolute Paths
```python
# ❌ BAD - User-specific path
db_path = "/Users/greglind/Projects/Sales and Marketing/data/db.sqlite"

# ❌ BAD - Windows-specific path  
data_dir = "C:\\Projects\\ForgeMarketing\\data"

# ❌ BAD - Unix-specific path
workspace = "/home/user/workspace"
```

**Problems:**
- Not portable across machines
- Breaks in production environments
- Not cross-platform compatible
- Requires manual changes for each deployment

### 2. String-Based Path Construction
```python
# ❌ BAD - Platform-specific separators
path = base_dir + "/" + "data" + "/" + "file.txt"

# ❌ BAD - Manual path joining
path = f"{base_dir}/data/file.txt"
```

**Problems:**
- Fails on Windows (uses `\` not `/`)
- Doesn't handle edge cases (double slashes, etc.)
- Not cross-platform

### 3. Relative Paths Without Context
```python
# ❌ BAD - Depends on current working directory
with open('data/file.txt', 'r') as f:
    content = f.read()
```

**Problems:**
- Breaks when script run from different directory
- Unpredictable in cron jobs or services
- Hard to debug

## ✅ Best Practices

### 1. Use Project-Relative Paths
```python
from pathlib import Path

# ✅ GOOD - Relative to current file
project_root = Path(__file__).parent.parent
data_dir = project_root / 'data'
db_path = project_root / 'data' / 'database.db'
```

**Benefits:**
- Works from any directory
- Portable across machines
- Cross-platform compatible

### 2. Use Environment Variables for Configuration
```python
import os
from pathlib import Path

# ✅ GOOD - Configurable via environment
project_root = Path(os.getenv('PROJECT_ROOT', Path(__file__).parent.parent))
db_path = os.getenv('DATABASE_PATH', str(project_root / 'data' / 'database.db'))
workspace_root = os.getenv('WORKSPACE_ROOT', str(project_root))
```

**Benefits:**
- Different paths for dev/staging/production
- No code changes needed for deployment
- Easy to override in docker/k8s

### 3. Accept Paths as Parameters
```python
from pathlib import Path
import os

class DataManager:
    def __init__(self, data_dir=None, db_path=None):
        """
        Initialize with configurable paths
        
        Args:
            data_dir: Directory for data files (default: project_root/data)
            db_path: Database file path (default: data_dir/database.db)
        """
        project_root = Path(__file__).parent.parent
        
        # Use parameter, env var, or default (in that order)
        if data_dir:
            self.data_dir = Path(data_dir)
        elif os.getenv('DATA_DIR'):
            self.data_dir = Path(os.getenv('DATA_DIR'))
        else:
            self.data_dir = project_root / 'data'
        
        if db_path:
            self.db_path = Path(db_path)
        elif os.getenv('DATABASE_PATH'):
            self.db_path = Path(os.getenv('DATABASE_PATH'))
        else:
            self.db_path = self.data_dir / 'database.db'
```

**Benefits:**
- Maximum flexibility
- Testable with custom paths
- Production-ready
- Backward compatible

### 4. Use pathlib.Path for All Path Operations
```python
from pathlib import Path

# ✅ GOOD - Use Path objects
project_root = Path(__file__).parent.parent
config_file = project_root / 'config' / 'settings.yaml'

# Check if exists
if config_file.exists():
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

# Create directories
output_dir = project_root / 'output' / 'reports'
output_dir.mkdir(parents=True, exist_ok=True)

# Iterate files
for file in (project_root / 'data').glob('*.json'):
    process_file(file)
```

**Benefits:**
- Object-oriented API
- Cross-platform
- Readable and maintainable
- Built-in path operations

## 🔧 Common Patterns

### Pattern 1: Project-Root Detection
```python
from pathlib import Path

# Option 1: Relative to current file
project_root = Path(__file__).parent.parent

# Option 2: Relative to current file (deeper nesting)
project_root = Path(__file__).parent.parent.parent

# Option 3: Search upward for marker file
def find_project_root(marker='.git'):
    current = Path(__file__).parent
    while current != current.parent:
        if (current / marker).exists():
            return current
        current = current.parent
    return Path(__file__).parent.parent  # fallback

project_root = find_project_root()
```

### Pattern 2: Configuration Hierarchy
```python
import os
from pathlib import Path

def get_config_path(config_name='config.yaml'):
    """
    Search for config in order:
    1. Environment variable
    2. Current directory
    3. User home directory
    4. Project root
    """
    # 1. Environment variable
    if os.getenv('CONFIG_PATH'):
        return Path(os.getenv('CONFIG_PATH'))
    
    # 2. Current directory
    cwd_config = Path.cwd() / config_name
    if cwd_config.exists():
        return cwd_config
    
    # 3. User home
    home_config = Path.home() / '.forgemarketing' / config_name
    if home_config.exists():
        return home_config
    
    # 4. Project root
    project_root = Path(__file__).parent.parent
    return project_root / 'config' / config_name
```

### Pattern 3: Data Directory Management
```python
from pathlib import Path
import os

class DataDirectory:
    """Manages data directory with configurable location"""
    
    def __init__(self, base_dir=None):
        if base_dir:
            self.base = Path(base_dir)
        elif os.getenv('DATA_DIR'):
            self.base = Path(os.getenv('DATA_DIR'))
        else:
            project_root = Path(__file__).parent.parent
            self.base = project_root / 'data'
        
        # Create subdirectories
        self.databases = self.base / 'databases'
        self.reports = self.base / 'reports'
        self.cache = self.base / 'cache'
        self.logs = self.base / 'logs'
        
        # Ensure directories exist
        for directory in [self.databases, self.reports, self.cache, self.logs]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_db_path(self, db_name):
        """Get path to database file"""
        return self.databases / db_name
    
    def get_report_path(self, report_name):
        """Get path to report file"""
        return self.reports / report_name
```

## 🌍 Environment Variables

### Standard Environment Variables
```bash
# Project root directory
PROJECT_ROOT=/var/www/forgemarketing

# Data directory
DATA_DIR=/var/www/forgemarketing/data

# Database paths
DATABASE_PATH=/var/www/forgemarketing/data/database.db
UNIFIED_DB_PATH=/var/www/forgemarketing/data/unified_outreach.db

# Workspace root (for legacy code)
WORKSPACE_ROOT=/var/www/forgemarketing

# Log directory
LOG_DIR=/var/log/forgemarketing

# Temporary files
TEMP_DIR=/tmp/forgemarketing
```

### Setting Environment Variables

**Development (.env file):**
```bash
PROJECT_ROOT=/Users/yourname/Projects/ForgeMarketing
DATA_DIR=/Users/yourname/Projects/ForgeMarketing/data
```

**Production (systemd):**
```ini
[Service]
Environment="PROJECT_ROOT=/var/www/forgemarketing"
Environment="DATA_DIR=/var/www/forgemarketing/data"
```

**Docker:**
```yaml
environment:
  - PROJECT_ROOT=/app
  - DATA_DIR=/app/data
```

## 🧪 Testing with Custom Paths

```python
import pytest
from pathlib import Path
import tempfile

def test_data_manager_with_custom_path():
    """Test DataManager with custom temporary directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = DataManager(data_dir=tmpdir)
        
        # Test operations
        test_file = manager.data_dir / 'test.txt'
        test_file.write_text('test data')
        
        assert test_file.exists()
        assert test_file.read_text() == 'test data'

def test_with_environment_variable(monkeypatch):
    """Test with environment variable"""
    test_dir = '/tmp/test_forgemarketing'
    monkeypatch.setenv('DATA_DIR', test_dir)
    
    manager = DataManager()
    assert str(manager.data_dir) == test_dir
```

## 📝 Migration Checklist

When converting code with hardcoded paths:

- [ ] Identify all hardcoded absolute paths
- [ ] Replace with `Path(__file__).parent...` pattern
- [ ] Add environment variable fallback
- [ ] Add optional constructor parameter
- [ ] Update documentation
- [ ] Add tests with custom paths
- [ ] Update deployment scripts
- [ ] Update .env.example

## 🛠️ Tools

### Path Audit Script
```bash
# Run path audit to find hardcoded paths
python3 ops/path_audit.py
```

### Quick Fix Template
```python
# Before
class MyClass:
    def __init__(self):
        self.db_path = "/Users/user/project/data/db.sqlite"

# After
from pathlib import Path
import os

class MyClass:
    def __init__(self, db_path=None):
        if db_path:
            self.db_path = Path(db_path)
        elif os.getenv('DATABASE_PATH'):
            self.db_path = Path(os.getenv('DATABASE_PATH'))
        else:
            project_root = Path(__file__).parent.parent
            self.db_path = project_root / 'data' / 'db.sqlite'
```

## 📚 References

- Python pathlib documentation: https://docs.python.org/3/library/pathlib.html
- Cross-platform paths: https://docs.python.org/3/library/os.path.html
- Environment variables: https://docs.python.org/3/library/os.html#os.environ

## 🎯 Summary

**Golden Rules:**
1. **Never hardcode absolute paths**
2. **Always use pathlib.Path**
3. **Make paths configurable via environment variables**
4. **Use project-relative paths as defaults**
5. **Test with custom paths**

Following these guidelines ensures ForgeMarketing is:
- ✅ Portable across environments
- ✅ Cross-platform compatible
- ✅ Production-ready
- ✅ Easy to deploy
- ✅ Testable
