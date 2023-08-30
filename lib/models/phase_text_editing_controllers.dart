import 'dart:math';

import 'package:bioptim_gui/models/optimal_control_program.dart';
import 'package:flutter/material.dart';

class PhaseTextEditingControllers {
  int _nbPhases = 1;
  final phaseController = TextEditingController(text: '1');

  // This is to keep track of how many controllers we have because we don't
  // delete them if we reduce _nbPhases
  int _nbPhasesMax = 1;

  set nbPhase(OptimalControlProgram ocp) {
    _nbPhases = ocp.nbPhases;
    _nbPhasesMax = max(_nbPhases, _nbPhasesMax);
    _updateAllControllers();
  }

  final nbShootingPointsControllers = <TextEditingController>[];
  final int Function({required int phaseIndex}) getNbShootingPoints;
  final Function(int value, {required int phaseIndex})
      onChangedNbShootingPoints;

  final phaseTimeControllers = <TextEditingController>[];
  final double Function({required int phaseIndex}) getPhaseTime;
  final Function(double value, {required int phaseIndex}) onChangedPhaseTime;

  PhaseTextEditingControllers({
    required this.getNbShootingPoints,
    required this.onChangedNbShootingPoints,
    required this.getPhaseTime,
    required this.onChangedPhaseTime,
  }) {
    _updateAllControllers();
  }

  void dispose() {
    for (int i = 0; i < _nbPhasesMax; i++) {
      nbShootingPointsControllers[i].dispose();
      phaseTimeControllers[i].dispose();
    }
  }

  void _updateAllControllers() {
    _updateController(
      nbShootingPointsControllers,
      initialValue: [
        for (int i = 0; i < _nbPhases; i++)
          getNbShootingPoints(phaseIndex: i).toString()
      ],
      onChanged: (String value, {required int phaseIndex}) =>
          onChangedNbShootingPoints(int.tryParse(value) ?? -1,
              phaseIndex: phaseIndex),
    );
    _updateController(
      phaseTimeControllers,
      initialValue: [
        for (int i = 0; i < _nbPhases; i++)
          getPhaseTime(phaseIndex: i).toString()
      ],
      onChanged: (String value, {required int phaseIndex}) =>
          onChangedPhaseTime(double.tryParse(value) ?? -1.0,
              phaseIndex: phaseIndex),
    );
  }

  void _updateController(controllers,
      {required List<String> initialValue,
      required Function(String value, {required int phaseIndex}) onChanged}) {
    if (controllers.length < _nbPhases) {
      for (int i = controllers.length; i < _nbPhases; i++) {
        controllers.add(TextEditingController());
        controllers[i].text = initialValue[i];
        controllers[i]
            .addListener(() => onChanged(controllers[i].text, phaseIndex: i));
      }
    } else {
      // Do not change anything if we already have the right number of phases

      // Also we don't mind having to much controllers declared so keep the
      // previously declared if we removed controllers
    }
  }
}
