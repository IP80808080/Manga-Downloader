import os
import io
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from fpdf import FPDF

from PIL import Image
from PyPDF2 import PdfMerger

# URL of the homepage
url = 'https://manga18.me/manga/this-worlds-breastfeeding-cafe'

# Send a request to the website
response = requests.get(url)

# Parse HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all <a> tags with class "chapter-link"
chapter_links = soup.find_all('a', class_='chapter-link')

# Extract the URLs from the <a> tags
chapter_urls = [link['href'] for link in chapter_links]

# Print the chapter URLs
print(chapter_urls)

url = "https://manga18.me/manga/this-worlds-breastfeeding-cafe"
res = requests.get(url)
soup = BeautifulSoup(res.content, "html.parser")

# find all the chapter URLs
chapter_urls = []
for a in soup.select("#chapter-list li a"):
    chapter_urls.append(urljoin(url, a["href"]))

# loop through each chapter URL
for i, chapter_url in enumerate(chapter_urls):
    # create a new directory for each chapter
    dir_path = f"chapter_{i + 1}"
    os.makedirs(dir_path, exist_ok=True)

    # get the html content of the chapter
    res = requests.get(chapter_url)
    soup = BeautifulSoup(res.content, "html.parser")

    # find all the image URLs in the chapter
    img_urls = []
    for img in soup.select(".reading-content img"):
        img_urls.append(urljoin(chapter_url, img["src"]))

    # loop through each image URL and download the image as a pdf
    for j, img_url in enumerate(img_urls):
        file_name = f"{j + 1}.pdf"
        file_path = os.path.join(dir_path, file_name)

        # download the image using requests
        res = requests.get(img_url)

        # save the image as a pdf using the fpdf library
        pdf = FPDF()
        pdf.add_page()
        pdf.image(io.BytesIO(res.content), 0, 0)
        pdf.output(file_path, "F")

image_files = [f for f in os.listdir('.') if f.endswith('.jpg')]

# sort the list of image file names by filename to ensure proper ordering
image_files.sort()

# create a PDF file for each chapter
chapters = [['chapter1', 10], ['chapter2', 15], ['chapter3', 20]]
for chapter in chapters:
    pdf_filename = chapter[0] + '.pdf'
    pdf_merger = PdfMerger()
    page_count = 0

    # add each image in the chapter to the PDF merger
    for i in range(chapter[1]):
        image_filename = chapter[0] + '_' + str(i + 1) + '.jpg'

        # open the image and get its dimensions
        image = Image.open(image_filename)
        width, height = image.size

        # if the image would get split on a random page, skip it
        if page_count % 2 == 1 and height > width:
            continue

        # add the image to the PDF merger
        pdf_merger.append(image_filename)
        page_count += 1

    # save the PDF file
    with open(pdf_filename, 'wb') as f:
        pdf_merger.write(f)


def check_image_quality(image_url):
    response = requests.get(image_url)
    img = Image.open(io.BytesIO(response.content))

    # Check if image resolution is greater than 72dpi
    if img.info['dpi'][0] < 72 or img.info['dpi'][1] < 72:
        return False

    # Check if image quality is greater than or equal to 95%
    if 'quality' in img.info:
        if img.info['quality'] < 95:
            return False

    return True


url = "https://manga18.me/manga/this-worlds-breastfeeding-cafe"

# Request the webpage and parse it using BeautifulSoup
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all the chapter links on the page
chapter_links = soup.find_all("a", class_="chapter-link")

# Define an empty list to store all the image URLs
image_urls = []

# Loop through each chapter link and extract the image URLs
for chapter_link in chapter_links:
    chapter_url = chapter_link["href"]
    chapter_response = requests.get(chapter_url)
    chapter_soup = BeautifulSoup(chapter_response.content, "html.parser")
    chapter_image_links = chapter_soup.find_all("img", class_="chapter-img")
    for chapter_image_link in chapter_image_links:
        image_urls.append(chapter_image_link["src"])

# Create a new PDF object and set the page size and orientation
pdf = FPDF(orientation="P", unit="mm", format="A4")


# Define a function to download and add an image to the PDF
def add_image_to_pdf(img_url):
    try:
        image_response = requests.get(img_url)
        with open("temp.jpg", "wb") as f:
            f.write(image_response.content)
        pdf.add_page()
        pdf.image("temp.jpg", x=10, y=10, w=190, h=277)
    except:
        pass  # Ignore any errors while downloading or adding the image to the PDF


# Loop through each image URL and add it to the PDF
for image_url in image_urls:
    add_image_to_pdf(image_url)

# Save the PDF file
pdf.output("this-worlds-breastfeeding-cafe.pdf", "F")
