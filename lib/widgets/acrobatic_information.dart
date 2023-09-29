import 'package:bioptim_gui/models/acrobatics_ocp_controllers.dart';
import 'package:bioptim_gui/widgets/positive_integer_text_field.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class AcrobaticInformation extends StatelessWidget {
  const AcrobaticInformation({super.key, required this.width});

  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = AcrobaticsOCPControllers.instance;

    return Column(
      children: [
        SizedBox(
          width: width,
          child: PositiveIntegerTextField(
            label: 'Number of somersaults *',
            controller: controllers.nbSomersaultsController,
            enabled: true,
            color: Colors.red,
          ),
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            SizedBox(
              width: width / 2 - 6,
              child: TextField(
                controller: controllers.finalTimeController,
                decoration: const InputDecoration(
                    enabledBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: Colors.red),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: Colors.red),
                    ),
                    labelText: 'Final time *',
                    border: OutlineInputBorder()),
                inputFormatters: [
                  FilteringTextInputFormatter.allow(RegExp(r'[0-9\.]'))
                ],
              ),
            ),
            const SizedBox(width: 12),
            SizedBox(
              width: width / 2 - 6,
              child: TextField(
                controller: controllers.finalTimeMarginController,
                decoration: const InputDecoration(
                    enabledBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: Colors.red),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: Colors.red),
                    ),
                    labelText: 'Final time margin *',
                    border: OutlineInputBorder()),
                inputFormatters: [
                  FilteringTextInputFormatter.allow(RegExp(r'[0-9\.]'))
                ],
              ),
            ),
          ],
        )
      ],
    );
  }
}
