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
import 'package:bioptim_gui/widgets/mayer_lagrande_radio.dart';
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

  Penalty _penaltyFactory(
    PenaltyFcn fcn, {
    required double? weight,
    required MinMax? minimizeOrMaximize,
    required MayerLagrange? mayerOrLagrange,
    required GenericFcn? genericFcn,
    required Nodes? nodes,
    required QuadratureRules? quadratureRules,
    required bool? quadratic,
    required bool? expand,
    required String? target,
    required bool? derivative,
    required bool? multiThread,
    required Map<String, dynamic>? arguments,
  }) {
    switch (fcn.runtimeType) {
      case LagrangeFcn:
        return Objective.lagrange(
          fcn as LagrangeFcn,
          weight: weight ?? 1,
          minimizeOrMaximize: minimizeOrMaximize ?? MinMax.minimize,
          mayerOrLagrange: mayerOrLagrange ?? MayerLagrange.mayer,
          genericFcn: genericFcn ?? GenericFcn.minimizeControls,
          nodes: nodes ?? Nodes.all,
          quadratureRules:
              quadratureRules ?? QuadratureRules.defaultQuadraticRule,
          quadratic: quadratic ?? true,
          expand: expand ?? true,
          target: target ?? 'None',
          derivative: derivative ?? false,
          multiThread: multiThread ?? false,
          arguments: arguments ?? {},
        );
      case MayerFcn:
        return Objective.mayer(
          fcn as MayerFcn,
          weight: weight ?? 1,
          minimizeOrMaximize: minimizeOrMaximize ?? MinMax.minimize,
          mayerOrLagrange: mayerOrLagrange ?? MayerLagrange.mayer,
          genericFcn: genericFcn ?? GenericFcn.minimizeControls,
          nodes: nodes ?? Nodes.end,
          quadratureRules:
              quadratureRules ?? QuadratureRules.defaultQuadraticRule,
          quadratic: quadratic ?? true,
          expand: expand ?? true,
          target: target ?? 'None',
          derivative: derivative ?? false,
          multiThread: multiThread ?? false,
          arguments: arguments ?? {},
        );
      case ConstraintFcn:
        return Constraint.generic(
          fcn: fcn as ConstraintFcn,
          nodes: nodes ?? Nodes.end,
          quadratureRules:
              quadratureRules ?? QuadratureRules.defaultQuadraticRule,
          quadratic: quadratic ?? true,
          expand: expand ?? true,
          target: target ?? 'None',
          derivative: derivative ?? false,
          multiThread: multiThread ?? false,
          arguments: arguments ?? {},
        );
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
                  penaltyFactory: (
                    fcn, {
                    arguments,
                    derivative,
                    expand,
                    target,
                    multiThread,
                    nodes,
                    quadratic,
                    quadratureRules,
                    weight,
                    minimizeOrMaximize,
                    mayerOrLagrange,
                    genericFcn,
                  }) {
                    return _penaltyFactory(
                      fcn,
                      arguments: arguments,
                      derivative: derivative,
                      expand: expand,
                      multiThread: multiThread,
                      nodes: nodes,
                      quadratic: quadratic,
                      quadratureRules: quadratureRules,
                      target: target,
                      weight: weight,
                      minimizeOrMaximize: minimizeOrMaximize,
                      mayerOrLagrange: mayerOrLagrange,
                      genericFcn: genericFcn,
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

  final Function(
    PenaltyFcn fcn, {
    required Map<String, dynamic>? arguments,
    required Nodes? nodes,
    required QuadratureRules? quadratureRules,
    required bool? quadratic,
    required bool? expand,
    required String? target,
    required bool? derivative,
    required bool? multiThread,
    required double? weight,
    required MinMax? minimizeOrMaximize,
    required MayerLagrange? mayerOrLagrange,
    required GenericFcn? genericFcn,
  }) penaltyFactory;
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
        Row(children: [
          SizedBox(
            width: (penalty.runtimeType == Objective)
                ? width *
                    0.87 // can't get it smaller because of the dropdown's text
                : width,
            child: CustomDropdownButton<PenaltyFcn>(
              title:
                  '${penalty.fcn.penaltyType} ${penaltyIndex + 1} (${penalty.fcn.penaltyTypeToString})',
              value: (penalty.runtimeType == Objective)
                  ? (penalty as Objective).genericFcn
                  : penalty.fcn,
              items: (penalty.runtimeType == Objective)
                  ? GenericFcn.values
                  : penalty.fcn.fcnValues,
              onSelected: (value) {
                if (value == penalty.fcn) return;

                if (penalty.runtimeType == Objective) {
                  var mayerOrLagrange = (penalty as Objective).mayerOrLagrange;

                  var newFcn = getObjectiveCorrepondance(
                      value as GenericFcn, mayerOrLagrange);

                  if (newFcn == null) {
                    // Mayer/Lagrange does not exist for this specific objective

                    // give the other type of objective
                    // (Mayer if Lagrange does not exist
                    // or Lagrange if Mayer does not exist)
                    // example: if Mayer.MINIMIZE_EXIST does not exist
                    // then give Lagrange.MINIMIZE_EXIST that exists
                    mayerOrLagrange = (mayerOrLagrange == MayerLagrange.mayer)
                        ? MayerLagrange.lagrange
                        : MayerLagrange.mayer;

                    newFcn = getObjectiveCorrepondance(
                      value,
                      mayerOrLagrange,
                    );
                  }

                  // Update to a brand new fresh penalty
                  penaltyInterface.update(
                      penaltyFactory(
                        newFcn as PenaltyFcn,
                        weight: null,
                        minimizeOrMaximize: null,
                        mayerOrLagrange: mayerOrLagrange,
                        genericFcn: value,
                        nodes: null,
                        quadratureRules: null,
                        derivative: null,
                        expand: null,
                        quadratic: null,
                        multiThread: null,
                        target: null,
                        arguments: null,
                      ),
                      penaltyIndex: penaltyIndex);
                } else {
                  penaltyInterface.update(
                      penaltyFactory(
                        value,
                        weight: null,
                        minimizeOrMaximize: null,
                        mayerOrLagrange: null,
                        genericFcn: null,
                        nodes: null,
                        quadratureRules: null,
                        derivative: null,
                        expand: null,
                        quadratic: null,
                        multiThread: null,
                        target: null,
                        arguments: null,
                      ),
                      penaltyIndex: penaltyIndex);
                }
              },
              isExpanded: false,
            ),
          ),
          if (penalty.runtimeType == Objective)
            SizedBox(
              width: width * 0.13,
              child: MayerLagrangeRadio(
                value: (penalty as Objective).mayerOrLagrange,
                customOnChanged: (value) {
                  if (value == penalty.mayerOrLagrange) return;

                  var newFcn = getObjectiveCorrepondance(
                    mayerLagrange2GenricFcn(
                        penalty.fcn as ObjectiveFcn)!, // always exists
                    value!,
                  );

                  if (newFcn == null) {
                    newFcn = penalty.fcn as ObjectiveFcn?;
                    value = penalty.mayerOrLagrange;
                  }

                  penaltyInterface.update(
                      penaltyFactory(
                        newFcn as PenaltyFcn,
                        weight: null,
                        minimizeOrMaximize: null,
                        mayerOrLagrange: value,
                        genericFcn: penalty.genericFcn,
                        nodes: null,
                        quadratureRules: null,
                        derivative: null,
                        quadratic: null,
                        expand: null,
                        multiThread: null,
                        target: null,
                        arguments: null,
                      ),
                      penaltyIndex: penaltyIndex);
                },
              ),
            ),
        ]),
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
              width: (penalty.runtimeType == Objective) ? width / 2 - 3 : width,
              child: CustomDropdownButton<Nodes>(
                title: 'Nodes to apply',
                value: penalty.nodes,
                items: Nodes.values,
                onSelected: (value) {
                  if (value == penalty.nodes) return;

                  final weight = penalty.runtimeType == Objective
                      ? (penalty as Objective).weight
                      : null;

                  final minimizeOrMaximize = penalty.runtimeType == Objective
                      ? (penalty as Objective).minimizeOrMaximize
                      : null;

                  final mayerOrLagrange = penalty.runtimeType == Objective
                      ? (penalty as Objective).mayerOrLagrange
                      : null;

                  final genericFcn = penalty.runtimeType == Objective
                      ? (penalty as Objective).genericFcn
                      : null;

                  penaltyInterface.update(
                      penaltyFactory(
                        penalty.fcn,
                        weight: weight,
                        minimizeOrMaximize: minimizeOrMaximize,
                        mayerOrLagrange: mayerOrLagrange,
                        genericFcn: genericFcn,
                        nodes: value,
                        quadratureRules: penalty.quadratureRules,
                        derivative: penalty.derivative,
                        quadratic: penalty.quadratic,
                        expand: penalty.expand,
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
            if (penalty.runtimeType == Objective)
              SizedBox(
                  width: width / 4 + 6,
                  child: MinMaxRadio(
                      value: (penalty as Objective).minimizeOrMaximize,
                      customOnChanged: (value) {
                        if (value == penalty.minimizeOrMaximize) return;

                        penaltyInterface.update(
                            penaltyFactory(
                              penalty.fcn,
                              weight: penalty.weight,
                              minimizeOrMaximize: value,
                              mayerOrLagrange: penalty.mayerOrLagrange,
                              genericFcn: penalty.genericFcn,
                              nodes: penalty.nodes,
                              quadratureRules: penalty.quadratureRules,
                              derivative: penalty.derivative,
                              quadratic: penalty.quadratic,
                              expand: penalty.expand,
                              multiThread: penalty.multiThread,
                              target: penalty.target,
                              arguments: penalty.arguments,
                            ),
                            penaltyIndex: penaltyIndex);
                      })),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: TextField(
                  controller: penaltyInterface.targetController(
                      penaltyIndex: penaltyIndex),
                  decoration: const InputDecoration(
                      label: Text('Target'), border: OutlineInputBorder()),
                  inputFormatters: [
                    FilteringTextInputFormatter.allow(RegExp(r'[0-9\.,]'))
                  ]),
            ),
          ],
        ),
        // Mayer objectives don't have integration_rule
        if (penalty.runtimeType != Objective ||
            (penalty as Objective).mayerOrLagrange != MayerLagrange.mayer)
          const SizedBox(height: 12),
        if (penalty.runtimeType != Objective ||
            (penalty as Objective).mayerOrLagrange != MayerLagrange.mayer)
          Row(
            children: [
              SizedBox(
                width: width,
                child: CustomDropdownButton<QuadratureRules>(
                  title: 'Integration rule',
                  value: penalty.quadratureRules,
                  items: QuadratureRules.values,
                  onSelected: (value) {
                    if (value == penalty.quadratureRules) return;

                    final weight = penalty.runtimeType == Objective
                        ? (penalty as Objective).weight
                        : null;
                    final minimizeOrMaximize = penalty.runtimeType == Objective
                        ? (penalty as Objective).minimizeOrMaximize
                        : null;
                    final mayerOrLagrange = penalty.runtimeType == Objective
                        ? (penalty as Objective).mayerOrLagrange
                        : null;
                    final genericFcn = penalty.runtimeType == Objective
                        ? (penalty as Objective).genericFcn
                        : null;

                    penaltyInterface.update(
                        penaltyFactory(
                          penalty.fcn,
                          weight: weight,
                          minimizeOrMaximize: minimizeOrMaximize,
                          mayerOrLagrange: mayerOrLagrange,
                          genericFcn: genericFcn,
                          nodes: penalty.nodes,
                          quadratureRules: value,
                          derivative: penalty.derivative,
                          quadratic: penalty.quadratic,
                          expand: penalty.expand,
                          multiThread: penalty.multiThread,
                          target: penalty.target,
                          arguments: penalty.arguments,
                        ),
                        penaltyIndex: penaltyIndex);
                  },
                  isExpanded: false,
                ),
              ),
            ],
          ),
        const SizedBox(height: 12),
        Row(
          children: [
            BooleanSwitch(
              initialValue: penalty.quadratic,
              customOnChanged: (value) {
                if (value == penalty.quadratic) return;

                final weight = penalty.runtimeType == Objective
                    ? (penalty as Objective).weight
                    : null;

                final minimizeOrMaximize = penalty.runtimeType == Objective
                    ? (penalty as Objective).minimizeOrMaximize
                    : null;

                final mayerOrLagrange = penalty.runtimeType == Objective
                    ? (penalty as Objective).mayerOrLagrange
                    : null;

                final genericFcn = penalty.runtimeType == Objective
                    ? (penalty as Objective).genericFcn
                    : null;

                penaltyInterface.update(
                    penaltyFactory(
                      penalty.fcn,
                      weight: weight,
                      minimizeOrMaximize: minimizeOrMaximize,
                      mayerOrLagrange: mayerOrLagrange,
                      genericFcn: genericFcn,
                      nodes: penalty.nodes,
                      quadratureRules: penalty.quadratureRules,
                      derivative: penalty.derivative,
                      quadratic: value,
                      expand: penalty.expand,
                      multiThread: penalty.multiThread,
                      target: penalty.target,
                      arguments: penalty.arguments,
                    ),
                    penaltyIndex: penaltyIndex);
              },
              leftText: 'Quadratic',
              width: width / 2 - 6,
            ),
            const SizedBox(width: 12),
            BooleanSwitch(
              initialValue: penalty.expand,
              customOnChanged: (value) {
                if (value == penalty.expand) return;

                final weight = penalty.runtimeType == Objective
                    ? (penalty as Objective).weight
                    : null;

                final minimizeOrMaximize = penalty.runtimeType == Objective
                    ? (penalty as Objective).minimizeOrMaximize
                    : null;

                final mayerOrLagrange = penalty.runtimeType == Objective
                    ? (penalty as Objective).mayerOrLagrange
                    : null;

                final genericFcn = penalty.runtimeType == Objective
                    ? (penalty as Objective).genericFcn
                    : null;

                penaltyInterface.update(
                    penaltyFactory(
                      penalty.fcn,
                      weight: weight,
                      minimizeOrMaximize: minimizeOrMaximize,
                      mayerOrLagrange: mayerOrLagrange,
                      genericFcn: genericFcn,
                      nodes: penalty.nodes,
                      quadratureRules: penalty.quadratureRules,
                      derivative: penalty.derivative,
                      quadratic: penalty.quadratic,
                      expand: value,
                      multiThread: penalty.multiThread,
                      target: penalty.target,
                      arguments: penalty.arguments,
                    ),
                    penaltyIndex: penaltyIndex);
              },
              leftText: 'Expand',
              width: width / 2 - 6,
            ),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            BooleanSwitch(
              initialValue: penalty.multiThread,
              customOnChanged: (value) {
                if (value == penalty.multiThread) return;

                final weight = penalty.runtimeType == Objective
                    ? (penalty as Objective).weight
                    : null;

                final minimizeOrMaximize = penalty.runtimeType == Objective
                    ? (penalty as Objective).minimizeOrMaximize
                    : null;

                final mayerOrLagrange = penalty.runtimeType == Objective
                    ? (penalty as Objective).mayerOrLagrange
                    : null;

                final genericFcn = penalty.runtimeType == Objective
                    ? (penalty as Objective).genericFcn
                    : null;

                penaltyInterface.update(
                    penaltyFactory(
                      penalty.fcn,
                      weight: weight,
                      minimizeOrMaximize: minimizeOrMaximize,
                      mayerOrLagrange: mayerOrLagrange,
                      genericFcn: genericFcn,
                      nodes: penalty.nodes,
                      quadratureRules: penalty.quadratureRules,
                      derivative: penalty.derivative,
                      quadratic: penalty.quadratic,
                      expand: penalty.expand,
                      multiThread: value,
                      target: penalty.target,
                      arguments: penalty.arguments,
                    ),
                    penaltyIndex: penaltyIndex);
              },
              leftText: 'MultiThread',
              width: width / 2 - 6,
            ),
            const SizedBox(width: 12),
            BooleanSwitch(
              initialValue: penalty.derivative,
              customOnChanged: (value) {
                if (value == penalty.derivative) return;

                final weight = penalty.runtimeType == Objective
                    ? (penalty as Objective).weight
                    : null;
                final minimizeOrMaximize = penalty.runtimeType == Objective
                    ? (penalty as Objective).minimizeOrMaximize
                    : null;

                final mayerOrLagrange = penalty.runtimeType == Objective
                    ? (penalty as Objective).mayerOrLagrange
                    : null;

                final genericFcn = penalty.runtimeType == Objective
                    ? (penalty as Objective).genericFcn
                    : null;

                penaltyInterface.update(
                    penaltyFactory(
                      penalty.fcn,
                      weight: weight,
                      minimizeOrMaximize: minimizeOrMaximize,
                      mayerOrLagrange: mayerOrLagrange,
                      genericFcn: genericFcn,
                      nodes: penalty.nodes,
                      quadratureRules: penalty.quadratureRules,
                      derivative: value,
                      quadratic: penalty.quadratic,
                      expand: penalty.expand,
                      multiThread: penalty.multiThread,
                      target: penalty.target,
                      arguments: penalty.arguments,
                    ),
                    penaltyIndex: penaltyIndex);
              },
              leftText: 'Derivative',
              width: width / 2 - 6,
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
