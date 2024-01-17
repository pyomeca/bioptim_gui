import 'package:bioptim_gui/models/acrobatics_data.dart';
import 'package:bioptim_gui/models/decision_variables_type.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/widgets/edit_bounds/variable_dof_column.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class DofEditRow extends StatelessWidget {
  final DecisionVariableType decisionVariableType;
  final int dofIndex;

  const DofEditRow({
    super.key,
    required this.decisionVariableType,
    required this.dofIndex,
  });

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      final int variableCount =
          decisionVariableType == DecisionVariableType.state
              ? data.phasesInfo[0].stateVariables.length
              : data.phasesInfo[0].controlVariables.length;

      return SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(
          children: [
            Column(
              children: [
                SizedBox(
                  width: 100,
                  child: Text(
                    decisionVariableType == DecisionVariableType.state
                        ? (data is AcrobaticsData
                            ? data.dofNames[dofIndex]
                            : '$dofIndex')
                        : '$dofIndex',
                    textAlign: TextAlign.center,
                    overflow: TextOverflow.clip,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            for (int variableIndex = 0;
                variableIndex < variableCount;
                variableIndex++)
              VariableDofColumn(
                  decisionVariableType: decisionVariableType,
                  variableIndex: variableIndex,
                  dofIndex: dofIndex),
          ],
        ),
      );
    });
  }
}
