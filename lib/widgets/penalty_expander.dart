import 'package:bioptim_gui/models/nodes.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:bioptim_gui/widgets/animated_expanding_widget.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class PenaltyExpander extends StatelessWidget {
  const PenaltyExpander({
    super.key,
    required this.penaltyType,
    required this.phaseIndex,
    required this.width,
  });

  final Type penaltyType;
  final int phaseIndex;
  final double width;

  String penaltyTypeToString(Type penaltyType) {
    switch (penaltyType) {
      case ObjectiveFcn:
        return 'Objective functions';
      case ConstraintFcn:
        return 'Constraints';
      default:
        throw 'Wrong penalty type';
    }
  }

  @override
  Widget build(BuildContext context) {
    final name = penaltyTypeToString(penaltyType);

    // TODO fetch this from the model
    final penalties = [
      Objective(LagrangeFcn.minimizeControls,
          nodes: Nodes.all, weight: 1, arguments: {}),
      Objective(LagrangeFcn.minimizeStates,
          nodes: Nodes.all, weight: 1, arguments: {}),
      Objective(MayerFcn.minimizeTime,
          nodes: Nodes.end, weight: 1, arguments: {}),
    ];

    return AnimatedExpandingWidget(
      header: SizedBox(
        width: width,
        height: 50,
        child: Align(
          alignment: Alignment.centerLeft,
          child: Text(
            name,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(height: 24),
          ...penalties.asMap().keys.map((index) => Padding(
                padding: const EdgeInsets.only(bottom: 24.0),
                child: _PathTile(
                  penalty: penalties[index],
                  penaltyIndex: index,
                  width: width,
                ),
              )),
          const SizedBox(height: 26),
        ],
      ),
    );
  }
}

class _PathTile extends StatelessWidget {
  const _PathTile({
    required this.penalty,
    required this.penaltyIndex,
    required this.width,
  });

  final Penalty penalty;
  final int penaltyIndex;
  final double width;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          width: width,
          child: CustomDropdownButton<PenaltyFcn>(
            title:
                '${penalty.fcn.penaltyType} ${penaltyIndex + 1} (${penalty.fcn.penaltyTypeToString})',
            value: penalty.fcn,
            items: penalty.fcn.fcnValues,
            onSelected: (value) {}, // TODO
            isExpanded: false,
          ),
        ),
        const SizedBox(height: 12),
        ...penalty.fcn.mandatoryArguments.map((e) => Padding(
              padding: const EdgeInsets.only(bottom: 12.0),
              child: Row(
                children: [
                  SizedBox(
                    width: width * 2 / 3 - 6,
                    child: TextField(
                        decoration: InputDecoration(
                            label: Text('Argument: ${e.name}'),
                            border: const OutlineInputBorder()),
                        inputFormatters: [
                          FilteringTextInputFormatter.allow(
                              e.dataType.regexpValidator)
                        ]),
                  ),
                  const SizedBox(width: 12),
                  SizedBox(
                    width: width * 1 / 3 - 6,
                    child: CustomDropdownButton<PenaltyArgumentType>(
                      title: 'Type',
                      value: e.dataType,
                      items: PenaltyArgumentType.values,
                    ),
                  ),
                ],
              ),
            )),
        Row(
          children: [
            SizedBox(
              width: width * 2 / 3 - 6,
              child: CustomDropdownButton<Nodes>(
                title: 'Nodes to apply to the ${penalty.fcn.penaltyType}',
                value: penalty.nodes,
                items: Nodes.values,
                onSelected: (value) {}, // TODO
                isExpanded: false,
              ),
            ),
            if (penalty.runtimeType == Objective)
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.only(left: 12.0),
                  child: TextField(
                      onChanged: (value) {}, // TODO
                      decoration: const InputDecoration(
                          label: Text('Weigth'), border: OutlineInputBorder()),
                      inputFormatters: [
                        FilteringTextInputFormatter.allow(RegExp(r'[0-9\.]'))
                      ]),
                ),
              ),
          ],
        ),
        const SizedBox(height: 14),
      ],
    );
  }
}
