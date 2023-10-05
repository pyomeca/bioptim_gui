import 'dart:io';

import 'package:bioptim_gui/models/bio_model.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/widgets/utils/custom_dropdown_button.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class BioModelChooser extends StatefulWidget {
  const BioModelChooser({super.key, required this.phaseIndex, this.width});

  final int phaseIndex;
  final double? width;
  @override
  BioModelChooserState createState() => BioModelChooserState();
}

class BioModelChooserState extends State<BioModelChooser> {
  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const CustomDropdownButton<BioModel>(
            title: 'Dynamic model',
            value: BioModel.biorbd,
            items: BioModel.values,
            // onSelected: (value) Alexandre: TODO implement this in the backend,
            isExpanded: false,
          ),
          Padding(
            padding: const EdgeInsets.only(left: 8.0, top: 4.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Flexible(
                    child: Text(data.modelPath.isEmpty
                        ? 'Select the model file'
                        : File(data.modelPath).uri.pathSegments.last)),
                Tooltip(
                  message: 'Select model path',
                  child: IconButton(
                    onPressed: () async {
                      final results = await FilePicker.platform.pickFiles(
                        type: FileType.custom,
                        allowedExtensions: ["bioMod"],
                      );
                      if (results == null) return;

                      data.updateField(
                          "model_path", results.files.single.path!);
                    },
                    icon: const Icon(Icons.file_upload_outlined),
                  ),
                )
              ],
            ),
          )
        ],
      );
    });
  }
}
