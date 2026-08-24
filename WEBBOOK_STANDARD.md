# WEBBOOK_STANDARD.md

## 1. 목적

이 저장소는 여러 연구·해설 프로젝트에서 완성된 Markdown 원고를 **내용을 변경하지 않고** GitHub를 거쳐 GitBook 웹북으로 발행·관리하기 위한 중앙 발행 저장소다.

핵심 원칙은 다음과 같다.

> 원본 Markdown은 손대지 않는다.
>
> GitHub는 콘텐츠의 기준 저장소다.
>
> GitBook은 실제 웹북 화면과 공개 사이트를 담당한다.
>
> 일반 발행에서는 자체 웹사이트나 웹북 엔진을 만들지 않는다.

---

## 2. 기본 발행 흐름

```text
연구·해설 프로젝트
→ 원본 Markdown / ZIP
→ 웹북 발행용 복사본 정규화
→ GitHub disnotons/webbooks
→ GitBook Git Sync
→ GitBook Space / Docs Site
→ 공개 웹북
```

필요할 때만 다음을 추가한다.

```text
GitBook 공개 링크 → 외부 도서관(Notion 등)
원본·발행본 ZIP → Google Drive 백업
```

Notion과 Drive는 필수 발행 단계가 아니다.

---

## 3. 서비스 역할

### GitHub

기본 저장소는 `disnotons/webbooks`, 기본 브랜치는 `main`이다.

관리 대상:

- Markdown 본문
- `README.md`
- `SUMMARY.md`
- `.gitbook.yaml`
- 이미지·첨부자료
- 파일명·폴더 구조
- 변경 이력
- 중앙 도서관 인덱스

### GitBook

담당 기능:

- 책 첫 페이지
- 사이드바 목차
- 페이지 이동
- 검색
- 모바일 화면
- 디자인
- 공개 URL
- 여러 Space를 한 Site에 연결할 수 있는 경우 중앙 내비게이션

본문과 목차의 기준본은 GitHub에 둔다. GitBook 편집기에서 임의로 따로 수정하여 GitHub와 내용이 갈라지게 만들지 않는다.

### Notion

필수가 아니다. 사용자가 원할 때만 외부 도서관·프런트 페이지·링크 모음으로 사용한다.

### Google Drive

원본 또는 발행본의 선택적 백업 서고다. Drive 작업 때문에 발행을 지연시키지 않는다.

---

## 4. 저장소 구조

```text
webbooks/
├─ library/
│  ├─ .gitbook.yaml
│  ├─ README.md
│  ├─ SUMMARY.md
│  └─ 분야별 안내 페이지
└─ books/
   ├─ aa/
   ├─ buddhism/
   ├─ christianity/
   ├─ jung/
   └─ 기타 분야/
```

개별 책의 기본 구조:

```text
books/<분야>/<책-slug>/
├─ .gitbook.yaml
├─ README.md
├─ SUMMARY.md
└─ Markdown 파일들
```

원칙:

> 책 폴더 하나 = GitBook Space 하나

책마다 GitHub 저장소를 새로 만들지 않는다.

`library/`도 하나의 별도 GitBook Space로 연결하며 책 본문을 복제하지 않는다.

---

## 5. 중앙 GitBook 도서관

`library/`는 모든 웹북을 발견하기 위한 중앙 입구다.

기본 역할:

- 분야별 분류
- 현재 발행된 책 목록
- 각 책의 간단한 소개
- GitBook 사이트 내 내비게이션의 시작 페이지

GitBook에서 여러 Space를 한 Docs Site의 Section으로 연결할 수 있는 경우:

```text
웹북 도서관 Space = 기본 Section
개별 책 Space = 각 Site Section
```

이 경우 GitBook이 Space 간 이동과 사이트 검색을 담당한다.

해당 기능을 사용할 수 없는 경우에는 `library/`를 별도 공개 Space로 유지하고 **실제로 확인된 개별 GitBook 공개 URL만** 분야별 페이지에 연결한다. URL을 추정하여 넣지 않는다.

새 책이 처음 공개되면 `library/` 인덱스도 한 번 갱신한다. 기존 책에 장만 추가되고 공개 URL이 유지되면 중앙 도서관을 불필요하게 수정하지 않는다.

---

## 6. GitBook 기본 파일

### `.gitbook.yaml`

