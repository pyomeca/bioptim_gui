import 'package:bioptim_gui/models/nodes.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
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

  String _penaltyTypeToString({required bool plural}) {
    switch (penaltyType) {
      case ObjectiveFcn:
        return plural ? 'Objective functions' : 'Objective function';
      case ConstraintFcn:
        return plural ? 'Constraints' : 'Constraint';
      default:
        throw 'Wrong penalty type';
    }
  }

  Penalty _penaltyFactory(PenaltyFcn fcn,
      {required double? weigth,
      required Nodes? nodes,
      required Map<String, dynamic>? arguments}) {
    switch (fcn.runtimeType) {
      case LagrangeFcn:
        return Objective.lagrange(fcn as LagrangeFcn,
            weight: weigth ?? 1,
            nodes: nodes ?? Nodes.all,
            arguments: arguments ?? {});
      case MayerFcn:
        return Objective.mayer(fcn as MayerFcn,
            weight: weigth ?? 1,
            nodes: nodes ?? Nodes.end,
            arguments: arguments ?? {});
      case ConstraintFcn:
        return Constraint.generic(
            fcn: fcn as ConstraintFcn,
            nodes: nodes ?? Nodes.end,
            arguments: arguments ?? {});
      default:
        throw 'Wrong penalty type';
    }
  }

  PenaltyInterface get _getPenaltyInterface {
    switch (penaltyType) {
      case ObjectiveFcn:
        return OptimalControlProgramControllers.instance
            .objectives(phaseIndex: phaseIndex);
      case ConstraintFcn:
        return OptimalControlProgramControllers.instance
            .constraints(phaseIndex: phaseIndex);
      default:
        throw 'Wrong penalty type';
    }
  }

  void _createPenalties() {
    _getPenaltyInterface.create();
  }

  @override
  Widget build(BuildContext context) {
    final penalties = _getPenaltyInterface.fetchAll();

    return AnimatedExpandingWidget(
      header: SizedBox(
        width: width,
        height: 50,
        child: Align(
          alignment: Alignment.centerLeft,
          child: Text(
            _penaltyTypeToString(plural: true),
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Align(
            alignment: Alignment.centerRight,
            child: _buildAddButton(
                _penaltyTypeToString(plural: false).toLowerCase()),
          ),
          const SizedBox(height: 24),
          ...penalties.asMap().keys.map((index) => Padding(
                padding: const EdgeInsets.only(bottom: 24.0),
                child: _PathTile(
                  key: ObjectKey(penalties[index]),
                  penaltyFactory: _penaltyFactory,
                  penaltyInterface: _getPenaltyInterface,
                  penaltyIndex: index,
                  width: width,
                ),
              )),
          const SizedBox(height: 26),
        ],
      ),
    );
  }

  Padding _buildAddButton(String name) {
    return Padding(
      padding: const EdgeInsets.only(right: 18.0, top: 12.0),
      child: InkWell(
        onTap: _createPenalties,
        child: Container(
            padding:
                const EdgeInsets.only(left: 12, right: 4, top: 2, bottom: 2),
            decoration: BoxDecoration(
                color: Colors.green, borderRadius: BorderRadius.circular(25)),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  'New $name',
                  style: const TextStyle(color: Colors.white),
                ),
                const Icon(
                  Icons.add,
                  color: Colors.white,
                ),
              ],
            )),
      ),
    );
  }
}

class _PathTile extends StatelessWidget {
  const _PathTile({
    required super.key,
    required this.penaltyFactory,
    required this.penaltyInterface,
    required this.penaltyIndex,
    required this.width,
  });

  final Function(PenaltyFcn fcn,
      {required Map<String, dynamic>? arguments,
      required Nodes? nodes,
      required double? weigth}) penaltyFactory;
  final PenaltyInterface penaltyInterface;
  final int penaltyIndex;
  final double width;

  @override
  Widget build(BuildContext context) {
    final penalty = penaltyInterface.fetch(penaltyIndex: penaltyIndex);
    final arguments = penalty.fcn.mandatoryArguments;

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
            onSelected: (value) {
              if (value.toString() == penalty.fcn.toString()) return;

              // Update to a brand new fresh penalty
              penaltyInterface.update(
                  penaltyFactory(value,
                      weigth: null, nodes: null, arguments: null),
                  penaltyIndex: penaltyIndex);
            },
            isExpanded: false,
          ),
        ),
        const SizedBox(height: 12),
        ...arguments.asMap().keys.map((index) => Padding(
              padding: const EdgeInsets.only(bottom: 12.0),
              child: Row(
                children: [
                  SizedBox(
                    width: width * 2 / 3 - 6,
                    child: TextField(
                        controller: penaltyInterface.argumentController(
                            penaltyIndex: penaltyIndex, argumentIndex: index),
                        decoration: InputDecoration(
                            label: Text('Argument: ${arguments[index].name}'),
                            border: const OutlineInputBorder()),
                        inputFormatters: [
                          FilteringTextInputFormatter.allow(
                              arguments[index].dataType.regexpValidator)
                        ]),
                  ),
                  const SizedBox(width: 12),
                  SizedBox(
                    width: width * 1 / 3 - 6,
                    child: CustomDropdownButton<PenaltyArgumentType>(
                      title: 'Type',
                      value: arguments[index].dataType,
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
                onSelected: (value) {
                  if (value.toString() == penalty.nodes.toString()) return;

                  final weight = penalty.runtimeType == Objective
                      ? (penalty as Objective).weight
                      : null;
                  penaltyInterface.update(
                      penaltyFactory(penalty.fcn,
                          weigth: weight,
                          nodes: value,
                          arguments: penalty.arguments),
                      penaltyIndex: penaltyIndex);
                },
                isExpanded: false,
              ),
            ),
            if (penalty.runtimeType == Objective)
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.only(left: 12.0),
                  child: TextField(
                      controller: penaltyInterface.weightController!(
                          penaltyIndex: penaltyIndex),
                      decoration: const InputDecoration(
                          label: Text('Weight'), border: OutlineInputBorder()),
                      inputFormatters: [
                        FilteringTextInputFormatter.allow(RegExp(r'[0-9\.]'))
                      ]),
                ),
              ),
          ],
        ),
        Align(
          alignment: Alignment.centerRight,
          child: InkWell(
            onTap: () {
              penaltyInterface.remove(penaltyIndex: penaltyIndex);
            },
            borderRadius: BorderRadius.circular(25),
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    'Remove ${penalty.fcn.penaltyType.toLowerCase()}',
                    style: const TextStyle(color: Colors.red),
                  ),
                  const SizedBox(width: 8),
                  const Icon(
                    Icons.delete,
                    color: Colors.red,
                  ),
                ],
              ),
            ),
          ),
        ),
        const SizedBox(height: 14),
      ],
    );
  }
}
