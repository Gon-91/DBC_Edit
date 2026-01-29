# DBC_Edit 프로젝트 문서 (초안)

> 이 문서는 현재 `DBC_Edit` 코드베이스(`src/`)의 계층 구조를 기준으로 실제 동작 흐름을 정리한 *프로젝트 단일 문서*입니다.  
> (작성일: 2026-01-28)

## 0. 구조 도식화(시각화)

### 0.1 계층(레이어) 구조

```
+--------------------+        triggers         +--------------------+
|        Views       | ----------------------> |      Usecases      |
| (Qt Widgets, UI)   |                         | (Action/Command)   |
+--------------------+                         +--------------------+
           |                                              |
           | Qt signals / models                           | orchestration
           v                                              v
+--------------------+                         +--------------------+
|     ViewModels     | <---------------------- |    Controllers     |
| (Qt Models/Signals)|        updates          | (thin adapters)    |
+--------------------+                         +--------------------+
           ^                                              |
           | model signals                                | IO / parsing
           |                                              v
+--------------------+                         +--------------------+
|       Models       | <---------------------- |      Services      |
| (App state/domain) |         returns         | (dbc_loader etc.)  |
+--------------------+                         +--------------------+

Notes
- Views는 Usecase를 호출하여 '무엇을 할지'를 트리거합니다.
- Usecase는 Controller를 통해 Model/Service를 조합해 실행 흐름을 완성합니다.
- Model은 상태를 보관하고 Qt Signal로 상태 변화를 통지합니다.
- ViewModel은 Model signal을 UI 친화적인 형태(QAbstractTableModel 등)로 제공/중계합니다.
```

### 0.2 대표 실행 흐름(파일 오픈 → 메시지 선택)

```
[User]
  | click "Open File"
  v
[MenuBar/UsecaseAction]
  | usecase.get("file.open").execute(parent)
  v
[Usecase: file.open]
  | QFileDialog -> file_path
  v
[FileController.open_file]
  | load_dbc_file(file_path)
  v
[Service: dbc_loader]
  | parse -> DBCFile(messages/signals)
  v
[AppModel.add_file]
  | files_changed.emit(file_names)
  v
[ExplorerViewModel]
  | files.emit(file_names)
  v
[ExplorerDock/FileTab]
  | update_filelist()

...

[User]
  | select message row
  v
[ExplorerDock]
  | usecase.get("message.select").execute(MessageViewData)
  v
[MessageController.select_message]
  | AppModel.select_message(MessageViewData)
  v
[AppModel]
  | MessageSignalModel(message) 생성
  | message_selected.emit(MessageSignalModel)
  v
[CentralViewModel]
  | SignalListModel.set_model()
  | SignalLayoutModel.set_model()
  v
[Signal views]
  | table/layout repaint
```

---

## 0.3 권장 구현 순서(1인 개발 기준)

`TODO.md`와 본 문서의 로드맵이 섞여 보일 수 있으나, 1인 개발에서는 아래 순서가 비용 대비 효과가 좋습니다.

1) **저장 기반(MVP) 먼저 고정**
- 목표: "원본 텍스트 최대 보존" + "변경된 Message 블록만 포맷 변경 허용"을 실제 저장으로 구현
- 필요한 최소 작업:
  - `dbc_loader`에 BO_ 블록 매핑(시작/끝 라인 index)
  - `dbc_writer`(신규)로 변경된 블록만 patch 저장
  - `file.save` 유스케이스 + 메뉴 연결
  - dirty 상태(파일/메시지 변경 추적)

2) **경로처리는 먼저 하되 '최소 변경'만**
- Windows 경로 문제를 피하기 위해, Phase 1 착수 전에 `file_name` 추출 정도만 `pathlib.Path(...).name`으로 교체
- 프로젝트 전체 경로처리 통일/대규모 리팩터는 Phase 3로 미룸

3) **편집 기능(usecases/message, usecases/signals) 확장**
- message add/remove/rename
- signal add/remove/update
- 저장 기반이 있는 상태에서 붙이면 재작업이 거의 없음

