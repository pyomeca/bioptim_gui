import 'package:bioptim_gui/models/acrobatics_ocp_controllers.dart';
import 'package:bioptim_gui/models/objective_type.dart';
import 'package:bioptim_gui/models/minimize_maximize.dart';
import 'package:bioptim_gui/models/nodes.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/models/optimal_control_program_type.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:bioptim_gui/models/quadrature_rules.dart';
import 'package:bioptim_gui/widgets/animated_expanding_widget.dart';
import 'package:bioptim_gui/widgets/boolean_switch.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:bioptim_gui/widgets/maximize_minimize_radio.dart';
import 'package:bioptim_gui/widgets/objective_type_radio.dart';
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
    required ObjectiveType? objectiveType,
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
          objectiveType: objectiveType ?? ObjectiveType.mayer,
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
          objectiveType: objectiveType ?? ObjectiveType.mayer,
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
                    objectiveType,
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
                      objectiveType: objectiveType,
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
    required ObjectiveType? objectiveType,
    required GenericFcn? genericFcn,
  }) penaltyFactory;

  ///
  /// This function is used to create a new penalty with the same arguments as the previous one
  /// except the ones that are not null in the parameters
  /// This is used to update the penalty when the user changes the penalty type
  Penalty _penaltyFactoryPartial(
    Penalty penalty,
    PenaltyFcn fcn, {
    double? weight,
    MinMax? minimizeOrMaximize,
    ObjectiveType? objectiveType,
    GenericFcn? genericFcn,
    Nodes? nodes,
    QuadratureRules? quadratureRules,
    bool? quadratic,
    bool? expand,
    String? target,
    bool? derivative,
    bool? multiThread,
    Map<String, dynamic>? arguments,
  }) {
    final objective =
        penalty.runtimeType == Objective ? (penalty as Objective) : null;

    fcn = fcn;
    weight = weight ?? objective?.weight;
    minimizeOrMaximize = minimizeOrMaximize ?? objective?.minimizeOrMaximize;
    objectiveType = objectiveType ?? objective?.objectiveType;
    genericFcn = genericFcn ?? objective?.genericFcn;
    nodes = nodes ?? penalty.nodes;
    quadratureRules = quadratureRules ?? penalty.quadratureRules;
    quadratic = quadratic ?? penalty.quadratic;
    expand = expand ?? penalty.expand;
    target = target ?? penalty.target;
    derivative = derivative ?? penalty.derivative;
    multiThread = multiThread ?? penalty.multiThread;
    arguments = arguments ?? penalty.arguments;

    switch (fcn.runtimeType) {
      case LagrangeFcn:
        return penaltyFactory(
          fcn,
          weight: weight,
          minimizeOrMaximize: minimizeOrMaximize,
          objectiveType: objectiveType,
          genericFcn: genericFcn,
          nodes: nodes,
          quadratureRules: quadratureRules,
          quadratic: quadratic,
          expand: expand,
          target: target,
          derivative: derivative,
          multiThread: multiThread,
          arguments: arguments,
        );
      case MayerFcn:
        return penaltyFactory(
          fcn,
          weight: weight,
          minimizeOrMaximize: minimizeOrMaximize,
          objectiveType: objectiveType,
          genericFcn: genericFcn,
          nodes: nodes,
          quadratureRules: quadratureRules,
          quadratic: quadratic,
          expand: expand,
          target: target,
          derivative: derivative,
          multiThread: multiThread,
          arguments: arguments,
        );
      case ConstraintFcn:
        return penaltyFactory(
          fcn,
          weight: weight,
          minimizeOrMaximize: minimizeOrMaximize,
          objectiveType: objectiveType,
          genericFcn: genericFcn,
          nodes: nodes,
          quadratureRules: quadratureRules,
          quadratic: quadratic,
          expand: expand,
          target: target,
          derivative: derivative,
          multiThread: multiThread,
          arguments: arguments,
        );
      default:
        throw 'Wrong penalty type';
    }
  }

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
                  var objectiveType = (penalty as Objective).objectiveType;

                  var newFcn = genericFcn2ObjectiveFcn(
                      value as GenericFcn, objectiveType);

                  if (newFcn == null) {
                    objectiveType = (objectiveType == ObjectiveType.mayer)
                        ? ObjectiveType.lagrange
                        : ObjectiveType.mayer;

                    newFcn = genericFcn2ObjectiveFcn(
                      value,
                      objectiveType,
                    );
                  }

                  // Update to a brand new fresh penalty
                  penaltyInterface.update(
                      penaltyFactory(
                        newFcn as PenaltyFcn,
                        weight: null,
                        minimizeOrMaximize: null,
                        objectiveType: objectiveType,
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
                        objectiveType: null,
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
            ),
          ),
          if (penalty.runtimeType == Objective)
            SizedBox(
              width: width * 0.13,
              child: ObjectiveTypeRadio(
                value: (penalty as Objective).objectiveType,
                customOnChanged: (value) {
                  if (value == penalty.objectiveType) return;

                  var newFcn = genericFcn2ObjectiveFcn(
                    objectiveFcn2GenericFcn(
                        penalty.fcn as ObjectiveFcn)!, // always exists
                    value!,
                  );

                  if (newFcn == null) {
                    newFcn = penalty.fcn as ObjectiveFcn?;
                    value = penalty.objectiveType;
                  }

                  penaltyInterface.update(
                      penaltyFactory(
                        newFcn as PenaltyFcn,
                        weight: null,
                        minimizeOrMaximize: null,
                        objectiveType: value,
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

                  penaltyInterface.update(
                      _penaltyFactoryPartial(
                        penalty,
                        penalty.fcn,
                        nodes: value,
                      ),
                      penaltyIndex: penaltyIndex);
                },
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
                            _penaltyFactoryPartial(
                              penalty,
                              penalty.fcn,
                              minimizeOrMaximize: value,
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
            (penalty as Objective).objectiveType != ObjectiveType.mayer)
          const SizedBox(height: 12),
        if (penalty.runtimeType != Objective ||
            (penalty as Objective).objectiveType != ObjectiveType.mayer)
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

                    penaltyInterface.update(
                        _penaltyFactoryPartial(
                          penalty,
                          penalty.fcn,
                          quadratureRules: value,
                        ),
                        penaltyIndex: penaltyIndex);
                  },
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

                penaltyInterface.update(
                    _penaltyFactoryPartial(
                      penalty,
                      penalty.fcn,
                      quadratic: value,
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

                penaltyInterface.update(
                    _penaltyFactoryPartial(
                      penalty,
                      penalty.fcn,
                      expand: value,
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

                penaltyInterface.update(
                    _penaltyFactoryPartial(
                      penalty,
                      penalty.fcn,
                      multiThread: value,
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

                penaltyInterface.update(
                    _penaltyFactoryPartial(
                      penalty,
                      penalty.fcn,
                      derivative: value,
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
