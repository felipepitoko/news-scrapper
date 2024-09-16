# news-scrapper
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
</ul>

<p>The robot should create an excel file with the title and some details about each news of the search.
It will also save the news main picture, when present.

Expected outputs:</p>
<ul>
<li><b>title:</b> the tile of the news.</li>
<li><b>link:</b> the weblink to the news.</li>
<li><b>description:</b> the brief description of the news content.</li>
<li><b>date:</b> the date the news was posted on the website.</li>
<li><b>image_link:</b> the link to news main picture.</li>
<li><b>image_name:</b> name of the main picture.</li>
<li><b>total_search_matches:</b> count of how many times the search text was found in both title and description.</li>
<li><b>money_mentioned:</b> True or False if money was mentioned even once, both on title and description.</li>
</ul>

