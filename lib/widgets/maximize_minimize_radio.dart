import 'package:bioptim_gui/widgets/custom_radio_button.dart';
import 'package:flutter/material.dart';

enum MinMax {
  maximize,
  minimize,
  ;

  @override
  String toString() {
    switch (this) {
      case MinMax.maximize:
        return 'Maximize';
      case MinMax.minimize:
        return 'Minimize';
    }
  }

  String toPythonString() {
    switch (this) {
      case MinMax.maximize:
        return '-'; // will be used to negate the weight for maximizing
      case MinMax.minimize:
        return '';
    }
  }
}

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
