import 'dart:convert';

import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/models/optimization_variable.dart';
import 'package:bioptim_gui/models/python_interface.dart';
import 'package:bioptim_gui/widgets/bio_model_chooser.dart';
import 'package:bioptim_gui/widgets/console_out.dart';
import 'package:bioptim_gui/widgets/dynamics_chooser.dart';
import 'package:bioptim_gui/widgets/number_of_phases_chooser.dart';
import 'package:bioptim_gui/widgets/optimal_control_program_type_chooser.dart';
import 'package:bioptim_gui/widgets/optimization_variable_chooser.dart';
import 'package:bioptim_gui/widgets/phase_information.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart';

class MainPage extends StatefulWidget {
  const MainPage({super.key, this.columnWidth = 400.0});

  final double columnWidth;

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  String? _scriptPath;
  int _phaseIndex = 0;

  Stream<String>? _output;
  Stream<String>? _outputError;
  final _scrollController = ScrollController();
  late final _ocpControllers =
      OptimalControlProgramControllers(hasChanged: () => setState(() {}));

  @override
  void dispose() {
    _scrollController.dispose();
    _ocpControllers.dispose();
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    PythonInterface.instance.registerToStatusChanged((status) {
      setState(() {});
    });
    PythonInterface.instance.initialize(environment: 'bioptim_gui');

    // TODO remove this prefilling, which is only for debug purpose
    // _currentOcp.addVariable(
    //     OptimizationVariable(
    //       name: 'q',
    //       bounds: Bound(
    //         nbElements: 2,
    //         interpolation: Interpolation.constantWithFirstAndLastDifferent,
    //       ),
    //       initialGuess: InitialGuess(
    //           nbElements: 2, interpolation: Interpolation.constant),
    //     ),
    //     from: OptimizationVariableType.state,
    //     phaseIndex: 0);
    // _currentOcp.addVariable(
    //     OptimizationVariable(
    //       name: 'qdot',
    //       bounds: Bound(
    //         nbElements: 2,
    //         interpolation: Interpolation.constantWithFirstAndLastDifferent,
    //       ),
    //       initialGuess: InitialGuess(
    //           nbElements: 2, interpolation: Interpolation.constant),
    //     ),
    //     from: OptimizationVariableType.state,
    //     phaseIndex: 0);
    // _currentOcp.fillBound('q',
    //     min: [0, -2, 0, 0, -2 * pi, pi],
    //     max: [0, 2, 0, 0, 2 * pi, pi],
    //     from: OptimizationVariableType.state,
    //     phaseIndex: 0);
    // _currentOcp.fillBound('qdot',
    //     min: [0, -10, 0, 0, -10 * pi, 0],
    //     max: [0, 10, 0, 0, 10 * pi, 0],
    //     from: OptimizationVariableType.state,
    //     phaseIndex: 0);

    // _currentOcp.addVariable(
    //     OptimizationVariable(
    //       name: 'tau',
    //       bounds: Bound(nbElements: 2, interpolation: Interpolation.constant),
    //       initialGuess: InitialGuess(
    //           nbElements: 2, interpolation: Interpolation.constant),
    //     ),
    //     from: OptimizationVariableType.control,
    //     phaseIndex: 0);
    // _currentOcp.fillBound('tau',
    //     min: [-100, 0],
    //     max: [100, 0],
    //     from: OptimizationVariableType.control,
    //     phaseIndex: 0);

    // _ocpControllers.ocp.addObjective(
    //     Objective(LagrangeFcn.minimizeControls, arguments: {'key': 'tau'}));
  }

  // Phases index is probably not useful anymore as it should be shown columnwise
  void _onSelectPhase(value) => setState(() => _phaseIndex = value);

  void _onExportFile() async {
    _scriptPath = await FilePicker.platform.saveFile(
      allowedExtensions: ['py'],
      type: FileType.custom,
    );
    if (_scriptPath == null) return;

    _ocpControllers.exportScript(_scriptPath!);
    setState(() {});
  }

