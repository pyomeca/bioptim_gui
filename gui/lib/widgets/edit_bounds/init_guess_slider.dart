import 'package:bioptim_gui/models/decision_variable_value_type.dart';
import 'package:bioptim_gui/models/decision_variables_type.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/models/variables.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:syncfusion_flutter_sliders/sliders.dart';

class InitGuessSlider extends StatefulWidget {
  const InitGuessSlider({
    super.key,
    required this.phaseIndex,
    required this.decisionVariableType,
    required this.variableIndex,
    required this.dofIndex,
    required this.nodeIndex,
  });

  final int phaseIndex;
  final DecisionVariableType decisionVariableType;
  final int variableIndex;
  final int dofIndex;
  final int nodeIndex;

  @override
  State<InitGuessSlider> createState() => _InitGuessSliderState();
}

class _InitGuessSliderState extends State<InitGuessSlider> {
  // Add a key to force recreation when phaseIndex changes
  Key get key => ValueKey<int>(widget.phaseIndex);
  double? _value;
  double _rangeMinValue = -1;
  double _rangeMaxValue = 1;

  @override
  void initState() {
    super.initState();
    final Variable variable =
        widget.decisionVariableType == DecisionVariableType.state
            ? context
                .read<OCPData>()
                .phasesInfo[widget.phaseIndex]
                .stateVariables[widget.variableIndex]
            : context
                .read<OCPData>()
                .phasesInfo[widget.phaseIndex]
                .controlVariables[widget.variableIndex];

    final int initGuessNbNodes = variable.initialGuess[widget.dofIndex].length;

    int boudCorrespondingNode = widget.nodeIndex;

    if (initGuessNbNodes == 2 && widget.nodeIndex != 0) {
      boudCorrespondingNode =
          variable.bounds.minBounds[widget.dofIndex].length - 1;
    }

    final double boundMinValue =
        variable.bounds.minBounds[widget.dofIndex][boudCorrespondingNode];
    final double boundMaxValue =
        variable.bounds.maxBounds[widget.dofIndex][boudCorrespondingNode];
    const double margin = 0.01;

    _rangeMinValue = boundMinValue - margin;
    _rangeMaxValue = boundMaxValue + margin;
    _value = variable.initialGuess[widget.dofIndex][widget.nodeIndex];
  }

  void _updateRange() {
    int boudCorrespondingNode = widget.nodeIndex;

    final Variable variable =
        widget.decisionVariableType == DecisionVariableType.state
            ? context
                .read<OCPData>()
                .phasesInfo[widget.phaseIndex]
                .stateVariables[widget.variableIndex]
            : context
                .read<OCPData>()
                .phasesInfo[widget.phaseIndex]
                .controlVariables[widget.variableIndex];

    final int initGuessNbNodes = variable.initialGuess[widget.dofIndex].length;

    if (initGuessNbNodes == 2 && widget.nodeIndex != 0) {
      boudCorrespondingNode =
          variable.bounds.minBounds[widget.dofIndex].length - 1;
    }

    final double boundMinValue =
        variable.bounds.minBounds[widget.dofIndex][boudCorrespondingNode];
    final double boundMaxValue =
        variable.bounds.maxBounds[widget.dofIndex][boudCorrespondingNode];
    const double margin = 0.01;

    setState(() {
      _rangeMinValue = boundMinValue - margin;
      _rangeMaxValue = boundMaxValue + margin;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return SfSlider.vertical(
        activeColor: Colors.black,
        inactiveColor: Colors.black,
        min: _rangeMinValue,
        max: _rangeMaxValue,
        value: _value,
        interval: (_rangeMinValue.abs() + _rangeMaxValue.abs()) / 5,
        showTicks: true,
        showLabels: true,
        onChangeEnd: (value) {
          data.updateDecisionVariableValue(
            widget.phaseIndex,
            widget.decisionVariableType,
            DecisionVariableValueType.initGuess,
            widget.variableIndex,
            widget.dofIndex,
            widget.nodeIndex,
            value,
          );

          _updateRange();
        },
        onChanged: (dynamic value) {
          setState(() {
            _value = value;
          });
        },
      );
    });
  }
}