4) 고도화/리팩터(undo/redo, validation, parser V2 등)

위 순서는 `TODO.md`의 Phase 1~3 우선순위와 동일합니다.

---

## 1. 목적 / 범위

- 목적: CAN DBC 파일을 빠르고 효율적으로 열람/편집하기 위한 데스크톱 UI 툴
- UI 프레임워크: **PySide6 (Qt)**
- 아키텍처 스타일: **MVVM + Usecase + Controller + Service + Domain Models** 조합

현재 구현 범위와 계획:

- 현재: **DBC 파일 로딩, 파일/메시지 탐색, 메시지 단위 시그널 리스트/레이아웃 표시**
- 예정: **메시지 및 시그널의 편집(추가/삭제/필드 변경) 및 저장**
  - 1차 목표 편집 단위(요구사항):
    - Signal: 추가/삭제/필드 변경
    - Message: **추가/삭제/이름 변경 포함**
  - `src/usecases/signals/`를 중심으로 시그널 add/remove/edit 계열 유스케이스 확장 예정
  - (추가) `src/usecases/message/`는 현재 select만 존재하므로, message edit 계열 유스케이스가 확장될 가능성이 큼

이 문서는 다음을 설명합니다.

- 전체 런타임 흐름(앱 시작 → 파일 오픈 → 파일 선택 → 메시지 선택 → 시그널 리스트/레이아웃 갱신)
- 각 계층(views/viewmodels/usecases/controllers/services/models)의 역할과 상호작용
- 현재 구조의 강점/리스크 및 유지보수 관점의 제안

## 2. 디렉터리 구조 요약

핵심 런타임 코드는 `src/` 아래에 위치합니다.

- `src/main.py`: 진입점(QApplication 생성 및 main window 표시)
- `src/app/`: 의존성 구성(AppContext) 및 메인 윈도우 생성(AppInitializer)
- `src/models/`: 전역 상태(AppModel) 및 도메인 모델/시그널 모델
- `src/services/`: 파일 파싱/IO 등 외부 리소스 처리 로직
- `src/controllers/`: UI 요청을 모델/서비스에 전달하는 얇은 조정(오케스트레이션)
- `src/usecases/`: UI 액션 단위의 실행 로직(Usecase)
- `src/viewmodels/`: Qt Model/Signal 기반의 화면 표현용 모델
- `src/views/`: Qt 위젯(메인윈도우/도킹/탭/위젯) 및 QAction

## 3. 런타임 흐름 (End-to-End)

### 3.1 앱 시작

1) `src/main.py:main()`
- `QApplication` 생성
- `create_main_window()` 호출
- `MainWindow.show()`
- `app.exec()`로 이벤트 루프 진입

2) `src/app/app_initializer.py:create_main_window()`
- `AppContext()` 생성
- `MainWindow(model=app_context.model, usecase=app_context.usecases)` 주입

3) `src/app/app_context.py:AppContext`
- `AppModel()` 생성
- `ControllerContext(model)` 생성
  - `FileController(model)`
  - `MessageController(model)`
- `UsecaseContext(controllers)` 생성
  - `file.open`, `file.close`, `file.select`, `message.select` 등 유스케이스 등록

즉, **의존성 구성은 AppContext에서 한번에 수행**되며, View는 usecase를 호출하는 방식으로 업무 로직을 트리거합니다.

---

### 3.2 파일 열기 (Menu → Usecase → Controller → Service → Model → ViewModel → View)

#### 1) 사용자가 메뉴에서 Open File 클릭
- `src/views/menu/menu_bar.py:MenuBar`
  - `UsecaseAction("Open File", parent, usecase.get("file.open"))`를 메뉴에 추가
- `src/views/actions/usecase_action.py:UsecaseAction`
  - QAction triggered 시 `self._usecase.execute(self._parent)` 호출

#### 2) Usecase 실행
- `src/usecases/file/__init__.py:Open.execute(parent)`
  - `QFileDialog.getOpenFileName(...)`로 DBC 파일 선택
  - 선택된 경로를 `FileController.open_file(file_path)`로 전달

