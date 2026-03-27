# 📡 API 명세서 — 전국축제 영역 (서범 담당)

> **프로젝트**: 지역 축제 통합 정보 플랫폼 (이음)  
> **작성일**: 2026년 3월 27일  
> **작성자**: 서범  
> **버전**: v1.0  
> **Base URL**: `/api`

---

## 1. API 총괄표

| API ID | Method | Endpoint | 설명 | 사용 화면 |
|--------|--------|----------|------|----------|
| API_FES_0010 | GET | `/api/festivals` | 축제 통합 목록 조회 | 전체 목록, 진행중 목록, 진행전 목록 |
| API_FES_0020 | GET | `/api/festivals/{festivalId}` | 축제 상세 정보 조회 | 진행중 상세, 진행전 상세 |
| API_FES_0040 | POST | `/api/festivals/{festivalId}/scrap` | 축제 찜하기 토글 | 진행중 목록, 진행중 상세 |
| API_FES_0050 | GET | `/api/festivals/{festivalId}/filters` | 필터 옵션 조회 | 진행중 목록 |
| API_REV_0010 | GET | `/api/festivals/{festivalId}/reviews` | 리뷰 목록 조회 | 진행중 상세 |
| API_REV_0011 | POST | `/api/festivals/{festivalId}/reviews` | 리뷰 신규 등록 | 진행중 상세 |
| API_REV_0012 | PATCH | `/api/reviews/{commentId}` | 리뷰 내용 수정 | 진행중 상세 |
| API_REV_0013 | DELETE | `/api/reviews/{commentId}` | 리뷰 삭제 | 진행중 상세 |
| API_REV_0020 | GET | `/api/festivals/{festivalId}/reviews/stats` | 리뷰 통계/별점 조회 | 진행중 목록, 진행중 상세 |

---

## 2. 화면-API 매핑표

### 2-1. 전국축제 > 전체 목록 (`/festivals`)

| Method | 요청 파라미터 | 응답 예시 | API ID | 설명 |
|--------|-------------|----------|--------|------|
| GET | `status`, `region` | `{ "list": [...], "total": 100 }` | API_FES_0010 | 축제 통합 목록 조회 |

### 2-2. 전국축제 > 진행중 목록 (`/festivals?status=ongoing`)

| Method | 요청 파라미터 | 응답 예시 | API ID | 설명 |
|--------|-------------|----------|--------|------|
| GET | `status`, `region` | `{ "list": [...], "total": 100 }` | API_FES_0010 | 축제 통합 목록 조회 |
| GET | `festivalId` | `{ "avgStar": 4.5, "dist": {} }` | API_FES_0050 | 필터 옵션 조회 |
| POST | `festivalId` | `{ "isScrapped": true }` | API_FES_0040 | 축제 찜하기 토글 |
| GET | `festivalId` | `{ "avgStar": 4.5, "dist": {} }` | API_REV_0020 | 리뷰 통계/별점 |

### 2-3. 전국축제 > 진행중 상세 (`/festivals/[id]`)

| Method | 요청 파라미터 | 응답 예시 | API ID | 설명 |
|--------|-------------|----------|--------|------|
| GET | `festivalId` | `{ "info": {...}, "stats": {...} }` | API_FES_0020 | 축제 상세 정보 조회 |
| POST | `festivalId` | `{ "isScrapped": true }` | API_FES_0040 | 축제 찜하기 토글 |
| GET | `festivalId` | `{ "reviews": [...] }` | API_REV_0010 | 리뷰 목록 조회 |
| GET | `festivalId` | `{ "avgStar": 4.5, "dist": {} }` | API_REV_0020 | 리뷰 통계 정보 조회 |
| POST | `postId`, `content` | `{ "commentId": 55 }` | API_REV_0011 | 리뷰 신규 등록 |
| PATCH | `commentId` | `{ "status": "SUCCESS" }` | API_REV_0012 | 리뷰 내용 수정 |
| DELETE | `commentId` | `{ "status": "REMOVED" }` | API_REV_0013 | 리뷰 삭제 |

### 2-4. 전국축제 > 진행전 목록 (`/festivals?status=upcoming`)

| Method | 요청 파라미터 | 응답 예시 | API ID | 설명 |
|--------|-------------|----------|--------|------|
| GET | `status`, `region` | `{ "list": [...], "total": 100 }` | API_FES_0010 | 축제 통합 목록 조회 |

### 2-5. 전국축제 > 진행전 상세 (`/festivals/[id]`)

