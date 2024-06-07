import google.generativeai as genai
import fitz
import re
from collections import defaultdict
from PIL import Image
import io
import PIL.Image
import os

			                                            # Setting up the API OF OUT PROGRAM

# THIS IS THE GOOGLE API CODE WHICH IS USED TO CONNECT TO THE GEMINI API.

genai.configure(api_key="AIzaSyBLp6FrsCS5P2l3-U-9hKJ-WWtLeY9cr10") 
model1 = genai.GenerativeModel('gemini-1.5-pro-latest')
model2 = genai.GenerativeModel('gemini-pro-vision')


# prints the number of models which we can use to get out information 
# Give the number of AI models that exists
print('\n')
print("These are the models we could use for our program")
print('\n')
for m in genai.list_models():
	if 'generateContent' in m.supported_generation_methods:
		print(m.name)
print('\n')




def explainPaper(file_path):
													# Methods which are crucial to our program

	# Function creates a Directory if a folder with the same name already exists

	def create_unique_folder(base_folder):
		folder = base_folder
		counter = 1
		while os.path.exists(folder):
			folder = f"{base_folder}{counter}"
			counter += 1
		os.makedirs(folder)
		return folder

	# Function which collects the images which are stored in a folder

	def collect_image_file_paths(folder):
		image_paths = []
		# print("\nList of saved image file paths:")
		for root, dirs, files in os.walk(folder):
			for file in files:
				if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
					image_path = os.path.join(root, file)
					image_paths.append(image_path)
					# print(image_path)
		return image_paths

	# Function to loop over the list of image file paths

	def loop_over_image_file_paths(file_paths):
		# print("\nProcessing image file paths:")
		image_description = ""
		i = 0;
		for image_path in file_paths:
			i += 1
			# print(f"{image_path}")
			image = PIL.Image.open(f"{image_path}")
			image
			image_response = model2.generate_content(["Write a short, description on what you see in the  the image ",
										image], stream=True)
			image_response.resolve()
			image_description += f"fig:" + str(i)
			image_description += f"{image_response.text}\n"
		# print(image_description)
		return image_description

	# Creates a Markdown file

	def create_markdown(text):

		base_name = "output"
		file_extension = ".md"
		counter = 1
		filename = f"{base_name}{counter}{file_extension}"

		while os.path.exists(filename):
			counter += 1
			filename = f"{base_name}{counter}{file_extension}"

		with open(filename, "w") as f:
			f.write(text)

		print(f"Markdown file created: {filename}\n")
	
													# Here starts the pdf loading program

	doc = fitz.open(file_path)
	text = ""
	for page in doc:
		text += page.get_text()

													# Extracting images from the PDF
	
	# Create a unique directory to store images
	base_folder = "extracted_images"
	images_folder = create_unique_folder(base_folder)

	for page_index in range(len(doc)):
		page = doc[page_index]
		image_list = page.get_images(full=True)
		
		# Print number of images found on the page
		if image_list:
			print(f"[+] Found a total of {len(image_list)} images on page {page_index}")
		else:
			print("[!] No images found on page", page_index)
		
		for image_index, img in enumerate(image_list, start=1):
			xref = img[0]
			base_image = doc.extract_image(xref)
			image_bytes = base_image["image"]
			image_ext = base_image["ext"]
			image = Image.open(io.BytesIO(image_bytes))


			# Save the image to the specified folder
			image_path = os.path.join(images_folder, f"image{page_index+1}_{image_index}.{image_ext}")
			image.save(image_path)
	
	# Adds the information about the imgages to the extracted pdf text
	text += loop_over_image_file_paths(collect_image_file_paths(images_folder))

			
	response = model1.generate_content(text + "This is a research paper along the images references are given. \
								  and Explain it in detail in three different parts , Introduction, Methodology  and conclusion.\
                                   The output must be of 3000 words" )
	response.resolve()
	# print(response.text)
	create_markdown(response.text)
        
	
	
fileName = input("Give me your file path to the PDF\n")
explainPaper(fileName)