#### 3) Controller가 Service를 호출해 파일을 파싱
- `src/controllers/file_controller.py:FileController.open_file(file_path)`
  - `load_dbc_file(file_path)` 호출

#### 4) Service에서 DBC 파싱 및 도메인 모델 생성
- `src/services/dbc_loader.py:load_dbc_file(file_path)`
  - 파일 내용을 읽고 `_parse_text(text)`로 메시지/시그널을 파싱
  - `DBCFile(file_path, file_name, raw_content, messages)` 생성

#### 5) Model에 파일 추가 및 시그널 발행
- `src/models/appmodel.py:AppModel.add_file(dbc_file)`
  - 내부 `_dbc_files` 목록에 추가
  - `files_changed.emit(file_names)` 발행

#### 6) ExplorerViewModel이 모델 시그널을 받아 View에 전달
- `src/viewmodels/explorer/explorer_view_model.py:ExplorerViewModel`
  - `AppModel.files_changed` → `_on_files_changed(files)`
  - `files.emit(files)`

#### 7) ExplorerDock이 파일 리스트 UI를 갱신
- `src/views/docks/explorer_dock.py:ExplorerDock`
  - `ExplorerViewModel.files` → `_update_filelist(filelist)`
  - `FileTab.update_filelist(filelist)`
  - `FileListWidget.update_filelist(filelist)`

---

### 3.3 파일 선택 (파일 리스트 클릭)

1) `FileListWidget.selectedfile` emit
- `src/views/widgets/filelist_widget.py:FileListWidget._currentitem()`

2) Dock이 usecase 호출
- `src/views/docks/explorer_dock.py:_on_file_selected(filename)`
  - `usecase.get("file.select").execute(filename)`

3) Controller → Model 반영
- `src/usecases/file/__init__.py:Select.execute(file_name)`
- `src/controllers/file_controller.py:select_file(file_name)`
- `src/models/appmodel.py:select_file(file_name)`
  - `file_selected.emit(messages)` 발행

4) ViewModel/ View 갱신
- `ExplorerViewModel._on_file_select(messages)` → `messages.emit(messages)`
- `ExplorerDock._update_messagelist(messagelist)` → `MessageTab.update_messagelist(messagelist)`

---

### 3.4 메시지 선택 (메시지 테이블 클릭)

1) `MessageTableWidget.selectedmessage` emit
- **현재 emit 타입은 `MessageViewData`** 입니다.

2) `ExplorerDock`이 메시지 선택 유스케이스 호출
- `ExplorerDock._on_message_selected(message_view_data)`
  - `usecase.get("message.select").execute(message_view_data)`

3) Controller → Model 반영
- `src/usecases/message/__init__.py:Select.execute(message_view_data)`
- `src/controllers/message_controller.py:select_message(message_view_data)`
- `src/models/appmodel.py:select_message(select_message)`
  - (현재 구현은) `MessageViewData`에 해당하는 `Message` 도메인 객체를 찾아 `MessageSignalModel(message)` 생성
  - `message_selected.emit(message_signal_model)` 발행

4) CentralViewModel이 message_selected를 받아 하위 ViewModel에 모델 전달
- `src/viewmodels/central/central_view_model.py:CentralViewModel._on_message_select(message_signal_model)`
  - `SignalListModel.set_model(message_signal_model)`
  - `SignalLayoutModel.set_model(message_signal_model)`

5) SignalListView / SignalLayoutView UI 갱신
- 리스트: `SignalListModel`(QAbstractTableModel) 갱신 이벤트 기반
- 레이아웃: `SignalLayoutModel.layout_changed` → `SignalLayoutView.update()` → `paintEvent` 재그림

---

## 4. 계층별 책임 정리

### 4.1 Views (`src/views/`)

- 사용자 입력(클릭/키) 수신
- usecase 호출 트리거
- ViewModel 시그널을 구독해 UI를 갱신

대표 구성:

