import 'package:bioptim_gui/models/optimal_control_program_type.dart';
import 'package:bioptim_gui/models/optimal_control_program.dart';
import 'package:flutter/foundation.dart';

///
/// This class mimics the strcture of the [OptimalControlProgram] class but in
/// a UI perspective. It creates all the required Controllers as well as it gets
/// or updates the values.
class OptimalControlProgramControllers {
  static final OptimalControlProgramControllers _instance =
      OptimalControlProgramControllers._internal();
  static OptimalControlProgramControllers get instance => _instance;
  OptimalControlProgramControllers._internal();

  bool get mustExport => _ocp.mustExport;
  Function(String path) get exportScript => _ocp.exportScript;

  final _ocp = OptimalControlProgram();
  // This is to keep track of how many controllers we have because we don't
  // delete them if we reduce _nbPhases

  ///
  /// This callback can be used so the UI is updated on any change
  void notifyListeners() {
    if (kDebugMode) print("OptimalControlProgramControllers: notifyListeners");
    if (_hasChanged != null) _hasChanged!();
    _ocp.notifyThatModelHasChanged();
  }

  void Function()? _hasChanged;
  void registerToStatusChanged(Function() callback) {
    _hasChanged = callback;
    notifyListeners();
  }

  ///
  /// All methods related to controlling the ocp type
  OptimalControlProgramType get ocpType => _ocp.generic.ocpType;
  void setOcpType(OptimalControlProgramType value) {
    _ocp.generic.ocpType = value;
    notifyListeners();
  }
}
