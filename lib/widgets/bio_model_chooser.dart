import 'dart:io';

import 'package:bioptim_gui/models/bio_model.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

class BioModelChooser extends StatelessWidget {
  const BioModelChooser({super.key, required this.phaseIndex, this.width});

  final int phaseIndex;
  final double? width;

  @override
  Widget build(BuildContext context) {
    final controllers = OptimalControlProgramControllers.instance;

    final bioModel = controllers.getBioModel(phaseIndex: phaseIndex);
    final modelPath = controllers.getModelPath(phaseIndex: phaseIndex);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        CustomDropdownButton<BioModel>(
          title: 'Dynamic model',
          value: bioModel,
          items: BioModel.values,
          onSelected: (value) =>
              controllers.setBioModel(value, phaseIndex: phaseIndex),
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
                    controllers.setModelPath(results.files.single.path!,
                        phaseIndex: phaseIndex);
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
