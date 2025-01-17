#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

// WiFi credentials
const char* ssid = "HEXABYTE_C3B0FC";
const char* password = "MELIANE123";
int led[]={D0,D1,D2,D3,D4};
// Create a web server object on port 80
ESP8266WebServer server(80);

// Handle root URL ("/")
void handleRoot() {
  server.send(200, "text/plain", "Hello, this is NodeMCU responding!");
}

// Handle a custom URL (e.g., "/status")
void handleStatus() {
  String response = "{";
  response += "\"status\": \"ok\", ";
  response += "\"uptime\": " + String(millis() / 1000) + " seconds";
  response += "}";

  server.send(200, "application/json", response);
}
void turnLedsOnOff() {
  String response = "{";
  bool hasArgs = false; // To check if any valid arguments were received
  
  // Process parameters for each LED
  for (int i = 0; i < 5; i++) {
    String argName = "led" + String(i);
    if (server.hasArg(argName)) {
      hasArgs = true;

      String state = server.arg(argName);
      
      // Turn LED on or off based on the parameter value
      if (state == "on") {
        digitalWrite(led[i], HIGH);
        response += "\"" + argName + "\": \"on\", ";
      } else if (state == "off") {
        digitalWrite(led[i], LOW);
        response += "\"" + argName + "\": \"off\", ";
      } else {
        response += "\"" + argName + "\": \"invalid\", ";
      }
    }
  }

  // Remove the trailing comma and space from the response if arguments were valid
  if (hasArgs) {
    response.remove(response.length() - 2);
  } else {
    response += "\"error\": \"No valid parameters received\"";
  }

  response += "}";
  Serial.println(response);
  // Send the response back to the client
  server.send(200, "application/json", response);
}

// Handle 404 (not found)
void handleNotFound() {
  String message = "404 Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";

  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }

  server.send(404, "text/plain", message);
}

void setup() {
  // Start Serial for debugging
  Serial.begin(115200);
  delay(10);
for (int i=0;i<5;i++){pinMode(led[i],OUTPUT);}
  // Connect to WiFi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Define routes
  server.on("/", handleRoot);
  server.on("/status", handleStatus);
  server.on("/led",turnLedsOnOff);
  server.onNotFound(handleNotFound);

  // Start the server
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  // Handle client requests
  server.handleClient();
}
