import cv2
import pickle
import numpy as np
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3
from gtts import gTTS
import pygame
import time
import os
from Control import WSClient
from config import WS_IP

# Load models and mappings
with open(r'D:\Education\projects\Hand last version\Hand\Models\digits_model.p', 'rb') as f:
    model_data_numbers = pickle.load(f)
    model_numbers = model_data_numbers['model']
    labels_dict_numbers = model_data_numbers['labels_dict']

with open(r'D:\Education\projects\Hand last version\Hand\Models\english_model.p', 'rb') as f:
    model_data_alphabet = pickle.load(f)
    model_alphabet = model_data_alphabet['model']
    labels_dict_alphabet = model_data_alphabet['labels_dict']

with open(r'D:\Education\projects\Hand last version\Hand\Models\arabic_model.pkl', 'rb') as f:
    model_data_arabic = pickle.load(f)
    model_arabic = model_data_arabic['model']
    labels_dict_arabic = model_data_arabic['label_dict']

arabic_map = {
    "Alef": "أ", "Beh": "ب", "Teh": "ت", "Theh": "ث", "Jeem": "ج",
    "Hah": "ح", "Khah": "خ", "Dal": "د", "thal": "ذ", "Reh": "ر",
    "Zain": "ز", "Seen": "س", "Sheen": "ش", "Sad": "ص", "Dad": "ض",
    "Tah": "ط", "Zah": "ظ", "Ain": "ع", "Ghain": "غ", "Feh": "ف",
    "Qaf": "ق", "Kaf": "ك", "Lam": "ل", "Meem": "م", "Noon": "ن",
    "Laa": "لا", "Al": "ال", "Teh_Marbuta": "ة", "Heh": "ه",
    "Waw": "و", "Yeh": "ي", "space": " ", "del": "⌫", "nothing": ""
}

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

