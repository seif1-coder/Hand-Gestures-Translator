# 🔌 IoT – Hand Gestures Translator  

This module connects the AI system with **hardware output** using **ESP8266**, **Arduino UNO**, and an **LCD display**. Recognized letters are sent from Python → ESP → Arduino → LCD.  

---

## ✨ Features  
- Display recognized letters in real time on an **LCD**  
- **ESP8266** receives predictions from AI system via WebSocket  
- **Arduino UNO** controls the LCD output  
- Special handling for **Arabic letters** (drawn bit by bit in code)  

---

## 🛠️ Components  
- Arduino UNO  
- ESP8266 Wi-Fi Module  
- LCD Display (I2C interface)  

---

## ⚙️ How to Run  
1. Flash ESP8266 + Arduino code using **Arduino IDE**.  
2. Connect the LCD via I2C.  
3. Run the AI script → results are sent automatically to LCD.  

**Special Commands:**  
- `*` → Reset  
- `#` → Delete  
- `" "` → Space  

---

