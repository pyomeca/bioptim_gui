import 'package:bioptim_gui/models/minimize_maximize.dart';
import 'package:bioptim_gui/widgets/custom_radio_button.dart';
import 'package:flutter/material.dart';

class MinMaxRadio extends StatelessWidget {
  final MinMax value;
  final ValueChanged<MinMax?> customOnChanged;

  const MinMaxRadio({
    Key? key,
    required this.value,
    required this.customOnChanged,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return CustomRadioButton<MinMax>(
      value: value,
      items: MinMax.values,
      customOnChanged: customOnChanged,
    );
  }
}
