import 'dart:math';

import 'package:bioptim_gui/models/dynamics.dart';
import 'package:bioptim_gui/models/optimization_variable.dart';
import 'package:flutter/material.dart';

class PhaseTextEditingControllers {
  int _nbPhases = 1;

  // This is to keep track of how many controllers we have because we don't
  // delete them if we reduce _nbPhases
  int _nbPhasesMax = 1;

  final nbShootingPoints = <TextEditingController>[];
  final int Function({required int phaseIndex}) getNbShootingPoints;
  final Function(int value, {required int phaseIndex})
      onChangedNbShootingPoints;

  final phaseDuration = <TextEditingController>[];
  final double Function({required int phaseIndex}) getPhaseDuration;
  final Function(double value, {required int phaseIndex})
      onChangedPhaseDuration;

  final phaseController = TextEditingController(text: '1');
  final void Function(int nbPhases) onChangedNbPhases;

  final List<Map<String, VariableTextEditingControllers>> states = [];
  final List<Map<String, VariableTextEditingControllers>> controls = [];
  final List<String> Function(
      {required int phaseIndex,
      required OptimizationVariableType from}) getVariableNames;
  final int Function(
      {required String name,
      required int phaseIndex,
      required OptimizationVariableType from}) getVariableNumberOfColumns;
  final void Function(
    int dimension, {
    required String name,
    required int phaseIndex,
    required OptimizationVariableType from,
  }) setVariableDimension;

  PhaseTextEditingControllers({
    required this.onChangedNbPhases,
    required this.getNbShootingPoints,
    required this.onChangedNbShootingPoints,
    required this.getPhaseDuration,
    required this.onChangedPhaseDuration,
    required this.getVariableNames,
    required this.getVariableNumberOfColumns,
    required this.setVariableDimension,
  }) {
    phaseController.addListener(() async {
      final tp = int.tryParse(phaseController.text);
      if (tp == null || tp < 1) return;
      _nbPhases = tp;
      _nbPhasesMax = max(_nbPhases, _nbPhasesMax);
      onChangedNbPhases(_nbPhases);
      // Wait for one frame so the the UI is updated
      WidgetsBinding.instance.addPostFrameCallback((timeStamp) {
        _updateAllControllers();
      });
    });
    _updateAllControllers();
  }

  void dispose() {
    phaseController.dispose();
    for (int i = 0; i < _nbPhasesMax; i++) {
      nbShootingPoints[i].dispose();
      phaseDuration[i].dispose();
    }
  }

  void setVariables(Dynamics dynamics, {required int phaseIndex}) {}

  void _updateAllControllers() {
    _updateController(
      nbShootingPoints,
      initialValue: [
        for (int i = 0; i < _nbPhases; i++)
          getNbShootingPoints(phaseIndex: i).toString()
      ],
      onChanged: (String value, {required int phaseIndex}) =>
          onChangedNbShootingPoints(int.tryParse(value) ?? -1,
              phaseIndex: phaseIndex),
    );
    _updateController(
      phaseDuration,
      initialValue: [
        for (int i = 0; i < _nbPhases; i++)
          getPhaseDuration(phaseIndex: i).toString()
      ],
      onChanged: (String value, {required int phaseIndex}) =>
          onChangedPhaseDuration(double.tryParse(value) ?? -1.0,
              phaseIndex: phaseIndex),
    );

    _updateVariableController(
      states,
      variableNames: ({required phaseIndex}) => getVariableNames(
          phaseIndex: phaseIndex, from: OptimizationVariableType.state),
      setDimension: (value, {required name, required phaseIndex}) =>
          setVariableDimension(value,
              name: name,
              phaseIndex: phaseIndex,
              from: OptimizationVariableType.state),
      getNumberOfBoundsColumns: ({required name, required phaseIndex}) =>
          getVariableNumberOfColumns(
              name: name,
              phaseIndex: phaseIndex,
              from: OptimizationVariableType.state),
    );
    _updateVariableController(
      controls,
      variableNames: ({required phaseIndex}) => getVariableNames(
          phaseIndex: phaseIndex, from: OptimizationVariableType.control),
      setDimension: (value, {required name, required phaseIndex}) =>
          setVariableDimension(value,
              name: name,
              phaseIndex: phaseIndex,
              from: OptimizationVariableType.control),
      getNumberOfBoundsColumns: ({required name, required phaseIndex}) =>
          getVariableNumberOfColumns(
              name: name,
              phaseIndex: phaseIndex,
              from: OptimizationVariableType.control),
    );
  }

  void _updateController(List<TextEditingController> controllers,
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

  void _updateVariableController(
      List<Map<String, VariableTextEditingControllers>> controllers,
      {required List<String> Function({required int phaseIndex}) variableNames,
      required Function(int value,
              {required String name, required int phaseIndex})
          setDimension,
      required int Function({required String name, required int phaseIndex})
          getNumberOfBoundsColumns}) {
    if (controllers.length < _nbPhases) {
      // For each of the new phases, declare all the required variables
      for (int i = controllers.length; i < _nbPhases; i++) {
        Map<String, VariableTextEditingControllers> tp = {};
        for (final name in variableNames(phaseIndex: i)) {
          tp[name] = VariableTextEditingControllers(name,
              setDimension: (value) =>
                  setDimension(value, name: name, phaseIndex: i),
              getNumberOfBoundsColumns: () =>
                  getNumberOfBoundsColumns(name: name, phaseIndex: i));
        }
        controllers.add(tp);
      }
    } else {
      // Do not change anything if we already have the right number of phases

      // Also we don't mind having to much controllers declared so keep the
      // previously declared if we removed controllers
    }
  }
}

class VariableTextEditingControllers {
  // TODO Add the capability to automatically fill end phase continuity with starting of next phase
  final name = TextEditingController();
  final dimension = TextEditingController(text: '1');
  void Function(int value) setDimension;

  int Function() getNumberOfBoundsColumns;
  final bounds = <TextEditingController>[];

  VariableTextEditingControllers(String name,
      {required this.setDimension, required this.getNumberOfBoundsColumns}) {
    this.name.text = name;
    _updateBounds(getNumberOfBoundsColumns());

    dimension.addListener(() {
      // The text field of dimension should only be positive integers
      final value = int.tryParse(dimension.text);
      if (value == null || value < 1) return;

      setDimension(value);
      _updateBounds(value * getNumberOfBoundsColumns());
    });
  }

  void _updateBounds(int length) {
    // We have to reset all the controllers since we don't know if the number of
    // dimension or column changed. This would make the textfield bouncing around
    // randomly.
    _disposeBounds();
    for (int i = 0; i < length; i++) {
      bounds.add(TextEditingController());
    }
  }

  void _disposeBounds() {
    for (final bound in bounds) {
      bound.dispose();
    }
    bounds.clear();
  }

  void dispose() {
    name.dispose();
    dimension.dispose();
    _disposeBounds();
  }
}
