import 'dart:convert';
import 'package:bioptim_gui/models/acrobatics_controllers.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:flutter/foundation.dart';

import 'package:bioptim_gui/models/api_config.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class RemoteBooleanSwitch extends StatefulWidget {
  final String endpoint;
  final bool defaultValue;
  final String leftText;
  final double width;
  final String requestKey;

  const RemoteBooleanSwitch({
    Key? key,
    required this.endpoint,
    required this.defaultValue,
    required this.leftText,
    required this.width,
    required this.requestKey,
  }) : super(key: key);

  @override
  RemoteBooleanSwitchState createState() => RemoteBooleanSwitchState();
}

class RemoteBooleanSwitchState extends State<RemoteBooleanSwitch> {
  late bool switchValue;

  @override
  void initState() {
    super.initState();
    switchValue = widget.defaultValue;
  }

  Future<void> _updateRemoteValue(bool value) async {
    final url = Uri.parse('${APIConfig.url}${widget.endpoint}');
    final headers = {'Content-Type': 'application/json'};
    final body = json.encode({widget.requestKey: value});

    final response = await http.put(url, headers: headers, body: body);

    if (response.statusCode != 200) {
      throw Exception('${widget.leftText} switch didn\'t update to $value');
    }

    if (kDebugMode) print('${widget.leftText} switch updated to $value');

    setState(() {
      switchValue = value;
    });

    // Alexandre: TODO find a prettier way to reset the export button
    AcrobaticsControllers.instance.notifyListeners();
    OptimalControlProgramControllers.instance.notifyListeners();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.width,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(widget.leftText),
          Switch(
            value: switchValue,
            onChanged: (bool value) => {_updateRemoteValue(value)},
            thumbIcon: MaterialStateProperty.resolveWith<Icon?>(
              (Set<MaterialState> states) {
                if (states.contains(MaterialState.selected)) {
                  return const Icon(Icons.check);
                }
                return const Icon(Icons.close);
              },
            ),
          ),
        ],
      ),
    );
  }
}
