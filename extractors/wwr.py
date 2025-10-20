from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
from models.job import Job

def get_jobs(keyword):
  all_jobs = []
  content = get_content(keyword)
  soup = BeautifulSoup(content, "html.parser")

  jobs = soup.find_all("div", class_="JobCard_container__zQcZs JobCard_container--variant-card___dlv1")

  for job in jobs:
    link = f"https://www.wanted.co.kr{job.find('a')['href']}"
    #https://www.wanted.co.kr/wd/315996

    title_element = job.find("strong", class_="JobCard_title___kfvj")
    title = title_element.text if title_element else "N/A"

    company_element = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__company__ByVLu")
    company = company_element.text if company_element else "N/A"

    experience_element = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__location__4_w0l")
    experience = experience_element.text if experience_element else "N/A"

    reward_element = job.find("span", class_="JobCard_reward__oCSIQ")
    reward = reward_element.text if reward_element else "N/A"
    
    job = Job(link, title, company, experience, reward)
    all_jobs.append(job)
  return all_jobs

#content 가져오기
def get_content(keyword):
  p = sync_playwright().start()

  browser = p.chromium.launch(headless=False)

  page = browser.new_page()

  #page.goto("https://www.wanted.co.kr")
  url = f"https://www.wanted.co.kr/search?query={keyword}&tab=position"
  page.goto(url)

  scroll_to_bottom(page)

  content = page.content()

  p.stop()
  return content

#scroll_to_bottom 
def scroll_to_bottom(page, delay=1, max_tries=30):
    last_height = 0

    for i in range(max_tries):
        # End 키를 눌러 스크롤 내리기
        page.keyboard.press("End")
        time.sleep(delay)

        # 현재 문서 높이 가져오기
        new_height = page.evaluate("document.body.scrollHeight")

        # 더 이상 스크롤이 안 내려갈 때 종료
        if new_height == last_height:
            print(f"스크롤 완료 (총 {i+1}회 시도)")
            break
        last_height = new_height

    else:
        print("최대 시도 횟수 도달 (페이지가 너무 길거나 무한스크롤일 수 있음)")