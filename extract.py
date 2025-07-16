import io
import os
import sys
import mss
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image
from google.cloud import vision_v1
from dotenv import load_dotenv

# ─── dotenv loading ─────────────────────────────────────────────────────────
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError(f"Missing GOOGLE_API_KEY in {dotenv_path!r}")

client = vision_v1.ImageAnnotatorClient(
    credentials=None,
    client_options={"api_key": API_KEY}
)
# ────────────────────────────────────────────────────────────────────────────

def capture_screen() -> bytes:
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = sct.grab(monitor)
        pil = Image.frombytes("RGB", img.size, img.rgb)
        buf = io.BytesIO()
        pil.save(buf, format="PNG")
        return buf.getvalue()

def ocr_image(image_bytes: bytes) -> str:
    image = vision_v1.Image(content=image_bytes)
    resp  = client.text_detection(image=image)
    if resp.error.message:
        raise RuntimeError(resp.error.message)
    ann = resp.text_annotations
    return ann[0].description if ann else ""

def show_text_popup(text: str):
    root = tk.Tk()
    root.title("OCR Output")
    root.geometry("400x300")
    txt = ScrolledText(root, wrap=tk.WORD)
    txt.pack(fill=tk.BOTH, expand=True)
    txt.insert(tk.END, text or "No text detected.")
    txt.configure(state="disabled")
    root.mainloop()

if __name__ == "__main__":
    try:
        img = capture_screen()
        txt = ocr_image(img)
        show_text_popup(txt)
    except Exception as e:
        show_text_popup(f"Error:\n{e}")