```yaml
root: ./

structure:
  readme: README.md
  summary: SUMMARY.md
```

불필요한 설정은 추가하지 않는다.

### `README.md`

GitBook Space의 첫 페이지다.

```markdown
# 책 제목

책에 대한 간단한 소개
```

확인되지 않은 저자·번역자·출판정보는 넣지 않는다.

### `SUMMARY.md`

GitBook 목차의 기준이다.

```markdown
# Summary

* [소개](README.md)
* [1.1 첫 번째 글](01-01_첫_번째_글.md)
* [1.2 두 번째 글](01-02_두_번째_글.md)
```

`book.yaml`은 기존 책에서 필요하면 유지할 수 있지만 새 GitBook 발행의 필수 파일로 만들지 않는다.

---

## 7. 원본 콘텐츠 보존

사용자가 내용 수정을 명시하지 않았다면 다음을 변경하지 않는다.

- 문장·표현
- 번역·해설
- H1 제목
- 문단·소제목
- 번호·인용
- 설명량·문체

웹북 발행은 콘텐츠 편집 작업이 아니다.

원본은 그대로 보존하고 발행용 복사본만 만든다.

---

## 8. 발행 파일명 결정

사용자가 원본 파일명을 미리 정리할 필요는 없다.

우선순위:

1. 문서의 공식 번호
2. 첫 번째 H1 정식 제목
3. 확정 목차의 번호와 제목
4. 기존 파일명

기본:

```text
01_제목.md
```

장·절:

```text
01-01_제목.md
```

100개 이상:

```text
001_제목.md
```

1,000개 이상:

```text
0001_제목.md
```

파일명에서는 공백 대신 `_`를 사용하고 URL에 불필요한 장식용 괄호·따옴표·특수문자는 제거한다. 본문 H1은 변경하지 않는다.

---

## 9. 공개 후 경로 보호

한 번 공개된 파일명과 경로는 사실상 영구 ID처럼 취급한다.

특별한 이유가 없으면 다음을 하지 않는다.

- 기존 파일명 변경
- 기존 폴더 이동
- 책 slug 변경
- 공개 파일 대량 개명
- GitBook Project Directory 변경
- 공개 URL 변경

새 표준보다 기존 공개 URL과 기존 경로의 보존을 우선한다.

---

## 10. 사용자가 `발행`이라고 하면

ZIP 또는 여러 Markdown 파일을 전달하고 `발행`이라고 하면 특별한 지시가 없는 한 다음을 수행한다.

```text
ZIP·MD 수집
→ 로컬에서 한 번만 해제
→ MD 수·H1·번호 분석
→ 기존 GitHub 경로 확인
→ 발행 파일명 일괄 결정
→ 본문 불변 발행용 복사본 생성
→ README.md 확인 또는 생성
→ SUMMARY.md 생성 또는 갱신
→ .gitbook.yaml 확인 또는 생성
→ 기존 파일 충돌 검사
→ 하나의 Git tree 구성
→ 하나의 commit 생성
→ main 반영
→ GitBook Git Sync 확인
→ 목차·본문·공개 URL 확인
→ 새 책이면 library 인덱스 갱신
→ 필요할 때만 외부 도서관 등록 또는 Drive 백업
```

---

## 11. GitHub 고속 발행

대량 발행은 가능한 한 Git Data API의 단일 tree/commit 방식으로 처리한다.

```text
현재 main commit 확인
→ 현재 tree 확인
→ 변경 파일 준비
→ create_tree
→ create_commit
→ update_ref(main)
```

기본 원칙:

> 책 하나의 한 차례 발행 = 가능한 한 commit 하나

동시에 다른 프로젝트가 `main`을 갱신할 수 있으므로 커밋 직전 최신 `main`과 base tree를 다시 확인한다.

---

## 12. 모바일 ZIP 예외

모바일에서 폴더 전체 업로드가 어려운 경우, 이미 발행 구조가 완성된 ZIP 한 개를 저장소 최상단에 올리고 `.github/workflows/mobile-zip-publish.yml`로 안전하게 풀어 배치하는 예외 공정을 허용한다.

이 공정은 원고를 분석·번역·재작성하지 않는다.

---

## 13. 느린 방식과 불필요한 자동화 금지

특별한 이유가 없는 한 다음을 하지 않는다.

