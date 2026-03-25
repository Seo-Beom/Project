# NCafe 프론트엔드 청사진 (Blueprint)

> 📅 작성일: 2026-01-21
> 🎯 목표: 카페 사장님용 메뉴 관리 페이지 프로토타입

---

## 1. 기술 스택 선정

### 🔧 Core Framework
| 기술 | 버전 | 선정 이유 |
|------|------|----------|
| **Next.js** | 15.x | SSR/SSG 지원, App Router, React 기반, 풀스택 가능 |
| **React** | 19.x | 컴포넌트 기반, 생태계, Next.js 내장 |
| **TypeScript** | 5.x | 타입 안정성, 개발 생산성 |

### 🎨 스타일링
| 기술 | 선정 이유 |
|------|----------|
| **CSS Modules** | 컴포넌트별 스코프, 유지보수 용이, 빌드 최적화 |
| **CSS Variables** | 테마 관리, 다크모드 지원 |

### 📦 주요 라이브러리
| 라이브러리 | 용도 | 필수 여부 |
|-----------|------|----------|
| `react-hook-form` | 폼 관리 (메뉴 등록/수정) | ✅ 필수 |
| `zustand` | 전역 상태 관리 (장바구니 등) | ✅ 필수 |
| `react-hot-toast` | 알림 토스트 | ⭕ 권장 |
| `lucide-react` | 아이콘 | ⭕ 권장 |
| `date-fns` | 날짜 포맷팅 | ⭕ 권장 |

### 🚫 사용하지 않는 것
| 기술 | 이유 |
|------|------|
| TailwindCSS | CSS Modules로 충분, 커스텀 디자인 시스템 구축 |
| Redux | Zustand가 더 가볍고 간단 |
| styled-components | CSS Modules 선호 |

---

## 2. 디렉토리 구조

```
ncafe/
├── backend/                    # 기존 Spring Boot (나중에)
│
└── frontend/                   # 📁 새로 생성
    ├── public/
    │   ├── images/
    │   │   └── menu/          # 메뉴 이미지
    │   └── fonts/
    │
    ├── app/                    # Next.js App Router
    │   ├── layout.tsx          # 루트 레이아웃
    │   ├── page.tsx            # 홈페이지
    │   ├── globals.css         # 전역 스타일 + CSS Variables
    │   │
    │   ├── (public)/           # 고객용 (나중에)
    │   │   └── [cafeId]/
    │   │       └── menus/
    │   │
    │   └── admin/              # 🎯 사장님용 (먼저 개발)
    │       ├── layout.tsx
    │       ├── _components/        # 📍 admin 레이아웃 전용 컴포넌트
    │       │   ├── AdminSidebar/
    │       │   └── AdminHeader/
    │       ├── page.tsx            # 대시보드
    │       ├── menus/
    │       │   ├── page.tsx        # 메뉴 목록    → /admin/menus
    │       │   ├── _components/    # 📍 메뉴 목록 전용 컴포넌트
    │       │   │   ├── MenuCard/
    │       │   │   ├── MenuList/
    │       │   │   └── CategoryTabs/
    │       │   ├── new/
    │       │   │   ├── page.tsx    # 메뉴 등록    → /admin/menus/new
    │       │   │   └── _components/ # 📍 메뉴 등록 전용 컴포넌트
    │       │   │       └── MenuForm/
    │       │   └── [id]/
    │       │       ├── page.tsx    # 메뉴 상세    → /admin/menus/123
    │       │       └── edit/
    │       │           ├── page.tsx # 메뉴 수정   → /admin/menus/123/edit
    │       │           └── _components/ # 📍 메뉴 수정 전용 컴포넌트
    │       │               └── MenuEditForm/
    │       ├── orders/             # (나중에)
    │       └── settings/           # (나중에)
    │
    ├── components/             # 🌐 전역 공용 컴포넌트만
    │   └── common/             # UI 기본 컴포넌트
    │       ├── Button/
    │       │   ├── Button.tsx
    │       │   └── Button.module.css
    │       ├── Input/
    │       ├── Modal/
    │       ├── Card/
    │       └── Toast/
    │
    ├── hooks/                  # 커스텀 훅
    │   ├── useMenu.ts
    │   └── useToast.ts
    │
    ├── stores/                 # Zustand 스토어
    │   ├── menuStore.ts
    │   └── authStore.ts
    │
    ├── services/               # API 호출 (나중에 백엔드 연동)
    │   ├── api.ts
    │   └── menuService.ts
    │
    ├── types/                  # TypeScript 타입
    │   ├── menu.ts
    │   ├── order.ts
    │   └── cafe.ts
    │
    ├── utils/                  # 유틸리티
    │   ├── format.ts
    │   └── validation.ts
    │
    ├── mocks/                  # 목업 데이터 (프로토타입용)
    │   └── menuData.ts
    │
    ├── next.config.js
    ├── tsconfig.json
    ├── package.json
    └── README.md
```

