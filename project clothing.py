import tkinter as tk
from tkinter import messagebox
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image, ImageTk

# Load the model once at the start
def load_model():
    try:
        model_id = "CompVis/stable-diffusion-v1-4"
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
        pipe.to("cuda" if torch.cuda.is_available() else "cpu")
        return pipe
    except Exception as e:
        messagebox.showerror("Model Loading Error", f"Error loading model: {e}")
        return None

# Generate the image based on the user input
def generate_image(prompt, pipe):
    try:
        image = pipe(prompt).images[0]
        return image
    except Exception as e:
        messagebox.showerror("Image Generation Error", f"Error generating image: {e}")
        return None

# Handle the generation and displaying of the image
def generate_and_display_image():
    user_input = description_text.get("1.0", "end-1c").strip()
    if not user_input:
        messagebox.showwarning("Input Error", "Please enter a description.")
        return

    # Display loading status
    status_label.config(text="Generating your design...")
    window.update_idletasks()

    # Generate the image
    image = generate_image(user_input, pipe)

    if image:
        # Resize image and display it
        img = image.resize((300, 300))
        img_tk = ImageTk.PhotoImage(img)

        canvas.create_image(150, 150, image=img_tk)
        canvas.image = img_tk  # Keep reference to image to prevent garbage collection
        status_label.config(text="Design generated successfully!")
    else:
        status_label.config(text="Failed to generate design.")

# Main window setup
window = tk.Tk()
window.title("CoutureAI: AI-Generated Fashion")
window.geometry("600x700")

# Title label
title_label = tk.Label(window, text="Describe your clothing idea and we'll generate an image.", font=("Arial", 14))
title_label.pack(pady=10)

# Description text box
description_text = tk.Text(window, height=5, width=50)
description_text.insert(tk.END, "A stylish red evening gown with floral patterns")
description_text.pack(pady=10)

# Generate button
generate_button = tk.Button(window, text="Generate Image", command=generate_and_display_image)
generate_button.pack(pady=10)

# Status label
status_label = tk.Label(window, text="", font=("Arial", 12))
status_label.pack(pady=10)

# Canvas for the image
canvas = tk.Canvas(window, width=300, height=300)
canvas.pack(pady=10)

# Load the model
pipe = load_model()

# Run the Tkinter event loop
window.mainloop()