| Method | 요청 파라미터 | 응답 예시 | API ID | 설명 |
|--------|-------------|----------|--------|------|
| GET | `festivalId` | `{ "info": {...}, "stats": {...} }` | API_FES_0020 | 축제 상세 정보 조회 |

---

## 3. API 상세 명세

---

### API_FES_0010: 축제 통합 목록 조회

| 항목 | 내용 |
|------|------|
| **API ID** | API_FES_0010 |
| **엔드포인트** | `GET /api/festivals` |
| **설명** | 상태·지역 필터를 적용한 축제 통합 목록을 페이징으로 반환 |
| **인증** | ✅ 비회원 (인증 불필요) |
| **담당자** | 서범 |

**Query Parameters:**

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---------|------|------|-------|------|
| status | string | ❌ | 전체 | `ongoing` (진행중) / `upcoming` (진행전) / `ended` (종료) |
| region | string | ❌ | 전체 | 지역 코드 (예: `seoul`, `gyeonggi`, `busan` 등) |
| page | int | ❌ | 1 | 페이지 번호 |
| size | int | ❌ | 10 | 한 페이지당 항목 수 (최대 50) |
| sort | string | ❌ | latest | `latest` / `popular` / `rating` |
| keyword | string | ❌ | | 검색 키워드 (축제명 대상) |

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "festivalId": 1,
        "title": "서울 벚꽃 축제 2026",
        "address": "서울특별시 영등포구 여의서로",
        "startDate": "2026-04-01",
        "endDate": "2026-04-10",
        "status": "ONGOING",
        "imageUrl": "https://example.com/images/festival_1.jpg",
        "avgStar": 4.5,
        "reviewCount": 23,
        "viewCount": 1520,
        "isScrapped": false
      }
    ],
    "total": 100,
    "page": 1,
    "size": 10,
    "totalPages": 10
  }
}
```

**에러 응답:**

| HTTP Status | 에러 코드 | 설명 |
|-------------|----------|------|
| 400 | `COMMON_001` | 잘못된 요청 파라미터 (유효하지 않은 status 값 등) |
| 500 | `COMMON_002` | 서버 내부 오류 |

---

### API_FES_0020: 축제 상세 정보 조회

| 항목 | 내용 |
|------|------|
| **API ID** | API_FES_0020 |
| **엔드포인트** | `GET /api/festivals/{festivalId}` |
| **설명** | 특정 축제의 상세 정보와 통계 데이터를 반환 |
| **인증** | ✅ 비회원 (인증 불필요) |
| **담당자** | 서범 |

**Path Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| festivalId | Long | ✅ | 축제 고유 ID |

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "info": {
      "festivalId": 1,
      "title": "서울 벚꽃 축제 2026",
      "description": "여의도 윤중로에서 펼쳐지는 벚꽃 축제입니다. 야간 조명과 함께 특별한 봄을 만끽하세요.",
      "address": "서울특별시 영등포구 여의서로",
      "startDate": "2026-04-01",
      "endDate": "2026-04-10",
      "status": "ONGOING",
      "imageUrl": "https://example.com/images/festival_1.jpg",
      "latitude": 37.5217,
      "longitude": 126.9219,
      "tel": "02-1234-5678",
      "homepage": "https://yeouido-cherry.kr",
      "category": "A02",
      "areaCode": "1",
      "isScrapped": false
    },
    "stats": {
      "avgStar": 4.5,
      "reviewCount": 23,
      "viewCount": 1521,
      "scrapCount": 156
    }
  }
}
```

**에러 응답:**

| HTTP Status | 에러 코드 | 설명 |
|-------------|----------|------|
| 404 | `FEST_001` | 존재하지 않는 축제 ID |
| 500 | `COMMON_002` | 서버 내부 오류 |

**비즈니스 규칙:**
- 상세 페이지 조회 시 `viewCount` +1 증가 (세션/쿠키 기반 중복 방지)
- 로그인 사용자일 경우 `isScrapped` 필드에 찜 여부 반영

---

### API_FES_0040: 축제 찜하기 토글

| 항목 | 내용 |
|------|------|
| **API ID** | API_FES_0040 |
| **엔드포인트** | `POST /api/festivals/{festivalId}/scrap` |
| **설명** | 축제 찜하기 상태를 토글 (찜 → 찜 해제, 찜 해제 → 찜) |
| **인증** | 🔒 회원 (JWT 필수) |
| **담당자** | 서범 |

**Path Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| festivalId | Long | ✅ | 축제 고유 ID |

