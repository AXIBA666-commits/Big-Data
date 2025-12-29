from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

# 创建 Edge 浏览器选项对象
options = Options()
# 在这里可以添加各种选项，例如：
# options.add_argument('--headless')  # 无界面模式

# 使用修改后的参数传递方式初始化 Edge 浏览器驱动
driver = webdriver.Edge(options=options)


def scrape_reviews(url, filename):
    """
    抓取指定 URL 的评论内容，并保存到指定文件中。
    Args:
        url (str): 要抓取的评论页面的 URL。
        filename (str): 要保存评论内容的文件名。
    """
    driver.get(url)

    with open(filename, 'w', encoding='utf-8') as file:
        def get_content(file):
            # 查找所有包含评价内容的元素
            try:
                pj_elements_content = driver.find_elements(By.CLASS_NAME, 'body-content')
                # 遍历每个元素，将文本内容写入文件
                for i in range(len(pj_elements_content)):
                    file.write(pj_elements_content[i].text + '\n')
            except Exception as e:
                print(f"获取评价内容失败: {e}")

        # 获取第一页的评论内容
        get_content(file)

        # 查找下一页按钮
        next_elements = driver.find_elements(By.XPATH, '//*[@class="next rv-maidian "]')
        print(next_elements)

        # 循环点击下一页，获取所有页的评论内容
        while next_elements:
            next_element = next_elements[0]
            try:
                time.sleep(1)  # 等待页面加载
                next_element.click()  # 点击下一页
                time.sleep(2)  # 等待页面加载完成
                get_content(file)  # 获取当前页的评论内容
                next_elements = driver.find_elements(By.XPATH, '//*[@class="next rv-maidian "]')  # 重新查找下一页按钮
            except Exception as e:
                print(f"点击下一页或获取评论失败: {e}")
                break


# 抓取中等评价
medium_reviews_url = 'https://review.suning.com/cluster_cmmdty_review/cluster-38249278-000000012389328846-0000000000-1-newest.htm?originalCmmdtyType=general&safp=d488778a.10004.loverRight.166'
scrape_reviews(medium_reviews_url, '评论.txt')

# 关闭浏览器
driver.quit()