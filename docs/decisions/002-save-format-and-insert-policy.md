# Decision 002 — 저장 전략(블록 patch), 포맷 규칙, Message 삽입 정책

Date: 2026-01-29  
Status: **Accepted**

## 배경(Context)

이 프로젝트는 DBC 파일을 편집하되 **원본 텍스트를 최대한 보존**하는 것을 목표로 합니다.
다만 편집/저장을 구현하려면, *변경된 부분*에 대해서는 항상 동일한 결과를 만들어내는 **결정적(deterministic) 출력 규칙**이 필요합니다.

따라서 저장은 아래 접근을 채택합니다.

- 파일 전체 원본 라인을 유지한다.
- 단, **변경된 Message 블록만** 텍스트를 재생성하여 교체한다(block patch).

여기서 *Message 블록*은 아래와 같이 정의합니다.

- `BO_ ...` 라인에서 시작
- 다음 `BO_ ...` 라인 직전까지(또는 파일 끝 EOF) 종료

## 결정(Decision)

### 1) 저장 시 원본 보존 범위

- 저장 시 원본 보존이 원칙이다.
- **dirty(변경됨)로 표시된 Message 블록 내부에서만** 아래를 허용한다.
  - 포맷 변경
  - 블록 내부 라인 재정렬

즉,
- 변경되지 않은 블록 및 블록 외부 텍스트는 **라인/순서/공백 포함 그대로 유지**한다.

### 2) Message 추가 시 삽입 위치 정책

- 기본 정책: **A — BO_ 섹션 끝에 추가**
  - 마지막 Message 블록(마지막 `BO_` 블록) 뒤에 새 블록을 추가한다.
- UI 옵션: **C — 현재 선택된 Message 뒤에 삽입**
  - 사용자가 “현재 메시지 뒤에 삽입”을 선택한 경우, 선택된 Message 블록 바로 뒤에 새 블록을 삽입한다.

정책 **B(ID 정렬)** 은 기본 정책으로 채택하지 않는다.
- 이유: 원본 보존 원칙과 충돌하여 대량 재정렬/대규모 diff를 유발하기 쉬움.
- 추후 “정렬 저장/정리” 같은 별도 모드로 제공 가능.

### 3) 변경된 Message 블록 내부 Canonical 포맷 규칙

> 아래 포맷 규칙은 **dirty Message 블록 내부에서만 적용**한다.

#### 3.1 `BO_` 라인 템플릿

Canonical:

- `BO_ {message_id} {message_name}: {dlc} {sender}`

규칙:
- 토큰 사이 공백 1개
- `:` 뒤 공백 1개

예:
- `BO_ 1234 MyMessage: 8 Vector__XXX`

#### 3.2 `SG_` 라인 템플릿

Canonical 구조:

- `SG_ {signal_name} : {start}|{length}@{byte_order}{value_type} ({factor},{offset}) [{min}|{max}] "{unit}" {receivers}`

규칙:
- `SG_` 뒤 공백 1개
- `{signal_name}` 뒤 공백 1개
- 콜론은 양쪽 공백 포함: `name␠:␠...`
- `({factor},{offset})`는 쉼표 주변 공백 없음
- `[{min}|{max}]` 내부 공백 없음
- `"{unit}"`는 항상 큰따옴표 포함(빈 문자열은 `""`)
- receivers는 공백 1개로 join

매핑:
- `byte_order`는 도메인 `ByteOrder`(Enum)로부터 DBC 표현(`@0/@1` 또는 이에 준하는 표현)으로 일관되게 생성한다.
- `value_type`은 도메인 `ValueType`(Enum)로부터 생성한다.
  - `ValueType.UNSIGNED` → `+`
  - `ValueType.SIGNED` → `-`

### 4) dirty 기준(파일 / message)

- 파일 단위 dirty
  - 저장 결과가 바뀌는 변경이 하나라도 존재하면 True
- message 단위 dirty(블록 patch 대상)
  - message identity(일반적으로 message id) 기준 set/list로 관리
  - 다음 중 하나라도 해당하면 해당 message는 dirty
    - BO_ 헤더 변경(id/name/dlc/sender)
    - SG_ 추가/삭제/변경
    - 시그널 속성 변경(저장 시 SG_ 라인에 영향을 주는 항목)

저장 성공 시:
- 파일 dirty 해제
- dirty message 목록/집합 초기화

## 결과(Consequences)

- 저장 시 원본 보존이 강해져 diff가 최소화된다.
- 변경된 블록 내부는 canonical 포맷으로 저장되므로 테스트/검증이 쉬워진다.
- 메시지/시그널 편집(usecase) 확장 시, “dirty 블록만 재생성” 규칙을 기반으로 안전하게 기능을 추가할 수 있다.
- 파일 전체 정렬/정리는 기본 모드가 아니라 옵션 기능(추후)로 유지된다.
