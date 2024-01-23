import 'dart:convert';
import 'dart:io';

import 'package:bioptim_gui/models/api_config.dart';
import 'package:bioptim_gui/models/python_interface.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
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
          filename: file.path,
        )));

    setState(() {
      bestFile = '';
      toDiscard = [];
    });

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
        bestFile = jsonData['best'] ?? '';
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
                  const Text('Select the pickle(s) to load and compare:'),
                  const SizedBox(height: 12),
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
                        const Text(
                          'Loaded files:',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 12),
                        for (final file in pickedFiles)
                          Text(file.path.split('/').last),
                        const SizedBox(height: 12),
                        // Best
                        const Text(
                          'Best solution:',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 12),
                        if (bestFile.isNotEmpty)
                          ListTile(
                            contentPadding: const EdgeInsets.symmetric(
                                horizontal: 8, vertical: 4),
                            trailing: const Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Text('Save video'),
                                Icon(Icons.video_file),
                              ],
                            ),
                            title: Text(
                              bestFile.split('/').last,
                            ),
                            onTap: () async {
                              final process = await PythonInterface.instance
                                  .runAnimateSolution(bestFile);

                              if (process == null) {
                                if (kDebugMode) {
                                  print('Failed to run animate solution');
                                }
                              }
                            },
                          ),
                        const SizedBox(height: 12),
                        // To discard
                        const Text(
                          'To discard:',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 12),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            for (final file in toDiscard)
                              ListTile(
                                contentPadding: const EdgeInsets.symmetric(
                                    horizontal: 8, vertical: 4),
                                trailing: const Icon(Icons.delete),
                                title: Text(
                                  file.split('/').last,
                                ),
                                onTap: () {
                                  File fileToDelete = File(file);
                                  fileToDelete.deleteSync();

                                  setState(() {
                                    toDiscard.remove(file);
                                  });
                                },
                              ),
                          ],
                        )
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
