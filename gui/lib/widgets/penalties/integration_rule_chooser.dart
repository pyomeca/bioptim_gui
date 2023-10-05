import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:bioptim_gui/widgets/utils/extensions.dart';
import 'package:flutter/material.dart';

class IntegrationRuleChooser extends StatelessWidget {
  const IntegrationRuleChooser({
    super.key,
    required this.width,
    required this.putEndpoint,
    this.defaultValue = "Rectangle left",
  });

  final double width;
  final String defaultValue;
  final String putEndpoint;

  @override
  Widget build(BuildContext context) {
    return CustomHttpDropdown(
      title: "Integration rule",
      width: width,
      defaultValue:
          defaultValue.toLowerCase().capitalize().replaceAll("_", " "),
      getEndpoint: "/penalties/integration_rules",
      putEndpoint: putEndpoint,
      requestKey: "integration_rule",
      customStringFormatting: (s) => s.replaceAll(" ", "_").toLowerCase(),
    );
  }
}
