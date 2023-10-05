import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:bioptim_gui/widgets/utils/extensions.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class InterpolationChooser extends StatelessWidget {
  const InterpolationChooser({
    super.key,
    required this.width,
    required this.putEndpoint,
    required this.requestKey,
    this.defaultValue = "Constant with first and last different",
    this.titlePrefix = "",
    this.customCallBack,
  });

  final double width;
  final String defaultValue;
  final String putEndpoint;
  final String requestKey;
  final String titlePrefix;
  final Function(http.Response)? customCallBack;

  @override
  Widget build(BuildContext context) {
    return CustomHttpDropdown(
      title: '$titlePrefix interpolation type',
      width: width,
      defaultValue:
          defaultValue.toLowerCase().replaceAll("_", " ").capitalize(),
      getEndpoint: "/variables/interpolation_type",
      putEndpoint: putEndpoint,
      requestKey: requestKey,
      customStringFormatting: (s) => s.replaceAll(" ", "_").toUpperCase(),
      customCallBack: customCallBack,
    );
  }
}