engine = pyttsx3.init()

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Gesture Recognition")
        self.root.attributes('-fullscreen', True)
        
        # Initialize components
        self.cap = cv2.VideoCapture(0)
        self.model_choice = "alphabets"
        self.esp = WSClient()
        self.sentence = ""
        self.last_prediction = ""
        self.repeat_count = 0

        # Background Image
        try:
            self.bg_image = Image.open(r"D:\System\wallpapers\wallpaperflare.com_wallpaper (3).jpg")
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")

        # Window Control Buttons (Top-Right)
        control_frame = tk.Frame(root, bg='#2C2F36')
        control_frame.place(relx=0.98, rely=0.02, anchor='ne')

        # Minimize Button
        tk.Button(control_frame, text="─", font=("Arial", 14, "bold"),
                fg="white", bg="#505050", command=root.iconify,
                width=2, height=1, relief="flat").pack(side=tk.LEFT, padx=2)

        # Maximize/Restore Button
        self.maximize_btn = tk.Button(control_frame, text="◻", font=("Arial", 14, "bold"),
                                    fg="white", bg="#505050", command=self.toggle_fullscreen,
                                    width=2, height=1, relief="flat")
        self.maximize_btn.pack(side=tk.LEFT, padx=2)

        # Close Button
        tk.Button(control_frame, text="✕", font=("Arial", 14, "bold"),
                fg="white", bg="#ff4444", command=self.on_close,
                width=2, height=1, relief="flat").pack(side=tk.LEFT, padx=2)

        # Video Feed
        self.video_frame = tk.Frame(root, bg="#2C2F36")
        self.video_frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        self.canvas = tk.Canvas(self.video_frame, width=800, height=600, 
                              bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_rectangle(5, 5, 795, 595, outline="#00FFFF", width=3)
        self.video_label = tk.Label(self.canvas, bg="#1e1e1e")
        self.video_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Model Selection Radio Buttons
        self.model_var = tk.StringVar(value="alphabets")
        self.radio_frame = tk.Frame(root, bg="#2C2F36")
        self.radio_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.radios = [
            ("English Alphabet", "alphabets"),
            ("Numbers", "numbers"),
            ("Arabic Letters", "arabic")
        ]

        for text, value in self.radios:
            rb = tk.Radiobutton(self.radio_frame, text=text, variable=self.model_var,
                    value=value, font=("Arial", 14, "bold"),
                    bg="#2C2F36", fg="white", selectcolor="#1E90FF",
                    activebackground="#1E90FF",indicatoron=0,width=12,padx=10,pady=5,
                    command=self.update_model)
            rb.pack(side=tk.LEFT, padx=20, ipadx=15, ipady=20)

        # Prediction Label
        self.prediction_label = tk.Label(root, text="Prediction: ", 
                                       font=("Arial", 18, "bold"), fg="#1E90FF", bg="#2C2F36")
        self.prediction_label.place(relx=0.5, rely=0.78, anchor=tk.CENTER)

        # Sentence Display
        self.sentence_label = tk.Label(root, text="", font=("Arial", 20, "bold"),
                                     fg="white", bg="#2C2F36", wraplength=1200)
        self.sentence_label.place(relx=0.5, rely=0.84, anchor=tk.CENTER)

        # Control Buttons
        self.button_frame = tk.Frame(root, bg="#2C2F36")
        self.button_frame.place(relx=0.5, rely=0.92, anchor=tk.CENTER)

        self.reset_btn = tk.Button(self.button_frame, text="🔁 Reset", font=("Arial", 14, "bold"),
                                fg="white", bg="#1E90FF", command=self.reset_sentence,
                                width=15, height=2)
        self.reset_btn.grid(row=0, column=0, padx=20, pady=5)

        self.speak_btn = tk.Button(self.button_frame, text="🗣️ Speak", font=("Arial", 14, "bold"),
                                fg="white", bg="#1E90FF", command=self.speak_sentence,
                                width=15, height=2)
        self.speak_btn.grid(row=0, column=1, padx=20, pady=5)

        # Key bindings
        self.root.bind("<Escape>", lambda event: self.on_close())
        self.root.bind("<space>", self.add_space)
        self.root.bind("<BackSpace>", self.delete_char)
        self.root.bind("<Return>", self.speak_sentence)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update_video()

    def toggle_fullscreen(self):
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
        self.maximize_btn.config(text="❒" if current_state else "◻")

    def on_close(self):
        """Clean up resources and close application"""
        self.cap.release()
        self.root.destroy()

    def update_model(self):
        self.model_choice = self.model_var.get()
        if self.model_choice == "arabic":
            self.reset_btn.config(text="🔁 إعادة تعيين")
            self.speak_btn.config(text="🗣️ نطق الجملة")
            self.prediction_label.config(text="الحرف المتوقع: ")
        else:
            self.reset_btn.config(text="🔁 Reset")
            self.speak_btn.config(text="🗣️ Speak")
            self.prediction_label.config(text="Prediction: ")

    def get_model_and_labels(self):
        if self.model_choice == "numbers":
            return model_numbers, labels_dict_numbers
        elif self.model_choice == "arabic":
            return model_arabic, labels_dict_arabic
        return model_alphabet, labels_dict_alphabet

    def add_space(self, event=None):
        self.sentence += " "
        # Handle Arabic display
        if self.model_choice == "arabic":
            self.prediction_label.config(text="التوقع: مسافة")
        else:
            self.prediction_label.config(text="Prediction: ␣ (space)")
        self.sentence_label.config(text=self.sentence)
        self.esp.send(" ")

    def delete_char(self, event=None):
        self.sentence = self.sentence[:-1]
        # Handle Arabic display
        if self.model_choice == "arabic":
            self.prediction_label.config(text="التوقع: حذف")
        else:
            self.prediction_label.config(text="Prediction: ⌫ (deleted)")
        self.sentence_label.config(text=self.sentence)
        self.esp.send("#")

    def reset_sentence(self):
        self.sentence = ""
        # Handle Arabic display
        if self.model_choice == "arabic":
            self.prediction_label.config(text="التوقع: ")
            self.reset_btn.config(text="🔁 إعادة تعيين")
            self.speak_btn.config(text="🗣️ نطق الجملة")
        else:
            self.prediction_label.config(text="Prediction: ")
            self.reset_btn.config(text="🔁 Reset")
            self.speak_btn.config(text="🗣️ Speak")
        self.sentence_label.config(text=self.sentence)
        self.esp.send("*")
        
        if self.model_choice == "arabic":
            self.play_gtts("تمت إعادة تعيين الجملة")
        else:
            engine.say("Sentence reset")
            engine.runAndWait()

    def speak_sentence(self, event=None):
        if self.sentence.strip():
            if self.model_choice == "arabic":
                self.play_gtts(self.sentence)
            else:
                engine.say(self.sentence)
                engine.runAndWait()

    def play_gtts(self, text):
        try:
            tts = gTTS(text=text, lang='ar')
            filename = "temp_arabic_audio.mp3"
            tts.save(filename)
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.music.unload()
            os.remove(filename)
        except Exception as e:
            print(f"Error in Arabic TTS: {e}")

    def update_video(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        predicted_label = ""
        model, labels_dict = self.get_model_and_labels()

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                features = []
                x_ = [lm.x for lm in hand_landmarks.landmark]
                y_ = [lm.y for lm in hand_landmarks.landmark]
                
                for lm in hand_landmarks.landmark:
                    features.extend([lm.x - min(x_), lm.y - min(y_)])

                if len(features) == 42:
                    prediction = model.predict([np.asarray(features)])
                    predicted_label = labels_dict[int(prediction[0])]
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if predicted_label == self.last_prediction:
            self.repeat_count += 1
        else:
            self.repeat_count = 0
        self.last_prediction = predicted_label

        if self.repeat_count == 15:
            if self.model_choice == "arabic":
                final_char = arabic_map.get(predicted_label, predicted_label)
                prediction_text = f"التوقع: {final_char}"
            else:
                final_char = predicted_label
                prediction_text = f"Prediction: {final_char}"

            if predicted_label in ["SPACE", "space"]:
                self.add_space()
            elif predicted_label in ["DEL", "del"]:
                self.delete_char()
            elif predicted_label not in ["nothing", "DEL", "SPACE", "Blank", "del", "space", "BLANK"]:
                self.sentence += final_char
                self.prediction_label.config(text=prediction_text)
                self.sentence_label.config(text=self.sentence)
                if(len(predicted_label)>0):
                    self.esp.send(predicted_label)

        # Update video feed
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img = img.resize((780, 580))
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        self.root.after(10, self.update_video)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()