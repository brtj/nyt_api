Example of use New York Times Article API based on 2 excercises.

1. Please create a program (implementation language is up to you) that based on New York Times Article API (https://developer.nytimes.com) does the following things:
	- pulls down all the articles published between Dec 18 and Dec 24 and sorts them by word count. The expected output is as follows:
	WORD_COUNT_1 https://www.nytimes.com/path/to/an/article/with/the/highest/wordcount
	WORD_COUNT_2 https://www.nytimes.com/path/to/an/article/with/the/highest/wordcount
	...

	- transforms JSON response to a YAML file as outlined below:
		
		articles:
			- headline: "ARTICLE_HEADLINE_1"
			  url: "https://www......
			  type: "ARTICLE_TYPE"
			- headline: "ARTICLE_HEADLINE_2"
			  url: "https://www......
			  type: "ARTICLE_TYPE"

2. Using article API mentioned above please create a script that produces CSV file with a number of articles published each day in December 2017. The goal is to import such files to Excel spreadsheet and present on a bar chart how number of articles fluctuated over the entire month. Expected CSV format:

2017-12-01;145
2017-12-02;248
....
