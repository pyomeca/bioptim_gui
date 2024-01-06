import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:bioptim_gui/widgets/acrobatics/somersault_informations.dart';
import 'package:bioptim_gui/widgets/penalties/penalty_expander.dart';
import 'package:bioptim_gui/widgets/utils/animated_expanding_widget.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class SomersaultGenerationMenu extends StatelessWidget {
  const SomersaultGenerationMenu({
    super.key,
    required this.width,
  });

  final double width;

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, acrobaticsData, child) {
      return Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          for (int i = 0; i < acrobaticsData.phasesInfo.length; i++)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 36),
              child: SizedBox(
                width: width,
                child: _buildSomersaultPhase(
                  somersaultIndex: i,
                  width: width,
                ),
              ),
            )
        ],
      );
    });
  }

  Widget _buildSomersaultPhase({
    required int somersaultIndex,
    required double width,
  }) {
    return Consumer<OCPData>(builder: (context, acrobaticsData, child) {
      return AnimatedExpandingWidget(
        header: Center(
          child: Text(
            'Information on ${acrobaticsData.phasesInfo[somersaultIndex].phaseName}',
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
        ),
        initialExpandedState: true,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 24),
            SomersaultInformation(
              somersaultIndex: somersaultIndex,
              width: width,
            ),
            const SizedBox(height: 12),
            const Divider(),
            PenaltyExpander(
              penaltyType: Objective,
              phaseIndex: somersaultIndex,
              width: width,
              endpointPrefix: '/acrobatics/phases_info',
            ),
            const Divider(),
            PenaltyExpander(
              penaltyType: Constraint,
              phaseIndex: somersaultIndex,
              width: width,
              endpointPrefix: '/acrobatics/phases_info',
            ),
          ],
        ),
      );
    });
  }
}
