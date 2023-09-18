import 'package:bioptim_gui/models/acrobatics_ocp_controllers.dart';
import 'package:bioptim_gui/widgets/positive_integer_text_field.dart';
import 'package:flutter/material.dart';

class AcrobaticsInformation extends StatelessWidget {
  const AcrobaticsInformation({
    super.key,
    required this.somersaultIndex,
    required this.width,
  });

  final int somersaultIndex;
  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = AcrobaticsOCPControllers.instance;

    return Row(
      children: [
        SizedBox(
          width: width / 2,
          child: PositiveIntegerTextField(
            label: 'Number of half twists',
            controller: controllers.nbHalfTwistsControllers[somersaultIndex],
          ),
        ),
        const SizedBox(width: 12),
      ],
    );
  }
}
