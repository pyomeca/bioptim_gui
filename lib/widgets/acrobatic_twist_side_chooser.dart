import 'package:bioptim_gui/models/acrobatics_ocp_controllers.dart';
import 'package:bioptim_gui/models/acrobatics_twist_side.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:flutter/material.dart';

class AcrobaticTwistSideChooser extends StatelessWidget {
  const AcrobaticTwistSideChooser({
    super.key,
    required this.width,
  });

  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = AcrobaticsOCPControllers.instance;

    return SizedBox(
      width: width,
      child: CustomDropdownButton<PreferredTwistSide>(
        value: controllers.preferredTwistSide,
        items: PreferredTwistSide.values,
        title: 'Preferred twist side *',
        onSelected: (value) => controllers.setPreferredTwistSide(value),
        color: Colors.red,
      ),
    );
  }
}
