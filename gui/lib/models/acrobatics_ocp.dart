import 'dart:convert';
import 'dart:io';

import 'package:bioptim_gui/models/api_config.dart';
import 'package:http/http.dart' as http;

///
/// This is only handle the code generation for the acrobatics ocp
class AcrobaticsOCPProgram {
  AcrobaticsOCPProgram();

  bool _hasPendingChangesToBeExported = true;
  void notifyThatModelHasChanged() => _hasPendingChangesToBeExported = true;
  bool get mustExport => _hasPendingChangesToBeExported;

  Future<void> exportScript(String path) async {
    _hasPendingChangesToBeExported = false;
    final file = File(path);

    Future<String> getGeneratedContent() async {
      final url = Uri.parse('${APIConfig.url}/acrobatics/generate_code');
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
