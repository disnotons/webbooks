# webbooks

웹북 발행 전용 중앙 저장소입니다.

이 저장소는 **원본 Markdown을 편집하는 곳이 아니라 발행용 복사본과 GitBook 연결 구조를 관리하는 곳**입니다.

## 현재 기본 구조

```text
각 연구·해설 프로젝트
→ 원본 Markdown
→ 웹북 발행용 복사본 정규화
→ GitHub disnotons/webbooks
→ GitBook Git Sync
→ GitBook 공개 웹북
```

독자용 중앙 입구는 `library/`를 별도의 GitBook Space로 연결하여 사용합니다.

```text
library/                         중앙 웹북 도서관 Space
books/<분야>/<책-slug>/          개별 책 GitBook Space
```

**Notion은 필수 발행 단계가 아닙니다.** 필요할 때 외부 도서관·링크 모음으로만 사용할 수 있습니다. Google Drive도 선택적인 백업 서고이며 GitHub 발행을 지연시키지 않습니다.

## 기본 고속 발행 흐름

```text
ZIP / Markdown
→ 로컬에서 한 번만 해제·분석
→ 발행 파일명 정규화
→ GitBook용 README.md / SUMMARY.md / .gitbook.yaml 준비
→ 충돌 검사
→ Git tree 생성
→ 단일 commit 생성
→ main 반영
→ GitBook Git Sync
→ 공개 화면 확인
→ 새 책이면 library 인덱스 갱신
```

## 책 폴더 표준

```text
books/<분야>/<책-slug>/
├─ .gitbook.yaml
├─ README.md
├─ SUMMARY.md
└─ Markdown 파일들
```

`.gitbook.yaml`의 기본값은 다음과 같습니다.

```yaml
root: ./

structure:
  readme: README.md
  summary: SUMMARY.md
```

## 중앙 도서관

`library/`는 책 본문을 복제하지 않습니다. 분야별 안내와 현재 발행된 책의 인덱스만 관리합니다.

GitBook에서 Site Sections를 사용할 수 있는 경우 `library/` Space를 기본 Section으로 두고 각 책 Space를 같은 Docs Site의 Section으로 연결합니다. 그렇지 않은 경우 `library/`를 별도 공개 Space로 사용하고, 확인된 개별 웹북 공개 URL만 연결합니다.

## 모바일 단일 ZIP 발행

모바일에서 폴더 전체 업로드가 어려운 경우에는 **가공이 끝난 GitBook 발행용 ZIP 한 개만 저장소 최상단에 업로드**할 수 있습니다.

```text
준비된 ZIP 1개
→ webbooks 저장소 최상단에 업로드
→ Commit changes
→ mobile-zip-publish.yml 자동 실행
→ ZIP 안전 검사
→ ZIP 안의 books/**를 저장소에 배치
→ 업로드 ZIP 자동 제거
→ main에 발행 commit 1개 추가
→ GitBook Git Sync
```

자동 공정은 원고를 편집하지 않습니다. 기존 콘텐츠 파일과 같은 경로에 서로 다른 내용이 발견되면 덮어쓰지 않고 실패합니다. `README.md`, `SUMMARY.md`, `.gitbook.yaml`, `book.yaml` 같은 발행 메타데이터만 갱신을 허용합니다.

## 저장소 원칙

- 원본 Markdown 본문은 발행 과정에서 수정하지 않습니다.
- 기존 공개 경로·파일명·GitBook Project Directory를 우선 보호합니다.
- 일반 API 발행은 가능한 한 책 하나를 하나의 Git tree와 하나의 commit으로 반영합니다.
- GitHub는 콘텐츠의 기준 저장소이고 GitBook은 읽기 화면과 공개 사이트를 담당합니다.
- 일반 발행에 자체 웹북 엔진이나 GitHub Pages를 사용하지 않습니다.
- GitBook 편집기에서 본문을 따로 고쳐 GitHub 기준본과 갈라지게 만들지 않습니다.
- Actions는 데이터 재조립에 사용하지 않는 것이 기본이며, **모바일에서 이미 준비된 ZIP 한 개를 안전하게 풀어 배치하는 공정만 예외**로 허용합니다.

## 주요 구조

```text
.github/workflows/mobile-zip-publish.yml
library/
books/
README.md
WEBBOOK_STANDARD.md
FAST_PUBLISH_PROTOCOL.md
```
