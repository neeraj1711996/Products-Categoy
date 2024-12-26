import os
import google.generativeai as genai
import tkinter as tk
from tkinter import filedialog, Text


genai.configure(api_key="API")


def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file


def process_input():
    image_path = filedialog.askopenfilename(title="Select an Image")
    text_input = text_box.get("1.0", tk.END).strip()

    if image_path and text_input:
       
        file = upload_to_gemini(image_path)
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
        )

        prompt = """
Act as Auction House, The Auction House categories the items based on the title, description and image provided as input and as output provides the category , subcategory and attributes.
The item can be placed in either one or more category  and either one or more subcategories (in the parentheses) if applicable. For the output, please return one more category( if applicable) and the subcategories. Also, for every item, give me the attributes for the item from the list of attributes matching the category selected for the item. Each category has pre-set of sub categories and attributes which are defined. 

The Generated output response should contain following data :- 
Category : Return one or more category 
Subcategory : Return the List of Subcategory associated with the Category . Return one or more subcategory( If applicable)  
Attributes : Return the List of attributes matching the category selected for the Item.

        
"""

        response = model.generate_content([
            prompt,
            text_input,
            file,
            "output: "
        ])
        
        # Output the API response
        response_box.config(state=tk.NORMAL)
        response_box.delete("1.0", tk.END)
        response_box.insert(tk.END, response.text)
        response_box.config(state=tk.DISABLED)

# Set up Tkinter UI
root = tk.Tk()
root.title("Gemini API - Categories & Attributes")

# Create a Text input box for text
text_label = tk.Label(root, text="Enter Text:")
text_label.pack()
text_box = tk.Text(root, height=5, width=50)
text_box.pack()

# Create a button to trigger image selection and processing
submit_button = tk.Button(root, text="Submit Image and Process", command=process_input)
submit_button.pack()

# Create a Text box to display the response
response_label = tk.Label(root, text="API Response:")
response_label.pack()
response_box = tk.Text(root, height=15, width=50)
response_box.pack()
response_box.config(state=tk.DISABLED)

# Run the Tkinter loop
root.mainloop()