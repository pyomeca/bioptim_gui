import 'dart:io';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class AcrobaticBioModelChooser extends StatefulWidget {
  const AcrobaticBioModelChooser({
    super.key,
    this.width,
    this.defaultValue = '',
  });

  final double? width;
  final String defaultValue;

  @override
  AcrobaticBioModelChooserState createState() =>
      AcrobaticBioModelChooserState();
}

class AcrobaticBioModelChooserState extends State<AcrobaticBioModelChooser> {
  String modelPath = '';

  @override
  void initState() {
    modelPath = widget.defaultValue;
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return SizedBox(
        width: widget.width,
        child: TextField(
          decoration: InputDecoration(
            labelText: "Model path *",
            enabledBorder: const OutlineInputBorder(
              borderSide: BorderSide(color: Colors.red),
            ),
            focusedBorder: const OutlineInputBorder(
              borderSide: BorderSide(color: Colors.red),
            ),
            suffixIcon: IconButton(
              icon: const Icon(Icons.file_upload_outlined),
              onPressed: () async {
                final results = await FilePicker.platform.pickFiles(
                  type: FileType.custom,
                  allowedExtensions: ["bioMod"],
                );
                if (results == null) return;

                data.updateField("model_path", results.files.single.path!);

                setState(() {
                  modelPath = results.files.single.path!;
                });
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
    });
  }
}
