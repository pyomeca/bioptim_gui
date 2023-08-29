import 'dart:io';

import 'package:bioptim_gui/models/bio_model.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

class BioModelChooser extends StatelessWidget {
  const BioModelChooser({
    super.key,
    required this.onSelectedBioModel,
    required this.onSelectedModelPath,
    required this.bioModel,
    required this.modelPath,
    this.width,
  });

  final Function(BioModel) onSelectedBioModel;
  final Function(String) onSelectedModelPath;
  final BioModel bioModel;
  final String modelPath;
  final double? width;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        CustomDropdownButton<BioModel>(
          title: 'Dynamic model',
          value: bioModel,
          items: BioModel.values,
          onSelected: (value) => onSelectedBioModel(value),
          isExpanded: false,
        ),
        Padding(
          padding: const EdgeInsets.only(left: 8.0, top: 4.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Flexible(
                  child: Text(modelPath.isEmpty
                      ? 'Select the model file'
                      : File(modelPath).uri.pathSegments.last)),
              Tooltip(
                message: 'Select model path',
                child: IconButton(
                  onPressed: () async {
                    final results = await FilePicker.platform.pickFiles(
                      type: FileType.custom,
                      allowedExtensions: [bioModel.extension],
                    );
                    if (results == null) return;

                    onSelectedModelPath(results.files.single.path!);
                  },
                  icon: const Icon(Icons.file_upload_outlined),
                ),
              )
            ],
          ),
        )
      ],
    );
  }
}
