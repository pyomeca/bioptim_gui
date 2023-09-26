import 'package:bioptim_gui/models/acrobatics_ocp_controllers.dart';
import 'package:bioptim_gui/models/nodes.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/models/optimal_control_program_type.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:bioptim_gui/models/quadrature_rules.dart';
import 'package:bioptim_gui/widgets/animated_expanding_widget.dart';
import 'package:bioptim_gui/widgets/boolean_switch.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:bioptim_gui/widgets/maximize_minimize_radio.dart';
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
      {required double? weight,
      required Nodes? nodes,
      required QuadratureRules? quadratureRules,
      required bool? quadratic,
      required bool? expand,
      required String? target,
      required bool? derivative,
      required bool? explicitDerivative,
      required bool? multiThread,
      required Map<String, dynamic>? arguments}) {
    switch (fcn.runtimeType) {
      case LagrangeFcn:
        return Objective.lagrange(fcn as LagrangeFcn,
            weight: weight ?? 1,
            nodes: nodes ?? Nodes.all,
            quadratureRules:
                quadratureRules ?? QuadratureRules.defaultQuadraticRule,
            arguments: arguments ?? {});
      case MayerFcn:
        return Objective.mayer(fcn as MayerFcn,
            weight: weight ?? 1,
            nodes: nodes ?? Nodes.end,
            quadratureRules:
                quadratureRules ?? QuadratureRules.defaultQuadraticRule,
            arguments: arguments ?? {});
      case ConstraintFcn:
        return Constraint.generic(
            fcn: fcn as ConstraintFcn,
            nodes: nodes ?? Nodes.end,
            quadratureRules:
                quadratureRules ?? QuadratureRules.defaultQuadraticRule,
            arguments: arguments ?? {});
      default:
        throw 'Wrong penalty type';
    }
  }

  PenaltyInterface get _getPenaltyInterface {
    switch (OptimalControlProgramControllers.instance.ocpType) {
      case OptimalControlProgramType.ocp:
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
      case OptimalControlProgramType.abrobaticsOCP:
        switch (penaltyType) {
          case ObjectiveFcn:
            return AcrobaticsOCPControllers.instance
                .objectives(somersaultIndex: phaseIndex);
          case ConstraintFcn:
            return AcrobaticsOCPControllers.instance
                .constraints(somersaultIndex: phaseIndex);
          default:
            throw 'Wrong penalty type';
        }
      default:
        throw 'Wrong OCP type';
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
                  penaltyFactory: (fcn,
                      {arguments,
                      derivative,
                      expand,
                      target,
                      explicitDerivative,
                      multiThread,
                      nodes,
                      quadratic,
                      quadratureRules,
                      weight}) {
                    return _penaltyFactory(
                      fcn,
                      arguments: arguments,
                      derivative: derivative,
                      expand: expand,
                      explicitDerivative: explicitDerivative,
                      multiThread: multiThread,
                      nodes: nodes,
                      quadratic: quadratic,
                      quadratureRules: quadratureRules,
                      target: target,
                      weight: weight,
                    );
                  },
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
      required QuadratureRules? quadratureRules,
      required bool? quadratic,
      required bool? expand,
      required String? target,
      required bool? derivative,
      required bool? explicitDerivative,
      required bool? multiThread,
      required double? weight}) penaltyFactory;
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
                      weight: null,
                      nodes: null,
                      quadratureRules: null,
                      derivative: null,
                      expand: null,
                      quadratic: null,
                      explicitDerivative: null,
                      multiThread: null,
                      target: null,
                      arguments: null),
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
                    width: width,
                    child: TextField(
                        controller: penaltyInterface.argumentController(
                            penaltyIndex: penaltyIndex, argumentIndex: index),
                        decoration: InputDecoration(
                            label: Text(
                                'Argument: ${arguments[index].name} (${arguments[index].dataType.toString()})'),
                            border: const OutlineInputBorder()),
                        inputFormatters: [
                          FilteringTextInputFormatter.allow(
                              arguments[index].dataType.regexpValidator)
                        ]),
                  ),
                ],
              ),
            )),
        Row(
          children: [
            SizedBox(
              width: width / 2 - 3,
              child: CustomDropdownButton<Nodes>(
                title: 'Nodes to apply',
                value: penalty.nodes,
                items: Nodes.values,
                onSelected: (value) {
                  if (value.toString() == penalty.nodes.toString()) return;

                  final weight = penalty.runtimeType == Objective
                      ? (penalty as Objective).weight
                      : null;
                  penaltyInterface.update(
                      penaltyFactory(
                        penalty.fcn,
                        weight: weight,
                        nodes: value,
                        quadratureRules: penalty.quadratureRules,
                        derivative: penalty.derivative,
                        quadratic: penalty.quadratic,
                        expand: penalty.expand,
                        explicitDerivative: penalty.explicitDerivative,
                        multiThread: penalty.multiThread,
                        target: penalty.target,
                        arguments: penalty.arguments,
                      ),
                      penaltyIndex: penaltyIndex);
                },
                isExpanded: false,
              ),
            ),
            if (penalty.runtimeType == Objective)
              SizedBox(
                width: width / 4 - 3,
                child: TextField(
                    controller: penaltyInterface.weightController!(
                        penaltyIndex: penaltyIndex),
                    decoration: const InputDecoration(
                        label: Text('Weight'), border: OutlineInputBorder()),
                    inputFormatters: [
                      FilteringTextInputFormatter.allow(RegExp(r'[0-9\.]'))
                    ]),
              ),
            SizedBox(
              width: width / 4 + 6,
              child: const MinMaxRadio(),
            )
          ],
        ),
        // const SizedBox(height: 12),
        // Row(
        //   children: [
        //     Expanded(
        //       child: TextField(
        //           controller: penaltyInterface.targetController!(
        //               penaltyIndex: penaltyIndex),
        //           decoration: const InputDecoration(
        //               label: Text('Target'), border: OutlineInputBorder()),
        //           inputFormatters: [
        //             FilteringTextInputFormatter.allow(RegExp(r'[0-9\.,]'))
        //           ]),
        //     ),
        //   ],
        // ),
        const SizedBox(height: 12),
        Row(
          children: [
            SizedBox(
              width: width * 2 / 3 - 6,
              child: CustomDropdownButton<QuadratureRules>(
                title: 'Integration rule',
                value: penalty.quadratureRules,
                items: QuadratureRules.values,
                onSelected: (value) {
                  if (value.toString() == penalty.quadratureRules.toString()) {
                    return;
                  }

                  final weight = penalty.runtimeType == Objective
                      ? (penalty as Objective).weight
                      : null;
                  penaltyInterface.update(
                      penaltyFactory(
                        penalty.fcn,
                        weight: weight,
                        nodes: penalty.nodes,
                        quadratureRules: value,
                        derivative: penalty.derivative,
                        quadratic: penalty.quadratic,
                        expand: penalty.expand,
                        explicitDerivative: penalty.explicitDerivative,
                        multiThread: penalty.multiThread,
                        target: penalty.target,
                        arguments: penalty.arguments,
                      ),
                      penaltyIndex: penaltyIndex);
                },
                isExpanded: false,
              ),
            ),
            const SizedBox(width: 12),
            BooleanSwitch(
              initialValue: true,
              customOnChanged: (value) {
                // penaltyInterface.update(
                //   penaltyFactory(
                //     penalty.fcn,
                //     weight: weight,
                //     nodes: penalty.nodes,
                //     quadratureRules: penalty.quadratureRules,
                //     derivative: penalty.derivative,
                //     quadratic: penalty.quadratic,
                //     expand: penalty.expand,
                //     explicitDerivative: penalty.explicitDerivative,
                //     multiThread: penalty.multiThread,
                //     target: penalty.target,
                //     arguments: penalty.arguments,
                //   ),
                //   penaltyIndex: penaltyIndex,
                // );
              },
              leftTextOn: 'Quadratic',
              leftTextOff: 'Quadratic',
              width: width / 3 - 6,
            ),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            BooleanSwitch(
              initialValue: true,
              customOnChanged: (value) {},
              leftTextOn: 'Expand',
              leftTextOff: 'Expand',
              width: width / 2 - 6,
            ),
            const SizedBox(width: 12),
            BooleanSwitch(
              initialValue: false,
              customOnChanged: (value) {
                // penaltyInterface.update(
                //   penaltyFactory(
                //     penalty.fcn,
                //     weight: weight,
                //     nodes: penalty.nodes,
                //     quadratureRules: penalty.quadratureRules,
                //     derivative: penalty.derivative,
                //     quadratic: penalty.quadratic,
                //     expand: penalty.expand,
                //     explicitDerivative: penalty.explicitDerivative,
                //     multiThread: penalty.multiThread,
                //     target: penalty.target,
                //     arguments: penalty.arguments,
                //   ),
                //   penaltyIndex: penaltyIndex,
                // );
              },
              leftTextOn: 'MultiThread',
              leftTextOff: 'MultiThread',
              width: width / 2 - 6,
            ),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            BooleanSwitch(
              initialValue: false,
              customOnChanged: (value) {},
              leftTextOn: 'Derivative',
              leftTextOff: 'Derivative',
              width: width / 2 - 6,
            ),
            const SizedBox(width: 12),
            BooleanSwitch(
                initialValue: false,
                customOnChanged: (value) {
                  // penaltyInterface.update(
                  //   penaltyFactory(
                  //     penalty.fcn,
                  //     weight: weight,
                  //     nodes: penalty.nodes,
                  //     quadratureRules: penalty.quadratureRules,
                  //     derivative: penalty.derivative,
                  //     quadratic: penalty.quadratic,
                  //     expand: penalty.expand,
                  //     explicitDerivative: penalty.explicitDerivative,
                  //     multiThread: penalty.multiThread,
                  //     target: penalty.target,
                  //     arguments: penalty.arguments,
                  //   ),
                  //   penaltyIndex: penaltyIndex,
                  // );
                },
                leftTextOn: 'Explicit derivative',
                leftTextOff: 'Explicit derivative',
                width: width * 1 / 2 - 6),
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
