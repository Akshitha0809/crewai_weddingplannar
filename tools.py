from crewai_tools import SerperDevTool,ScrapeWebsiteTool,PDFSearchTool,FileReadTool
search_tool = SerperDevTool()
file_search_tool = FileReadTool(file_path='format.txt')
scrapewebtool = ScrapeWebsiteTool(website_url=['https://www.wedmegood.com/',"https://weddingz.in/"])
file_search_tool2 = FileReadTool(file_path='perviousdata.txt')

#website_url=['https://www.wedmegood.com/',"https://weddingz.in/"]