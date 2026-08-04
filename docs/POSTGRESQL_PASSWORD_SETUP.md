# 🔧 PostgreSQL 비밀번호 설정 및 접속 해결

## 현재 상황
✅ PostgreSQL 18 설치됨
✅ PATH 설정 완료 (PowerShell 프로필에 추가)
✅ pgpass.conf 파일 생성됨 (비밀번호 자동입력)
❌ postgres 사용자 비밀번호 불일치

---

## 🎯 3가지 해결 방법

### 방법 1: pgAdmin으로 비밀번호 확인/설정 (권장) ⭐

#### Step 1: pgAdmin 열기
```
1. Windows 시작 메뉴 클릭
2. "pgAdmin" 입력 및 검색
3. "pgAdmin 4" 실행
```

#### Step 2: 서버 연결
```
1. pgAdmin 웹 브라우저가 열림 (http://localhost:5050)
2. 왼쪽 트리에서 "Servers" 클릭
3. PostgreSQL 서버 우클릭
4. "Properties" 선택
5. "Connection" 탭에서 Host, Port, Username 확인
```

#### Step 3: 비밀번호 변경
```
1. Servers → PostgreSQL → 우클릭
2. "Change password..." 선택
3. 새 비밀번호 입력 (예: postgres)
4. 저장
```

#### Step 4: pgpass.conf 업데이트
비밀번호가 "postgres"가 아니면:

PowerShell에서:
```powershell
$pgpassFile = "$env:APPDATA\postgresql\pgpass.conf"

@"
localhost:5432:*:postgres:YOUR_NEW_PASSWORD
"@ | Out-File -FilePath $pgpassFile -Encoding ASCII -Force

Write-Host "✅ pgpass.conf 업데이트 완료"
```

---

### 방법 2: .env 파일에 실제 비밀번호 입력

.env 파일을 편집합니다:

```env
# 실제 비밀번호를 입력
DATABASE_URL=postgresql://postgres:YOUR_ACTUAL_PASSWORD@localhost:5432/question_bank
```

**YOUR_ACTUAL_PASSWORD**를 PostgreSQL 설치 시 설정한 비밀번호로 바꾸세요.

---

### 방법 3: 비밀번호 없이 로컬 호스트 접속 (Trust 모드)

PostgreSQL 설정 파일을 수정하여 localhost에서는 비밀번호 없이 접속 가능하게 합니다.

1. PostgreSQL 설정 파일 찾기:
```powershell
"C:\Program Files\PostgreSQL\18\data\pg_hba.conf"
```

2. 파일 편집 (메모장):
```
# 라인 찾기
host    all             all             127.0.0.1/32            md5

# 변경
host    all             all             127.0.0.1/32            trust
```

3. PostgreSQL 서비스 재시작:
```powershell
Restart-Service PostgreSQL*
```

---

## ✅ 설정 확인 (아래 중 하나 실행)

### 옵션 1: pgpass.conf 사용
```bash
psql -U postgres -h localhost -l
```

### 옵션 2: 비밀번호 명시
```bash
psql -U postgres -h localhost -W
# 비밀번호 입력
```

### 옵션 3: 연결 문자열 사용
```bash
psql postgresql://postgres:YOUR_PASSWORD@localhost:5432/postgres
```

---

## 🚀 성공하면

데이터베이스 생성:
```bash
psql -U postgres -c "CREATE DATABASE question_bank;"

# 확인
psql -U postgres -l
```

테이블 생성:
```bash
cd question_bank_system
python init_local_db.py
```

---

## 💡 가장 간단한 해결책

### pgAdmin 사용 추천 절차:

1. **pgAdmin 열기** (Windows 시작 메뉴)
2. **Servers → PostgreSQL 선택**
3. **오른쪽 클릭 → "Change password"**
4. **새 비밀번호 입력** (예: `postgres`)
5. **저장**
6. **다음 명령 실행**:
```bash
# pgpass.conf 업데이트
$pgpassFile = "$env:APPDATA\postgresql\pgpass.conf"
@"
localhost:5432:*:postgres:postgres
"@ | Out-File -FilePath $pgpassFile -Encoding ASCII -Force

# 데이터베이스 생성
psql -U postgres -c "CREATE DATABASE question_bank;"
```

---

## 🔍 현재 비밀번호 추측 테스트

PostgreSQL 설치 시 기본값으로 설정된 것 같으니, 다음을 시도해보세요:

```bash
# 비밀번호 없음 (최신 PostgreSQL 기본값)
$env:PGPASSWORD=""; psql -U postgres -h localhost -l

# 비밀번호 "password"
$env:PGPASSWORD="password"; psql -U postgres -h localhost -l

# 비밀번호 "postgres"
$env:PGPASSWORD="postgres"; psql -U postgres -h localhost -l

# 비밀번호 "admin"
$env:PGPASSWORD="admin"; psql -U postgres -h localhost -l
```

작동한 비밀번호를 pgpass.conf에 저장하면 됩니다.

---

## 📞 최종 확인

```bash
# PATH 설정 확인
psql --version

# pgpass.conf 확인
Get-Content "$env:APPDATA\postgresql\pgpass.conf"

# PowerShell 프로필 확인 (PATH 추가 확인)
Get-Content $PROFILE
```
