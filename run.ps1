# PowerShell 실행 예시
# 가상환경 활성화 후 아래처럼 실행하세요
# .\.venv\Scripts\Activate.ps1

$env:YT_API_KEY = "YOUR_YT_KEY"
$env:SERVICE_ACCOUNT_FILE = "C:\path\to\service-account.json"
$env:SHEET_ID = "YOUR_SHEET_ID"
python main.py --keyword "tutorial" --min-views 1000 --max-results 25
