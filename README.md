# webbooks

웹북 발행 전용 저장소입니다.

이 저장소는 **원본 Markdown을 편집하는 곳이 아니라 발행용 복사본을 관리하는 곳**입니다.

## 고속 발행 흐름

```text
ZIP / Markdown
→ 로컬에서 한 번만 해제·분석
→ 발행 파일명 정규화
→ book.yaml 생성
→ Git tree 생성
→ 단일 commit 생성
→ main ref 갱신
→ GitHub Pages 배포
```

## 저장소 원칙

- 책 하나는 가능한 한 하나의 Git tree와 하나의 commit으로 반영합니다.
- `.webbook-upload`, 전송 조각, 복구용 workflow, trigger commit/PR을 발행 수단으로 사용하지 않습니다.
- GitHub Actions는 사이트 빌드·배포에만 사용합니다.
- `books/`에는 발행용 Markdown과 `book.yaml`만 둡니다.
- 원본 Markdown 본문은 발행 과정에서 수정하지 않습니다.

## 기본 구조

```text
.github/workflows/deploy-pages.yml
books/
site/
tools/prepare_webbook.py
WEBBOOK_STANDARD.md
FAST_PUBLISH_PROTOCOL.md
```
