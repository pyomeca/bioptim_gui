import 'dart:developer';
import 'dart:io';

import 'package:flutter/services.dart';

enum PythonInterfaceStatus {
  uninitialized,
  initializing,
  failedAlreadyInitializing,
  failedMissingAnaconda,
  failedCreatingEnvironment,
  failedInstallingBioptim,
  failedUnknown,
  ready,
  isRunning,
}

class PythonInterface {
  static final PythonInterface _instance = PythonInterface._internal();
  static PythonInterface get instance => _instance;

  void registerToStatusChanged(Function(PythonInterfaceStatus) callback) =>
      _onStatusChangedCallbacks.add(callback);
  final List<Function(PythonInterfaceStatus status)> _onStatusChangedCallbacks =
      [];

  // TODO add common fix tips for user (such as running the app inside anaconda)
  String _workingDirectory = '.';
  bool _skipEnvironmentLoading = false;
  String? _environment;
  PythonInterfaceStatus _status = PythonInterfaceStatus.uninitialized;
  PythonInterfaceStatus get status => _status;
  set status(PythonInterfaceStatus value) {
    _status = value;
    for (final callback in _onStatusChangedCallbacks) {
      callback(_status);
    }
  }

  Future<Process?> runFile(String path,
      {String? overrideWorkingDirectory}) async {
    // TODO Better fail if not ready (popup?)
    if (status != PythonInterfaceStatus.ready) return null;
    status = PythonInterfaceStatus.isRunning;

    Future<void> changeStatusWhenDone(Process process) async {
      await process.exitCode;
      status = PythonInterfaceStatus.ready;
    }

    final process = await Process.start(
        '${_skipEnvironmentLoading ? '' : _loadEnvironmentCommand}python',
        [path],
        runInShell: true,
        workingDirectory: overrideWorkingDirectory ?? _workingDirectory);

    changeStatusWhenDone(process);
    return process;
  }

  Future<PythonInterfaceStatus> initialize(
      {String? workingDirectory, String? environment}) async {
    if (status == PythonInterfaceStatus.initializing) {
      // Do not initalize twice
      return PythonInterfaceStatus.failedAlreadyInitializing;
    }

    // Setup some internal values
    _workingDirectory = workingDirectory ?? '.';
    _environment = environment;
    status = PythonInterfaceStatus.initializing;

    // If bioptim is already installed there is no need to do anything else
    if (await _isBioptimInstalled(skipEnvironmentLoading: true)) {
      _skipEnvironmentLoading = true;
      status = PythonInterfaceStatus.ready;
      return status;
    }

    if (await _isBioptimInstalled()) {
      status = PythonInterfaceStatus.ready;
      return status;
    }

    // Otherwise, try to install it using anaconda
    if (!(await _isAnacondaInstalled())) {
      status = PythonInterfaceStatus.failedMissingAnaconda;
      return status;
    }

    // Check if current installation was made by this script
    if (!(await _isCondaEnvironmentInstalled())) {
      if (!(await _installCondaEnvironment())) {
        status = PythonInterfaceStatus.failedCreatingEnvironment;
        return status;
      }
    }

    if (!(await _installBioptim())) {
      status = PythonInterfaceStatus.failedInstallingBioptim;
      return status;
    }

    if (!(await _isBioptimInstalled())) {
      status = PythonInterfaceStatus.failedUnknown;
      return status;
    }

    status = PythonInterfaceStatus.ready;
    return status;
  }

  PythonInterface._internal();

  String get _loadEnvironmentCommand =>
      _environment == null ? '' : 'conda activate $_environment && ';

  void _logProcess(String functionName, ProcessResult result) {
    if (result.exitCode != 0) {
      log('$functionName failed with error:\n${result.stderr}');
    } else {
      log('$functionName success');
    }
  }

  Future<bool> _isAnacondaInstalled() async {
    final result = await Process.run('conda', ['-V'],
        runInShell: true, workingDirectory: _workingDirectory);
    _logProcess('isAnacondaInstalled', result);
    return result.exitCode == 0;
  }

  Future<bool> _isCondaEnvironmentInstalled() async {
    final result = await Process.run('conda', ['env', 'list'],
        runInShell: true, workingDirectory: _workingDirectory);
    _logProcess('isCondaEnvironmentInstalled', result);
    return result.stdout.contains(_environment);
  }

  Future<bool> _installCondaEnvironment() async {
    final result = await Process.run(
        'conda', ['create', '-n$_environment', '-y'],
        runInShell: true, workingDirectory: _workingDirectory);
    _logProcess('installCondaEnvironment', result);
    return result.exitCode == 0;
  }

  Future<bool> _isBioptimInstalled(
      {bool skipEnvironmentLoading = false}) async {
    // First we have to get the test file from the assets folder
    const bioptimTesterFileName = 'bioptim_tester.py';
    final newBioptimTester = File('$_workingDirectory/$bioptimTesterFileName');
    newBioptimTester.writeAsString(
        await rootBundle.loadString('assets/$bioptimTesterFileName'));

    // Then we can run the file to test if bioptim is installed
    final result = await Process.run(
        '${skipEnvironmentLoading ? '' : _loadEnvironmentCommand}python',
        [bioptimTesterFileName],
        runInShell: true,
        workingDirectory: _workingDirectory);
    _logProcess('isBioptimInstalled', result);

    // Now clean the mess
    newBioptimTester.delete();

    return result.exitCode == 0;
  }

  Future<bool> _installBioptim() async {
    final result = await Process.run('${_loadEnvironmentCommand}conda',
        ['install', '-cconda-forge', 'bioptim', '-y'],
        runInShell: true, workingDirectory: _workingDirectory);
    _logProcess('installBioptim', result);
    return result.exitCode == 0;
  }
}
