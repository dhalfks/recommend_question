# PostgreSQL 비밀번호 입력 없이 자동 접속 설정

## 방법 1: pgpass.conf 파일 생성 (권장) ⭐

### Step 1: pgpass 파일 생성

PowerShell에서:

```powershell
$pgpassDir = "$env:APPDATA\postgresql"
$pgpassFile = "$pgpassDir\pgpass.conf"

# 디렉토리 생성
if (!(Test-Path $pgpassDir)) {
    New-Item -ItemType Directory -Path $pgpassDir -Force | Out-Null
}

# pgpass.conf 생성
@"
localhost:5432:*:postgres:postgres
"@ | Out-File -FilePath $pgpassFile -Encoding ASCII -Force

# 권한 설정 (중요!)
icacls $pgpassFile /inheritance:r /grant:r "$env:USERNAME`:(F)" | Out-Null

Write-Host "✅ pgpass.conf 생성 완료"
Write-Host "📝 위치: $pgpassFile"
```

### Step 2: 접속 테스트

```bash
psql -U postgres -h localhost
# 비밀번호 프롬프트 없이 바로 접속됨
```

---

## 방법 2: 환경 변수로 비밀번호 설정

```powershell
$env:PGPASSWORD = "postgres"
psql -U postgres -h localhost -c "CREATE DATABASE question_bank;"
```

---

## 방법 3: 연결 문자열로 접속

```bash
psql postgresql://postgres:postgres@localhost:5432/question_bank
```

---

## ✅ 데이터베이스 생성 명령어

pgpass 설정 후:

```bash
psql -U postgres -c "CREATE DATABASE question_bank;"
```

---

## 🔧 설정 확인

```bash
# pgpass 파일 확인
cat "$env:APPDATA\postgresql\pgpass.conf"

# 데이터베이스 목록 확인
psql -U postgres -l
```
