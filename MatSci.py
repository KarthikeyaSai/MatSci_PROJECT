import google.generativeai as genai
import PyPDF2

GOOGLE_API_KEY='AIzaSyBLp6FrsCS5P2l3-U-9hKJ-WWtLeY9cr10'
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

# Open the PDF file in binary mode
pdf_file = open('OOPS Voting System.pdf', 'rb')

# Create a PDF reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Get the number of pages in the PDF
num_pages = len(pdf_reader.pages)
print(f"Number of pages: {num_pages}")

# Extract text from the first page
page = pdf_reader.pages[0]
text = page.extract_text()
print(text)

response = model.generate_content(text + " " + 
                                  "this is text from a pdf about Online voting system in java. Help us understand it and give extra information about it too")
print("  " + response.text + "   ")

# Close the PDF file
pdf_file.close()