import 'package:bioptim_gui/models/decision_variables_type.dart';
import 'package:bioptim_gui/widgets/edit_bounds/bound_chart.dart';
import 'package:bioptim_gui/widgets/edit_bounds/dof_phase_sliders.dart';
import 'package:flutter/material.dart';

class VariableDofColumn extends StatelessWidget {
  final DecisionVariableType decisionVariableType;
  final int variableIndex;
  final int dofIndex;

  const VariableDofColumn({
    super.key,
    required this.decisionVariableType,
    required this.variableIndex,
    required this.dofIndex,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        BoundChart(
          key: Key('BoundChart_${dofIndex}_state_$variableIndex'),
          decisionVariableType: decisionVariableType,
          variableIndex: variableIndex,
          dofIndex: dofIndex,
        ),
        DofPhaseSliders(
          decisionVariableType: decisionVariableType,
          variableIndex: variableIndex,
          dofIndex: dofIndex,
        ),
      ],
    );
  }
}
