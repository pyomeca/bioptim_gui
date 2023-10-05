import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:bioptim_gui/widgets/utils/extensions.dart';
import 'package:flutter/material.dart';

class NodesChooser extends StatelessWidget {
  const NodesChooser({
    super.key,
    required this.width,
    required this.putEndpoint,
    this.defaultValue = "All shooting",
  });

  final double width;
  final String defaultValue;
  final String putEndpoint;

  @override
  Widget build(BuildContext context) {
    return CustomHttpDropdown(
      title: "Nodes to apply",
      width: width,
      defaultValue:
          defaultValue.toLowerCase().replaceAll("_", " ").capitalize(),
      getEndpoint: "/penalties/nodes",
      putEndpoint: putEndpoint,
      requestKey: "nodes",
      customStringFormatting: (s) => s.replaceAll(" ", "_").toLowerCase(),
    );
  }
}
