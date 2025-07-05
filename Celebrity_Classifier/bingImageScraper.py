from icrawler.builtin import BingImageCrawler

crawler = BingImageCrawler(storage={'root_dir': 'MS_Dhoni 2'})
crawler.crawl(keyword='MS_Dhoni', max_num=300, min_size=(500,650))