- Markdown마다 개별 create/update
- 파일마다 별도 commit
- Contents API 순차 반복 업로드
- ZIP 조각 분할
- 데이터 재조립용 Actions
- recovery workflow
- 검증용 반복 commit
- trigger용 branch·PR
- Actions를 이용한 `main` 재작성

---

## 14. 자체 웹북 엔진과 GitHub Pages 사용 금지

GitBook을 최종 플랫폼으로 사용하므로 일반 발행에서는 다음을 새로 만들거나 유지·확장하지 않는다.

```text
site/
tools/build_site.py
책별 HTML/CSS/JavaScript
chapters.json
책별 Pages workflow
정적 웹북 빌드 엔진
```

Markdown에 HTML·CSS·JavaScript·수동 이전·다음 링크를 넣지 않는다.

목차·검색·페이지 이동·모바일 화면·공개 사이트는 GitBook이 담당한다.

---

## 15. 충돌과 기존 데이터 보호

동일한 발행 파일명이 이미 있으면 자동 덮어쓰기하지 않는다.

확인:

- 같은 문서의 업데이트인가
- 다른 문서인가
- 교체 지시가 있었는가

교체 지시가 없으면 기존 파일을 보존한다.

별도 지시 없이 다음을 하지 않는다.

- 기존 책·Space 삭제
- 기존 공개 URL 변경
- 기존 파일 대량 개명
- 다른 책 파일 삭제
- 기존 Markdown 덮어쓰기
- 원본 삭제
- 본문 재작성

---

## 16. 발행 후 검증

기본 확인:

1. GitHub commit 반영
2. 대상 MD와 발행 MD 수 일치
3. `SUMMARY.md`와 실제 순서 일치
4. GitBook Git Sync 완료
5. README 정상 표시
6. 목차 정상 표시
7. 공개 URL에서 새 문서 열림
8. 기존 문서·URL 유지
9. 새 책이면 중앙 도서관 인덱스 반영

동일한 항목을 불필요하게 반복 검증하지 않는다.

---

## 17. 실패 시 처리

전체 공정을 다시 하지 않고 실패한 단계만 수정한다.

- 로컬 준비 실패 → 로컬만 수정
- tree 실패 → tree만 수정
- commit 실패 → commit만 수정
- SUMMARY 문제 → SUMMARY만 수정
- GitBook Sync 실패 → Sync만 확인
- 공개 문제 → GitBook 사이트 설정만 확인
- 도서관 링크 문제 → 확인된 공개 URL만 수정

---

## 18. 완료 기준

다음이 충족되면 완료다.

- 원본 본문 불변
- 대상 MD와 발행 MD 수 일치
- 파일명·목차 순서 정상
- 기존 파일 무단 덮어쓰기 없음
- GitHub 반영 완료
- `SUMMARY.md` 정상
- GitBook Sync 완료
- 공개 웹북 정상 열림
- 기존 공개 URL 보호
- 새 책이면 중앙 GitBook 도서관에 반영

---

## 19. 규칙 우선순위

1. 사용자의 최신 명시적 지시
2. 기존 GitBook 공개 URL 보호
3. 기존 GitHub 경로 보호
4. 원본 콘텐츠 보존
5. 확정 목차·번호·순서 보존
6. 기존 발행 파일명 보호
7. GitBook Git Sync 구조
8. GitHub 단일 tree/commit 고속 발행
9. 중앙 도서관 일관성
10. 관리 편의성
11. 디자인

---

## 20. 핵심 운영 원칙

> 각 연구 프로젝트는 원고를 만든다.
>
> 웹북 프로젝트는 발행 구조만 정규화한다.
>
> 원본 Markdown은 손대지 않는다.
>
> GitHub가 콘텐츠 기준 저장소다.
>
> GitBook이 웹북 화면·검색·공개 사이트와 중앙 독자 경험을 담당한다.
>
> 한 저장소 안에 여러 책을 보관한다.
>
> 책 폴더 하나를 GitBook Space 하나에 연결한다.
>
> `library/`를 중앙 웹북 도서관 Space로 사용한다.
>
> `README.md`는 첫 페이지, `SUMMARY.md`는 목차다.
>
> 자체 웹북 엔진과 GitHub Pages는 일반 발행에 사용하지 않는다.
>
> 책 한 차례 발행은 가능한 한 하나의 Git tree와 하나의 commit으로 처리한다.
>
> Notion과 Drive는 선택 사항이다.
