# webbooks

웹북 발행 전용 저장소입니다.

이 저장소는 **원본 Markdown을 편집하는 곳이 아니라 발행용 복사본을 관리하는 곳**입니다.

## 기본 고속 발행 흐름

```text
ZIP / Markdown
→ 로컬에서 한 번만 해제·분석
→ 발행 파일명 정규화
→ GitBook용 README.md / SUMMARY.md / .gitbook.yaml 준비
→ Git tree 생성
→ 단일 commit 생성
→ main 반영
→ GitBook Git Sync
```

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

ZIP은 미리 다음과 같은 발행 구조를 포함해야 합니다.

```text
books/<분야>/<책-slug>/
├─ .gitbook.yaml
├─ README.md
├─ SUMMARY.md
└─ Markdown 파일들
```

자동 공정은 원고를 편집하지 않습니다. 기존 콘텐츠 파일과 같은 경로에 서로 다른 내용이 발견되면 덮어쓰지 않고 실패합니다. `README.md`, `SUMMARY.md`, `.gitbook.yaml`, `book.yaml` 같은 발행 메타데이터만 갱신을 허용합니다.

## 저장소 원칙

- 원본 Markdown 본문은 발행 과정에서 수정하지 않습니다.
- 기존 공개 경로와 파일을 우선 보호합니다.
- 일반 API 발행은 가능한 한 책 하나를 하나의 Git tree와 하나의 commit으로 반영합니다.
- GitHub Actions를 데이터 재조립에 사용하지 않는 것이 기본이며, **모바일에서 준비된 ZIP 한 개를 안전하게 풀어 배치하는 공정만 예외**로 허용합니다.
- ZIP 안에는 `books/**` 외의 경로를 넣지 않습니다.

## 주요 구조

```text
.github/workflows/mobile-zip-publish.yml
books/
README.md
WEBBOOK_STANDARD.md
FAST_PUBLISH_PROTOCOL.md
```
