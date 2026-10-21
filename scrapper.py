import requests
from bs4 import BeautifulSoup

def search_incruit(keyword, pages=1):
    jobs = []
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }
    for i in range(pages): 
        page = i * 30
        url = f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}&startno={page}"
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        lis = soup.find_all("li", class_="c_col")
        print(f"{i + 1} 페이지 크롤링 중... (수집: {len(lis)}건)")
        
        for li in lis:
            try:
                company = li.find("a", class_="cpname").text.strip()
                title_a = li.find("div", class_="cell_mid").find("a")
                title = title_a.text.strip()
                link = title_a.get("href")

                # 조건 세부 파싱 (지역, 경력, 학력, 고용형태)
                spans = [s.get_text(strip=True) for s in li.select(".cl_md span")]
                location = spans[0] if len(spans) > 0 else "지역무관"
                experience = spans[1] if len(spans) > 1 else "경력무관"
                education = spans[2] if len(spans) > 2 else "학력무관"
                job_type = spans[3] if len(spans) > 3 else "정규직"

                # 마감일 파싱
                last_el = li.select_one(".cell_last")
                deadline = last_el.get_text(" ", strip=True) if last_el else "채용시 마감"

                # 직무 및 기술스택 태그
                tags_el = li.select(".cl_btm span")
                tags = [
                    t.get_text(strip=True).rstrip(',')
                    for t in tags_el
                    if t.get_text(strip=True) and not t.get_text(strip=True).startswith('~') and '등록' not in t.get_text() and '수정' not in t.get_text()
                ]

                job_data = {
                    "company": company,
                    "title": title,
                    "location": location,
                    "experience": experience,
                    "education": education,
                    "job_type": job_type,
                    "deadline": deadline,
                    "tags": tags,
                    "link": link
                }
                jobs.append(job_data)
            except Exception as e:
                pass

    return jobs
