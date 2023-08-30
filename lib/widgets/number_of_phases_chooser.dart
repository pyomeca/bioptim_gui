import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:bioptim_gui/widgets/positive_integer_text_field.dart';
import 'package:flutter/material.dart';

class NumberOfPhasesChooser extends StatefulWidget {
  const NumberOfPhasesChooser({
    super.key,
    required this.onChangedNumberOfPhases,
    required this.onSelectPhase,
    required this.numberOfPhases,
    required this.width,
  });

  final Function(int value) onChangedNumberOfPhases;
  final Function(int value) onSelectPhase;
  final double width;
  final int numberOfPhases;

  @override
  State<NumberOfPhasesChooser> createState() => _NumberOfPhasesChooserState();
}

class _NumberOfPhasesChooserState extends State<NumberOfPhasesChooser> {
  int _currentPhase = 0;
  late final phaseController = TextEditingController(text: '1');

  @override
  void dispose() {
    phaseController.dispose();
    super.dispose();
  }

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
            controller: phaseController,
            onChanged: widget.onChangedNumberOfPhases,
            enabled:
                false, // TODO remove this line when python exporter is ready
          ),
        ),
        if (widget.numberOfPhases > 1)
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
                    for (int i = 0; i < widget.numberOfPhases; i++) i + 1
                  ],
                  onSelected: (value) {
                    widget.onSelectPhase(value - 1);
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
