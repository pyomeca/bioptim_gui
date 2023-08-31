import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:bioptim_gui/widgets/positive_integer_text_field.dart';
import 'package:flutter/material.dart';

class NumberOfPhasesChooser extends StatefulWidget {
  const NumberOfPhasesChooser({
    super.key,
    required this.controllers,
    required this.width,
  });

  final double width;
  final OptimalControlProgramControllers controllers;

  @override
  State<NumberOfPhasesChooser> createState() => _NumberOfPhasesChooserState();
}

class _NumberOfPhasesChooserState extends State<NumberOfPhasesChooser> {
  int _currentPhase = 0;

  @override
  Widget build(BuildContext context) {
    final width = widget.width * 1 / 2 - 6;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          width: width,
          child: PositiveIntegerTextField(
            label: 'Number of phases',
            controller: widget.controllers.nbPhasesController,
            enabled:
                true, // TODO remove this line when python exporter is ready
          ),
        ),
        if (widget.controllers.nbPhases > 1)
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Divider(),
              const SizedBox(height: 8),
              SizedBox(
                width: width,
                // To facilitate the vizualisation of the user, the first phase is
                // set to 1 instead of 0
                child: CustomDropdownButton<int>(
                  title: 'Showing phase',
                  value: _currentPhase + 1,
                  items: [
                    for (int i = 0; i < widget.controllers.nbPhases; i++) i + 1
                  ],
                  onSelected: (value) {
                    widget.controllers.nbPhases = value - 1;
                    setState(() => _currentPhase = value - 1);
                  },
                  isExpanded: false,
                ),
              ),
            ],
          )
      ],
    );
  }
}
