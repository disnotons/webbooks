# WEBBOOK_ENGINE.md

## 목적

`books/`에 표준 웹북 데이터가 들어오면 공통 프레임이 자동으로 도서관과 책별 읽기 화면을 생성한다.
Markdown 본문은 빌드 과정에서 수정하지 않는다.

## 데이터와 엔진 분리

- `books/`: 발행 데이터 (`book.yaml` + Markdown)
- `site/`: 모든 책이 공유하는 화면·스타일·브라우저 코드
- `tools/prepare_webbook.py`: ZIP/MD를 발행 구조로 준비
- `tools/build_site.py`: `books/`를 읽어 정적 Pages 사이트 생성
- `.github/workflows/deploy-pages.yml`: `main` 반영 후 한 번 빌드·배포

## 자동 출력

`book.yaml`이 있는 폴더는 자동으로 한 권의 웹북이 된다.

예:

```text
books/christianity/mechthild/book.yaml
books/christianity/mechthild/chapters/01_....md
```

빌드 후:

```text
/christianity/mechthild/
/catalog.json
```

이 생성된다. 책별 HTML/CSS/JS를 원고와 함께 저장할 필요가 없다.

## 읽기 기능

공통 엔진이 다음을 제공한다.

- 전체 웹북 도서관
- 책별 전체 목차
- 목차 검색
- 이전·다음 이동
- 모바일 목차
- 다크 모드
- 읽기 진행 표시
- 맨 위로 이동
- 현재 장 URL 공유
- Markdown 렌더링

## 로컬 확인

```bash
python tools/build_site.py --books books --site site --output _site
python -m http.server 8000 -d _site
```

## 발행 원칙

책 데이터 반영은 기존 `FAST_PUBLISH_PROTOCOL.md`를 따른다.
즉 책 하나는 로컬에서 준비한 뒤 Git tree 하나와 commit 하나로 `main`에 반영한다.
Actions는 책 데이터를 운반하거나 재조립하지 않고 사이트 빌드·배포만 담당한다.
