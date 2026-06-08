param(
    [string]$RemoteUrl
)

if (-not $RemoteUrl) {
    $RemoteUrl = Read-Host "Enter remote repository URL (e.g. https://github.com/you/repo.git)"
}

Write-Host ('About to remove nested e_mobix/.git, amend the commit, and push to {0}' -f $RemoteUrl) -ForegroundColor Yellow
$confirm = Read-Host 'Proceed? (y/N)'
if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Host 'Aborted.'
    exit 1
}

if (Test-Path -Path 'e_mobix\.git') {
    Write-Host 'Removing nested e_mobix\.git...'
    Remove-Item -Recurse -Force 'e_mobix\.git'
} else {
    Write-Host 'No nested e_mobix\.git found - continuing...'
}

Write-Host 'Staging all changes...'
git add -A

Write-Host 'Amending initial commit (will reuse commit message)...'
git commit --amend --no-edit

if (-not $RemoteUrl) {
    Write-Host 'No remote URL provided.'
    exit 1
}

Write-Host 'Adding remote origin (or updating URL if it exists)...'
$existing = git remote
if ($LASTEXITCODE -ne 0) {
    Write-Host 'git remote failed; ensure git is installed and this is a git repo'
    exit 1
}

if ($existing -match 'origin') {
    git remote set-url origin $RemoteUrl
} else {
    git remote add origin $RemoteUrl
}

Write-Host "Setting branch to 'main' and pushing..."
git branch -M main
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host 'Push completed.' -ForegroundColor Green
} else {
    Write-Host 'Push failed. Check git output above.' -ForegroundColor Red
}