**Request Headers:**

| 헤더 | 값 | 필수 |
|------|-----|------|
| Authorization | `Bearer {JWT}` | ✅ |

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "festivalId": 1,
    "isScrapped": true,
    "message": "축제가 찜 목록에 추가되었습니다."
  }
}
```

```json
// 찜 해제 시
{
  "success": true,
  "data": {
    "festivalId": 1,
    "isScrapped": false,
    "message": "축제가 찜 목록에서 제거되었습니다."
  }
}
```

**에러 응답:**

| HTTP Status | 에러 코드 | 설명 |
|-------------|----------|------|
| 401 | `AUTH_001` | 인증이 필요합니다 |
| 404 | `FEST_001` | 존재하지 않는 축제 ID |
| 500 | `COMMON_002` | 서버 내부 오류 |

---

### API_FES_0050: 필터 옵션 조회

| 항목 | 내용 |
|------|------|
| **API ID** | API_FES_0050 |
| **엔드포인트** | `GET /api/festivals/{festivalId}/filters` |
| **설명** | 축제 목록 화면에서 사용할 필터 옵션 데이터 (평균 별점, 별점 분포 등) 반환 |
| **인증** | ✅ 비회원 (인증 불필요) |
| **담당자** | 서범 |

**Path Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| festivalId | Long | ✅ | 축제 고유 ID |

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "avgStar": 4.5,
    "dist": {
      "5": 45,
      "4": 30,
      "3": 15,
      "2": 7,
      "1": 3
    },
    "regions": [
      { "code": "seoul", "name": "서울", "count": 45 },
      { "code": "gyeonggi", "name": "경기", "count": 32 },
      { "code": "busan", "name": "부산", "count": 18 }
    ],
    "categories": [
      { "code": "A02", "name": "문화예술", "count": 28 },
      { "code": "A03", "name": "전통행사", "count": 15 }
    ]
  }
}
```

**에러 응답:**

| HTTP Status | 에러 코드 | 설명 |
|-------------|----------|------|
| 404 | `FEST_001` | 존재하지 않는 축제 ID |
| 500 | `COMMON_002` | 서버 내부 오류 |

---

### API_REV_0010: 리뷰 목록 조회

| 항목 | 내용 |
|------|------|
| **API ID** | API_REV_0010 |
| **엔드포인트** | `GET /api/festivals/{festivalId}/reviews` |
| **설명** | 특정 축제에 대한 리뷰 목록을 페이징으로 반환 |
| **인증** | ✅ 비회원 (인증 불필요) |
| **담당자** | 서범 |

**Path Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| festivalId | Long | ✅ | 축제 고유 ID |

**Query Parameters:**

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---------|------|------|-------|------|
| page | int | ❌ | 1 | 페이지 번호 |
| size | int | ❌ | 10 | 한 페이지당 항목 수 |
| sort | string | ❌ | latest | `latest` (최신순) / `rating` (별점순) |

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "reviews": [
      {
        "reviewId": 1,
        "userId": 5,
        "nickname": "축제러버",
        "profileImage": "/uploads/profiles/5.jpg",
        "rating": 5,
        "content": "정말 멋진 축제였습니다! 야간 조명이 특히 인상적이었어요.",
        "imageUrl": "/uploads/reviews/1.jpg",
        "createdAt": "2026-04-11T14:30:00",
        "updatedAt": "2026-04-11T14:30:00",
        "isOwner": false
      },
      {
        "reviewId": 2,
        "userId": 12,
        "nickname": "여행매니아",
        "profileImage": "/uploads/profiles/12.jpg",
        "rating": 4,
        "content": "분위기가 좋았지만 사람이 너무 많았어요.",
        "imageUrl": null,
        "createdAt": "2026-04-12T10:15:00",
        "updatedAt": "2026-04-12T10:15:00",
        "isOwner": false
      }
    ],
    "page": 1,
    "size": 10,
    "totalElements": 23,
    "totalPages": 3
  }
}
```

**에러 응답:**

| HTTP Status | 에러 코드 | 설명 |
|-------------|----------|------|
| 404 | `FEST_001` | 존재하지 않는 축제 ID |
| 500 | `COMMON_002` | 서버 내부 오류 |

---

### API_REV_0011: 리뷰 신규 등록

| 항목 | 내용 |
|------|------|
| **API ID** | API_REV_0011 |
| **엔드포인트** | `POST /api/festivals/{festivalId}/reviews` |
| **설명** | 특정 축제에 대한 리뷰를 신규 등록 |
| **인증** | 🔒 회원 (JWT 필수) |
| **Content-Type** | `multipart/form-data` |
| **담당자** | 서범 |

**Path Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| festivalId | Long | ✅ | 축제 고유 ID |

**Request Body (multipart/form-data):**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| content | string | ✅ | 리뷰 내용 (10~500자) |
| rating | int | ✅ | 별점 (1~5) |
| image | file | ❌ | 리뷰 이미지 (최대 5MB, jpg/png/webp) |

**Request 예시:**
```
POST /api/festivals/1/reviews
Content-Type: multipart/form-data
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...

