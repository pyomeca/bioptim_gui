import 'package:bioptim_gui/models/acrobatics_controllers.dart';
import 'package:bioptim_gui/models/acrobatics_data.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class CollisionCheckbox extends StatefulWidget {
  const CollisionCheckbox({super.key, this.defaultValue = false});

  final bool defaultValue;

  @override
  State<CollisionCheckbox> createState() => _CollisionCheckboxState();
}

class _CollisionCheckboxState extends State<CollisionCheckbox> {
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
          (data as AcrobaticsData).updateField("collision_constraint", value);

          setState(() {
            isChecked = value!;
          });
        },
      );
    });
  }
}
