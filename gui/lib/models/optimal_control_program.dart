import 'dart:io';

import 'package:bioptim_gui/models/generic_ocp_config.dart';

import 'dart:convert';

import 'package:bioptim_gui/models/api_config.dart';
import 'package:http/http.dart' as http;

///
/// This class only handles the code generation for generic OCPs
class OptimalControlProgram {
  ///
  /// Constructor

  OptimalControlProgram();

  ///
  /// Setters and Getters

  bool _hasPendingChangesToBeExported = true;
  void notifyThatModelHasChanged() => _hasPendingChangesToBeExported = true;
  bool get mustExport => _hasPendingChangesToBeExported;

  GenericOptimalControlProgram generic = GenericOptimalControlProgram();

  Future<void> exportScript(String path) async {
    _hasPendingChangesToBeExported = false;

    final file = File(path);

    Future<String> getGeneratedContent() async {
      final url = Uri.parse('${APIConfig.url}/generic_ocp/generate_code');
      final response = await http.get(url);
      if (response.statusCode == 200) {
        return response.body;
      } else {
        throw Exception("Code generation failed API level");
      }
    }

    final generatedContent = json.decode(await getGeneratedContent());

    file.writeAsStringSync(generatedContent);
  }
}
