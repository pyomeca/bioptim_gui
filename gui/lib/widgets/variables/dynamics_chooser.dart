import 'package:bioptim_gui/widgets/variables/dynamic_chooser.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

class DynamicsChooser extends StatelessWidget {
  const DynamicsChooser(
      {super.key, required this.phaseIndex, required this.width});

  final int phaseIndex;
  final double width;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Expanded(
            child: DynamicChooser(
          width: width,
          phaseIndex: phaseIndex,
        )),
        const SizedBox(width: 12),
        InkWell(
          onTap: () {
            // final value = false; // TODO reimplement
            // // controllers.setDynamics(
            // //     Dynamics(type: dynamics.type, isExpanded: value),
            // //     phaseIndex: phaseIndex);
          },
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Checkbox(
                value: true,
                onChanged: (bool? value) {
                  if (kDebugMode) print("yes");
                },
                // TODO reimplement
                // onChanged: (value) => controllers.setDynamics(
                //     Dynamics(type: dynamics.type, isExpanded: value!),
                //     phaseIndex: phaseIndex),
              ),
              const Text('Expand\ndynamics'),
              const SizedBox(width: 12),
            ],
          ),
        ),
      ],
    );
  }
}