content: "정말 멋진 축제였습니다!"
rating: 5
image: (binary file)
```

**Response (201 Created):**

```json
{
  "success": true,
  "data": {
    "commentId": 55,
    "festivalId": 1,
    "rating": 5,
    "content": "정말 멋진 축제였습니다!",
    "createdAt": "2026-04-11T14:30:00"
  }
}
```

**유효성 검사:**

| 필드 | 규칙 |
|------|------|
| content | 10자 이상, 500자 이하 |
| rating | 1~5 사이 정수 |
| image | 5MB 이하, 허용 확장자: jpg, png, webp |

**비즈니스 규칙:**
- 축제당 1인 1리뷰만 가능
- ~~ENDED 상태 축제만 리뷰 작성 가능 (프로젝트 정책에 따라 ONGOING 허용 여부 결정)~~

**에러 응답:**

| HTTP Status | 에러 코드 | 설명 |
|-------------|----------|------|
| 400 | `COMMON_001` | 유효성 검사 실패 (내용 길이, 별점 범위 등) |
| 401 | `AUTH_001` | 인증이 필요합니다 |
| 403 | `REVIEW_002` | 종료된 축제만 리뷰를 작성할 수 있습니다 |
| 404 | `FEST_001` | 존재하지 않는 축제 ID |
| 409 | `REVIEW_003` | 이미 해당 축제에 리뷰를 작성하셨습니다 |

---

### API_REV_0012: 리뷰 내용 수정

| 항목 | 내용 |
|------|------|
| **API ID** | API_REV_0012 |
| **엔드포인트** | `PATCH /api/reviews/{commentId}` |
| **설명** | 본인 리뷰의 내용을 수정 (부분 수정 지원) |
| **인증** | 🔒 회원 (JWT 필수, 본인만) |
| **담당자** | 서범 |

**Path Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| commentId | Long | ✅ | 리뷰(댓글) 고유 ID |

**Request Body:**

```json
{
  "content": "수정된 리뷰 내용입니다. 다시 가고 싶은 축제!",
  "rating": 4
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| content | string | ❌ | 수정할 리뷰 내용 (10~500자) |
| rating | int | ❌ | 수정할 별점 (1~5) |

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "commentId": 55,
    "status": "SUCCESS",
    "content": "수정된 리뷰 내용입니다. 다시 가고 싶은 축제!",
    "rating": 4,
    "updatedAt": "2026-04-12T09:00:00"
  }
}
```

**에러 응답:**

| HTTP Status | 에러 코드 | 설명 |
|-------------|----------|------|
| 400 | `COMMON_001` | 유효성 검사 실패 |
| 401 | `AUTH_001` | 인증이 필요합니다 |
| 403 | `REVIEW_004` | 본인의 리뷰만 수정할 수 있습니다 |
| 404 | `REVIEW_001` | 리뷰를 찾을 수 없습니다 |

---

### API_REV_0013: 리뷰 삭제

| 항목 | 내용 |
|------|------|
| **API ID** | API_REV_0013 |
| **엔드포인트** | `DELETE /api/reviews/{commentId}` |
| **설명** | 본인 리뷰를 삭제 처리 |
| **인증** | 🔒 회원 (JWT 필수, 본인만) |
| **담당자** | 서범 |

**Path Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| commentId | Long | ✅ | 리뷰(댓글) 고유 ID |

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "commentId": 55,
    "status": "REMOVED",
    "deletedAt": "2026-04-12T10:00:00"
  }
}
```

**비즈니스 규칙:**
- 소프트 삭제 처리 (`status = REMOVED`)
- 삭제 시 해당 축제의 평균 별점 재계산

**에러 응답:**

| HTTP Status | 에러 코드 | 설명 |
|-------------|----------|------|
| 401 | `AUTH_001` | 인증이 필요합니다 |
| 403 | `REVIEW_004` | 본인의 리뷰만 삭제할 수 있습니다 |
| 404 | `REVIEW_001` | 리뷰를 찾을 수 없습니다 |

