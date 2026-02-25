import streamlit as st
import asyncio
import sys
from playwright.async_api import async_playwright

st.title("🌐 브라우저 실행 해결사 (마지막 도전)")

url = st.text_input("접속 주소", value="https://www.google.com")

async def run_playwright(target_url):
    async with async_playwright() as p:
        st.write("1. 브라우저 엔진 실행 중...")
        # 윈도우 호환성을 위해 브라우저 실행 시 약간의 여유를 줍니다.
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        st.write(f"2. {target_url} 접속 중...")
        await page.goto(target_url, timeout=60000)
        
        title = await page.title()
        await browser.close()
        return title

if st.button("실행"):
    with st.status("작업 진행 중...") as status:
        try:
            # Windows에서 NotImplementedError 방지를 위한 정책 강제 설정
            if sys.platform == 'win32':
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            
            # 새 루프 생성 및 실행
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            
            try:
                result_title = new_loop.run_until_complete(run_playwright(url))
                st.success(f"✅ 성공! 페이지 제목: {result_title}")
            finally:
                new_loop.close()
                
        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")
            st.warning("여전히 안 된다면, 현재 터미널을 완전히 끄고 다시 실행해 보세요.")