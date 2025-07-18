### v1.0.1
#### 코드 수정
1. @/src @/scripts 를 \보고 LLM에 코드를 수정해달라고 할 때, 기존 기능은 잃지 않고 호환성과 실행에도 문제 없도록 하고 싶은데 그렇게 하기 위해서 LLM이 읽어야 하는 필수 문서를 작성하려고 해 Todolist를 갱신해서 작업 진행해줘 고급 전문가 수준으로@func_for_LLM.md 이 파일에 작성해줘. 내용을 개편해도 좋아

2. 지금 프로그램에서 "프로젝트 목록" 부분에 프로젝트 이름이 길어지면 ...으로 표시되는 문제가 발생해. 모두 표시되도록 해줘@func_for_LLM.md 을 보고 기존 기능은 잃지 않고 호환성과 실행에도 문제 없도록 진행해줘

3. 데이터 백업 복원 시 아래와 같이 표시되는데,
   reply = QMessageBox.question(
   self, "백업 복원 확인",
   f"정말로 '{filename}' 백업으로 복원하시겠습니까?\n\n"
   "현재 데이터는 자동으로 백업된 후 선택한 백업으로 교체됩니다.",
   QMessageBox.Yes | QMessageBox.No,
   QMessageBox.No
   )
   
   아래 이 부분을 삭제해주고
   "현재 데이터는 자동으로 백업된 후 선택한 백업으로 교체됩니다.",
   
   현재 데이터를 자동으로 백업할 지 묻는 부분을 추가해줘

4. @/scripts 에 있는 배포 파일들 정상 작동하는 지 확인해줘@func_for_LLM.md 을 보고 기존 기능은 잃지 않고 호환성과 실행에도 문제 없도록 진행해줘. "배포 파일" 말한거야

5. @/ProgressProgram_vtest 안의 exe 파일 테스트해줘 잘 실행되는지

6. failed to execute script 'main' due to unhandled exception: no module named 'utils'라고 떠. 배포 단계부터 실행까지 다시 테스트해줘. @func_for_LLM.md 을 보고 기존 기능은 잃지 않고 호환성과 실행에도 문제 없도록 진행해줘

#### changelog
1. @CHANGELOG.md 에 따라서 @CHANGELOG.md 개편해줘@/archive 여기에 v1.0.1 추가해줘
	
	1.0.1 추가하는 걸 가장 먼저 수행하고 그 이후로 단계적으로 수행해줘. 
	v1.0.1에서 수행한 사항은 다음과 같아
	
	v1.0.1 fix: 사용자 보고 문제 해결 및 기능 개선
	- 프로젝트 내부 사항 수정 후, 다른 프로젝트로 넘어가던 현상 수정
	- 프로젝트 목록의 하위 내용 중 제목 모두 표시 안되던 사항 수정
	- 데이터 복원 시 자동으로 현재 백업 생성하는 기능 수정
		- 백업 여부를 묻는 기능 추가

2. 아 미안해 누락한 사항이 있어. 스크립트 관련 수정사항도 추가해줘

#### README
1. @README_dist.md @README.md 의 내용도 개편해줘
   
2. 최신 버전의 구글 드라이브 링크는 아래와 같아  
	@https://drive.google.com/drive/folders/
	1QsoBvBSgSW3gyhl780cP7_yarD5C1lR8?usp=sharing

##### 라이선스
1. 내 프로그램을 누구나 다 사용하는 건 상관없는데, 비상업적 용도로만 사용했으면 좋겠어 이러면 그냥 아무나 사용가능한데, 누군가는 내걸로 사업화도 못하고 돈주고 팔지도 못한다는거 아니야?
   (답변)
	네, 정확히 이해하셨습니다! 그런 경우에는 CC BY-NC (Creative Commons Attribution-NonCommercial) 라이선스가 가장 적합합니다.
	
	CC BY-NC의 주요 특징:
	
	1. 허용되는 것 ✅
	
	- 자유로운 사용
	
	- 소스코드 공유
	
	- 수정 및 개선
	
	- 재배포
	
	1. 금지되는 것 ❌
	
	- 상업적 사용
	
	- 판매
	
	- 광고 수익
	
	- 영리 목적 활용

2. CC BY-NC 4.0 라이선스로 전문적이고 명확하게 변경. 먼저 LICENSE 파일을 수정. README.md의 라이선스 섹션을 더 명확하게 업데이트

3. Goranidesu 라고 바꿔줘 내 깃허브 아이디야 혹시 관련해서 라이센스에 문제가 있게 하는 게 있을까? 어떤 부분엔 Progress Team의 일환이다 이런거 적혀있는데
   (답변)
	   네, Progress Team을 Goranidesu로 변경하고, 일관성을 체크하겠습니다.
	   먼저 LICENSE 파일을 수정하겠습니다:
	   이제 프로젝트 전체에서 "Progress Team" 관련 언급을 찾아보겠습니다