  void _onRunScript() async {
    final process = await PythonInterface.instance.runFile(_scriptPath!);
    if (process == null) return;

    setState(() {
      _output = process.stdout.transform(utf8.decoder);
      _outputError = process.stderr.transform(utf8.decoder);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Bioptim code generator'),
      ),
      body: RawScrollbar(
        controller: _scrollController,
        thumbVisibility: true,
        thumbColor: Theme.of(context).colorScheme.secondary,
        thickness: 8,
        radius: const Radius.circular(25),
        child: SingleChildScrollView(
          controller: _scrollController,
          child: Center(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                SizedBox(
                  width: widget.columnWidth,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const SizedBox(height: 12),
                      OptimalControlProgramTypeChooser(
                          controllers: _ocpControllers),
                      const SizedBox(height: 12),
                      NumberOfPhasesChooser(
                        controllers: _ocpControllers,
                        width: widget.columnWidth,
                      ),
                      const SizedBox(height: 12),
                      _buildPhase(phaseIndex: _phaseIndex),
                      const SizedBox(height: 12),
                      Center(child: _buildExportOrRunScriptButton()),
                    ],
                  ),
                ),
                _buildOutputScreens(),
                const SizedBox(height: 50),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildPhase({required int phaseIndex}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Information on the phase',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 12),
        BioModelChooser(controllers: _ocpControllers, phaseIndex: phaseIndex),
        const SizedBox(height: 12),
        // TODO Removed the combobox for showing the phases and replace by columns
        PhaseInformation(
          controllers: _ocpControllers,
          phaseIndex: phaseIndex,
          width: widget.columnWidth,
        ),
        const SizedBox(height: 12),
        DynamicsChooser(
          controllers: _ocpControllers,
          phaseIndex: phaseIndex,
          width: widget.columnWidth,
        ),
        const SizedBox(height: 12),
        const Divider(),
        _buildVariableType(
            from: OptimizationVariableType.state, phaseIndex: phaseIndex),
        const SizedBox(height: 12),
        const Divider(),
        _buildVariableType(
            from: OptimizationVariableType.control, phaseIndex: phaseIndex),
      ],
    );
  }

  Widget _buildVariableType(
      {required OptimizationVariableType from, required int phaseIndex}) {
    final variables =
        _ocpControllers.getVariableMap(from: from, phaseIndex: phaseIndex);

    late List<Map<String, VariableTextEditingControllers>> controllers;
    switch (from) {
      case OptimizationVariableType.state:
        controllers = _ocpControllers.states;
      case OptimizationVariableType.control:
        controllers = _ocpControllers.controls;
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '${from.name} variables',
          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
        // TODO Add foldable so it takes less space
        ...variables.names.map((name) {
          return Padding(
            padding: const EdgeInsets.only(bottom: 24.0),
            child: SizedBox(
              width: widget.columnWidth,
              child: OptimizationVariableChooser(
                controllers: controllers[phaseIndex][name]!,
                variable: variables[name],
                isMandatory: true,
                width: widget.columnWidth,
              ),
            ),
          );
        }),
      ],
    );
  }

  Widget _buildOutputScreens() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        if (_output != null)
          Padding(
            padding: const EdgeInsets.only(top: 12.0),
            child: ConsoleOut(output: _output!),
          ),
        if (_outputError != null)
          Padding(
            padding: const EdgeInsets.only(top: 12.0),
            child: ConsoleOut(output: _outputError!, textColor: Colors.red),
          ),
      ],
    );
  }

  Widget _buildExportOrRunScriptButton() {
    if (_ocpControllers.mustExport || _scriptPath == null) {
      return ElevatedButton(
          onPressed: _onExportFile, child: const Text('Export script'));
    }

    final status = PythonInterface.instance.status;

    final scriptName = basename(_scriptPath!);
    switch (status) {
      case PythonInterfaceStatus.uninitialized:
      case PythonInterfaceStatus.initializing:
        return Tooltip(
          message: 'Waiting for python to be ready.\n'
              'This can take some time if it is the first time.',
          child:
              ElevatedButton(onPressed: null, child: Text('Run $scriptName')),
        );

      case PythonInterfaceStatus.failedAlreadyInitializing:
      case PythonInterfaceStatus.failedCreatingEnvironment:
      case PythonInterfaceStatus.failedInstallingBioptim:
      case PythonInterfaceStatus.failedMissingAnaconda:
      case PythonInterfaceStatus.failedUnknown:
        return Tooltip(
          message: 'Failed to load python.',
          child:
              ElevatedButton(onPressed: null, child: Text('Run $scriptName')),
        );
      case PythonInterfaceStatus.ready:
        return Tooltip(
          message: 'Run the prepared program.',
          child: ElevatedButton(
              onPressed: _onRunScript, child: Text('Run $scriptName')),
        );
      case PythonInterfaceStatus.isRunning:
        return Tooltip(
          message: 'Currently optimizing, please wait until it is finished.',
          child: ElevatedButton(
              onPressed: null, child: Text('Running $scriptName')),
        );
    }
  }
}