- `MainWindow`: 전체 레이아웃 구성(메뉴/도킹/중앙 위젯)
- `MenuBar` + `UsecaseAction`: 메뉴 액션을 usecase에 연결
- `ExplorerDock`: Files/Messages 탭 제공, 파일/메시지 선택 이벤트를 usecase로 전달
- `CenteralWidget`: SignalListView + SignalLayoutView를 수평 Splitter로 배치

### 4.2 ViewModels (`src/viewmodels/`)

- 모델 시그널을 UI 친화적인 형태로 변환/중계
- Qt Model(`QAbstractTableModel`)을 통해 View가 데이터 접근하도록 제공

대표 구성:

- `ExplorerViewModel`: `files_changed`, `file_selected`를 View 시그널로 중계
- `CentralViewModel`: 메시지 선택에 따른 하위 모델 세팅
- `SignalListModel`: 시그널 리스트를 위한 TableModel
- `SignalLayoutModel`: 레이아웃 변경 알림 시그널 발행

### 4.3 Usecases (`src/usecases/`)

- UI 액션 단위의 실행 흐름(예: file.open, file.select, file.close, message.select)
- Controller 호출 및 입력 수집(QFileDialog 등)을 담당

예정(확장):

- Signals 계열
  - `signals.add`, `signals.remove`, `signals.update_field`, `signals.set_color` 등
- Message 계열(요구사항에 포함)
  - `message.add`, `message.remove`, `message.rename` 등

### 4.4 Controllers (`src/controllers/`)

- Service 호출 및 Model 업데이트 요청
- 얇은 오케스트레이션 레이어(현재는 매우 Thin)

### 4.5 Services (`src/services/`)

- 외부 리소스 I/O 및 파싱
- 예: `dbc_loader.load_dbc_file()`

향후 저장 기능 관점에서 다음 서비스가 필요합니다.

- `dbc_writer` (가칭): **원본 텍스트 최대 보존**을 목표로, 변경된 메시지 블록만 반영하여 저장

### 4.6 Models / Domain (`src/models/`)

- 앱 전역 상태 보관(AppModel)
- 도메인 데이터 구조(메시지/시그널/dbc 파일)
- Signal 기반 상태 변화 통지

---

## 5. 저장(Write-back) 전략 제안 (원본 텍스트 최대 보존)

요구사항:

- 주석/순서/공백 등 *원본 텍스트를 최대한 보존*
- 단, 변경이 발생한 경우
  - 라인 추가/삭제 허용
  - **변경된 Message 블록(BO_ ~ next BO_) 내부에서만 재정렬/포맷 변경 허용**

권장 접근(점진적):

### 5.1 Block-patch(메시지 블록 단위 패치) 전략 (권장)

- `DBCFile.raw_content`를 “소스 오브 트루스”로 유지
- 파싱 시 메시지/시그널을 만들면서, 각 Message 블록의 원본 위치를 추적
  - 예: BO_ 라인 index, 블록 종료 라인 index(다음 BO_ 직전)
  - Signal(SG_) 라인은 블록 내부에서 상대 위치로 추적 가능
- 저장 시에는 "변경된 message"에 대해서만
  - 해당 범위(블록)를 새 텍스트로 재구성
  - 원본 raw_content의 해당 범위를 교체

이 방식은 다음을 동시에 만족시키기 쉽습니다.

- 변경되지 않은 메시지 블록은 완전히 원본 보존
- 변경된 블록 내부는 포맷 정리/재정렬을 점진적으로 적용 가능

### 5.2 메시지/시그널 편집 요구사항과의 정합

- Signal 추가/삭제: 해당 Message 블록에서 SG_ 라인 삽입/삭제
- Signal 필드 변경: 해당 SG_ 라인(또는 관련 라인) 교체
- Message 이름 변경: 해당 BO_ 라인 교체
- Message 추가: 파일 적절한 위치(일반적으로 BO_ 섹션)에 새 블록 삽입
- Message 삭제: 해당 블록 범위 삭제

---

## 6. 현재 코드베이스 관찰 (강점 / 리스크)

### 강점

