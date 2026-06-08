Push helper
===============

This folder contains a PowerShell helper to flatten a nested `e_mobix` repo (remove the nested `.git`), amend the initial commit, and push the repository to GitHub.

Usage (PowerShell from the project root):

```powershell
.\	ools\push_to_github.ps1
```

Or provide the remote URL as an argument:

```powershell
.\tools\push_to_github.ps1 https://github.com/<you>/<repo>.git
```

Notes:
- The script assumes `git` is installed and available on the PATH.
- Review the script before running. Backup your repo if unsure.
