import 'package:bioptim_gui/models/acrobatics_ocp.dart';
import 'package:flutter/foundation.dart';

///
/// This class mimics the strcture of the [AcrobaticsOCPProgram] class but in
/// a UI perspective. It creates all the required Controllers as well as it gets
/// or updates the values.
class AcrobaticsControllers {
  static final AcrobaticsControllers _instance =
      AcrobaticsControllers._internal();
  static AcrobaticsControllers get instance => _instance;
  AcrobaticsControllers._internal();

  bool get mustExport => _ocp.mustExport;
  Function(String path) get exportScript => _ocp.exportScript;

  final _ocp = AcrobaticsOCPProgram();
  // This is to keep track of how many controllers we have because we don't
  // delete them if we reduce _nbPhases

  ///
  /// This callback can be used so the UI is updated on any change
  void notifyListeners() {
    if (kDebugMode) print("AcrobaticsControllers: notifyListeners");
    if (_hasChanged != null) _hasChanged!();
    _ocp.notifyThatModelHasChanged();
  }

  void Function()? _hasChanged;
  void registerToStatusChanged(Function() callback) {
    _hasChanged = callback;
    notifyListeners();
  }
}
