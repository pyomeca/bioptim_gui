import 'package:bioptim_gui/models/mayer_lagrange_enum.dart';
import 'package:bioptim_gui/widgets/custom_radio_button.dart';
import 'package:flutter/material.dart';

class MayerLagrangeRadio extends StatelessWidget {
  final ObjectiveType value;
  final ValueChanged<ObjectiveType?> customOnChanged;

  const MayerLagrangeRadio({
    Key? key,
    required this.value,
    required this.customOnChanged,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return CustomRadioButton<ObjectiveType>(
      value: value,
      items: ObjectiveType.values,
      customOnChanged: customOnChanged,
    );
  }
}
