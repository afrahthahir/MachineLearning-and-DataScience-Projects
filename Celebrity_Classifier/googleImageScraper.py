from icrawler.builtin import GoogleImageCrawler

google_crawler = GoogleImageCrawler(storage={'root_dir': 'MS_Dhoni 2'})
google_crawler.crawl(
    keyword='MS_Dhoni',
    max_num=300,
    min_size=(500,950),  # width x height
    file_idx_offset=0
)
# import sys
# print(sys.executable)
