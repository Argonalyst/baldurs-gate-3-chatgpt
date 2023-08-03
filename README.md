# Baldur's Gate 3 + Langchain + ChatGPT

## Description

This is a Python-based project that uses web scraping. The script currently targets the website 'https://baldursgate3.wiki.fextralife.com', but it can be easily modified to scrape content from other websites.

- Extract text content from a website and save it to a file.
- Use the jupyter notebook to generate embeddings and "chat" with the content.

## Dependencies

- Python 3.7 or later
- Requests
- BeautifulSoup
- transformers
- regex
- langchain
- pickle
- requests

## Functions

- `get_content_url()`: Extracts text content from the target website and saves it to a file named 'website_content.txt'.

- `clean_and_save_file_content(input_file_path, output_file_path)`: Reads a text file, removes newline characters and HTML tags, and saves the cleaned content to a new file.

- `estimate_cost(file_path, max_length=1024, cost_per_1k_tokens=0.0004)`: Estimates the cost of tokenizing and processing the text data from a file. The cost is based on the number of tokens and the specified cost per 1000 tokens.

- `estimate_time(file_path, max_length=1024, tokens_per_minute=1000000)`: Estimates the time it would take to process the text data from a file, based on the number of tokens and the specified processing speed in tokens per minute.

- `clean_parentheses_braces(file_path, output_file_path)`: Reads a text file, removes any text within parentheses and braces, and saves the cleaned content to a new file.

- `clean_special_chars(file_path, output_file_path)`: Reads a text file, removes special characters, and saves the cleaned content to a new file.

## Notes

Please note that web scraping should be done ethically and responsibly. Always respect the website's robots.txt file and terms of service.

This script was designed for educational purposes and is not intended for large-scale scraping operations.

