# TODO

> 정렬 원칙(1인 개발 기준): **저장 기반(MVP) → 편집(usecase) → UI 확장 → 고도화/리팩터**  
> 리팩터(경로/네이밍 등)는 *전면 적용*을 먼저 하지 않고, Phase 1 진행에 필요한 **최소 변경**만 선반영합니다.

## Phase 0 - 결정 사항(규칙/정책 확정)

- [x] 저장 시 원본 라인 보존 범위 확정: **변경된 Message 블록(BO_ ~ next BO_) 내부만 포맷/재정렬 허용**
- [x] Message 추가 시 삽입 위치 정책 결정: **A(BO_ 섹션 끝에 추가) + C(현재 선택 메시지 뒤에 삽입 옵션)**
- [x] 저장 시 포맷팅 규칙(변경된 Message 블록 내부) 정의
  - [x] BO_ 라인 템플릿(공백/정렬)
  - [x] SG_ 라인 템플릿(공백/정렬)
- [x] dirty 기준 정의
  - [x] 파일 단위 dirty
  - [x] message 단위 dirty(블록 patch 대상)

> 결정 문서: `docs/decisions/002-save-format-and-insert-policy.md`

---

## Phase 1 - 저장 기반(원본 보존 + Message 블록 patch) MVP (최우선)

### 0) Phase 1 착수 전 최소 리팩터(필수)
- [ ] **경로 처리 최소 수정**
  - [ ] `file_name = Path(file_path).name` 형태로 파일명 추출을 `pathlib`로 변경(Windows 대응)
  - [ ] ※ 전체 경로처리 통일은 Phase 3로 미룸

### 1) 파싱 확장(블록 매핑)
- [ ] `services/dbc_loader.py`
  - [ ] raw 라인 유지(`raw_lines`) 또는 raw_content를 라인 단위로 다루는 구조 추가
  - [ ] BO_ 메시지 블록 범위 매핑(시작/끝 라인 index) 생성
  - [ ] (선택) SG_ 라인 index 매핑(정밀 patch)
  - [ ] 파싱 실패/미지원 라인 처리 정책 추가(원본 유지)

### 2) 저장기 서비스 추가
- [ ] `services/dbc_writer.py` (신규)
  - [ ] Message 블록 텍스트 생성 함수
  - [ ] 변경된 Message 블록만 교체하는 patch 함수
  - [ ] Message add/remove/rename 반영을 위한 블록 삽입/삭제/교체 API
  - [ ] atomic save(임시 파일 → replace) 고려
  - [ ] Windows 인코딩/경로 처리(utf-8 기본) 처리

### 3) file.save 유스케이스/연결
- [ ] `usecases/file/` 또는 `usecases/file.py`
  - [ ] `file.save` 유스케이스 추가
  - [ ] `file.save_as` 유스케이스 추가(선택)
- [ ] `views/menu/menu_bar.py`
  - [ ] Save / Save As 메뉴 추가
  - [ ] Ctrl+S 단축키(선택)

### 4) 모델에 dirty 상태 도입
- [ ] `models/appmodel.py`
  - [ ] 파일 단위 dirty 플래그
  - [ ] 변경된 message 목록(블록 patch 대상) 관리
  - [ ] dirty 변경 시그널 emit(선택)

---

## Phase 2 - 편집 기능 1차(요구사항: Message + Signal 편집)

> 전제: Phase 1(저장 기반)이 동작해야 편집 기능을 안전하게 확장할 수 있음.

### 1) Message 편집 유스케이스(요구사항 C)
- [ ] `usecases/message/`
  - [ ] `message.add`
  - [ ] `message.remove`
  - [ ] `message.rename`
- [ ] Controller/Model API 정리
  - [ ] MessageViewData → Domain(Message) 변환 책임 위치 단일화

### 2) Signal 편집 유스케이스
- [ ] `usecases/signals/`
  - [ ] `signals.add`
  - [ ] `signals.remove`
  - [ ] `signals.update_field`
  - [ ] (선택) `signals.set_color`, `signals.set_byte_order`

### 3) ViewModel 편집 경로 연결
- [ ] `viewmodels/central/signal_list_model.py`
  - [ ] editable 컬럼 정의 및 `flags()` 구현
  - [ ] `setData()`에서 직접 모델 변경 대신 유스케이스 호출로 연결
- [ ] `viewmodels/central/central_view_model.py`
  - [ ] view에서 private 속성 접근 제거(공개 프로퍼티 제공)

### 4) View(UI) 편집 UI 추가
- [ ] Message 탭
  - [ ] rename UI(더블클릭/컨텍스트 메뉴/다이얼로그)
  - [ ] add/remove UI(버튼/컨텍스트 메뉴)
- [ ] Signal 리스트
  - [ ] add/remove UI
  - [ ] 테이블 편집 delegate/검증

---

## Phase 3 - 안정화/고도화 + 리팩터(필요할 때)

- [ ] Undo/Redo 기반 마련(유스케이스를 커맨드처럼 누적)
- [ ] Validation 강화(비트 오버랩, 길이 범위, endian/bit order 등)
- [ ] 파서 고도화(코멘트/밸류테이블/멀티플렉싱 등)
- [ ] 로깅 통일(print 제거, logger로 통일)
- [ ] 저장 실패/파싱 실패 UX(QMessageBox)

### Refactor / Cleanup (Phase 1~2 이후)

- [ ] `usecases/file.py` vs `usecases/file/__init__.py` 중복 정리(한 방식으로 통일)
- [ ] 오탈자 정리: `CenteralWidget` → `CentralWidget` (점진적 변경)
- [ ] `views/docks/signal_dock.py` 빈 파일 정리(삭제 또는 TODO 명시)
