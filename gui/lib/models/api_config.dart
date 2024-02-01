///
/// A class that stores the API configuration for HTTP calls in the application.
/// This includes the common request headers and API URL.
class APIConfig {
  static String url = "http://localhost:8000";
  static Map<String, String> headers = {'Content-Type': 'application/json'};
}
