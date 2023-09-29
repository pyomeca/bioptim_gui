import 'dart:io';

import 'package:bioptim_gui/models/acrobatics_ocp_controllers.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

class AcrobaticBioModelChooser extends StatelessWidget {
  const AcrobaticBioModelChooser({
    super.key,
    this.width,
  });

  final double? width;

  @override
  Widget build(BuildContext context) {
    final controllers = AcrobaticsOCPControllers.instance;

    final bioModel = controllers.getBioModel();
    final modelPath = controllers.getModelPath();

    return SizedBox(
      width: width,
      child: TextField(
        decoration: InputDecoration(
          labelText: "Model path *",
          enabledBorder: const OutlineInputBorder(
            borderSide: BorderSide(color: Colors.red), // Unfocused border color
          ),
          focusedBorder: const OutlineInputBorder(
            borderSide: BorderSide(color: Colors.red), // Focused border color
          ),
          suffixIcon: IconButton(
            icon: const Icon(Icons.file_upload_outlined),
            onPressed: () async {
              final results = await FilePicker.platform.pickFiles(
                type: FileType.custom,
                allowedExtensions: [bioModel.extension],
              );
              if (results == null) return;
              controllers.setModelPath(results.files.single.path!);
            },
          ),
        ),
        autofocus: true,
        controller: TextEditingController(
          text: modelPath.isEmpty
              ? 'Select the model file'
              : File(modelPath).uri.pathSegments.last,
        ),
        readOnly: true,
        style: const TextStyle(
          color: Colors.black,
        ),
      ),
    );
  }
}
