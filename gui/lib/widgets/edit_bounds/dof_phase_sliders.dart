import 'package:bioptim_gui/models/decision_variables_type.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/models/variables.dart';
import 'package:bioptim_gui/widgets/edit_bounds/bound_slider_range.dart';
import 'package:bioptim_gui/widgets/edit_bounds/init_guess_slider.dart';
import 'package:bioptim_gui/widgets/utils/custom_dropdown_button.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class DofPhaseSliders extends StatefulWidget {
  const DofPhaseSliders({
    super.key,
    required this.decisionVariableType,
    required this.variableIndex,
    required this.dofIndex,
  });

  final DecisionVariableType decisionVariableType;
  final int variableIndex;
  final int dofIndex;

  @override
  State<DofPhaseSliders> createState() => _DofPhaseSlidersState();
}

class _DofPhaseSlidersState extends State<DofPhaseSliders> {
  int _phaseIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      final Variable variable = widget.decisionVariableType ==
              DecisionVariableType.state
          ? data.phasesInfo[_phaseIndex].stateVariables[widget.variableIndex]
          : data.phasesInfo[_phaseIndex].controlVariables[widget.variableIndex];

      final int boundNbNode = variable.bounds.minBounds[widget.dofIndex].length;
      final int initGuessNbNode = variable.initialGuess[widget.dofIndex].length;

      final List<int> phaseList = [];
      for (int i = 0; i < data.nbPhases; i++) {
        phaseList.add(i);
      }

      return Row(
        children: [
          SizedBox(
            width: 60,
            child: CustomDropdownButton<int>(
              title: "Phase",
              items: phaseList,
              value: _phaseIndex,
              onSelected: (int? newValue) {
                setState(() {
                  _phaseIndex = newValue!;
                });
              },
            ),
          ),
          for (int boundIndex = 0; boundIndex < boundNbNode; boundIndex++)
            Column(
              children: [
                const Text('Bounds'),
                BoundSliderRange(
                  key: ValueKey<int>(_phaseIndex),
                  phaseIndex: _phaseIndex,
                  decisionVariableType: widget.decisionVariableType,
                  variableIndex: widget.variableIndex,
                  dofIndex: widget.dofIndex,
                  nodeIndex: boundIndex,
                )
              ],
            ),
          for (int initGuessIndex = 0;
              initGuessIndex < initGuessNbNode;
              initGuessIndex++)
            Column(children: [
              const Text('Init guess'),
              InitGuessSlider(
                key: ValueKey<int>(_phaseIndex),
                phaseIndex: _phaseIndex,
                decisionVariableType: widget.decisionVariableType,
                variableIndex: widget.variableIndex,
                dofIndex: widget.dofIndex,
                nodeIndex: initGuessIndex,
              ),
            ]),
        ],
      );
    });
  }
}
