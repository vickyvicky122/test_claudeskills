# Story 1.1: Project Initialization & Basic Script

Status: review

## Story

As a **developer**,
I want **to set up the project structure with dependencies**,
so that **I have a working foundation to build upon**.

## Acceptance Criteria

1. **AC1:** Project directory `lln_explorer/` exists with correct structure
2. **AC2:** `lln_explorer.py` main script file exists (empty skeleton is acceptable)
3. **AC3:** `requirements.txt` contains numpy and matplotlib
4. **AC4:** `output/` directory exists with `.gitkeep` file
5. **AC5:** `.gitignore` file exists with Python standard ignores + output folder
6. **AC6:** `pip install -r requirements.txt` succeeds without errors

## Tasks / Subtasks

- [x] Task 1: Create project directory structure (AC: 1)
  - [x] 1.1: Create `lln_explorer/` root directory
  - [x] 1.2: Create `output/` subdirectory
  - [x] 1.3: Create `output/.gitkeep` empty file

- [x] Task 2: Create requirements.txt (AC: 3, 6)
  - [x] 2.1: Create `requirements.txt` with content:
    ```
    numpy
    matplotlib
    ```
  - [x] 2.2: Verify `pip install -r requirements.txt` succeeds

- [x] Task 3: Create .gitignore (AC: 5)
  - [x] 3.1: Create `.gitignore` with Python standard ignores:
    ```
    # Byte-compiled / optimized / DLL files
    __pycache__/
    *.py[cod]
    *$py.class

    # Virtual environments
    .venv/
    venv/
    ENV/

    # Distribution / packaging
    dist/
    build/
    *.egg-info/

    # IDE
    .idea/
    .vscode/
    *.swp

    # Output directory (generated figures)
    output/*.png
    !output/.gitkeep
    ```

- [x] Task 4: Create main script skeleton (AC: 2)
  - [x] 4.1: Create `lln_explorer.py` with minimal skeleton:
    ```python
    #!/usr/bin/env python3
    """
    LLN Explorer (Lite) - Law of Large Numbers Visualization Tool

    A CLI tool for visualizing the Law of Large Numbers through:
    - Sample path convergence (Strong LLN)
    - Deviation probability decay (Weak LLN)
    - Variance decay with theory overlay
    """

    def main():
        """Main entry point."""
        pass

    if __name__ == '__main__':
        main()
    ```

- [x] Task 5: Verify complete structure (AC: 1-6)
  - [x] 5.1: Run `ls -la lln_explorer/` to confirm all files exist
  - [x] 5.2: Run `pip install -r lln_explorer/requirements.txt` to verify dependencies install
  - [x] 5.3: Run `python lln_explorer/lln_explorer.py` to verify script executes without error

## Dev Notes

### Architecture Compliance

- **Single-file implementation** per NFR7 — all code goes in `lln_explorer.py`
- **Python 3.14** required per Architecture decision
- **Dependencies:** NumPy + Matplotlib only (NFR6)
- **No starter template** — build from scratch per Architecture

### Project Structure (from Architecture)

```
lln_explorer/
├── lln_explorer.py          # Main script (single file)
├── requirements.txt         # numpy, matplotlib
├── .gitignore               # Python gitignore
└── output/                  # Default output directory (gitignored)
    └── .gitkeep
```

**Note:** README.md, LICENSE, and tests/ are optional for this story. Focus on minimal viable structure.

### File Organization Pattern (Top-Down)

The `lln_explorer.py` skeleton should follow this section order (to be filled in later stories):
1. Imports
2. Constants (DEFAULT_M, DEFAULT_N, etc.)
3. Distribution dictionary (DISTRIBUTIONS)
4. Simulation functions
5. Plot functions
6. CLI setup (parse_args, validate_args)
7. Main orchestration
8. Entry point

### PEP 8 Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Functions | snake_case | `plot_sample_paths()` |
| Variables | snake_case | `running_mean` |
| Constants | UPPER_CASE | `DEFAULT_M` |

### References

- [Source: docs/planning-artifacts/architecture.md#Project-Structure]
- [Source: docs/planning-artifacts/architecture.md#Initialization-Command]
- [Source: docs/planning-artifacts/epics.md#Story-1.1]
- [GitHub Issue: #2](https://github.com/vickyvicky122/test_claudeskills/issues/2)

## Dev Agent Record

### Agent Model Used

Claude Opus 4.5 (claude-opus-4-5-20251101)

### Debug Log References

- pip install required venv due to PEP 668 restrictions on system Python
- Created .venv in lln_explorer/ directory for dependency isolation

### Completion Notes List

- All 5 tasks completed successfully
- Project structure matches architecture specification
- Dependencies install correctly in virtual environment
- Main script skeleton executes without error
- All acceptance criteria satisfied (AC1-AC6)

### File List

- `lln_explorer/` (directory created)
- `lln_explorer/lln_explorer.py` (main script skeleton)
- `lln_explorer/requirements.txt` (numpy, matplotlib)
- `lln_explorer/.gitignore` (Python standard ignores)
- `lln_explorer/output/` (directory created)
- `lln_explorer/output/.gitkeep` (empty placeholder)
- `lln_explorer/.venv/` (virtual environment - gitignored)
