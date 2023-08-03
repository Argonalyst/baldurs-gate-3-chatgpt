# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from transformers import GPT2TokenizerFast

def get_content_url():
    
    # Set up the target URL and the headers
    url = "https://baldursgate3.wiki.fextralife.com"  # Replace with your target URL
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Set up a session
    with requests.Session() as s:
        s.headers.update(headers)
    
        visited_urls = set()  # Track visited URLs to avoid duplicates

        # Make a GET request to the website
        r = s.get(url)
        
        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(r.content, "html.parser")
        
        # Find all links on the webpage
        links = soup.find_all('a')
        
        # Initialize an empty string to store the text
        text_content = ""
        
        # Iterate over the links
        for link in links:
            # Get the href attribute from the link
            href = link.get('href')
        
            # Check if the URL is relative
            if href and href.startswith('/'):
                # Convert the relative URL to an absolute URL
                href = urljoin(url, href)
                
            # Skip external links and already visited links
            if not href.startswith(url) or href in visited_urls:
                continue
            
            visited_urls.add(href)
        
            # Make a GET request to the linked page
            try:
                r = s.get(href)
                page_soup = BeautifulSoup(r.content, "html.parser")
        
                # Extract the main content from the specific tags
                paragraphs = page_soup.find_all('p')
                headers = page_soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                list_items = page_soup.find_all('li')
    
                for tag in paragraphs + headers + list_items:
                    text_content += tag.get_text() + '\n'
            except Exception as e:
                print(f"Could not load page {href}: {e}")
                continue
        
        # Write the text content to a .txt file
        with open("website_content.txt", "w", encoding='utf-8') as f:
            f.write(text_content)

def clean_and_save_file_content(input_file_path: str, output_file_path: str) -> str:
    """
    Function to clean the content of a file and save it to a new file.
    It removes newline characters and code tags.

    Args:
    input_file_path (str): The path to the input file.
    output_file_path (str): The path to the output file.

    Returns:
    str: Status message indicating whether the function executed successfully.
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Remove newline characters
        content_no_newline = content.replace('\n', ' ')
        
        # Remove code within tags
        content_no_tags = re.sub('<.*?>', '', content_no_newline)

        # Write the cleaned content to a new file
        with open(output_file_path, "w", encoding='utf-8') as f:
            f.write(content_no_tags)

        return "File cleaned and saved successfully."
    except FileNotFoundError:
        return "The input file was not found."

def estimate_cost(file_path: str, max_length: int = 1024, cost_per_1k_tokens: float = 0.0004) -> float: # Ada model costs 0.0004 cents / 1k tokens
    """
    Function to estimate the cost of tokenizing and embedding the text from a file.

    Args:
    file_path (str): The path to the file.
    max_length (int): The maximum length of a chunk of text.
    cost_per_1k_tokens (float): The cost per 1000 tokens.

    Returns:
    float: The estimated cost.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

        # Split the text into chunks of max_length
        chunks = [text[i: i + max_length] for i in range(0, len(text), max_length)]

        num_tokens = sum(len(tokenizer.encode(chunk)) for chunk in chunks)
        
        # Calculate the cost
        cost = (num_tokens / 1000) * cost_per_1k_tokens

        print('Cost: '+str(cost))
        return cost
    except FileNotFoundError:
        return "The file was not found."


def estimate_time(file_path: str, max_length: int = 1024, tokens_per_minute: int = 1000000) -> float:
    """
    Function to estimate the time to process the text from a file.

    Args:
    file_path (str): The path to the file.
    max_length (int): The maximum length of a chunk of text.
    tokens_per_minute (int): The number of tokens that can be processed per minute.

    Returns:
    float: The estimated time in minutes.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

        # Split the text into chunks of max_length
        chunks = [text[i: i + max_length] for i in range(0, len(text), max_length)]

        num_tokens = sum(len(tokenizer.encode(chunk)) for chunk in chunks)
        
        # Calculate the time
        time = num_tokens / tokens_per_minute
        print('Time: '+str(time))

        return time
    except FileNotFoundError:
        return "The file was not found."
    
def clean_parentheses_braces(file_path: str, output_file_path: str) -> str:
    """
    Function to clean the content of a file by removing text within parentheses and braces.
    It saves the cleaned content to a new file.

    Args:
    file_path (str): The path to the input file.
    output_file_path (str): The path to the output file.

    Returns:
    str: Status message indicating whether the function executed successfully.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Remove text within parentheses and braces
        content_cleaned = re.sub(r'\(.*?\)|\{.*?\}', '', content)

        # Write the cleaned content to a new file
        with open(output_file_path, "w", encoding='utf-8') as f:
            f.write(content_cleaned)

        return "File cleaned and saved successfully."
    except FileNotFoundError:
        return "The input file was not found."

def clean_special_chars(file_path: str, output_file_path: str) -> str:
    """
    Function to clean the content of a file by removing special characters and unwanted strings.
    It saves the cleaned content to a new file.

    Args:
    file_path (str): The path to the input file.
    output_file_path (str): The path to the output file.

    Returns:
    str: Status message indicating whether the function executed successfully.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Remove special characters
        content_cleaned = re.sub(r'[\W_]+', ' ', content)

        # Write the cleaned content to a new file
        with open(output_file_path, "w", encoding='utf-8') as f:
            f.write(content_cleaned)

        return "File cleaned and saved successfully."
    except FileNotFoundError:
        return "The input file was not found."

def main():
    
    get_content_url()    
    clean_and_save_file_content("website_content.txt", "website_content_parsed.txt")    
    clean_special_chars("website_content_parsed.txt", "website_content_parsed.txt")    
    estimate_cost("website_content_parsed.txt")    
    estimate_time("website_content_parsed.txt")

if __name__ == '__main__':
    main()