import 'package:bioptim_gui/models/acrobatics_controllers.dart';
import 'package:bioptim_gui/models/api_config.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/widgets/utils/custom_dropdown_button.dart';
import 'package:bioptim_gui/widgets/utils/extensions.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class CustomHttpDropdown extends StatefulWidget {
  const CustomHttpDropdown({
    super.key,
    required this.title,
    required this.width,
    required this.defaultValue,
    required this.getEndpoint,
    required this.putEndpoint,
    required this.requestKey,
    this.color = Colors.black,
    this.customStringFormatting = _defaultToString,
    this.customCallBack,
  });

  final String title;
  final double width;
  final String defaultValue;
  final String getEndpoint;
  final String putEndpoint;
  // the key used in the request of the put method
  final String requestKey;
  final Color color;

  final Function(String) customStringFormatting;
  static String _defaultToString(String s) => s.toString().toLowerCase();

  final Function(http.Response)? customCallBack;

  @override
  CustomHttpDropdownState createState() => CustomHttpDropdownState();
}

class CustomHttpDropdownState extends State<CustomHttpDropdown> {
  String _selectedValue = '';
  List<String> _availableValues = [];

  @override
  void initState() {
    super.initState();
    _selectedValue = widget.defaultValue;
    _fetchAvailableValues();
  }

  Future<void> _fetchAvailableValues() async {
    final url = Uri.parse('${APIConfig.url}${widget.getEndpoint}');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      final List<dynamic> responseData = json.decode(response.body);
      final values = responseData
          .map((value) =>
              value.toString().replaceAll("_", " ").toLowerCase().capitalize())
          .toList();
      setState(() {
        _availableValues = values;
      });
    }
  }

  Future<void> _updateValue(String value) async {
    final requestValue = widget.customStringFormatting(value);
    final url = Uri.parse('${APIConfig.url}${widget.putEndpoint}');
    final headers = {'Content-Type': 'application/json'};
    final body = json.encode({widget.requestKey: requestValue});

    final response = await http.put(url, headers: headers, body: body);

    if (response.statusCode != 200) {
      throw Exception(
          'Error while changing ${widget.title} to value $requestValue');
    }

    setState(() {
      _selectedValue = value;
    });

    if (kDebugMode) print('${widget.title} changed to value $requestValue');

    // Alexandre: TODO find a prettier way to reset the export button
    AcrobaticsControllers.instance.notifyListeners();
    OptimalControlProgramControllers.instance.notifyListeners();

    if (widget.customCallBack != null) widget.customCallBack!(response);
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.width,
      child: CustomDropdownButton<String>(
        value: _selectedValue,
        items: _availableValues,
        title: widget.title,
        onSelected: (value) => _updateValue(value),
        color: widget.color,
      ),
    );
  }
}
