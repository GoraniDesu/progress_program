# Progress Program 사용자 가이드

## 📋 프로그램 소개
Progress Program은 복잡한 기능에 지친 사용자를 위한 간단한 진척도 관리 도구입니다.

### 🎯 주요 기능
- **진척도 관리**: 프로젝트별 할 일 관리 및 자동 진척도 계산
- **간단한 노트**: 날짜/시간 자동 기록되는 메모 기능

---

## 🚀 시작하기

### 설치 방법
1. `dist/ProgressProgram.exe` 파일을 원하는 위치에 복사
2. 더블클릭으로 실행

### 첫 실행
1. 프로그램 실행 시 좌측에 프로젝트 목록이 표시됩니다
2. 우측에 "프로젝트를 선택하거나 새로 만들어보세요! 🚀" 메시지가 표시됩니다

---

## 📖 사용 방법

### 1. 프로젝트 생성
1. 좌측 상단의 **"+ 새 프로젝트"** 버튼 클릭
2. 프로젝트 제목과 설명 입력
3. **"확인"** 버튼 클릭

### 2. 할 일 관리
1. 생성된 프로젝트를 클릭하여 선택
2. 우측 상단에 진척도 바가 표시됩니다
3. **"📋 할 일"** 탭에서:
   - **"+ 할 일 추가"** 버튼으로 새 할 일 생성
   - 체크박스 클릭으로 완료 처리
   - 🗑️ 버튼으로 할 일 삭제

### 3. 노트 작성
1. **"📝 노트"** 탭으로 이동
2. **"+ 노트 추가"** 버튼 클릭
3. 자유롭게 메모 작성 (날짜/시간 자동 기록)

### 4. 진척도 확인
- 할 일을 완료할 때마다 자동으로 진척도가 업데이트됩니다
- 진척도 바의 색상이 완성도에 따라 변경됩니다:
  - 🔴 0-25%: 빨간색
  - 🟠 25-50%: 주황색  
  - 🟡 50-75%: 노란색
  - 🟢 75-100%: 초록색

---

## 💡 사용 팁

### 효과적인 프로젝트 관리
1. **큰 프로젝트는 작은 할 일로 나누기**
   - 예: "웹사이트 만들기" → "디자인", "개발", "테스트", "배포"

2. **구체적인 할 일 작성**
   - 좋은 예: "로그인 페이지 UI 완성"
   - 나쁜 예: "개발하기"

3. **정기적인 노트 작성**
   - 진행 상황, 문제점, 아이디어 등을 자유롭게 기록

### 데이터 관리
- 모든 데이터는 `data/progress.db` 파일에 저장됩니다
- 백업을 위해 이 파일을 안전한 곳에 복사해두세요

---

## 🔧 문제 해결

### 프로그램이 실행되지 않을 때
1. Windows Defender나 백신 프로그램에서 차단했는지 확인
2. 관리자 권한으로 실행 시도
3. `data` 폴더 쓰기 권한 확인

### 데이터가 사라졌을 때
1. `data/progress.db` 파일이 있는지 확인
2. 백업 파일이 있다면 복원

### 기타 문제
- 프로그램을 재시작해보세요
- 문제가 지속되면 `data` 폴더를 삭제하고 새로 시작하세요

---

## 📁 파일 구조
```
ProgressProgram.exe     # 실행 파일
data/
  └── progress.db       # 데이터베이스 파일 (자동 생성)
```

---

## 🎉 즐거운 프로젝트 관리!

Progress Program으로 여러분의 프로젝트를 체계적이고 즐겁게 관리해보세요! 

**핵심 원칙: 간단하게, 꾸준히, 시각적으로! 📊✨** 