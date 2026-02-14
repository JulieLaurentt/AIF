import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
import io

def load_and_predict():
    # Open file dialog to select image
    file_path = filedialog.askopenfilename()

    # Check if a file was selected
    if not file_path:
        return

    # Load and display the image
    img = Image.open(file_path)
    img = img.resize((300, 300))  # resize for display
    img_tk = ImageTk.PhotoImage(img)
    label_image.config(image=img_tk)
    label_image.image = img_tk

    # Convert image to bytes
    img_binary = io.BytesIO()
    img.save(img_binary, format="PNG")

    # Send request to the API
    try:
        response = requests.post("http://127.0.0.1:5075/predict", data=img_binary.getvalue())
        
        if response.status_code == 200:
            predicted_label = response.json()["prediction"]
            # Mise à jour avec couleur et police visible
            label_text.config(
                text=f"Predicted Label: {predicted_label}", 
                fg="red", 
                font=("Arial", 16, "bold")
            )
            # Force le rafraîchissement de l'interface
            label_text.update_idletasks()
        else:
            label_text.config(text=f"Erreur API: {response.status_code}", fg="orange")
            
    except Exception as e:
        label_text.config(text="Erreur de connexion", fg="orange")
        print(f"Erreur : {e}")

# Set up main GUI window
root = tk.Tk()
root.title("Image Classifier")

# Button to load image and predict
btn_load = tk.Button(root, text="Load Image", command=load_and_predict)
btn_load.pack(pady=20)

# Label to display the image
label_image = tk.Label(root)
label_image.pack(pady=20)

# Initial label text as empty (it will be updated after predicting)
label_text = tk.Label(root, text="")
label_text.pack(pady=20)

root.mainloop()
