import 'dart:convert';
import 'package:bioptim_gui/models/acrobatics_controllers.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/models/optimal_control_program_type.dart';
import 'package:bioptim_gui/models/python_interface.dart';
import 'package:bioptim_gui/screens/generate_code_page/acrobatics/acrobatics_menu.dart';
import 'package:bioptim_gui/screens/generate_code_page/generic/generic_menu.dart';
import 'package:bioptim_gui/widgets/console_out.dart';
import 'package:bioptim_gui/widgets/generic_ocp/optimal_control_program_type_chooser.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart';

class GenerateCode extends StatefulWidget {
  const GenerateCode({super.key, this.columnWidth = 400.0});

  final double columnWidth;

  @override
  State<GenerateCode> createState() => _GenerateCodeState();
}

class _GenerateCodeState extends State<GenerateCode> {
  final _verticalScroll = ScrollController();
  final _trailingKey = GlobalKey<_BuildTraillingState>();

  @override
  void dispose() {
    _verticalScroll.dispose();
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    PythonInterface.instance.registerToStatusChanged((status) => forceRedraw());
    OptimalControlProgramControllers.instance
        .registerToStatusChanged(forceRedraw);
    AcrobaticsControllers.instance.registerToStatusChanged(forceRedraw);
  }

  void forceRedraw() {
    _trailingKey.currentState?.setState(() {});
    setState(() {});
  }

  final controllers = OptimalControlProgramControllers.instance;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: RawScrollbar(
        controller: _verticalScroll,
        thumbVisibility: true,
        thumbColor: Theme.of(context).colorScheme.secondary,
        thickness: 8,
        radius: const Radius.circular(25),
        child: SingleChildScrollView(
          controller: _verticalScroll,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 12),
              Center(
                child: SizedBox(
                  width: widget.columnWidth,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      OptimalControlProgramTypeChooser(
                          width: widget.columnWidth),
                    ],
                  ),
                ),
              ),
              if (controllers.ocpType == OptimalControlProgramType.ocp)
                GenericMenu(columnWidth: widget.columnWidth),
              if (controllers.ocpType ==
                  OptimalControlProgramType.abrobaticsOCP)
                AcrobaticsMenu(columnWidth: widget.columnWidth),
              const SizedBox(height: 12),
              const Divider(),
              const SizedBox(height: 12),
              _BuildTrailling(key: _trailingKey),
              const SizedBox(height: 50),
            ],
          ),
        ),
      ),
    );
  }
}

class _BuildTrailling extends StatefulWidget {
  const _BuildTrailling({super.key});

  @override
  State<_BuildTrailling> createState() => _BuildTraillingState();
}

class _BuildTraillingState extends State<_BuildTrailling> {
  String? _scriptPath;
  Stream<String>? _output;
  Stream<String>? _outputError;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _buildExportOrRunScriptButton(),
        const SizedBox(height: 12),
        _buildOutputScreens(),
      ],
    );
  }

  Widget _buildExportOrRunScriptButton() {
    final controllers = OptimalControlProgramControllers.instance;
    final acrobaticsControllers = AcrobaticsControllers.instance;

    if ((controllers.ocpType == OptimalControlProgramType.ocp &&
            controllers.mustExport) ||
        (controllers.ocpType == OptimalControlProgramType.abrobaticsOCP &&
            acrobaticsControllers.mustExport) ||
        _scriptPath == null) {
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

  void _onExportFile() async {
    final controllers = OptimalControlProgramControllers.instance;
    final acrobaticsControllers = AcrobaticsControllers.instance;

    _scriptPath = await FilePicker.platform.saveFile(
      allowedExtensions: ['py'],
      type: FileType.custom,
    );
    if (_scriptPath == null) return;

    if (controllers.ocpType == OptimalControlProgramType.ocp) {
      controllers.exportScript(_scriptPath!);
    } else if (controllers.ocpType == OptimalControlProgramType.abrobaticsOCP) {
      acrobaticsControllers.exportScript(_scriptPath!);
    } else {
      throw Exception('Unknown OCP type');
    }

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
}
