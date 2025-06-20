# Install DeepSeek Browser Automation dependencies on Windows
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  Write-Error "Python 3 is required"
  exit 1
}
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

