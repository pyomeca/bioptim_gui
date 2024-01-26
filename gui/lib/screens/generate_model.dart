import 'package:flutter/material.dart';
// import http

class GenerateModel extends StatelessWidget {
  const GenerateModel({super.key, this.columnWidth = 400.0});

  final double columnWidth;

  // TODO
  // request http.post localhost:8001/process_yeadon_model/
  // see request body in YeadonModelGenerator API doc
  // uses the image paths for now, won't work with docker

  @override
  Widget build(BuildContext context) {
    return const Text("Generate Model Page");
    // FilePicker to choose the images
  }
}