---

### API_REV_0020: 리뷰 통계/별점 조회

| 항목 | 내용 |
|------|------|
| **API ID** | API_REV_0020 |
| **엔드포인트** | `GET /api/festivals/{festivalId}/reviews/stats` |
| **설명** | 특정 축제의 리뷰 통계 (평균 별점, 별점 분포) 반환 |
| **인증** | ✅ 비회원 (인증 불필요) |
| **담당자** | 서범 |

**Path Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| festivalId | Long | ✅ | 축제 고유 ID |

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "festivalId": 1,
    "avgStar": 4.5,
    "totalReviews": 23,
    "dist": {
      "5": 10,
      "4": 8,
      "3": 3,
      "2": 1,
      "1": 1
    }
  }
}
```

**에러 응답:**

| HTTP Status | 에러 코드 | 설명 |
|-------------|----------|------|
| 404 | `FEST_001` | 존재하지 않는 축제 ID |
| 500 | `COMMON_002` | 서버 내부 오류 |

---

## 4. 화면별 API 호출 흐름도

```mermaid
sequenceDiagram
    participant U as 사용자 (브라우저)
    participant S as 서버

    Note over U,S: 전체/진행중/진행전 목록 화면
    U->>S: GET /api/festivals?status=ongoing&region=seoul
    S-->>U: 200 { list: [...], total: 100 }

    Note over U,S: 목록에서 찜하기 클릭
    U->>S: POST /api/festivals/1/scrap
    S-->>U: 200 { isScrapped: true }

    Note over U,S: 축제 상세 화면 진입
    U->>S: GET /api/festivals/1
    S-->>U: 200 { info: {...}, stats: {...} }
    U->>S: GET /api/festivals/1/reviews/stats
    S-->>U: 200 { avgStar: 4.5, dist: {...} }
    U->>S: GET /api/festivals/1/reviews?page=1
    S-->>U: 200 { reviews: [...] }

    Note over U,S: 리뷰 작성
    U->>S: POST /api/festivals/1/reviews
    S-->>U: 201 { commentId: 55 }

    Note over U,S: 리뷰 수정
    U->>S: PATCH /api/reviews/55
    S-->>U: 200 { status: "SUCCESS" }

    Note over U,S: 리뷰 삭제
    U->>S: DELETE /api/reviews/55
    S-->>U: 200 { status: "REMOVED" }
```

---

## 5. 공통 응답 포맷

```json
// 성공 응답
{
  "success": true,
  "data": { ... },
  "error": null
}

// 실패 응답
{
  "success": false,
  "data": null,
  "error": {
    "code": "FEST_001",
    "message": "존재하지 않는 축제입니다."
  }
}
```

---

## 6. 에러 코드 표 (축제·리뷰 영역)

| 에러 코드 | HTTP Status | 설명 |
|----------|-------------|------|
| `AUTH_001` | 401 | 인증이 필요합니다 |
| `AUTH_003` | 403 | 접근 권한이 없습니다 |
| `AUTH_004` | 401 | 토큰이 만료되었습니다 |
| `FEST_001` | 404 | 축제를 찾을 수 없습니다 |
| `REVIEW_001` | 404 | 리뷰를 찾을 수 없습니다 |
| `REVIEW_002` | 403 | 종료된 축제만 리뷰를 작성할 수 있습니다 |
| `REVIEW_003` | 409 | 이미 해당 축제에 리뷰를 작성하셨습니다 |
| `REVIEW_004` | 403 | 본인의 리뷰만 수정/삭제할 수 있습니다 |
| `COMMON_001` | 400 | 잘못된 요청입니다 |
| `COMMON_002` | 500 | 서버 내부 오류가 발생했습니다 |

---

## 7. 인증 레벨 범례

| 표기 | 의미 | 헤더 |
|------|------|------|
| ✅ 비회원 | 인증 없이 접근 가능 | 없음 |
| 🔒 회원 | JWT 필수 (role=USER) | `Authorization: Bearer {JWT}` |
| 🔐 관리자 | JWT 필수 (role=ADMIN) | `Authorization: Bearer {JWT}` |

---

> **문서 이력**
>
> | 버전 | 날짜 | 작성자 | 내용 |
> |------|------|-------|------|
> | v1.0 | 2026-03-27 | 서범 | 최초 작성 — 축제 영역 9개 API 상세 명세 |