- 의존성 구성(AppContext)과 실행(AppInitializer)이 분리되어 있어 테스트/확장에 유리
- View → Usecase → Controller → Service/Model 흐름이 명확함
- `MessageSignalModel` 도입으로 “선택된 메시지의 시그널” 컨텍스트 모델이 분리됨
- `SignalLayoutView`는 ViewModel 시그널 기반으로 repaint되어 MVVM 구조에 부합
- 메시지 선택 이벤트를 `MessageViewData`(view-friendly DTO)로 두는 방향은 UI 결합도를 낮추는 데 유리

### 리스크/개선 포인트(당장 치명적이지 않지만 향후 유지보수에 영향)

1) View에서 ViewModel의 private 속성 직접 접근
- 예: `CenteralWidget`가 `self._viewmodel._signallistmodel`에 직접 접근
- 제안: `CentralViewModel`에 public property 제공

2) 파일 경로 처리(Windows/Unix 혼용)
- `file_path.split("/")[-1]`는 Windows 경로에서 깨질 수 있음
- 제안: `pathlib.Path(file_path).name`

3) MessageViewData ↔ Domain 변환 책임 위치
- 현재는 `AppModel.select_message` 내부에서 도메인 메시지를 찾음
- 제안: 변환 책임을 한 곳으로 모으기
  - (안 A) MessageController/Usecase에서 domain Message를 찾아 AppModel에 전달
  - (안 B) AppModel에 `select_message_by_identity(message_id, name, length)` 같은 명시적 API 제공

4) DBC 파서/작성기(V2)
- 현재 정규식 기반으로 BO_/SG_ 일부만 파싱
- 저장 기능(특히 message add/remove/rename)이 들어오면 “원본 블록 매핑/부분 수정” 요구가 커지므로
  - 파서 결과에 block mapping(원본 블록 범위 추적)이 포함되도록 확장 권장

5) logging 일관성
- print/log 혼재
- 제안: `logger.get_logger`로 통일

---

## 7. 향후 방향성(구현 로드맵) 제안

### 7.1 단기(1~2주)

- 경로 처리: pathlib로 통일
- ViewModel 공개 API 정리(underscore 접근 제거)
- `usecases/signals/` 설계 및 최소 유스케이스 스켈레톤 추가
  - `signals.add`, `signals.remove`, `signals.update_field`
- `usecases/message/` 확장 스켈레톤 추가
  - `message.add`, `message.remove`, `message.rename`
- “dirty 상태” 도입
  - 파일별 변경 여부 표시(탭 제목에 * 등)

### 7.2 중기(1~2달)

- DBC 저장(원본 보존 + block patch) MVP 구현
  - 변경된 Message 블록만 재구성 후 raw_content에 패치
  - message add/remove/rename + signal add/remove/update_field 지원
- Undo/Redo 기반 마련
  - usecase를 command 형태로 누적

### 7.3 장기

- DBC 파서 고도화(코멘트/밸류테이블/멀티플렉싱 등)
- 비교/병합(merge) UI
- 강력한 validation(비트 오버랩, length 총합, endianness 등)

---

## 8. 구조 리뷰 및 조언 (요약)

- 현재 구조는 “읽기/탐색” 범위에서는 충분히 단순하고 명확합니다.
- 편집/저장 기능이 들어오면 복잡도가 증가하므로, 다음 3가지를 우선순위로 권장합니다.

1) **편집 이벤트(Usecase) 중심 설계**
- UI에서 직접 model을 건드리지 않고
- `signals.*` / `message.*` 유스케이스가 변경을 수행

2) **원본 보존 저장을 위한 Message 블록 매핑 확보**
- 파서 단계에서 BO_ 블록 범위를 추적
- 저장 시 변경된 블록만 재구성/교체

3) **Domain/DTO 변환 책임 단일화**
- MessageViewData를 계속 쓸 경우, domain 변환을 ‘한 레이어’에서만 하도록 정리

(필요 시) 위 내용을 기준으로 다음 작업으로 `dbc_writer` 서비스 설계 및 `usecases/signals/`, `usecases/message/` 스켈레톤을 실제 코드로 확장하는 단계까지 진행할 수 있습니다.
