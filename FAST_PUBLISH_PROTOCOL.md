# FAST_PUBLISH_PROTOCOL.md

이 문서는 `disnotons/webbooks` 저장소의 고속 웹북 발행 운영 규칙이다.

## 사용자가 `발행`이라고 하면

ZIP 또는 Markdown 입력을 한 책 단위로 처리한다.

1. 입력을 로컬 작업공간에서 한 번만 해제·수집한다.
2. 원본 Markdown 본문은 수정하지 않는다.
3. 공식 번호 → 첫 H1 → 확정 목차 → 기존 파일명 순으로 발행 파일명을 결정한다.
4. 발행용 복사본과 GitBook용 `README.md`, `SUMMARY.md`, `.gitbook.yaml`을 준비한다.
5. 기존 GitHub 경로와 파일 충돌을 확인한다.
6. 커밋 직전 최신 `main` commit과 tree를 다시 확인한다.
7. 정상 API 발행에서는 변경분을 하나의 Git tree로 구성한다.
8. 하나의 commit을 만들고 `main`에 반영한다.
9. GitBook Git Sync와 공개 화면을 확인한다.
10. 새 책이면 `library/`의 해당 분야 인덱스를 갱신한다. 기존 책에 장만 추가되고 공개 URL이 유지되면 중앙 도서관은 수정하지 않는다.
11. Notion 등 외부 도서관은 사용자가 원할 때만 등록한다.
12. Drive 백업은 필요할 때 책 폴더 또는 릴리스 ZIP 단위로 처리하며 GitHub 발행을 지연시키지 않는다.

## 기본 GitHub 반영 방식

```text
로컬 준비
→ 최신 main 확인
→ create_tree
→ create_commit
→ update_ref(main)
→ GitBook Git Sync
```

가능하면 **책 하나 = commit 하나**를 기본으로 한다.

여러 연구 프로젝트가 같은 `main`을 동시에 갱신할 수 있으므로 오래된 tree를 기준으로 커밋하지 않는다.

## GitBook 중앙 도서관

중앙 독자용 입구는 저장소의 `library/`를 사용한다.

```text
library/                         중앙 웹북 도서관 Space
books/<분야>/<책-slug>/          개별 책 Space
```

새 책을 처음 공개할 때만 분야별 인덱스에 추가한다.

GitBook에서 여러 Space를 한 Docs Site에 연결할 수 있으면 `library/`를 기본 Section으로 두고 개별 책 Space를 Section으로 연결한다. 해당 기능을 사용할 수 없으면 확인된 개별 공개 URL만 `library/`에서 링크한다. URL을 추정하지 않는다.

## 모바일 단일 ZIP 예외

모바일에서는 GitHub에 폴더를 통째로 업로드하기 어렵기 때문에, **이미 발행 구조가 완성된 ZIP 한 개를 저장소 최상단에 올리는 방식**을 예외적으로 허용한다.

사용자는 다음만 수행하면 된다.

```text
가공된 GitBook ZIP 1개
→ disnotons/webbooks 저장소 최상단에 업로드
→ Commit changes
```

그러면 `.github/workflows/mobile-zip-publish.yml`이 다음을 자동 처리한다.

```text
ZIP 검사
→ books/** 경로만 허용
→ 경로 탈출·심볼릭 링크·비정상 대용량 차단
→ .gitbook.yaml / README.md / SUMMARY.md 존재 확인
→ books/에 압축 해제
→ 기존 콘텐츠와 다른 파일 충돌 시 중단
→ 발행 메타데이터만 갱신 허용
→ 업로드 ZIP 제거
→ main에 발행 commit 1개 생성
→ GitBook Git Sync 대상 데이터 갱신
```

이 예외는 **이미 Chat 단계에서 가공이 끝난 ZIP을 운반하고 푸는 용도**일 뿐이다. Actions가 원고를 다시 분석하거나 번역·해설·본문을 수정하지 않는다.

ZIP의 기본 내부 구조는 다음과 같다.

```text
books/<분야>/<책-slug>/
├─ .gitbook.yaml
├─ README.md
├─ SUMMARY.md
└─ Markdown 파일들
```

## 금지

일반 발행에서는 다음을 사용하지 않는다.

- 파일마다 `create_file` 또는 `update_file`
- 파일마다 별도 commit
- base64·텍스트·유니코드 조각 분할 전송
- recovery / materialize / 책별 one-shot publish workflow를 새로 만드는 방식
- 검증을 위한 반복 commit
- Actions에서 기존 `main`을 강제로 재작성하는 방식
- 자체 웹북 엔진
- GitHub Pages 정적 웹북 빌드

단, 위의 **모바일 단일 ZIP 예외 공정**은 허용한다.

## 충돌 보호

모바일 ZIP 자동 발행에서도 기존 파일 보호를 우선한다.

- 기존 콘텐츠 파일과 경로가 같고 바이트가 동일함 → 그대로 통과
- 기존 콘텐츠 파일과 경로가 같고 내용이 다름 → 자동 덮어쓰기 금지, 작업 중단
- `README.md`, `SUMMARY.md`, `.gitbook.yaml`, `book.yaml` → 발행 구조 갱신을 위해 교체 허용
- ZIP 밖의 기존 책·폴더·공개 경로 → 변경 금지

## 실패 시

전체 공정을 다시 하지 않고 실패한 단계만 수정한다.

- ZIP 구조 실패 → ZIP만 다시 가공
- 충돌 실패 → 충돌 파일만 확인
- Action 실패 → 해당 Action 로그만 확인
- GitBook Sync 실패 → GitBook 연결만 확인
- 중앙 도서관 링크 실패 → 실제 공개 URL만 재확인

## 완료 기준

- 원본 본문이 변경되지 않음
- 대상 MD와 발행 MD 수가 일치함
- `SUMMARY.md`와 실제 순서가 일치함
- 기존 파일을 의도치 않게 덮어쓰지 않음
- GitHub 반영 완료
- GitBook Git Sync 완료
- 공개 URL 정상 열림
- 새 책이면 `library/` 인덱스 반영
