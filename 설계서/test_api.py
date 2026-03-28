import urllib.request, ssl, json, urllib.parse

ssl._create_default_https_context = ssl._create_unverified_context

SERVICE_KEY = "322e530c75f9c8df08b2302da8e51cf93bc1d45b5f5c285e6ca8432a45727562"
BASE = "https://apis.data.go.kr/B551011/KorService2"

def build_url(endpoint, **params):
    p = {"serviceKey": SERVICE_KEY, "MobileOS": "ETC", "MobileApp": "IEUM", "_type": "json", "numOfRows": "10", "pageNo": "1"}
    p.update(params)
    return BASE + "/" + endpoint + "?" + urllib.parse.urlencode(p)

def call_api(name, endpoint, **params):
    url = build_url(endpoint, **params)
    print("")
    print("=" * 70)
    print("[TEST] " + name)
    print("=" * 70)
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
            rc = data.get("response",{}).get("header",{}).get("resultCode","?")
            rm = data.get("response",{}).get("header",{}).get("resultMsg","?")
            tc = data.get("response",{}).get("body",{}).get("totalCount","?")
            items_raw = data.get("response",{}).get("body",{}).get("items",{})
            if isinstance(items_raw, dict):
                items = items_raw.get("item", [])
            elif items_raw == "" or items_raw is None:
                items = []
            else:
                items = items_raw

            status = "PASS" if rc == "0000" else "FAIL"
            print(">> [{}] resultCode={} | resultMsg={} | totalCount={}".format(status, rc, rm, tc))

            if isinstance(items, list):
                for i, item in enumerate(items[:2]):
                    txt = json.dumps(item, ensure_ascii=False)
                    if len(txt) > 400:
                        txt = txt[:400] + "..."
                    print("   item[{}]: {}".format(i, txt))
                if len(items) > 2:
                    print("   ... +{} more items".format(len(items)-2))
            elif isinstance(items, dict):
                txt = json.dumps(items, ensure_ascii=False)
                if len(txt) > 400:
                    txt = txt[:400] + "..."
                print("   item: {}".format(txt))
            
            return data
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")[:300]
        print(">> [FAIL] HTTP {} - {}".format(e.code, body))
        return None
    except Exception as e:
        print(">> [FAIL] ERROR: {}".format(e))
        return None

# ===== START =====
print("=" * 70)
print("  Korean Tourism API (KorService2) - Full Test")
print("  Base URL: " + BASE)
print("=" * 70)

# 1. 지역코드조회
call_api("1. 지역코드조회 (areaCode2)", "areaCode2", numOfRows="20")

# 2. 서비스분류코드조회
call_api("2. 서비스분류코드조회 (categoryCode2)", "categoryCode2", numOfRows="10")

# 3. 지역기반 관광정보조회 (서울, 축제)
resp3 = call_api("3. 지역기반관광정보조회 (areaBasedList2)", "areaBasedList2",
                  contentTypeId="15", areaCode="1", numOfRows="3", arrange="D")

# 4. 키워드검색
call_api("4. 키워드검색조회 (searchKeyword2)", "searchKeyword2",
         keyword="%EC%B6%95%EC%A0%9C", contentTypeId="15", numOfRows="3")

# 5. 위치기반 관광정보조회
call_api("5. 위치기반관광정보조회 (locationBasedList2)", "locationBasedList2",
         mapX="126.9219", mapY="37.5217", radius="5000", contentTypeId="15", numOfRows="3")

# 6. 동기화목록조회
call_api("6. 동기화목록조회 (areaBasedSyncList2)", "areaBasedSyncList2",
         contentTypeId="15", numOfRows="3", showflag="1")

# 7. 분류체계코드조회 (하위)
call_api("7. 분류체계코드조회 (categoryCode2 cat1=A02)", "categoryCode2", cat1="A02", numOfRows="10")

# ===== 상세 API (contentId 필요) =====
cid = None
ttl = ""
if resp3:
    items_raw = resp3.get("response",{}).get("body",{}).get("items",{})
    if isinstance(items_raw, dict):
        items = items_raw.get("item", [])
    else:
        items = []
    if isinstance(items, list) and len(items) > 0:
        cid = items[0].get("contentid")
        ttl = items[0].get("title", "")
    elif isinstance(items, dict):
        cid = items.get("contentid")
        ttl = items.get("title", "")

if cid:
    print("")
    print("*" * 70)
    print("  Detail APIs - contentId={} ({})".format(cid, ttl))
    print("*" * 70)

    # 8. 공통정보조회
    call_api("8. 공통정보조회 (detailCommon2)", "detailCommon2",
             contentId=cid, contentTypeId="15",
             defaultYN="Y", firstImageYN="Y", addrinfoYN="Y", mapinfoYN="Y", overviewYN="Y")

    # 9. 소개정보조회
    call_api("9. 소개정보조회 (detailIntro2)", "detailIntro2",
             contentId=cid, contentTypeId="15")

    # 10. 반복정보조회
    call_api("10. 반복정보조회 (detailInfo2)", "detailInfo2",
             contentId=cid, contentTypeId="15")

    # 11. 이미지정보조회
    call_api("11. 이미지정보조회 (detailImage2)", "detailImage2",
             contentId=cid, imageYN="Y", subImageYN="Y")

    # 12. 반려동물동반여행정보
    call_api("12. 반려동물동반여행정보 (detailPetTour2)", "detailPetTour2",
             contentId=cid, contentTypeId="15")

    # 13. 법정동코드조회 (서울 시군구)
    call_api("13. 법정동코드조회 (areaCode2 areaCode=1)", "areaCode2",
             areaCode="1", numOfRows="30")
else:
    print("")
    print(">> contentId not found, skipping detail API tests")

print("")
print("=" * 70)
print("  All 13 API tests completed!")
print("=" * 70)
