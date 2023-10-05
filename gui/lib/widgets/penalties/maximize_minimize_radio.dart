import 'dart:convert';

import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:bioptim_gui/widgets/utils/extensions.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class MinMaxRadio extends StatefulWidget {
  const MinMaxRadio({
    super.key,
    required this.weightValue,
    required this.phaseIndex,
    required this.objectiveIndex,
  });

  final double weightValue;
  final int phaseIndex;
  final int objectiveIndex;

  @override
  MinMaxRadioState createState() => MinMaxRadioState();
}

class MinMaxRadioState extends State<MinMaxRadio> {
  String _selectedValue = '';

  @override
  void initState() {
    super.initState();
    _selectedValue = widget.weightValue > 0 ? "minimize" : "maximize";
  }

  @override
  Widget build(BuildContext context) {
    final List<String> values = ["maximize", "minimize"];

    return Consumer<OCPData>(builder: (context, data, child) {
      void updatePenalty(String newValue) async {
        final response = await data.requestMaker.updateMaximizeMinimize(
            widget.phaseIndex, widget.objectiveIndex, newValue);

        setState(() {
          _selectedValue = newValue;
        });

        final Penalty newObjective = Objective.fromJson(
            json.decode(response.body) as Map<String, dynamic>);

        data.updatePenalty(widget.phaseIndex, "objective",
            widget.objectiveIndex, newObjective);
      }

      return Column(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          for (final value in values)
            Row(
              children: [
                Radio<String>(
                  value: value,
                  groupValue: _selectedValue,
                  onChanged: (newValue) {
                    updatePenalty(newValue!);
                  },
                ),
                Text(value.capitalize()),
              ],
            ),
        ],
      );
    });
  }
}
