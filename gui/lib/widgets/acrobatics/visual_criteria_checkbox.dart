import 'package:bioptim_gui/models/acrobatics_data.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class VisualCriteriaCheckbox extends StatefulWidget {
  const VisualCriteriaCheckbox({super.key, this.defaultValue = false});

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

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return Checkbox(
        checkColor: Colors.white,
        value: isChecked,
        onChanged: (bool? value) async {
          (data as AcrobaticsData).updateField("with_visual_criteria", value);

          setState(() {
            isChecked = value!;
          });
        },
      );
    });
  }
}
