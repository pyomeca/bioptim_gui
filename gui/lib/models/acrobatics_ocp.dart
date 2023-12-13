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

    Future<String> getGeneratedContent() async {
      final url = Uri.parse('${APIConfig.url}/acrobatics/generate_code');
      final body = json.encode({
        "model_path":
            "", // TODO useless for now but might be used in the future
        "save_path": path,
      });
      final response =
          await http.post(url, body: body, headers: APIConfig.headers);
      if (response.statusCode == 200) {
        return response.body;
      } else {
        throw Exception("Code generation failed API level");
      }
    }

    final responseData = json.decode(await getGeneratedContent());
    final generatedContent = responseData['generated_code'];

    final codeFile = File(path);
    codeFile.writeAsStringSync(generatedContent);

    for (final modelModelPath in responseData['new_models']) {
      final newModel = modelModelPath[0];
      final newModelPath = modelModelPath[1];
      final modelFile = File(newModelPath);
      modelFile.writeAsStringSync(newModel);
    }
  }
}
