import 'dart:math';

import 'package:bioptim_gui/models/decision_variables.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:bioptim_gui/widgets/positive_integer_text_field.dart';
import 'package:flutter/material.dart';

class DecisionVariableExpander extends StatefulWidget {
  const DecisionVariableExpander({
    super.key,
    required this.from,
    required this.phaseIndex,
    required this.width,
  });

  final DecisionVariableType from;
  final int phaseIndex;
  final double width;

  @override
  State<DecisionVariableExpander> createState() =>
      _DecisionVariableExpanderState();
}

class _DecisionVariableExpanderState extends State<DecisionVariableExpander> {
  bool _isExpanded = true;

  late final _names = OptimalControlProgramControllers.instance
      .getVariableNames(from: widget.from, phaseIndex: widget.phaseIndex);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        InkWell(
          onTap: () => setState(() => _isExpanded = !_isExpanded),
          child: SizedBox(
            width: widget.width,
            height: 50,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    '${widget.from.name} variables',
                    style: const TextStyle(
                        fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                ),
                Icon(_isExpanded ? Icons.expand_less : Icons.expand_more),
              ],
            ),
          ),
        ),
        if (_isExpanded)
          ..._names.map((name) {
            return _DecisionVariableChooser(
              name: name,
              phaseIndex: widget.phaseIndex,
              from: widget.from,
              width: widget.width,
            );
          }),
      ],
    );
  }
}

class _DecisionVariableChooser extends StatelessWidget {
  const _DecisionVariableChooser({
    required this.name,
    required this.from,
    required this.phaseIndex,
    required this.width,
  });

  final String name;
  final int phaseIndex;
  final DecisionVariableType from;
  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = OptimalControlProgramControllers.instance;

    final bounds = controllers
        .getVariable(name: name, phaseIndex: phaseIndex, from: from)
        .bounds;
    final initialGuess = controllers
        .getVariable(name: name, phaseIndex: phaseIndex, from: from)
        .initialGuess;

    final boundsControllers = controllers.getVariableBoundsControllers(
        name: name, phaseIndex: phaseIndex, from: from);
    final initialGuessControllers =
        controllers.getVariableInitialGuessControllers(
            name: name, phaseIndex: phaseIndex, from: from);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        const SizedBox(height: 24),
        Row(
          children: [
            SizedBox(
              width: width * 2 / 3 - 8,
              child: TextField(
                decoration: const InputDecoration(
                    label: Text('Variable name'), border: OutlineInputBorder()),
                controller: controllers.getVariableNameController(
                    name: name, phaseIndex: phaseIndex, from: from),
                enabled: false,
              ),
            ),
            const SizedBox(width: 12),
            SizedBox(
              width: width / 3 - 8,
              child: PositiveIntegerTextField(
                label: 'Dimension',
                controller: controllers.getVariableDimensionController(
                    name: name, phaseIndex: phaseIndex, from: from),
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        CustomDropdownButton<Interpolation>(
          title: 'Bounds interpolation type',
          value: bounds.interpolation,
          items: Interpolation.values,
          onSelected: (value) => controllers.setVariableBoundsInterpolation(
              value,
              name: name,
              phaseIndex: phaseIndex,
              from: from),
        ),
        const SizedBox(height: 12),
        CustomDropdownButton<Interpolation>(
          title: 'Initial guess interpolation type',
          value: initialGuess.interpolation,
          items: Interpolation.values,
          onSelected: (value) =>
              controllers.setVariableInitialGuessInterpolation(value,
                  name: name, phaseIndex: phaseIndex, from: from),
        ),
        const SizedBox(height: 32),
        _DataFiller(
            title: 'Min bounds',
            path: bounds,
            pathControllers: boundsControllers['minBounds']!,
            boxWidth: width * 7 / 8 / 3),
        const SizedBox(height: 12),
        _DataFiller(
            title: 'Max bounds',
            path: bounds,
            pathControllers: boundsControllers['maxBounds']!,
            boxWidth: width * 7 / 8 / 3),
        const SizedBox(height: 12),
        _DataFiller(
            title: 'Initial guess',
            path: initialGuess,
            pathControllers: initialGuessControllers,
            boxWidth: width * 7 / 8 / 3),
        const SizedBox(height: 16),
      ],
    );
  }
}

class _DataFiller extends StatelessWidget {
  const _DataFiller({
    required this.title,
    required this.path,
    required this.pathControllers,
    required this.boxWidth,
  });

  final String title;
  final Path path;
  final List<TextEditingController> pathControllers;
  final double boxWidth;

// TODO Add a graph that interacts with the matrix. So user can either fill by hand or by graph
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(fontWeight: FontWeight.bold),
          ),
          Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              ...path.interpolation.colNames.map((name) => SizedBox(
                  width: boxWidth,
                  child: Text(name, textAlign: TextAlign.center))),
            ],
          ),
          const SizedBox(height: 8),
          SizedBox(
            width: boxWidth * min(path.nbCols, 3),
            // TODO GridView does not work well for unknown nbCol... This should be done using an actual for loop
            // TODO Manage when there is more than 3 columns (scrolling?)
            child: GridView.count(
              childAspectRatio: 2.5,
              shrinkWrap: true,
              crossAxisCount: path.nbCols,
              children: [
                ...pathControllers.map((controller) => SizedBox(
                      width: 70,
                      child: TextField(
                          controller: controller,
                          enabled: true,
                          decoration: const InputDecoration(
                              border: OutlineInputBorder())),
                    )),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
