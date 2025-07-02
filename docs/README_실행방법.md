# Progress Program 실행 방법

## 🚀 빠른 시작

### 1단계: 환경 설정 (최초 1회만)
```
scripts/setup_env.bat 더블클릭
```
- conda 가상환경 생성
- PySide6 자동 설치

### 2단계: 프로그램 실행
```
scripts/run.bat 더블클릭
```

## 💻 수동 실행 (고급 사용자)

### conda 환경 활성화
```bash
conda activate progress_env
```

### 프로그램 실행
```bash
python src/main.py
```

## 🔧 문제 해결

### 환경이 없다고 나오는 경우
```bash
conda create -n progress_env python=3.9 -y
conda run -n progress_env pip install PySide6
```

### import 오류가 나는 경우
- 프로젝트 루트 디렉토리에서 실행하는지 확인
- conda 환경이 제대로 활성화되었는지 확인

## 📁 파일 구조
```
progress_program/
├── scripts/               # 실행 스크립트
│   ├── run.bat           # 프로그램 실행 (👈 이걸 더블클릭!)
│   └── setup_env.bat     # 환경 설정 (최초 1회)
├── src/                  # 소스 코드
│   ├── main.py           # 메인 프로그램
│   ├── database/         # 데이터베이스
│   ├── ui/               # 사용자 인터페이스
│   └── utils/            # 유틸리티
├── config/               # 설정 파일
│   └── theme_settings.json # 테마 설정
└── data/                 # 데이터 저장 (자동 생성)
    └── progress.db       # SQLite 데이터베이스
```

## 🎉 사용법
1. `scripts/setup_env.bat` 실행 (최초 1회)
2. `scripts/run.bat` 실행
3. 좌측에서 "새 프로젝트" 클릭
4. 프로젝트 선택하고 할 일 추가
5. 체크박스로 완료 표시
6. 진척도 실시간 확인! 