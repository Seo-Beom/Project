$serviceKey = "322e530c75f9c8df08b2302da8e51cf93bc1d45b5f5c285e6ca8432a45727562"
$baseUrl = "https://apis.data.go.kr/B551011/KorService2"
$common = "serviceKey=" + $serviceKey + "&MobileOS=ETC&MobileApp=IEUM&_type=json"

function Test-Api {
    param([string]$Name, [string]$Url)
    Write-Host ""
    Write-Host "=== $Name ===" -ForegroundColor Yellow
    try {
        $resp = Invoke-RestMethod -Uri $Url -Method Get -TimeoutSec 15
        $json = $resp | ConvertTo-Json -Depth 5 -Compress
        if ($json.Length -gt 1500) {
            Write-Host $json.Substring(0, 1500)
            Write-Host "... (truncated)"
        } else {
            Write-Host $json
        }
        $rc = $resp.response.header.resultCode
        $rm = $resp.response.header.resultMsg
        $tc = $resp.response.body.totalCount
        Write-Host ">> Result: [$rc] $rm | totalCount: $tc" -ForegroundColor Cyan
        return $resp
    } catch {
        Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# 1. 지역코드조회
$url1 = $baseUrl + "/areaCode1?" + $common + "&numOfRows=20"
Test-Api -Name "1. 지역코드조회 (areaCode1)" -Url $url1

# 2. 서비스분류코드조회
$url2 = $baseUrl + "/categoryCode1?" + $common + "&numOfRows=10"
Test-Api -Name "2. 서비스분류코드조회 (categoryCode1)" -Url $url2

# 3. 지역기반 관광정보조회
$url3 = $baseUrl + "/areaBasedList1?" + $common + "&contentTypeId=15&areaCode=1&numOfRows=3&arrange=D"
$listResp = Test-Api -Name "3. 지역기반관광정보조회 (areaBasedList1)" -Url $url3

# 4. 키워드검색
$url4 = $baseUrl + "/searchKeyword1?" + $common + "&keyword=%EC%B6%95%EC%A0%9C&contentTypeId=15&numOfRows=3"
Test-Api -Name "4. 키워드검색조회 (searchKeyword1)" -Url $url4

# 5. 위치기반 관광정보조회
$url5 = $baseUrl + "/locationBasedList1?" + $common + "&mapX=126.9219&mapY=37.5217&radius=5000&contentTypeId=15&numOfRows=3"
Test-Api -Name "5. 위치기반관광정보조회 (locationBasedList1)" -Url $url5

# 6. 동기화목록조회
$url6 = $baseUrl + "/areaBasedSyncList1?" + $common + "&contentTypeId=15&numOfRows=3&showflag=1"
Test-Api -Name "6. 동기화목록조회 (areaBasedSyncList1)" -Url $url6

# 7. 분류체계코드조회 (cat1=A02)
$url7 = $baseUrl + "/categoryCode1?" + $common + "&cat1=A02&numOfRows=10"
Test-Api -Name "7. 분류체계코드조회 (categoryCode1 cat1=A02)" -Url $url7

# contentId 추출
$cid = $null
if ($listResp -and $listResp.response.body.items.item) {
    $items = $listResp.response.body.items.item
    if ($items -is [array]) { $cid = $items[0].contentid; $ttl = $items[0].title }
    else { $cid = $items.contentid; $ttl = $items.title }
}

if ($cid) {
    Write-Host ""
    Write-Host "=== contentId=$cid ($ttl) 사용 ===" -ForegroundColor Magenta

    # 8. 공통정보조회
    $url8 = $baseUrl + "/detailCommon1?" + $common + "&contentId=$cid&contentTypeId=15&defaultYN=Y&firstImageYN=Y&addrinfoYN=Y&mapinfoYN=Y&overviewYN=Y"
    Test-Api -Name "8. 공통정보조회 (detailCommon1)" -Url $url8

    # 9. 소개정보조회
    $url9 = $baseUrl + "/detailIntro1?" + $common + "&contentId=$cid&contentTypeId=15"
    Test-Api -Name "9. 소개정보조회 (detailIntro1)" -Url $url9

    # 10. 반복정보조회
    $url10 = $baseUrl + "/detailInfo1?" + $common + "&contentId=$cid&contentTypeId=15"
    Test-Api -Name "10. 반복정보조회 (detailInfo1)" -Url $url10

    # 11. 이미지정보조회
    $url11 = $baseUrl + "/detailImage1?" + $common + "&contentId=$cid&imageYN=Y&subImageYN=Y"
    Test-Api -Name "11. 이미지정보조회 (detailImage1)" -Url $url11

    # 12. 반려동물동반여행정보
    $url12 = $baseUrl + "/detailPetTour1?" + $common + "&contentId=$cid&contentTypeId=15"
    Test-Api -Name "12. 반려동물동반여행정보 (detailPetTour1)" -Url $url12

    # 13. 법정동코드조회
    $url13 = $baseUrl + "/areaCode1?" + $common + "&areaCode=1&numOfRows=5"
    Test-Api -Name "13. 법정동코드조회 (areaCode1 areaCode=1)" -Url $url13
} else {
    Write-Host "contentId를 가져올 수 없어 상세 API 테스트 건너뜀" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== 전체 테스트 완료 ===" -ForegroundColor Green
