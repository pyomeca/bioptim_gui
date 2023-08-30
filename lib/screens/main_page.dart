import 'dart:convert';
import 'dart:math';

import 'package:bioptim_gui/models/bio_model.dart';
import 'package:bioptim_gui/models/optimal_control_program.dart';
import 'package:bioptim_gui/models/optimal_control_program_type.dart';
import 'package:bioptim_gui/models/optimization_variable.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:bioptim_gui/models/phase_text_editing_controllers.dart';
import 'package:bioptim_gui/models/python_interface.dart';
import 'package:bioptim_gui/widgets/bio_model_chooser.dart';
import 'package:bioptim_gui/widgets/console_out.dart';
import 'package:bioptim_gui/widgets/optimal_control_program_type_chooser.dart';
import 'package:bioptim_gui/widgets/phase_information.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart';

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  final _currentOcp = OptimalControlProgram();
  String? _scriptPath;

  Stream<String>? _output;
  Stream<String>? _outputError;
  final _scrollController = ScrollController();

  late final _phaseControllers = PhaseTextEditingControllers(
    getNbShootingPoints: _currentOcp.getNbShootingPoints,
    onChangedNbShootingPoints: _onSettingNbShootingPoints,
    getPhaseTime: _currentOcp.getPhaseTime,
    onChangedPhaseTime: _onSettingPhaseTime,
  );

  @override
  void dispose() {
    _scrollController.dispose();
    _phaseControllers.dispose();
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
    _currentOcp.addVariable(
        OptimizationVariable(
          name: 'q',
          bounds: Bound(
            nbElements: 2,
            interpolation: Interpolation.constantWithFirstAndLastDifferent,
          ),
          initialGuess: InitialGuess(
              nbElements: 2, interpolation: Interpolation.constant),
        ),
        from: OptimizationVariableType.state,
        phaseIndex: 0);
    _currentOcp.addVariable(
        OptimizationVariable(
          name: 'qdot',
          bounds: Bound(
            nbElements: 2,
            interpolation: Interpolation.constantWithFirstAndLastDifferent,
          ),
          initialGuess: InitialGuess(
              nbElements: 2, interpolation: Interpolation.constant),
        ),
        from: OptimizationVariableType.state,
        phaseIndex: 0);
    _currentOcp.fillBound('q',
        min: [0, -2, 0, 0, -2 * pi, pi],
        max: [0, 2, 0, 0, 2 * pi, pi],
        from: OptimizationVariableType.state,
        phaseIndex: 0);
    _currentOcp.fillBound('qdot',
        min: [0, -10, 0, 0, -10 * pi, 0],
        max: [0, 10, 0, 0, 10 * pi, 0],
        from: OptimizationVariableType.state,
        phaseIndex: 0);

    _currentOcp.addVariable(
        OptimizationVariable(
          name: 'tau',
          bounds: Bound(nbElements: 2, interpolation: Interpolation.constant),
          initialGuess: InitialGuess(
              nbElements: 2, interpolation: Interpolation.constant),
        ),
        from: OptimizationVariableType.control,
        phaseIndex: 0);
    _currentOcp.fillBound('tau',
        min: [-100, 0],
        max: [100, 0],
        from: OptimizationVariableType.control,
        phaseIndex: 0);

    _currentOcp.addObjective(
        Objective(LagrangeFcn.minimizeControls, arguments: {'key': 'tau'}));
  }

  void _onSelectedOcp(OptimalControlProgramType value) =>
      setState(() => _currentOcp.ocpType = value);

  void _onSelectedBioModel(BioModel value, {required int phaseIndex}) =>
      setState(() => _currentOcp.setBioModel(value, phaseIndex: phaseIndex));

  void _onSelectedModelPath(String value, {required int phaseIndex}) =>
      setState(() => _currentOcp.setModelPath(value, phaseIndex: phaseIndex));

  void _onSettingNbShootingPoints(int value, {required int phaseIndex}) =>
      setState(
          () => _currentOcp.setNbShootingPoints(value, phaseIndex: phaseIndex));

  void _onSettingPhaseTime(double value, {required int phaseIndex}) {
    debugPrint(value.toString());
    setState(() => _currentOcp.setPhaseTime(value, phaseIndex: phaseIndex));
  }

  void _onExportFile() async {
    _scriptPath = await FilePicker.platform.saveFile(
      allowedExtensions: ['py'],
      type: FileType.custom,
    );
    if (_scriptPath == null) return;

    _currentOcp.exportScript(_scriptPath!);
    setState(() {});
  }

  void _onRunScript() async {
    final python = PythonInterface.instance;
    // TODO Better fail if not ready (popup?)
    if (python.status != PythonInterfaceStatus.ready) return;

    final process = await python.runFile(_scriptPath!);
    if (process == null) return;

    setState(() {
      _output = process.stdout.transform(utf8.decoder);
      _outputError = process.stderr.transform(utf8.decoder);
    });
  }

  @override
  Widget build(BuildContext context) {
    const columnWidth = 400.0;

    // TODO Do a proper for loop
    const phaseIndex = 0;

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
                  width: columnWidth,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const SizedBox(height: 12),
                      OptimalControlProgramTypeChooser(
                        value: _currentOcp.ocpType,
                        onSelected: _onSelectedOcp,
                      ),
                      const SizedBox(height: 12),
                      BioModelChooser(
                        onSelectedBioModel: (value) =>
                            _onSelectedBioModel(value, phaseIndex: phaseIndex),
                        onSelectedModelPath: (value) =>
                            _onSelectedModelPath(value, phaseIndex: phaseIndex),
                        bioModel:
                            _currentOcp.getBioModel(phaseIndex: phaseIndex),
                        modelPath:
                            _currentOcp.getModelPath(phaseIndex: phaseIndex),
                      ),
                      const SizedBox(height: 12),
                      PhaseInformation(
                        columnWidth: columnWidth,
                        nbShootingPointController: _phaseControllers
                            .nbShootingPointsControllers[phaseIndex],
                        phaseTimeController:
                            _phaseControllers.phaseTimeControllers[phaseIndex],
                      ),
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
    if (_currentOcp.hasPendingChanges || _scriptPath == null) {
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
