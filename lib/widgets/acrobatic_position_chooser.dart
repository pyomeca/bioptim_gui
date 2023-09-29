import 'package:bioptim_gui/models/acrobatics_ocp_controllers.dart';
import 'package:bioptim_gui/models/acrobatics_position.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:flutter/material.dart';

class AcrobaticPositionChooser extends StatelessWidget {
  const AcrobaticPositionChooser({
    super.key,
    required this.width,
  });

  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = AcrobaticsOCPControllers.instance;

    return SizedBox(
      width: width,
      child: CustomDropdownButton<AcrobaticsPosition>(
        value: controllers.position,
        items: AcrobaticsPosition.values,
        title: 'Jump position *',
        onSelected: (value) => controllers.setPosition(value),
        color: Colors.red,
      ),
    );
  }
}
