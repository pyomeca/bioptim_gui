import 'dart:convert';

import 'package:bioptim_gui/models/acrobatics_controllers.dart';
import 'package:bioptim_gui/models/api_config.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';

class VisualCriteriaCheckbox extends StatefulWidget {
  const VisualCriteriaCheckbox({Key? key, this.defaultValue = false})
      : super(key: key);

  final bool defaultValue;

  @override
  State<VisualCriteriaCheckbox> createState() => _VisualCriteriaCheckboxState();
}

class _VisualCriteriaCheckboxState extends State<VisualCriteriaCheckbox> {
  late bool isChecked;

  @override
  void initState() {
    super.initState();
    isChecked = widget.defaultValue;
  }

  Future<http.Response> updateVisualCriteria(bool value) async {
    final url = Uri.parse('${APIConfig.url}/acrobatics/with_visual_criteria');
    final headers = {'Content-Type': 'application/json'};
    final body = json.encode({'with_visual_criteria': value});

    final response = await http.put(url, headers: headers, body: body);

    if (response.statusCode != 200) {
      throw Exception(
          'Error while changing visual criteria to value ${value ? 'on' : 'off'}');
    }

    setState(() {
      isChecked = value;
    });

    // Alexandre: TODO find a prettier way to reset the export button
    AcrobaticsControllers.instance.notifyListeners();
    OptimalControlProgramControllers.instance.notifyListeners();

    if (kDebugMode) print('Visual criteria ${value ? 'on' : 'off'}');

    return response;
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return Checkbox(
        checkColor: Colors.white,
        value: isChecked,
        onChanged: (bool? value) async {
          final response = await updateVisualCriteria(value!);
          if (response.statusCode == 200) {
            data.updatePhaseInfo(json.decode(response.body) as List<dynamic>);
          }
        },
      );
    });
  }
}