4. 이름은 pollux, 아이디는 GoraniDesu로 했는데 추가수정 요하지 않지?
   (답변)
   네, 이름과 아이디를 정확하게 반영하도록 수정하겠습니다. 대소문자도 정확히 'GoraniDesu'로 맞추겠습니다.
   
   모든 파일에서: 이름을 "pollux"로 표시 GitHub 아이디를 정확히 "GoraniDesu"로 수정 (대소문자 구분) 가능한 경우 둘 다 표시 (예: "pollux (GoraniDesu)")

5. @/progress_program 에서 Progress_team 또는 그와 준하는 이름 검색해서 모두 수정해줘. 

6. 라이선스 또는 영어로 라이선스 검색해서 수정 필요한 사항 없는지 확인 후 개편해줘

### v1.1.0
#### 코드 수정
1. 노트 작성 부분에서 사용자가 "노트추가" 기능을 이용한 후에 더 작성할 내용이 있다면 작성한 후 저장할 수 있게 해줘. 지금은 기록만 해두고 저장하는 기능이 없어서 프로젝트를 변환하면 기록했던 내용이 사라지는 문제가 있어@func_for_LLM.md 을 보고 기존 기능은 잃지 않고 호환성과 실행에도 문제 없도록 진행해줘

#### changelog
1. 수정한 내용 정리해줘 changelog 등에 기재할 내용으로 간단명료하게
   (답변)
	노트 기능 개선 (v1.1.0)  
	추가된 기능  
	노트 저장 버튼 (💾) 추가  
	프로젝트 전환 시 저장되지 않은 노트 내용 저장 확인 기능  
	변경된 기능  
	타임스탬프 표시를 "노트 추가" 버튼 사용 시에만 적용  
	저장 버튼(💾)으로 저장 시 타임스탬프 없이 내용만 저장  
	노트 저장 방식을 덮어쓰기 방식으로 변경 (이전: 누적 방식)  
	버그 수정  
	프로젝트 전환 시 작성 중인 노트 내용이 사라지는 문제 해결  
	동일한 내용 중복 저장 방지  
	빈 내용 저장 시 기존 노트 자동 삭제 처리

#### README
1. README 검색해서 파일 살펴보고 수정 필요한 부분 있으면 수정해줘
   
2. 1.0.1 검색해서 1.1.0 으로 수정해야 하는 거 찾아주고 개편해줘

3. 버전이 바뀌면서 수정되어야 하는 목록 리스트해줘
   (답변)
   소스 코드 버전 정보 [ ] src/init.py: __version__ = "1.1.0" [ ] src/main.py: app.setApplicationVersion("1.1.0") 빌드 스크립트 관련 [ ] scripts/build_release.ps1 실행 시 버전 인자: 1.1.0 [ ] scripts/build_release.bat 실행 시 버전 인자: 1.1.0 [ ] 배포 폴더명: ProgressProgram_1.1.0/ 문서 - README 파일들 [ ] README.md [ ] 제목의 버전 번호 [ ] 다운로드 링크의 버전 표시 [ ] 빌드 명령어 예시의 버전 번호 [ ] 빌드 스크립트 개선사항 섹션의 버전 [ ] 실행 파일 호환성 섹션의 버전 [ ] README_dist.md [ ] 배포 폴더 구조의 버전 [ ] 업데이트 설명의 버전 [ ] 문제 해결 가이드의 버전 참조 문서 - 변경 로그 [ ] CHANGELOG.md [ ] 새 버전 섹션 추가 [ ] 날짜 정보 [ ] GitHub 비교 링크 업데이트 [ ] docs/changelog/CHANGELOG.md [ ] 목차 테이블에 새 버전 추가 [ ] 새 버전 섹션 추가 [ ] 날짜 정보 [ ] GitHub 비교 링크 업데이트 [ ] docs/changelog/README.md [ ] 최종 업데이트 날짜와 버전 릴리스 노트 [ ] docs/changelog/archive/v1.1.0_release_notes.md 생성 [ ] 버전 및 날짜 [ ] 주요 변경사항 [ ] 기능 설명 [ ] 호환성 정보 프로젝트 가이드 [ ] docs/guides/project_guide/after_v1.0/user_prompt.md [ ] 새 버전 섹션 추가 [ ] 변경사항 기록 기타 참조 [ ] 이전 버전을 참조하는 모든 문서에서 "v1.0.1 이상" 같은 표현 확인 [ ] 새로운 기능/변경사항에 대한 사용자 가이드 업데이트 [ ] 문제 해결 가이드의 버전 참조 업데이트 테스트 관련 [ ] 새 버전으로 빌드된 실행 파일 테스트 [ ] 이전 버전과의 호환성 테스트 [ ] 새로운 기능 테스트

4. 