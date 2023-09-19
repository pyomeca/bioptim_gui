import 'package:bioptim_gui/models/decision_variables.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:bioptim_gui/widgets/animated_expanding_widget.dart';
import 'package:bioptim_gui/widgets/bio_model_chooser.dart';
import 'package:bioptim_gui/widgets/decision_variable_expander.dart';
import 'package:bioptim_gui/widgets/dynamics_chooser.dart';
import 'package:bioptim_gui/widgets/penalty_expander.dart';
import 'package:bioptim_gui/widgets/phase_information.dart';
import 'package:flutter/material.dart';

class PhaseGenerationMenu extends StatelessWidget {
  const PhaseGenerationMenu({super.key, required this.width});

  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = OptimalControlProgramControllers.instance;

    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        for (int i = 0; i < controllers.nbPhases; i++)
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 36),
            child: SizedBox(width: width, child: _buildPhase(phaseIndex: i)),
          ),
      ],
    );
  }

  Widget _buildPhase({required int phaseIndex}) {
    final controllers = OptimalControlProgramControllers.instance;

    return AnimatedExpandingWidget(
      header: Center(
        child: Text(
          controllers.nbPhases > 1
              ? 'Information on phase ${phaseIndex + 1}'
              : 'Information on the phase',
          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
      initialExpandedState: true,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(height: 24),
          BioModelChooser(phaseIndex: phaseIndex),
          const SizedBox(height: 12),
          PhaseInformation(phaseIndex: phaseIndex, width: width),
          const SizedBox(height: 12),
          DynamicsChooser(
            phaseIndex: phaseIndex,
            width: width,
          ),
          const SizedBox(height: 12),
          const Divider(),
          DecisionVariableExpander(
              from: DecisionVariableType.state,
              phaseIndex: phaseIndex,
              width: width),
          const SizedBox(height: 12),
          const Divider(),
          DecisionVariableExpander(
            from: DecisionVariableType.control,
            phaseIndex: phaseIndex,
            width: width,
          ),
          const SizedBox(height: 12),
          const Divider(),
          PenaltyExpander(
            penaltyType: ObjectiveFcn,
            phaseIndex: phaseIndex,
            width: width,
          ),
          const Divider(),
          PenaltyExpander(
            penaltyType: ConstraintFcn,
            phaseIndex: phaseIndex,
            width: width,
          ),
        ],
      ),
    );
  }
}