---

## 3. 디자인 시스템

### 🎨 Color Palette
```css
:root {
  /* Primary - 따뜻한 갈색 계열 (커피 테마) */
  --color-primary-50: #fdf8f6;
  --color-primary-100: #f2e8e5;
  --color-primary-200: #eaddd7;
  --color-primary-500: #a47551;
  --color-primary-600: #8b5a3c;
  --color-primary-700: #6f4a31;
  
  /* Neutral */
  --color-gray-50: #fafafa;
  --color-gray-100: #f5f5f5;
  --color-gray-200: #e5e5e5;
  --color-gray-500: #737373;
  --color-gray-700: #404040;
  --color-gray-900: #171717;
  
  /* Semantic */
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;
  
  /* Background */
  --bg-primary: #ffffff;
  --bg-secondary: #fafafa;
  --bg-tertiary: #f5f5f5;
}
```

### 📐 Typography
```css
:root {
  --font-sans: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
  
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
}
```

### 📏 Spacing
```css
:root {
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-5: 1.25rem;  /* 20px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --space-10: 2.5rem;  /* 40px */
  --space-12: 3rem;    /* 48px */
}
```

### 🔲 Border Radius
```css
:root {
  --radius-sm: 0.25rem;   /* 4px */
  --radius-md: 0.5rem;    /* 8px */
  --radius-lg: 0.75rem;   /* 12px */
  --radius-xl: 1rem;      /* 16px */
  --radius-full: 9999px;
}
```

---

## 4. Phase 1 개발 범위

> **📋 체크리스트 사용 안내 (AI 필독)**
> - 아래 `- [ ]` 항목은 **구현 진행 상황**을 추적하는 체크리스트입니다.
> - **기능 구현이 완료되면** AI가 해당 항목을 `- [x]`로 체크해주세요.
> - 새로운 AI 세션이 시작되더라도, 이 체크리스트를 보고 **어디까지 진행되었는지** 파악한 후 이어서 진행하세요.
> - 체크된 항목은 완료, 체크되지 않은 항목은 미완료를 의미합니다.

### 🎯 메뉴 관리 페이지 기능

#### 4.1 메뉴 목록 페이지 (`/admin/menus`)
- [x] 카테고리별 탭 필터 (커피, 음료, 디저트 등)
- [x] 메뉴 카드 그리드 뷰
- [x] 메뉴 검색
- [x] 품절 토글 (목록에서 바로)
- [x] 메뉴 순서 변경 (드래그앤드롭)
- [x] 메뉴 삭제

#### 4.2 메뉴 상세 페이지 (`/admin/menus/[id]`)
- [x] 메뉴 정보 표시 (이름, 가격, 설명, 이미지)
- [x] 옵션 정보 표시
- [x] 판매 상태 표시
- [x] 수정 페이지로 이동 버튼
- [x] 삭제 버튼

#### 4.3 메뉴 등록 페이지 (`/admin/menus/new`)
- [x] 메뉴명 (한글/영문)
- [x] 가격
- [x] 설명
- [x] 카테고리 선택
- [x] 이미지 업로드 (드래그앤드롭)
- [x] 옵션 관리 (사이즈, 샷 추가 등)
- [x] 판매 상태 (판매중/품절/숨김)

