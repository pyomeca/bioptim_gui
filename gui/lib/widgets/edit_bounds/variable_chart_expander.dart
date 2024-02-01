import 'package:bioptim_gui/models/decision_variables_type.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/models/variables.dart';
import 'package:bioptim_gui/widgets/edit_bounds/dof_edit_row.dart';
import 'package:bioptim_gui/widgets/utils/animated_expanding_widget.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class VariableChart extends StatelessWidget {
  final DecisionVariableType decisionVariableType;

  const VariableChart({
    super.key,
    required this.decisionVariableType,
  });

  @override
  Widget build(BuildContext context) {
    return AnimatedExpandingWidget(
        header: SizedBox(
          height: 50,
          child: Align(
            alignment: Alignment.center,
            child: Text(
              '${decisionVariableType.toString()} variables',
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
          ),
        ),
        child: Consumer<OCPData>(builder: (context, data, child) {
          final Variable variable =
              decisionVariableType == DecisionVariableType.state
                  ? data.phasesInfo[0].stateVariables[0]
                  : data.phasesInfo[0].controlVariables[0];
          final int dofCount = variable.dimension;

          return Column(children: [
            for (int dofIndex = 0; dofIndex < dofCount; dofIndex++)
              DofEditRow(
                decisionVariableType: decisionVariableType,
                dofIndex: dofIndex,
              ),
          ]);
        }));
  }
}
