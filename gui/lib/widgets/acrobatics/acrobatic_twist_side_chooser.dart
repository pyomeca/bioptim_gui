import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:flutter/material.dart';

class AcrobaticTwistSideChooser extends StatelessWidget {
  const AcrobaticTwistSideChooser({
    super.key,
    required this.width,
    this.defaultValue = "Left",
  });

  final double width;
  final String defaultValue;

  @override
  Widget build(BuildContext context) {
    return CustomHttpDropdown(
      title: "Preferred twist side *",
      width: width,
      defaultValue: defaultValue,
      getEndpoint: "/acrobatics/preferred_twist_side",
      putEndpoint: "/acrobatics/preferred_twist_side",
      requestKey: "preferred_twist_side",
      color: Colors.red,
    );
  }
}
