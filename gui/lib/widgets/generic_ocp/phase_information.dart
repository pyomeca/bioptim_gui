import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/widgets/utils/positive_float_text_field.dart';
import 'package:bioptim_gui/widgets/utils/positive_integer_text_field.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class PhaseInformation extends StatelessWidget {
  const PhaseInformation({
    super.key,
    required this.phaseIndex,
    required this.width,
  });

  final int phaseIndex;
  final double width;

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return Row(
        children: [
          SizedBox(
            width: width / 2 - 6,
            child: PositiveIntegerTextField(
              label: 'Number of shooting points',
              value: data.phaseInfo[phaseIndex].nbShootingPoints.toString(),
              onSubmitted: (newValue) {
                if (newValue.isNotEmpty) {
                  data.updatePhaseField(
                      phaseIndex, "nb_shooting_points", newValue);
                }
              },
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: PositiveFloatTextField(
              value: data.phaseInfo[phaseIndex].duration.toString(),
              label: 'Phase time (s)',
              onSubmitted: (newValue) {
                if (newValue.isNotEmpty) {
                  data.updatePhaseField(phaseIndex, "duration", newValue);
                }
              },
            ),
          ),
        ],
      );
    });
  }
}
