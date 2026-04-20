#include <ESP8266WiFi.h>
#include <WiFiClient.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* thingspeak_api = "YOUR_THINGSPEAK_API";
const char* server = "api.thingspeak.com";

int light_pin = D1;
int sensor_pin = D0;
int vehicle_count = 0;

WiFiClient client;

void setup() {
  Serial.begin(115200);
  pinMode(light_pin, OUTPUT);
  pinMode(sensor_pin, INPUT);
  
  WiFi.begin(ssid, password);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  Serial.println(WiFi.status() == WL_CONNECTED ? "\nWiFi Connected" : "\nWiFi Failed");
}

void send_to_thingspeak(int count, int status) {
  if (client.connect(server, 80)) {
    String url = "/update?api_key=" + String(thingspeak_api) 
                 + "&field1=" + String(count) 
                 + "&field2=" + String(status);
    
    client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                 "Host: " + server + "\r\n" +
                 "Connection: close\r\n\r\n");
    
    while (client.connected()) {
      if (client.available()) {
        String line = client.readStringUntil('\n');
        Serial.println(line);
      }
    }
    client.stop();
  }
}

void control_lights(int count) {
  if (count > 0) {
    digitalWrite(light_pin, HIGH);
    Serial.println("Lights ON");
  } else {
    digitalWrite(light_pin, LOW);
    Serial.println("Lights OFF");
  }
}

void loop() {
  if (Serial.available()) {
    vehicle_count = Serial.parseInt();
    Serial.println("Received: " + String(vehicle_count));
  }
  
  control_lights(vehicle_count);
  send_to_thingspeak(vehicle_count, digitalRead(light_pin));
  
  delay(15000);
}
