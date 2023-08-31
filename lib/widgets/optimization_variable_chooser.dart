import 'package:bioptim_gui/models/optimization_variable.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:bioptim_gui/widgets/positive_integer_text_field.dart';
import 'package:flutter/material.dart';

class OptimizationVariableChooser extends StatefulWidget {
  const OptimizationVariableChooser(
      {super.key,
      required this.controllers,
      required this.variable,
      required this.isMandatory,
      required this.width});

  final OptimizationVariable variable;
  final VariableTextEditingControllers controllers;
  final bool isMandatory;
  final double width;

  @override
  State<OptimizationVariableChooser> createState() =>
      _OptimizationVariableChooserState();
}

class _OptimizationVariableChooserState
    extends State<OptimizationVariableChooser> {
  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        const SizedBox(height: 12),
        Row(
          children: [
            SizedBox(
              width: widget.width / 3 - 8,
              child: TextField(
                decoration: const InputDecoration(
                    label: Text('Variable name'), border: OutlineInputBorder()),
                controller: widget.controllers.name,
                enabled: !widget.isMandatory,
              ),
            ),
            const SizedBox(width: 12),
            SizedBox(
              width: widget.width / 3 - 8,
              child: PositiveIntegerTextField(
                label: 'Dimension',
                controller: widget.controllers.dimension,
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        CustomDropdownButton<Interpolation>(
          title: 'Bounds interpolation type',
          value: widget.variable.bounds.interpolation,
          items: Interpolation.values,
          onSelected: (value) => {}, // TODO
        ),
        const SizedBox(height: 12),
        Center(
            child: SizedBox(width: widget.width * 7 / 8, child: _DataFiller())),
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
