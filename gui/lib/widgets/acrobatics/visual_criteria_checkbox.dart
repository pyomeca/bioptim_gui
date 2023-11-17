import 'dart:convert';

import 'package:bioptim_gui/models/api_config.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

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

  Future<void> updateVisualCriteria(bool value) async {
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

    if (kDebugMode) print('Visual criteria ${value ? 'on' : 'off'}');
  }

  @override
  Widget build(BuildContext context) {
    return Checkbox(
      checkColor: Colors.white,
      value: isChecked,
      onChanged: (bool? value) async {
        await updateVisualCriteria(value!);
      },
    );
  }
}
