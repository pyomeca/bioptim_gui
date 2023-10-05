class Variable {
  String name;
  int dimension;
  String boundsInterpolationType;
  Bounds bounds;
  String initialGuessInterpolationType;
  List<List<double>> initialGuess;

  Variable.fromJson(Map<String, dynamic> variableData)
      : name = variableData["name"],
        dimension = variableData["dimension"],
        boundsInterpolationType = variableData["bounds_interpolation_type"],
        bounds = Bounds.fromJson(variableData["bounds"]),
        initialGuessInterpolationType =
            variableData["initial_guess_interpolation_type"],
        initialGuess = (variableData["initial_guess"] as List<dynamic>)
            .map((dynamic list) {
          if (list is List<dynamic>) {
            return list.map((dynamic value) {
              if (value is double) {
                return value;
              } else {
                return 0.0;
              }
            }).toList();
          } else {
            return <double>[];
          }
        }).toList();
}

class Bounds {
  List<List<double>> minBounds;
  List<List<double>> maxBounds;

  Bounds.fromJson(Map<String, dynamic> boundsData)
      : minBounds =
            (boundsData["min_bounds"] as List<dynamic>).map((dynamic list) {
          if (list is List<dynamic>) {
            return list.map((dynamic value) {
              if (value is double) {
                return value;
              } else {
                return 0.0;
              }
            }).toList();
          } else {
            return <double>[];
          }
        }).toList(),
        maxBounds =
            (boundsData["max_bounds"] as List<dynamic>).map((dynamic list) {
          if (list is List<dynamic>) {
            return list.map((dynamic value) {
              if (value is double) {
                return value;
              } else {
                return 0.0;
              }
            }).toList();
          } else {
            return <double>[];
          }
        }).toList();
}
