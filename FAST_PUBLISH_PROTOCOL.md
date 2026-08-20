# FAST_PUBLISH_PROTOCOL.md

이 문서는 `disnotons/webbooks` 저장소의 고속 웹북 발행 운영 규칙이다.

## 사용자가 `발행`이라고 하면

ZIP 또는 Markdown 입력을 한 책 단위로 처리한다.

1. 입력을 로컬 작업공간에서 한 번만 해제·수집한다.
2. 원본 Markdown 본문은 수정하지 않는다.
3. 공식 번호 → 첫 H1 → 확정 목차 → 기존 파일명 순으로 발행 파일명을 결정한다.
4. 발행용 복사본과 `book.yaml`을 로컬에서 한 번에 만든다.
5. 기존 GitHub 경로와 파일 충돌을 확인한다.
6. 새 MD와 `book.yaml`을 하나의 Git tree로 구성한다.
7. 하나의 commit을 만들고 `main` ref를 갱신한다.
8. Pages 배포를 한 번 확인한다.
9. 새 책이면 Notion 도서관에 한 번 등록한다. 기존 공개 URL이 유지되면 Notion은 다시 수정하지 않는다.
10. Drive 백업은 필요할 때 책 폴더 또는 릴리스 ZIP 단위로 처리하며 GitHub 발행을 지연시키지 않는다.

## GitHub 반영 방식

정상 발행은 다음 흐름만 사용한다.

```text
로컬 준비
→ create_tree
→ create_commit
→ update_ref(main)
→ Pages
```

가능하면 `create_tree`에 파일 내용을 직접 포함한다. 필요할 때만 `create_blob`을 사용한다.

**책 하나 = commit 하나**를 기본으로 한다.

## 금지

정상 발행에서 다음을 사용하지 않는다.

- 파일마다 `create_file` 또는 `update_file`
- 파일마다 별도 commit
- `.webbook-upload` 전송 폴더
- base64·텍스트·유니코드 조각 분할 전송
- GitHub Actions에서 데이터 재조립
- recovery / materialize / one-shot publish workflow
- trigger용 branch·PR·commit
- 검증을 위한 반복 commit
- Actions에서 `main` 강제 재작성

GitHub Actions는 사이트 빌드와 Pages 배포에만 사용한다.

## 저장소 청결 규칙

정상 상태의 저장소에는 다음이 없어야 한다.

```text
.webbook-upload/
.webbook-debug/
recovery 전용 데이터 폴더
책별 일회성 workflow
trigger 전용 파일·브랜치에 의존하는 발행 구조
```

`books/`에는 실제 발행 데이터만 둔다.

## 실패 시

전체 공정을 처음부터 반복하지 않는다.

- 로컬 준비 실패 → 로컬 준비만 수정
- tree 실패 → tree 입력만 수정
- commit 실패 → commit 단계만 수정
- Pages 실패 → Pages만 확인

이미 성공한 단계를 위해 새 trigger commit을 만들지 않는다.

## 완료 기준

- 대상 MD 수와 발행 MD 수가 일치함
- 원본 본문이 변경되지 않음
- `book.yaml`과 실제 파일 순서가 일치함
- 기존 파일을 의도치 않게 덮어쓰지 않음
- 책 단위 단일 commit이 `main`에 반영됨
- Pages 배포 성공
- 공개 URL 열림
- 새 책인 경우에만 Notion 도서관 등록
