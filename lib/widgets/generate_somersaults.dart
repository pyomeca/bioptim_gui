import 'package:bioptim_gui/models/acrobatics_ocp_controllers.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:bioptim_gui/widgets/animated_expanding_widget.dart';
import 'package:bioptim_gui/widgets/penalty_expander.dart';
import 'package:bioptim_gui/widgets/somersault_informations.dart';
import 'package:flutter/material.dart';

class SomersaultGenerationMenu extends StatelessWidget {
  const SomersaultGenerationMenu({super.key, required this.width});

  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = AcrobaticsOCPControllers.instance;

    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        for (int i = 0; i < controllers.nbSomersaults; i++)
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 36),
            child: SizedBox(
                width: width,
                child: _buildSomersault(somersaultIndex: i, width: width)),
          ),
      ],
    );
  }

  Widget _buildSomersault(
      {required int somersaultIndex, required double width}) {
    final controllers = AcrobaticsOCPControllers.instance;

    return AnimatedExpandingWidget(
      header: Center(
        child: Text(
          controllers.nbSomersaults > 1
              ? 'Information on somersault ${somersaultIndex + 1}'
              : 'Information on the somersault',
          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
      initialExpandedState: true,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(height: 24),
          SomersaultInformation(
            somersaultIndex: somersaultIndex,
            width: width,
          ),
          const SizedBox(height: 12),
          const Divider(),
          PenaltyExpander(
            penaltyType: ObjectiveFcn,
            phaseIndex: somersaultIndex,
            width: width,
          ),
          const Divider(),
          PenaltyExpander(
            penaltyType: ConstraintFcn,
            phaseIndex: somersaultIndex,
            width: width,
          ),
        ],
      ),
    );
  }
}
