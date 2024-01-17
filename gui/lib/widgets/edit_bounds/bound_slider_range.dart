import 'package:bioptim_gui/models/decision_variable_value_type.dart';
import 'package:bioptim_gui/models/decision_variables_type.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/models/variables.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:syncfusion_flutter_sliders/sliders.dart';

class BoundSliderRange extends StatefulWidget {
  const BoundSliderRange({
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
  State<BoundSliderRange> createState() => _BoundSliderRangeState();
}

class _BoundSliderRangeState extends State<BoundSliderRange> {
  // Add a key to force recreation when phaseIndex changes
  Key get key => ValueKey<int>(widget.phaseIndex);

  SfRangeValues? _values;
  double? _minValue;
  double? _maxValue;
  double? _oldStart;
  double? _oldEnd;
  final rangeMargin = 0.25;
  final tickNumber = 5;

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

    double minValue =
        variable.bounds.minBounds[widget.dofIndex][widget.nodeIndex];
    double maxValue =
        variable.bounds.maxBounds[widget.dofIndex][widget.nodeIndex];
    final double margin =
        (maxValue.abs() + minValue.abs()) * rangeMargin + 0.01;
    // + 0.01 is to avoid the case where minValue == maxValue

    _minValue = minValue - margin;
    _maxValue = maxValue + margin;

    if (minValue == maxValue) {
      minValue = minValue - 0.01;
      maxValue = maxValue + 0.01;
    }

    _values = SfRangeValues(minValue, maxValue);

    _oldStart = minValue;
    _oldEnd = maxValue;
  }

  ///
  /// Update the _minValue and _maxValue so that the slider always have a margin
  void _updateRanges() {
    final double margin =
        (_oldEnd!.abs() + _oldStart!.abs()) * rangeMargin + 0.01;
    _minValue = _oldStart! - margin;
    _maxValue = _oldEnd! + margin;
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return SfRangeSlider.vertical(
        min: _minValue!,
        max: _maxValue!,
        values: _values!,
        interval: (_minValue!.abs() + _maxValue!.abs()) / tickNumber,
        showTicks: true,
        showLabels: true,
        enableTooltip: true,
        onChangeEnd: (SfRangeValues values) {
          if (values.start != _oldStart) {
            data.updateDecisionVariableValue(
              widget.phaseIndex,
              widget.decisionVariableType,
              DecisionVariableValueType.minBound,
              widget.variableIndex,
              widget.dofIndex,
              widget.nodeIndex,
              values.start,
            );

            _oldStart = values.start;
            _updateRanges();
          } else {
            data.updateDecisionVariableValue(
              widget.phaseIndex,
              widget.decisionVariableType,
              DecisionVariableValueType.maxBound,
              widget.variableIndex,
              widget.dofIndex,
              widget.nodeIndex,
              values.end,
            );

            _oldEnd = values.end;
            _updateRanges();
          }
        },
        onChanged: (SfRangeValues values) {
          setState(() {
            _values = values;
          });
        },
      );
    });
  }
}
