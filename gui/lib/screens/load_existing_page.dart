import 'dart:convert';
import 'dart:io';

import 'package:bioptim_gui/models/api_config.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart';
import 'package:http/http.dart' as http;

class LoadExisting extends StatefulWidget {
  const LoadExisting({super.key, this.columnWidth = 400.0});

  final double columnWidth;

  @override
  State<LoadExisting> createState() => _LoadExistingState();
}

class _LoadExistingState extends State<LoadExisting> {
  List<File> pickedFiles = [];
  String bestFile = '';
  List<String> toDiscard = [];

  void requestBestAndDiscard() {
    final url = Uri.parse('${APIConfig.url}/load_existing/load');
    final request = http.MultipartRequest('POST', url);
    request.files.addAll(pickedFiles.map((file) => http.MultipartFile.fromBytes(
          'files',
          file.readAsBytesSync(),
          filename: basename(file.path),
        )));

    request.send().then((response) async {
      if (response.statusCode != 200) {
        if (kDebugMode) {
          throw Exception(
              'Error while loading existing solution ${await response.stream.bytesToString()}');
        }
      }

      final jsonResponse = await response.stream.bytesToString();
      final jsonData = jsonDecode(jsonResponse);

      setState(() {
        bestFile = jsonData['best'];
        toDiscard = List<String>.from(jsonData['to_discard']);
      });
    });
  }

  void handleFilePickerOnPressed() async {
    final results = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ["pkl"],
      allowMultiple: true,
    );
    if (results == null) return;

    setState(() {
      pickedFiles = results.paths.map((path) => File(path!)).toList();
    });

    requestBestAndDiscard();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          const SizedBox(height: 12),
          Center(
            child: SizedBox(
              width: widget.columnWidth,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  ElevatedButton(
                    onPressed: handleFilePickerOnPressed,
                    child: const Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text('Load best solution'),
                        Icon(Icons.file_upload_outlined),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),
                  if (pickedFiles.isNotEmpty)
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Loaded files:'),
                        const SizedBox(height: 12),
                        for (final file in pickedFiles)
                          Text(basename(file.path)),
                        const SizedBox(height: 12),
                        // Best
                        const Text('Best solution:'),
                        const SizedBox(height: 12),
                        Text(basename(bestFile)),
                        const SizedBox(height: 12),
                        // To discard
                        const Text('To discard:'),
                        const SizedBox(height: 12),
                        for (final file in toDiscard) Text(file),
                      ],
                    ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
