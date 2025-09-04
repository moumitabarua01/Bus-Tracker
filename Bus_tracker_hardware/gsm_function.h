#include <WiFi.h>
#include <HTTPClient.h>
#include <TinyGPS++.h>

const char* ssid = "Redmi 10C";
const char* password = "naeem1234";
// const char* serverUrl = "http://192.168.210.161/tracker/api/location/";
const char* serverUrl = "http://192.168.191.161:8000/tracker/api/location/";


#define RXPin 16  
#define TXPin 17  
HardwareSerial gpsSerial(1);  
TinyGPSPlus gps;

void setup() {
  Serial.begin(115200);
  gpsSerial.begin(9600, SERIAL_8N1, RXPin, TXPin);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
}

void loop() {
  // Read GPS data
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }

  // If GPS location is valid, send it
  if (gps.location.isValid()) {
    float lat = gps.location.lat();
    float lng = gps.location.lng();

    // Only send data if lat and lng are valid and not zero
    if (lat != 0.0 && lng != 0.0) {
      String jsonData = "{\"lat\": " + String(lat, 6) + ", \"lng\": " + String(lng, 6) + "}";
      Serial.println("Sending JSON: " + jsonData);

      // Check WiFi connection status before sending data
      if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi disconnected! Reconnecting...");
        WiFi.begin(ssid, password);
        int attempts = 0;
        while (WiFi.status() != WL_CONNECTED && attempts < 10) {
          delay(1000);
          Serial.print(".");
          attempts++;
        }
        if (WiFi.status() == WL_CONNECTED) {
          Serial.println("\nReconnected to WiFi!");
        } else {
          Serial.println("\nFailed to reconnect.");
          return; // Don't proceed if WiFi is still disconnected
        }
      }

      // Send POST request to server
      HTTPClient http;
      http.begin(serverUrl);
      http.addHeader("Content-Type", "application/json");

      int httpResponseCode = http.POST(jsonData);

      // Log the HTTP response code and server response
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.println("Server Response: " + response);
      } else {
        Serial.println("Error sending data");
        Serial.print("HTTP Error: ");
        Serial.println(httpResponseCode);
      }
      http.end();
    } else {
      Serial.println("Invalid GPS location data. Skipping this update.");
    }
  } else {
    Serial.println("GPS data not available yet. Waiting for valid data...");
  }

  delay(5000); // Delay before sending the next update
}
