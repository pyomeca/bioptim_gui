import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/widgets/utils/positive_integer_text_field.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class NumberOfPhasesChooser extends StatelessWidget {
  const NumberOfPhasesChooser({
    super.key,
    required this.width,
  });

  final double width;

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return SizedBox(
        width: width * 1 / 2 - 6,
        child: PositiveIntegerTextField(
          label: 'Number of phases',
          value: data.nbPhases.toString(),
          enabled: true,
          onSubmitted: (newValue) async {
            if (newValue.isNotEmpty) {
              data.updateField("nb_phases", newValue);
            }
          },
        ),
      );
    });
  }
}
