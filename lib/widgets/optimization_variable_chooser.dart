import 'package:bioptim_gui/models/optimization_variable.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:bioptim_gui/widgets/positive_integer_text_field.dart';
import 'package:flutter/material.dart';

class OptimizationVariableChooser extends StatelessWidget {
  const OptimizationVariableChooser({
    super.key,
    required this.name,
    required this.from,
    required this.phaseIndex,
    required this.width,
  });

  final String name;
  final int phaseIndex;
  final OptimizationVariableType from;
  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = OptimalControlProgramControllers.instance;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        const SizedBox(height: 12),
        Row(
          children: [
            SizedBox(
              width: width / 3 - 8,
              child: TextField(
                decoration: const InputDecoration(
                    label: Text('Variable name'), border: OutlineInputBorder()),
                controller: controllers.getVariableNameController(
                    name: name, phaseIndex: phaseIndex, from: from),
                enabled: false, // TODO get this from the variable
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
          value: controllers
              .getVariable(name: name, phaseIndex: phaseIndex, from: from)
              .bounds
              .interpolation,
          items: Interpolation.values,
          onSelected: (value) => controllers.setVariableBoundsInterpolation(
              value,
              name: name,
              phaseIndex: phaseIndex,
              from: from),
        ),
        const SizedBox(height: 12),
        Center(
            child: SizedBox(width: width * 7 / 8, child: const _DataFiller())),
      ],
    );
  }
}

class _DataFiller extends StatelessWidget {
  const _DataFiller();

// TODO Add a graph that interacts with the matrix. So user can either fill by hand or by graph
  @override
  Widget build(BuildContext context) {
    return GridView.count(
      childAspectRatio: 3.5,
      shrinkWrap: true,
      crossAxisCount: 3,
      children: const [
        Text(
          'Start',
          textAlign: TextAlign.center,
        ),
        Text(
          'Intermediates',
          textAlign: TextAlign.center,
        ),
        Text(
          'Last',
          textAlign: TextAlign.center,
        ),
        TextField(
            decoration: InputDecoration(
                border: OutlineInputBorder(), label: Text('Coucou'))),
        TextField(
            decoration: InputDecoration(
                border: OutlineInputBorder(), label: Text('Coucou'))),
        TextField(
            decoration: InputDecoration(
                border: OutlineInputBorder(), label: Text('Coucou'))),
        TextField(
            decoration: InputDecoration(
                border: OutlineInputBorder(), label: Text('Coucou'))),
      ],
    );
  }
}
