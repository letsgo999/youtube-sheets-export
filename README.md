# YouTube → Google Sheets 자동화 스크립트

목적: 특정 키워드로 유튜브에서 최근 영상을 검색해 조회수가 특정 기준(예: 1,000) 이상인 영상만 골라 Google Sheets로 저장합니다.

주요 파일
- `main.py` : 유튜브 검색 → 필터 → 구글 시트 기록의 핵심 로직
- `requirements.txt` : 필요한 파이썬 패키지 목록
- `.env.example` : 설정 예시
- `run.ps1` : PowerShell 예제 실행 스크립트
- `tests/test_filter.py` : 간단한 유닛 테스트

빠른 시작
1) 필요한 라이브러리 설치
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Google API 준비
- YouTube Data API (API Key) 생성 → `YT_API_KEY`
- Google Cloud에서 서비스 계정 생성 → JSON 키 파일을 다운로드하고 `SERVICE_ACCOUNT_FILE` 경로로 지정
- Google Sheets에서 새 스프레드시트를 만들고, 서비스 계정 이메일을 편집자 권한으로 추가 → `SHEET_ID` 사용

3) 환경 변수 설정(.env)
- `YT_API_KEY`, `SERVICE_ACCOUNT_FILE`, `SHEET_ID`, `MIN_VIEWS`(예:1000), `KEYWORD`, `MAX_RESULTS` 등

4) 실행
```powershell
# PowerShell 예제
python main.py --keyword "입력할 키워드" --min-views 1000
```

보안 주의
- 서비스 계정 JSON과 API 키는 절대 공개 저장소에 올리지 마세요.
- 테스트 시에는 별도 테스트 시트를 만들어 사용하세요.

문의 및 확장 아이디어
- 정기 스케줄링(윈도우 태스크 스케줄러, 크론, 또는 Cloud Functions) 추가
- 필터 조건(조회수, 업로드 일자 범위, 채널 제외/포함) 확장
- 결과를 CSV/Slack으로도 전송
