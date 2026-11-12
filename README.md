# 국내주식 퀀트 자동매매 — 개발환경 구축 매뉴얼 (v0.1)

> 학습용 DEMO입니다. 현재 실거래·모의투자 주문 모두 전송하지 않습니다. 종목 및 점수는 가상 데이터입니다.

## 1. 사전 준비 (Windows 10/11)
Python 3.13, Git, VS Code(Python 확장), MySQL 8.0.x, MySQL Workbench 8 설치. PowerShell에서 확인:

```powershell
py --version
git --version
mysql --version
```

## 2. 소스코드 다운로드
```powershell
mkdir C:\programs\works -Force
cd C:\programs\works
git clone https://github.com/itlects/202611_stock_quent_trader.git
cd 202611_stock_quent_trader
```

## 3. Python 가상환경 구성
```powershell
py -3.13 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

VS Code에서 'Python: Select Interpreter' → 프로젝트의 .venv\Scripts\python.exe 선택.

## 4. 개발 서버 실행
```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

- 상태 확인 http://127.0.0.1:8000/health
- Swagger 문서 http://127.0.0.1:8000/docs
- 후보 확인 http://127.0.0.1:8000/api/candidates
- 선택 현황 http://127.0.0.1:8000/api/selection

정상 상태는 `orders_enabled:false`입니다.

## 5. 사용자 승인 및 자동 선정 실습
Swagger POST /api/selection → Try it out → Execute:

B. 사용자 승인:
```json
{"mode":"approval","codes":["DEMO001","DEMO002"]}
```

A. 전체 자동 선정(예제는 80점 이상 가상 종목):
```json
{"mode":"auto","codes":[]}
```

GET /api/selection에서 결과 확인. 이 단계는 '선정'만 수행하고 주문은 보내지 않습니다.

## 6. MySQL 기초 스키마 준비
Workbench에서 `sql/01_schema.sql`을 열고 실행합니다. CLI를 사용할 때 Windows CMD에서:
```cmd
mysql -u root -p < sql\01_schema.sql
```

테이블: `quant_candidates`, `trade_audit`. **현재 API는 MySQL에 연결하지 않는 독립 실행 데모**이고 DB 연계는 다음 단계입니다.

## 7. 테스트
```powershell
python -m pytest -q
```

## 8. 서비스 운영 서버(차기 구축)
개발 서버: localhost + --reload / 운영 서버: 비밀키 별도 보관 + 인증/접근통제 + HTTPS 리버스 프록시 + 로그/장애 알림 + 실행 프로세스 관리자. 실제 주문 API는 모의투자 검증과 위험관리(주문 한도·중복 방지·긴급 중단·체결 점검) 이후 분리 배포합니다. 외부 공개는 아직 금지합니다.

## 9. 보안
.env 및 API 키·계좌정보를 GitHub에 커밋하지 않습니다. 실거래 주문을 활성화하지 않습니다. FastAPI Swagger를 외부 인터넷에 공개하지 않습니다.

## 10. 이어질 단계
키움 REST 인증 및 시세 데이터 수집 → MySQL 저장 → 퀀트 팩터 → 승인 UI → 백테스트 → 모의주문 엔진 → 운영 서버. 

- Notion: https://app.notion.com/p/416b2e6bf807801895e5c81d18a0abdc
- Drive: https://drive.google.com/drive/folders/12IS7ovd_SB_Ng1VuirSA0EC76jwImjof
