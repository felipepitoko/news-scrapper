<h1>News Scrapper</h1>

<h2>Description</h2>
<p>
An simple and neat scrapper mainly on python and selenium to get some news.

The objective of this project is to show an code example of rpaframework and robocorp solution.
</p>

<h2>How it works</h2>
<p>
The robot should access an news website and interact with it, getting the newest news given some possible filters.

Inputs:
</p>
<ul>
<li><b>search_phrase:</b> some text to search for. Ex.: "elections in the usa"</li>
<li><b>topic_sort_key:</b> a topic to filter the search results. Ex.: "Business"</li>
<li><b>months_to_search:</b> the count of months to get news of. Ex.: 1 for only this month, 2 to this and the last month, and so on.</li>
<li><b>order_by:</b> "newest", "oldest" or "relevance", wich is the default*.</li>
</ul>
<p>*I noticed that latimes webpage would lost the search context when "newest" order was selected is sort options. So, i decided to put an variable to trigger or not this behavior.</p>

<p>The robot should create on output directory an excel file with title and some details about each news of the search.
It will also save the news main picture, when present.

Expected outputs:</p>
<ul>
<li><b>news_list.xlsx</b></li>
<li><b>name_of_the_picture.png</b> (One for each news, when the news have an main picture.)</li>
</ul>

<p>Expected data on the excel file:</p>
<ul>
<li><b>title:</b> the title of the news.</li>
<li><b>link:</b> the weblink to the news.</li>
<li><b>description:</b> the brief description of the news content.</li>
<li><b>date:</b> the date the news was posted on the website.</li>
<li><b>image_link:</b> the link to news main picture.</li>
<li><b>image_name:</b> name of the main picture.</li>
<li><b>total_search_matches:</b> count of how many times the search text was found in both title and description.</li>
<li><b>money_mentioned:</b> True or False if money was mentioned even once, both on title and description.</li>
</ul>


