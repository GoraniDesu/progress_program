# CHANGELOG

Progress Program의 모든 주목할 만한 변경사항이 이 파일에 기록됩니다.
이 문서는 [Keep a Changelog](https://keepachangelog.com/) 표준을 따르며, 모든 버전 정보가 최신순으로 정렬되어 있습니다.

## [Unreleased]

## [1.1.0] - 2025-07-07
### Added
- 노트 저장 버튼(💾) 추가
- 프로젝트 전환 시 저장되지 않은 노트 내용 저장 확인 기능

### Changed
- 타임스탬프 표시를 "노트 추가" 버튼 사용 시에만 적용
- 저장 버튼(💾)으로 저장 시 타임스탬프 없이 내용만 저장
- 노트 저장 방식을 덮어쓰기 방식으로 변경 (이전: 누적 방식)

### Fixed
- 프로젝트 전환 시 작성 중인 노트 내용이 사라지는 문제 해결
- 동일한 내용 중복 저장 방지
- 빈 내용 저장 시 기존 노트 자동 삭제 처리

## [1.0.1] - 2025-07-06
### Fixed
- 프로젝트 내용 수정 후 다른 프로젝트로 자동 전환되던 문제 수정
- 프로젝트 목록의 긴 제목이 완전히 표시되지 않던 문제 해결
- `build_release.bat` 실행 시 venv 환경에서 Python 경로를 찾지 못하는 문제 수정
- dist 폴더 내 실행 파일의 모듈 import 오류 해결
  - PyInstaller 경로 설정 로직 개선
  - 패키지 경로 자동 감지 기능 추가

### Changed
- 데이터 복원 시 자동 백업 대신 사용자 선택 방식으로 변경
  - 복원 전 현재 데이터 백업 여부를 묻는 다이얼로그 추가
- 배포 스크립트 환경 감지 로직 강화
  - conda/venv 환경 자동 감지 개선
  - 가상환경 활성화 상태 확인 추가
  - 의존성 패키지 자동 설치 기능 추가
  - 오류 메시지 상세화

## [1.0.0] - 2025-07-05
### Added
- 프로젝트 100% 달성 시 도장(Stamp) 기능 추가
  - 2초 지연 후 나타나 6초간 유지되다가 3초에 걸쳐 사라지는 애니메이션
  - 원형/사각형 도장이 45° 기울어져 임의의 위치에 표시

### Changed
- 빌드/배포 자동화 시스템 완성
  - `scripts/build_release.bat`(CMD), `build_release.ps1`(PowerShell) 스크립트 추가
  - conda/venv 환경 자동 감지 및 필요 패키지 설치
  - 리소스 번들링 자동화

### Fixed
- one-file 모드에서 내부 모듈을 찾지 못하던 문제 수정
- 빌드 스크립트가 특정 Python 환경에서 실패하던 문제 수정
- 축하 애니메이션 중복 실행 문제 해결

## [0.5.2] - 2025-07-03
### Changed
- 대규모 프로젝트 퍼포먼스 최적화
  - DB 인덱싱으로 로딩 속도 2배 향상
  - UI 렌더링 최적화

### Fixed
- 백업 파일 복원 시 DB 락 문제 해결
- 다크모드 비활성화 버튼 가독성 개선
- 설정 파일 쓰기 권한 오류 수정

## [0.5.0] - 2025-07-03
### Added
- Fluid ProgressBar 도입
  - 물결 애니메이션 효과
  - GPU 가속 렌더링
  - 동적 색상 변경

### Changed
- 백업 시스템 강화
  - 자동 정리 정책 추가
  - 복원 마법사 UI 도입

## [0.4.2] - 2025-07-03
### Changed
- 데이터베이스 성능 최적화
- UI 업데이트 로직 개선
- ProgressBar 색상 보정

### Fixed
- 메모리 누수 문제 해결
- DB 파일 잠금 문제 수정

## [0.4.0] - 2025-07-03
### Added
- 파티클 축하 효과
- 진척도 바 색상 진화
- 사용자 정의 테마 시스템
- ZIP 기반 백업/복원
- 키보드 단축키

## [0.3.1] - 2025-07-03
### Changed
- UI/UX 개선
  - 아이콘 변경
  - 다크모드 완성
  - 버튼 시인성 개선
- 마감일 기능 향상
- 백업/복원 기능 활성화

## [0.2.0] - 2025-07-03
### Added
- 테마 시스템 (라이트/다크 모드)
- 더블클릭 편집 기능
- 완료 항목 관리 기능

## [0.1.0] - 2025-07-03
### Added
- 프로젝트 관리 기능
- 할 일 관리 기능
- 진척도 추적 기능
- 노트 기능
- SQLite 기반 데이터 저장

[Unreleased]: https://github.com/GoraniDesu/progress_program/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/GoraniDesu/progress_program/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/GoraniDesu/progress_program/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/GoraniDesu/progress_program/compare/v0.5.2...v1.0.0
[0.5.2]: https://github.com/GoraniDesu/progress_program/compare/v0.5.0...v0.5.2
[0.5.0]: https://github.com/GoraniDesu/progress_program/compare/v0.4.2...v0.5.0
[0.4.2]: https://github.com/GoraniDesu/progress_program/compare/v0.4.0...v0.4.2
[0.4.0]: https://github.com/GoraniDesu/progress_program/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/GoraniDesu/progress_program/compare/v0.2.0...v0.3.1
[0.2.0]: https://github.com/GoraniDesu/progress_program/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/GoraniDesu/progress_program/releases/tag/v0.1.0 