#### 4.4 메뉴 수정 페이지 (`/admin/menus/[id]/edit`)
- [x] 기존 메뉴 정보 불러오기
- [x] 메뉴명 (한글/영문) 수정
- [x] 가격 수정
- [x] 설명 수정
- [x] 카테고리 변경
- [x] 이미지 변경
- [x] 옵션 관리 (추가/수정/삭제)
- [x] 판매 상태 변경

#### 4.5 공통 레이아웃
- [x] 사이드바 네비게이션
- [x] 헤더 (카페명, 프로필)
- [ ] 반응형 (모바일 대응)

---

## 5. 목업 데이터 구조

```typescript
// types/menu.ts
interface Menu {
  id: string;
  korName: string;
  engName: string;
  description: string;
  price: number;
  category: MenuCategory;        // 카테고리 정보 (또는 categoryId: string)
  images: MenuImage[];           // 여러 이미지 지원
  isAvailable: boolean;
  isSoldOut: boolean;
  sortOrder: number;
  options: MenuOption[];
  createdAt: Date;
  updatedAt: Date;
}

interface MenuImage {
  id: string;
  url: string;
  isPrimary: boolean;            // 대표 이미지 여부
  sortOrder: number;
}

interface MenuOption {
  id: string;
  name: string;
  type: 'radio' | 'checkbox';
  required: boolean;
  items: OptionItem[];
}

interface OptionItem {
  id: string;
  name: string;
  priceDelta: number; // 추가 가격 (0이면 무료)
}

interface MenuCategory {
  id: string;
  korName: string;               // 한글명 (예: "커피", "음료")
  engName: string;               // 영문명 (예: "Coffee", "Beverage")
  icon?: string;                 // 아이콘 (선택)
  sortOrder: number;             // 정렬 순서
}
```

---

## 6. 개발 순서

```
Step 1: 프로젝트 초기화
├── Next.js 프로젝트 생성
├── 필수 라이브러리 설치
├── 디렉토리 구조 생성
└── CSS Variables 설정 (디자인 시스템)

Step 2: 공통 컴포넌트
├── Button, Input, Card 등
├── AdminSidebar, AdminHeader
├── Modal, Toast
└── 이미지 업로드 컴포넌트 (다중 이미지 지원)

Step 3: 메뉴 목록 페이지 (/admin/menus)
├── MenuCard 컴포넌트
├── MenuList 컴포넌트
├── CategoryTabs 컴포넌트
├── 목업 데이터로 렌더링
├── 품절 토글 기능
└── 메뉴 검색 기능

Step 4: 메뉴 상세 페이지 (/admin/menus/[id])
├── 메뉴 정보 표시
├── 다중 이미지 갤러리
├── 옵션 정보 표시
└── 수정/삭제 버튼

Step 5: 메뉴 등록 페이지 (/admin/menus/new)
├── MenuForm 컴포넌트
├── 다중 이미지 업로드 UI (대표 이미지 선택)
├── 카테고리 선택
├── 옵션 관리 UI
└── 폼 유효성 검사

Step 6: 메뉴 수정 페이지 (/admin/menus/[id]/edit)
├── 기존 데이터 불러오기
├── MenuForm 재사용
├── 이미지 추가/삭제/대표 변경
└── 저장 및 취소

Step 7: 피드백 & 개선
├── UX 개선
├── 애니메이션 추가
└── 반응형 최적화
```

---

## 7. 실행 명령어

```bash
# 프로젝트 시작
cd frontend
npm run dev

# 빌드
npm run build

# 린트
npm run lint
```

---

## ✅ 승인 체크리스트

아래 항목을 확인해주세요:

- [ ] Next.js 15 + TypeScript 사용 동의
- [ ] CSS Modules 스타일링 방식 동의
- [ ] 디렉토리 구조 동의
- [ ] 디자인 컬러 (커피 테마 갈색 계열) 동의
- [ ] Phase 1 개발 범위 동의

> 💬 수정이 필요한 부분이 있으면 알려주세요!
