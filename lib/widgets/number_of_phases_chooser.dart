import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class NumberOfPhasesChooser extends StatefulWidget {
  const NumberOfPhasesChooser({
    super.key,
    required this.onChangedNumberOfPhases,
    required this.onSelectPhase,
    required this.numberOfPhases,
    required this.columnWidth,
  });

  final Function(int value) onChangedNumberOfPhases;
  final Function(int value) onSelectPhase;
  final double columnWidth;
  final int numberOfPhases;

  @override
  State<NumberOfPhasesChooser> createState() => _NumberOfPhasesChooserState();
}

class _NumberOfPhasesChooserState extends State<NumberOfPhasesChooser> {
  int _currentPhase = 0;
  late final phaseController =
      TextEditingController(text: (_currentPhase + 1).toString());

  @override
  Widget build(BuildContext context) {
    final width = widget.columnWidth * 1 / 2 - 6;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          width: width,
          child: Focus(
            onFocusChange: (hasFocus) {
              if (!hasFocus) {
                if (phaseController.text == '' ||
                    int.tryParse(phaseController.text) == 0) {
                  phaseController.text = '1';
                }
                final nbPhases = int.parse(phaseController.text);
                widget.onChangedNumberOfPhases(nbPhases);
                setState(() {
                  if (_currentPhase >= nbPhases) _currentPhase = nbPhases - 1;
                });
              }
            },
            child: TextField(
              controller: phaseController,
              decoration: const InputDecoration(
                  labelText: 'Number of phases', border: OutlineInputBorder()),
              inputFormatters: [FilteringTextInputFormatter.digitsOnly],
              enabled: true,
            ),
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
