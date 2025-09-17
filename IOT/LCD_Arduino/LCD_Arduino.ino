//lcd code 8 letters only

#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
LiquidCrystal_I2C lcd1(0x27, 16, 2);
LiquidCrystal_I2C lcd2(0x27, 16, 2);
LiquidCrystal_I2C lcd3(0x27, 16, 2);


byte alef[8]  = {  B00100, B00100, B00100, B00100, B00100, B00100, B00100, B00000 };
byte baa[8]   = { B00001, B00001, B00001, B00001, B11111, B00000, B00100, B00000 };
byte taa[8]   = { B00000, B01010, B00000, B00001, B00001, B00001, B11111, B00000 };
byte theh[8]  = {  B00100, B01010, B00000, B00001, B00001, B00001, B11111, B00000 };
byte jeem[8]  = { B00000, B01100, B00010, B11111, B00000, B00100, B00000, B00000 };
byte hah[8]   = { B00000, B01100, B00010, B11111, B00000, B00000, B00000, B00000 };
byte khah[8]  = { B00100, B00000, B01100, B00010, B11111, B00000, B00000, B00000  };
byte dal[8]   = { B00000, B00000, B00100, B00010, B01110, B00000, B00000, B00000 };

String displayText = ""; 

void setup() {
lcd.init();
lcd.backlight();
Serial.begin(115200);

lcd.createChar(0, alef);
lcd.createChar(1, baa);
lcd.createChar(2, taa);
lcd.createChar(3, theh);
lcd.createChar(4, jeem);
lcd.createChar(5, hah);
lcd.createChar(6, khah);
lcd.createChar(7, dal);

}

void loop() {
if (Serial.available()) {
  String letter = Serial.readStringUntil('\n');
  letter.trim();

  if (letter == "*") {
    displayText = "";

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Reset");
    delay(1000);
  } else if (letter == "#") {
    if (displayText.length() > 0) {
      displayText.remove(displayText.length() - 1); 
    }
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Last letter");
    lcd.setCursor(0, 1);
    lcd.print("is deleted");
    delay(1000);
  }
  else if (letter == "Alef") {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.write(0);
    delay(3000); 
    lcd.clear();
  } else if (letter == "Beh") {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.write(1); 
    delay(3000); 
    lcd.clear();
    } else if (letter == "Teh") {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.write(2); 
      delay(3000);
      lcd.clear();
    } else if (letter == "Theh") {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.write(3); 
      delay(3000); 
      lcd.clear();
    } else if (letter == "Jeem") {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.write(4); 
      delay(3000); 
      lcd.clear();
    }else if (letter == "Hah") {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.write(5); 
      delay(3000); 
      lcd.clear();
  }else if (letter == "Khah") {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.write(6);
      delay(3000); 
      lcd.clear();
  }else if (letter == "Dal") {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.write(7); 
      delay(3000); 
      lcd.clear();
  }else if (letter == "call") {
          displayText += letter;

  }else if (letter == "dislike") {
          displayText += letter;

  }else if (letter == "fist") {
            displayText += letter;

  }else if (letter == "mute") {
            displayText += letter;

  }else if (letter == "like") {
            displayText += letter;

  }else if (letter == "four") {
        displayText += letter;

  }else if (letter == "palm") {
          displayText += letter;

  }
  else if (letter == "ok") {
          displayText += letter;

  }
  else if (letter == "one") {
          displayText += letter;

  }else if (letter == "peace_inverted") {
          displayText += letter;

  }
  else if (letter == "peace") {
            displayText += letter;

  }else if (letter == "stop") {
          displayText += letter;

  }else if (letter == "rock") {
          displayText += letter;

  }else if (letter == "three") {
        displayText += letter;

  }else if (letter == "stop_inverted") {
          displayText += letter;

  }else if (letter == "two_up_inverted") {
        displayText += letter;

  }else if (letter == "two_up") {
    displayText += letter;

  }else if (letter == "three2") {
    displayText += letter;

  }else {
    if (isAscii(letter[0])) {
    displayText += letter;
  }
}

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(displayText.substring(0, 16));
  if (displayText.length() > 16) {
    lcd.setCursor(0, 1);
    lcd.print(displayText.substring(16, 32));
  }
}
}