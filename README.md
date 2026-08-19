# Webbooks

웹북 전용 통합 저장소입니다.

이 저장소는 여러 연구·해설 프로젝트에서 제작된 Markdown 원고를 **발행용 구조로 정규화하여 관리하고 웹북으로 출판하기 위한 전용 저장소**입니다.

## 기본 원칙

- 원본 Markdown은 수정하지 않습니다.
- 발행용 복사본의 파일명·폴더·메타데이터만 표준화합니다.
- 기존 공개 URL과 기존 발행본을 우선 보호합니다.
- 책마다 별도 저장소를 만들지 않고 이 저장소 안에서 통합 관리합니다.
- Markdown 콘텐츠와 웹사이트 기능을 분리합니다.

## 기본 구조

```text
webbooks/
├─ books/               # 발행용 Markdown과 book.yaml
│  ├─ buddhism/
│  ├─ christianity/
│  ├─ jung/
│  ├─ hawkins/
│  ├─ bailey/
│  └─ other/
├─ site/                # 공통 웹북 엔진·디자인
├─ WEBBOOK_STANDARD.md  # 공통 발행 규격
└─ README.md
```

새 웹북은 원본 MD를 그대로 보존한 채 `books/` 아래에 발행용 복사본을 만들고, 번호·파일명·`book.yaml`만 표준화합니다.

상세 규격은 `WEBBOOK_STANDARD.md`를 따릅니다.
