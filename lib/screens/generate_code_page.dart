import 'dart:convert';
import 'package:bioptim_gui/models/acrobatics_ocp_controllers.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/models/optimal_control_program_type.dart';
import 'package:bioptim_gui/models/python_interface.dart';
import 'package:bioptim_gui/widgets/acrobatic_bio_model_chooser.dart';
import 'package:bioptim_gui/widgets/acrobatic_position_chooser.dart';
import 'package:bioptim_gui/widgets/acrobatic_sport_type_chooser.dart';
import 'package:bioptim_gui/widgets/acrobatic_twist_side_chooser.dart';
import 'package:bioptim_gui/widgets/generate_phases.dart';
import 'package:bioptim_gui/widgets/console_out.dart';
import 'package:bioptim_gui/widgets/generate_somersaults.dart';
import 'package:bioptim_gui/widgets/number_of_phases_chooser.dart';
import 'package:bioptim_gui/widgets/acrobatic_information.dart';
import 'package:bioptim_gui/widgets/optimal_control_program_type_chooser.dart';
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
    AcrobaticsOCPControllers.instance.registerToStatusChanged(forceRedraw);
  }

  void forceRedraw() {
    _trailingKey.currentState?.setState(() {});
    setState(() {});
  }

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
              _HeaderBuilder(width: widget.columnWidth),
              const SizedBox(height: 12),
              const Divider(),
              const SizedBox(height: 12),
              _PhaseBuilder(width: widget.columnWidth),
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

class _HeaderBuilder extends StatelessWidget {
  const _HeaderBuilder({
    required this.width,
  });

  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = OptimalControlProgramControllers.instance;

    return Center(
      child: SizedBox(
        width: width,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            OptimalControlProgramTypeChooser(width: width),
            const SizedBox(height: 12),
            if (controllers.ocpType == OptimalControlProgramType.ocp)
              _GenericOCPHeaderBuilder(width: width)
            else if (controllers.ocpType ==
                OptimalControlProgramType.abrobaticsOCP)
              _AcrobaticsHeaderBuilder(width: width),
          ],
        ),
      ),
    );
  }
}

class _GenericOCPHeaderBuilder extends StatelessWidget {
  const _GenericOCPHeaderBuilder({
    required this.width,
  });

  final double width;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 12),
        NumberOfPhasesChooser(width: width),
      ],
    );
  }
}

class _AcrobaticsHeaderBuilder extends StatelessWidget {
  const _AcrobaticsHeaderBuilder({
    required this.width,
  });

  final double width;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        AcrobaticSportTypeChooser(width: width),
        const SizedBox(height: 12),
        AcrobaticBioModelChooser(width: width),
        const SizedBox(height: 12),
        AcrobaticInformation(width: width),
        const SizedBox(height: 12),
        Row(
          children: [
            SizedBox(
              width: width / 2 - 6,
              child: AcrobaticTwistSideChooser(width: width),
            ),
            const SizedBox(width: 12),
            SizedBox(
              width: width / 2 - 6,
              child: AcrobaticPositionChooser(width: width),
            ),
          ],
        ),
      ],
    );
  }
}

class _PhaseBuilder extends StatefulWidget {
  const _PhaseBuilder({required this.width});

  final double width;

  @override
  State<_PhaseBuilder> createState() => _PhaseBuilderState();
}

class _PhaseBuilderState extends State<_PhaseBuilder> {
  final _horizontalScroll = ScrollController();

  @override
  void dispose() {
    _horizontalScroll.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final controllers = OptimalControlProgramControllers.instance;
    return RawScrollbar(
      controller: _horizontalScroll,
      thumbVisibility: true,
      thumbColor: Theme.of(context).colorScheme.secondary,
      thickness: 8,
      radius: const Radius.circular(25),
      child: SingleChildScrollView(
        controller: _horizontalScroll,
        scrollDirection: Axis.horizontal,
        child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (controllers.ocpType == OptimalControlProgramType.ocp)
                PhaseGenerationMenu(width: widget.width),
              if (controllers.ocpType ==
                  OptimalControlProgramType.abrobaticsOCP)
                SomersaultGenerationMenu(width: widget.width),
            ]),
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
    final acrobaticsControllers = AcrobaticsOCPControllers.instance;

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
    final acrobaticsControllers = AcrobaticsOCPControllers.instance;

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
