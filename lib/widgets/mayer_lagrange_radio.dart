import 'package:bioptim_gui/widgets/custom_radio_button.dart';
import 'package:flutter/material.dart';

enum MayerLagrange {
  mayer,
  lagrange,
  ;

  @override
  String toString() {
    switch (this) {
      case mayer:
        return '\u2133'; // German mark M
      case lagrange:
        return '\u2112'; // Laplace L
    }
  }
}

class MayerLagrangeRadio extends StatelessWidget {
  final MayerLagrange value;
  final ValueChanged<MayerLagrange?> customOnChanged;

  const MayerLagrangeRadio({
    Key? key,
    required this.value,
    required this.customOnChanged,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return CustomRadioButton<MayerLagrange>(
      value: value,
      items: MayerLagrange.values,
      customOnChanged: customOnChanged,
    );
  }
}
